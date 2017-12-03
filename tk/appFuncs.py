# coding=utf-8
"""
Script Name: appFuncs.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script will find all the path of modules, icons, images ans store them to a file
"""
import sqlite3 as lite

# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import cv2
import datetime
import json
import logging
import os
import pip
import platform
import requests
import shutil
import subprocess
import sys
import unicodedata
import urllib
import yaml
from pyunpack import Archive

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

def downloadSingleFile(url, path_to, *args):
    doDL = urllib.urlretrieve(url, path_to)
    logger.info(doDL)
    logger.info("Downloaded to: %s" % str(path_to))

def extactingFiles(inDir, file_name, outDir, *args):
    Archive(os.path.join(inDir, file_name)).extractall(outDir)

def system_call(args, cwd="."):
    print("Running '{}' in '{}'".format(str(args), cwd))
    subprocess.call(args, cwd=cwd)
    pass

def fix_image_files(root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        # sys.stdout.write('.')
        for dir in dirs:
            system_call("mogrify *.png", "{}".format(os.path.join(path, dir)))

def object_config(directory, mode, *args):
    operatingSystem = platform.system()

    if operatingSystem == "Windows" or operatingSystem == "Darwin":
        if mode == "h":
            if operatingSystem == "Windows":
                subprocess.call(["attrib", "+H", directory])
            elif operatingSystem == "Darwin":
                subprocess.call(["chflags", "hidden", directory])
        elif mode == "s":
            if operatingSystem == "Windows":
                subprocess.call(["attrib", "-H", directory])
            elif operatingSystem == "Darwin":
                subprocess.call(["chflags", "nohidden", directory])
        else:
            logger.error("ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
    else:
        logger.error("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

def batch_config(listObj, mode, *args):

    for obj in listObj:
        if os.path.exists(obj):
            object_config(obj, mode)
        else:
            logger.info('Could not find the specific path: %s' % obj)

def clean_unnecessary_file(var, *args):
    directory = os.getenv('PIPELINE_TOOL')

    profile = []
    for root, dirs, file_names in os.walk(directory):
        for file_name in file_names:
            if var in file_name:
                pth = os.path.join(root, file_name)
                profile.append(pth)

    if len(profile) is None:
        sys.exit()

    for f in profile:
        logger.info('removing %s' % f)
        os.remove(f)

def getfilePath(directory=None):

    """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    if directory is None:
        print 'you need to give a specific path to inspect'
        sys.exit()

    if not os.path.exists(directory):
        print 'the directory is not exists'
        sys.exit()

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def batchResizeImage(imgDir=None, imgResDir=None, size=[100, 100], sub=False, ext='.png', mode=1):
    if imgDir == None:
        sys.exit()

    if not os.path.exists(imgDir):
        print 'The source folder: %s is not exists' % imgDir
        sys.exit()

    if imgResDir == None:
        imgResDir = imgDir

    if not os.path.exists(imgResDir):
        os.mkdir(imgResDir)

    if not sub:
        images = [i for i in os.listdir(imgDir) if i.endswith(ext)]
    else:
        filePths = getfilePath(imgDir)
        images = [os.path.abspath(i) for i in filePths if i.endswith(ext)]

    resized_images = []

    for image in images:
        imgPth = os.path.join(imgDir, image)
        resizedName = 'resized_%s' % image
        resDir = os.path.join(imgResDir, resizedName)
        img = cv2.imread(imgPth, mode)
        resized_image = cv2.resize(img, (size[0], size[1]))
        cv2.imwrite(resDir, resized_image)

        resized_images.append(resDir)

    return images, resized_images

def dataHandle(type='json', mode='r', filePath=None, data={}, *args):
    """
    json and yaml: read, write, edit... etc
    """
    if type == 'json':
        indent = 4
        if mode == 'r' or mode == 'r+':
            with open(filePath, mode) as f:
                info = json.load(f)
        elif mode == 'w' or mode == 'w+':
            with open(filePath, mode) as f:
                info = json.dump(data, f, indent=indent)
        else:
            with open(filePath, mode) as f:
                info = json.dump(data, f, indent=indent)
    elif type == 'yaml':
        if mode == 'r' or mode == 'r+':
            with open(filePath, mode) as f:
                info = yaml.load(f)
        elif mode == 'w' or mode == 'w+':
            with open(filePath, mode) as f:
                info = yaml.dump(data, f, default_flow_style=False)
        else:
            with open(filePath, mode) as f:
                info = yaml.dump(data, f, default_flow_style=False)

    return info

def getAllInstalledPythonPackage(*args):
    pyPkgs = {}

    pyPkgs['__mynote__'] = 'import pip; pip.get_installed_distributions()'

    for package in pip.get_installed_distributions():
        name = package.project_name  # SQLAlchemy, Django, Flask-OAuthlib
        key = package.key  # sqlalchemy, django, flask-oauthlib
        module_name = package._get_metadata("top_level.txt")  # sqlalchemy, django, flask_oauthlib
        location = package.location  # virtualenv lib directory etc.
        version = package.version  # version number

        pyPkgs[name] = [key, version, location]

    pkgConfig = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/pkgs.config.yml')

    with open(pkgConfig, 'w') as f:
        yaml.dump(pyPkgs, f, default_flow_style=False)

    return pyPkgs

# Execute a python file
def executing(name, path, *args):
    """
    Executing a python file
    :param name: python file name
    :param path: path to python file
    :return: executing in command prompt
    """
    logger.info('Executing %s from %s' % (name, path))
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
    logger.info('Using pip to install %s' % name)

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
        # logger.info('package "%s" is already installed' % name)
        pass
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

def getAvatar(name, *args):
    imgFile = name + '.avatar.jpg'
    imgDir = os.path.join(os.getenv('PIPELINE_TOOL'), 'imgs')
    imgPth = os.path.join(imgDir, imgFile)
    if os.path.exists(imgPth):
        return imgPth
    else:
        scrPth = os.path.join(imgDir, 'default.avatar.jpg')
        shutil.copy2(scrPth, imgPth)
        return imgPth

# Get the full path of image via icon file name
def downloadFromURL(link, *args):
    fileName = os.path.basename(link)
    imgPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'imgs')
    avatarPth = os.path.join(imgPth, fileName)
    if not os.path.exists(avatarPth):
        downloadSingleFile(link, avatarPth)

    return avatarPth

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
        self.outPut = ''.join(["%02X" % ord(x) for x in strInput])
        return self.outPut

    def hexToStr(self, hexInput):
        """
        convert a hexadecimal string to a string which could be readable
        :param hexInput: hexadecimal string
        :return: readable string
        """
        bytes = []
        hexStr = ''.join(hexInput.split(" "))
        for i in range(0, len(hexStr), 2):
            bytes.append(chr(int(hexStr[i:i + 2], 16)))

        self.outPut = ''.join(bytes)
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
        output = Encode().strToHex(input)
    elif mode == 'str':
        output = Encode().hexToStr(input)
    elif mode == 'ascii':
        output = Encode().ascii(input)
    else:
        output = Encode().utf8(input)

    return output


# ----------------------------------------------------------------------------------------------------------- #
"""                MAIN CLASS 2: GET MODULE INFO - GET ALL INFO OF MODULES, ICONS, IMAGES                   """
# ----------------------------------------------------------------------------------------------------------- #
class Proceduring():
    """
    This is some function that will use many time
    """
    dt = datetime.datetime

    def __init__(self):
        # logger.info('Start procedural')
        pass

    def getDate(self):
        t = datetime.datetime.timetuple(datetime.datetime.now())
        dateOutput = '%s.%s.%s' % (str(t.tm_mday), str(t.tm_mon), str(t.tm_year))
        return dateOutput

    def getTime(self):
        t = datetime.datetime.timetuple(datetime.datetime.now())
        timeOutput = '%s:%s' % (str(t.tm_hour), str(t.tm_min))
        return timeOutput

    def createLog(self, event='Create Log', *args):
        log = {}
        log[proc('date')] = event
        logPth = os.path.join(os.getcwd(), 'sql_tk/db/user.log')
        logger.info(event)
        dataHandle('json', 'w+', logPth, log)
        logger.info("log: %s" % logPth)

def encoding(message):
    output = encode(message, mode='hex')
    return output

def decoding(message):
    output = encode(message, mode='str')
    return output

def logRecord(event):
    # logger.info('Log created')
    output = Proceduring().createLog(event=event)
    return output

def query_list_unix_id(*args):
    dataPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/meta_data.db')
    conn = lite.connect(dataPth)
    c = conn.cursor()
    ce = c.execute
    ce("SELECT unix FROM loginCf")
    rows = c.fetchall()
    unix_list = [row[0] for row in rows]
    return unix_list

def checkUserLogin(username):
    dataPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/meta_data.db')
    conn = lite.connect(dataPth)
    c = conn.cursor()
    ce = c.execute
    ce("SELECT username FROM loginCf")
    tuples = [t for t in c.fetchall()]
    usernameList = [str(t[0]) for t in tuples]

    print usernameList

    user = {}

    if username in usernameList:
        index = usernameList.index(username)
        ce("SELECT * FROM loginCf")
        tuples = [t for t in c.fetchall()]
        user[username] = tuples[index]

def create_location_stamp():
    r = requests.get('https://api.ipdata.co').json()
    info = {}
    for key in r:
        k = (str(key))
        content = str(r[key])
        info[k] = content
    ip = info['ip']
    city = info['city']
    country = info['country_name']
    return ip, city, country

def proc(unix, operation=None):
    t = Proceduring().getTime()
    # d = Proc().getDate()
    if operation == 'date':
        output = Proceduring().getDate()
    elif operation == 'time':
        output = Proceduring().getTime()
    elif operation == 'log out':
        output = logRecord('User %s logged out at %s' % (unix, t))
    elif operation == 'log in':
        output = logRecord('User %s logged in at %s' % (unix, t))
    elif operation == 'update':
        output = logRecord('Update data at %s' % t)
    elif operation == 'restart':
        output = logRecord('User %s restart app at %s' % (unix, t))
    elif operation == 'rc':
        logRecord('User %s has recofigured at %s' % (unix, t))
    else:
        output = None

    return output

def query_local_product_id():
    path = os.path.join(os.getenv('PIPELINE_TOOL'), 'sql_tk/db/pc.config.yml')
    info = dataHandle('yaml', 'r', path)
    return info['Product ID']

# --------------------------------------------------------------------------------------------------------
"""                                                END OF CODE                                         """
# --------------------------------------------------------------------------------------------------------
