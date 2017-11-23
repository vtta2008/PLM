# coding=utf-8
"""
Script Name: appFuncs.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script will find all the path of modules, icons, images ans store them to a file
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import os, sys, logging, json, subprocess, pip, uuid, unicodedata, datetime
from tk import defaultVariable as var

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
PLUGIN = var.MAIN_PLUGIN
PACKAGE = var.MAIN_PACKPAGE
NAMES = var.MAIN_NAMES
USER = var.USERNAME
# example of a normal string (English, readable)
STRINPUT = var.STRINPUT
# example of a string in hexadecimal code
HEXINPUT = var.HEXINPUT
# list of keywords to run script by user
OPERATION = var.OPERATION['encode']

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

def createToken(*args):
    token = uuid.uuid4()
    return token

def dataHandle(filePath, mode, indent=4, *args):
    """
    json functions: read, write, edit... etc
    """

    # print filePath

    if mode=='r' or mode=='r+':
        if not os.path.exists(filePath):
            logger.debug('file is not exists')
            sys.exit()
        else:
            with open(filePath, mode) as f:
                return json.load(f)
    elif mode == 'a' or mode == 'a+':
        if not os.path.exists(filePath):
            logger.debug('file is not exists')
            sys.exit()
        else:
            with open(filePath, mode) as f:
                return json.dump(filePath, f, indent=indent)
    elif mode == 'w' or mode =='w+':
        with open(filePath, mode) as f:
            return json.dump(filePath, f, indent=indent)

def getAllInstalledPythonPackage(*args):
    pyPkgs = {}

    pyPkgs['__mynote__'] = 'import pip; pip.get_installed_distributions()'

    for package in pip.get_installed_distributions():
        name = package.project_name # SQLAlchemy, Django, Flask-OAuthlib
        key = package.key # sqlalchemy, django, flask-oauthlib
        module_name = package._get_metadata("top_level.txt") # sqlalchemy, django, flask_oauthlib
        location = package.location # virtualenv lib directory etc.
        version = package.version # version number

        pyPkgs[name] = [key, version, location]

    pkgInfo = os.path.join(os.getenv('PROGRAMDATA'), 'PipelineTool/scrInfo/apps.pipeline')

    # print pkgInfo, os.path.exists(pkgInfo)

    if not os.path.exists(pkgInfo):
        from tk import getData
        reload(getData)
        getData.initialize()

    with open(pkgInfo, 'w') as f:
        json.dump(pyPkgs, f, indent=4)

    return pyPkgs

# Execute a python file
def executing(name, path, *args):
    """
    Executing a python file
    :param name: python file name
    :param path: path to python file
    :return: executing in command prompt
    """
    logger.info( 'Executing %s from %s' % (name, path) )
    pth = os.path.join(path, name)
    if os.path.exists(pth):
        subprocess.call([sys.executable, pth])

# Install package via pip command (cmd)
def install_package(name, *args):
    """
    Install python component via command prompt
    :param name: name of component
    :return:
    """
    logger.info( 'Using pip to install %s' % name )

    subprocess.Popen('pip install %s' % name, shell=True).wait()

# Check plugin is installed or not
def checkPackageInstall(name, *args):
    """
    check python component, if false, it will install component
    :param name:
    :return:
    """
    # logger.info( 'Trying to import %s' % name )
    allPkgs = getAllInstalledPythonPackage()

    if name in allPkgs:
        logger.info('package "%s" is already installed' % name)
    else:
        logger.info('package "%s" is not installed, '
                    'execute package installation procedural' % name)
        install_package(name)

# Create environment variable by custom key
def createKey(key, path, *args):
    """
    Create custom enviroment Key in sys.
    all of those keys are temporary,
    it will be none once pipeline tool shut down.
    :param key: name of the key
    :param scrInstall: source scripts of pipline tool app
    :param toolName: name of the folder where contains the tool
    :return: a teamporary environment variable.
    """
    logger.info('install new environment variable')

    os.environ[key] = path

# Check the value of environment variable
def checkEnvKey(key, path, *args):
    try:
        pth = os.getenv(key)

        if pth == None or pth == '':
            createKey(key, path)

    except KeyError:
        createKey(key, path)
    else:
        pass

# Get the full path of icon via icon file name
def getIcon(name, *args):
    iconName = name + '.icon.png'
    rootPth = os.getcwd().split('ui')[0]
    iconPth = os.path.join(os.path.join(rootPth, 'icons'), iconName)
    return iconPth

# Get the full path of image via icon file name
def avatar(userName, *args):
    img = userName + '.avatar.jpg'
    imgPth = os.path.join(os.getcwd(), 'imgs')
    avatarPth = os.path.join(imgPth, img)
    return avatarPth

# Save information of current log in user account for next time.
def saveCurrentUserLogin(userName, remember=False, *args):
    userDataPth = os.path.join(os.getenv('PROGRAMDATA'), 'PipelineTool/scrInfo/user.info')

    with open(userDataPth, 'r') as f:
        userData = json.load(f)

    userData[userName].append(remember)

    curUser = {}
    curUser[userName] = userData[userName]
    currentUserLoginPth = os.path.join(os.getenv('PROGRAMDATA'), 'PipelineTool/user.tempLog')
    with open(currentUserLoginPth, 'w') as f:
        json.dump(curUser, f, indent=4)

    logger.info('save file to %s' % currentUserLoginPth)

# ----------------------------------------------------------------------------------------------------------- #
"""                        MAIN CLASS 1: ENDCODE - ENCODE STRING TO HEXADECIMAL                             """
# ----------------------------------------------------------------------------------------------------------- #
class Encode():
    """
    This is the main class with function to encode a string to hexadecimal or revert.
    """
    def ascii(self, rawInput):
        """
        convert another type of unicode to be compatible in python
        :param rawInput: input
        :return: unicode string
        """
        outPut = unicodedata.normalize('NFKD', rawInput).encode('ascii', 'ignore').decode('ascii')

        return outPut

    def utf8(self, rawInput):
        outPut = rawInput.encode('utf-8')
        return outPut

    def typeToStr(self, rawInput):
        """
        convert to string
        :param rawInput: input which may not be a string type
        :return: string type input
        """
        if type(rawInput) is not 'string':
            rawStr = str(rawInput)
        else:
            rawStr = rawInput

        return rawStr

    def strToHex(self, strInput):
        """
        convert string to hexadecimal
        :param strInput: string input
        :return: hexadecimal
        """
        self.outPut = ''.join ( ["%02X" % ord (x) for x in strInput] )
        return self.outPut

    def hexToStr(self, hexInput):
        """
        convert a hexadecimal string to a string which could be readable
        :param hexInput: hexadecimal string
        :return: readable string
        """
        bytes = []
        hexStr = ''.join( hexInput.split(" ") )
        for i in range(0, len(hexStr), 2):
            bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

        self.outPut = ''.join( bytes )
        return self.outPut

# ------------------------------------------------------
# FUNCTION TO OPERATE THE ENCODING
# ------------------------------------------------------
def encode(input=STRINPUT, mode=OPERATION[0]):
    """
    Base on given mode it will tells script what to do
    :param input: type of input, string by default
    :param mode: given mode to convert string to hexadecimal or revert.
    :return: string
    """
    if mode == 'hex':
       output = Encode().strToHex( input )
    elif mode == 'str':
        output = Encode().hexToStr( input )
    elif mode== 'ascii':
        output = Encode().ascii( input )
    else:
        output = Encode().utf8(input)

    return output


# ----------------------------------------------------------------------------------------------------------- #
"""                MAIN CLASS 2: GET MODULE INFO - GET ALL INFO OF MODULES, ICONS, IMAGES                   """
# ----------------------------------------------------------------------------------------------------------- #
class Proc():
    """
    This is some function that will use many time
    """
    dt = datetime.datetime

    def __init__(self):
        # logger.info('Start procedural')
        pass

    def getDate(self):
        t = datetime.datetime.timetuple( datetime.datetime.now() )
        dateOutput = '%s/%s/%s' % (str(t.tm_mday), str(t.tm_mon), str(t.tm_year))
        return dateOutput

    def getTime(self):
        t = datetime.datetime.timetuple(datetime.datetime.now() )
        timeOutput = '%s:%s' % (str(t.tm_hour), str(t.tm_min))
        return timeOutput

    def createLog(self, event='Create Log', names=NAMES, package=PACKAGE):
        log = {}
        log[proc('date')] = event
        with open( os.path.join(package['appData'], names['log']), 'a+') as f:
            json.dump(log, f, indent=4)

def encoding(message):
    output = encode(message, mode='hex')
    return output

def decoding(message):
    output = encode(message, mode='str')
    return output

def logRecord(event):
    # logger.info('Log created')
    output = Proc().createLog(event=event)
    return output

def proc(operation=None, name=NAMES['log'], path=PACKAGE['info']):
    t = Proc().getTime()
    d = Proc().getDate()
    u = USER

    if operation == 'date':
        output = Proc().getDate()
    elif operation == 'time':
        output = Proc().getTime()
    elif operation == 'log out':
        output = logRecord('User %s logged out at %s' % (u,t))
    elif operation == 'log in':
        output = logRecord('User %s logged in at %s' % (u,t))
    elif operation == 'update':
        output = logRecord('Update data at %s' % t)
    elif operation == 'restart':
        output = logRecord('User %s restart app at %s' % (u, t) )
    else:
        output=None

    return output

# --------------------------------------------------------------------------------------------------------
"""                                                END OF CODE                                         """
# --------------------------------------------------------------------------------------------------------