# coding=utf-8
"""
Script Name: utils.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Here is where a lot of function need to use multiple times overall
"""
# -------------------------------------------------------------------------------------------------------------
""" Import modules """
# -------------------------------------------------------------------------------------------------------------
# Python
import datetime
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import urllib
import cv2
import pip
import requests
import winshell
import yaml
from pyunpack import Archive
from functools import partial

# PyQt5
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

# Plt tools
import variables as var

# ------------------------------------------------------
""" Variables """
# ------------------------------------------------------
config_path = os.path.join(os.getenv(('PIPELINE_TOOL'), 'appData'))

USER = var.USERNAME
# example of a normal string (English, readable)
STRINPUT = var.STRINPUT
# example of a string in hexadecimal code
HEXINPUT = var.HEXINPUT
# list of keywords to run script by user
OPERATION = var.OPERATION['encode']

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """
# -------------------------------------------------------------------------------------------------------------
logPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'logs', 'utilities.log')
logger = logging.getLogger('utilities')
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Functions content """
# -------------------------------------------------------------------------------------------------------------
def str2bool(arg):
    return str(arg).lower() in ['true', 1, '1', 'ok']

def bool2str(arg):
    if arg:
        return "True"
    else:
        return "False"

def downloadSingleFile(url, path_to, *args):
    execute_download = urllib.urlretrieve(url, path_to)
    logger.info(execute_download)
    logger.info("Downloaded to: %s" % str(path_to))

def extract_files(inDir, file_name, outDir, *args):
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

def get_file_path(directory=None):

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

def batch_resize_image(imgDir=None, imgResDir=None, size=[100, 100], sub=False, ext='.png', mode=1):

    """
    resize multiple images at once
    :param imgDir: the path of images will be resized
    :param imgResDir: the path to store images after resizing
    :param size: how big or small images will be resized

    """

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
        filePths = get_file_path(imgDir)
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

def resize_image(imgPthSrc, imgPthDes, size=[100,100]):

    img = cv2.imread(imgPthSrc, 1)
    resized_image = cv2.resize(img, (size[0], size[1]))
    cv2.imwrite(imgPthDes, resized_image)

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

def get_list_python_packages_installed(*args):
    pyPkgs = {}

    pyPkgs['__mynote__'] = 'import pip; pip.get_installed_distributions()'

    for package in pip.get_installed_distributions():
        name = package.project_name  # SQLAlchemy, Django, Flask-OAuthlib
        key = package.key  # sqlalchemy, django, flask-oauthlib
        module_name = package._get_metadata("top_level.txt")  # sqlalchemy, django, flask_oauthlib
        location = package.location  # virtualenv lib directory etc.
        version = package.version  # version number

        pyPkgs[name] = [key, version, location]

    pkgConfig = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData/pkgs_config.yml')

    with open(pkgConfig, 'w') as f:
        yaml.dump(pyPkgs, f, default_flow_style=False)

    return pyPkgs

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

def install_package(name, *args):
    """
    Install python package via command prompt
    :param name: name of component
    :return:
    """
    logger.info('Using pip to install %s' % name)

    subprocess.Popen('pip install %s' % name, shell=True).wait()

def inspection_backage(name, *args):
    """
    check python component, if false, it will install component
    :param name:
    :return:
    """
    # logger.info( 'Trying to import %s' % name )
    allPkgs = get_list_python_packages_installed()

    if name in allPkgs:
        # logger.info('package "%s" is already installed' % name)
        pass
    else:
        logger.info('package "%s" is not installed, '
                    'execute package installation procedural' % name)
        install_package(name)

def create_env_key(key, path, *args):
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

def inspect_env_key(key, path, *args):
    try:
        pth = os.getenv(key)

        if pth == None or pth == '':
            create_env_key(key, path)

    except KeyError:
        create_env_key(key, path)
    else:
        pass

def get_avatar(name, *args):
    imgFile = name + '.avatar.jpg'
    imgPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'imgs', imgFile)

    if os.path.exists(imgPth):
        pass
    else:
        scrPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'imgs', 'default.avatar.jpg')
        shutil.copy2(scrPth, imgPth)
    return imgPth

def download_image_from_url(link, *args):
    fileName = os.path.basename(link)
    imgPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'imgs')
    avatarPth = os.path.join(imgPth, fileName)
    if not os.path.exists(avatarPth):
        downloadSingleFile(link, avatarPth)

    return avatarPth

def open_app(pth, *args):
    subprocess.Popen(pth)

# ----------------------------------------------------------------------------------------------------------- #
""" Plt app functions """

def screenshot(*args):
    from ui import ui_screenshot
    reload(ui_screenshot)
    dlg = ui_screenshot.Screenshot()
    dlg.exec_()

# ----------------------------------------------------------------------------------------------------------- #
""" PtQt5 Layout Functions """

def get_icon(name, *args):
    iconName = name + '.icon.png'
    iconPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'icons', iconName)
    return iconPth

def get_web_icon(name, *args):
    iconName = name + '.icon.png'
    iconPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'icons', 'Web.icon', iconName)
    return iconPth

# ----------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------------------------------------------------------------------- #
""" Enconding """

class Encode():
    """
    This is the main class with function to encode a string to hexadecimal or revert.
    """
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
    else:
        output = Encode().utf8(input)

    return output

def encoding(message):
    output = encode(message, mode='hex')
    return output

def decoding(message):
    output = encode(message, mode='str')
    return output

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
# ----------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------------------------------------------------------------------- #
""" Get config info of modules, files etc. """

class Get_current_time():
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

class Generate_info(object):

    """
    This class will find all the info of python, icon, image files and folders then store them to info files in
    info folder
    """

    def __init__(self):
        super(Generate_info, self).__init__()

        """
        Initialize the main class functions
        :param package: the package of many information stored from default variable
        :param names: the dictionary of names stored from default variable
        :returns: all installed app info, package app info, icon info, image info, pc info.
        
        """
        # logger.info('Updating data paths')

        package = var.PLT_PACKAGE

        self.createAllInfoFiles(package)

    def getModuleInfo(self, package):
        """
        Get all the info of modules
        :param package: the package of many information stored from default variable
        :param names: the dictionary of names stored from default variable
        :return: modules.info
        """
        # Create info module dictionary
        moduleInfo = {}
        moduleInfo['root'] = package['root']
        moduleInfo['app module'] = os.path.join(package['root'], package['py'][0])
        moduleInfo['app ui'] = os.path.join(package['root'], package['py'][1])

        for pyFol in package['py']:
            pyPth = os.path.join(package['root'], pyFol)
            if os.path.exists(pyPth):
                sys.path.append(pyPth)
            files = [f for f in os.listdir(pyPth) if f.endswith('PipelineTool.py')]
            for file in files:
                if '__init__' in file:
                    pass
                else:
                    pth = os.path.join(pyPth, file)
                    moduleInfo[file.split('PipelineTool.py')[0]] = pth

        return moduleInfo

    def getIconInfo(self, package):
        """
        Get all the info of icons
        :param package: the package of many information stored from default variable
        :param names: the dictionsary of names stored from default variable
        :return: icons.info
        """
        # Create dictionary for icon info
        iconInfo = {}
        iconInfo['Sep'] = 'separato.png'
        iconInfo['File'] = 'file.png'
        iconInfo['iconPth'] = os.path.join(os.getenv('PIPELINE_TOOL'), package['image'][0])
        icons = [f for f in os.listdir(iconInfo['iconPth']) if '.icon' in f]
        if len(icons) == 0:
            iconInfo['icons'] = None
        else:
            for i in icons:
                iconInfo[i.split('.icon')[0]] = os.path.join(iconInfo['iconPth'], i)
        iconNames = [f for f in iconInfo]
        icons = {}
        icons['name'] = iconNames
        return iconInfo

    def getImgInfo(self, package):
        """
        Get all the info of images
        :param package: the package of many information stored from default variable
        :return: imgs.info
        """
        imgInfo = {}
        imgInfo['imgPth'] = os.path.join(package['root'], package['image'][1])
        imgs = [f for f in os.listdir(imgInfo['imgPth']) if '.img' in f]
        if len(imgs) == 0:
            imgInfo['imgs'] = None
        else:
            for i in imgs:
                imgInfo[i.split('.png')[0]] = os.path.join(imgInfo['imgPth'], i)
        return imgInfo

    def getAllAppInfo(self):
        """
        It will find and put all the info of installed apps to two list: appname and path
        :param filters: self.appName, self.appPath
        :return: self.appName, self.appPath
        """
        shortcuts = {}
        appName = []
        appPth = []
        all_programs = winshell.programs(common=1)
        for dirpath, dirnames, filenames in os.walk(all_programs):
            relpath = dirpath[1 + len(all_programs):]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(dirpath, f)) for f in filenames])
        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                appName.append(name)
                appPth.append(lnk.path)
        appInfo = {}
        for name in appName:
            pth = appPth[appName.index(name)]
            pth = encode(pth, 'utf8')
            name = encode(name, 'utf8')
            appInfo[name] = pth
        return appInfo

    def getPackageAppInfo(self, package):
        """
        It will Check if there is more than 1 version is installed
        :param package: the package of many information stored from default variable
        :param names: the dictionary of names stored from default variable
        :return: final app info
        """
        self.appInfo = self.getAllAppInfo()
        keys = [k for k in self.appInfo if not self.appInfo[k].endswith(package['ext'][0])]
        self.appInfo = self.deleteKey(keys, True)
        jobs = []
        for key in package['job']:
            for job in package[key]:
                jobs.append(job)

        keys = []
        for job in jobs:
            for key in self.appInfo:
                if job in key:
                    keys.append(key)

        pth = [self.appInfo[k] for k in keys]
        self.appInfo = {}
        for k in sorted(keys):
            self.appInfo[k] = pth[keys.index(k)]

        for k in package['filter']:
            for key in keys:
                if k in key:
                    del self.appInfo[key]

        return self.appInfo

    def createAllInfoFiles(self, package):
        """
        Run all the functions inside class and take all the return info then store them to files
        :param package: the package of many information stored from default variable
        :return: info files
        """
        info = {}
        iconInfo = self.getIconInfo(package)
        trackKeys = {}

        allapps = self.getAllAppInfo()
        appsConfig_yaml = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'config', 'app_config.yml')
        appsConfig_json = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'config', 'app_config.json')

        dataHandle('yaml', 'w', appsConfig_yaml, allapps)
        dataHandle('json', 'w', appsConfig_json, allapps)

        self.appInfo = self.getPackageAppInfo(package)
        for key in self.appInfo:
            # fix nukeX path
            if 'NukeX' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
            # fix Hiero path
            if 'Hiero' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
            # fix UVLayout path
            if 'UVLayout' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"

        # trackList = PACKAGE['TD'] + PACKAGE['Comp'] + PACKAGE['Design'] + PACKAGE['Office']

        for icon in iconInfo:
            for key in self.appInfo:
                if icon in key:
                    trackKeys[icon] = [key, iconInfo[icon], self.appInfo[key]]
        # insert info which is not in installed apps
        trackKeys['Logo'] = ['pipeline manager', iconInfo['Logo'], '']
        trackKeys['Sep'] = ['separator', iconInfo['Sep'], 'separator']
        trackKeys['File'] = ['File', iconInfo['File'], '']
        trackKeys['Exit'] = ['Exit application', iconInfo['Exit'], '']
        trackKeys['About'] = ['About pipeline tool', iconInfo['About'], 'About pipeline tool']
        trackKeys['Credit'] = ['Credit', iconInfo['Credit'], 'Thanks to all of you']
        trackKeys['Help'] = ['Introduction', iconInfo['Help'], '']
        trackKeys['CleanPyc'] = ['Clean .pyc files', iconInfo['CleanPyc'], '']
        trackKeys['ReConfig'] = ['Re configuring data', iconInfo['Reconfig'], '']

        # Davinci Resolve
        davinciPth = os.path.join(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')

        if os.path.exists(davinciPth):
            trackKeys['Resolve'] = ['Davinci Resolve 14', get_icon('Resolve'), davinciPth]

        with open(os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'config', 'app_config.yml'), 'r') as f:
            fixInfo = yaml.load(f)

        dbBrowserPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'external_app', 'sqlbrowser', 'SQLiteDatabaseBrowserPortable.exe')
        advanceRenamerPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'external_app', 'batchRenamer', 'ARen.exe')
        qtDesigner = os.path.join(os.getenv('PROGRAMDATA'),'Anaconda2', 'Library', 'bin', 'designer.exe')

        for keys in fixInfo:
            # print keys
            # Pycharm.
            if 'JetBrains PyCharm' in keys:
                trackKeys['PyCharm'] = ['PyCharm', get_icon('Pycharm'), fixInfo['JetBrains PyCharm 2017.3.3']]

            # Sumblime text.
            if 'Sublime Text 3' in keys:
                trackKeys['SublimeText 3'] = ['Sublime Text 3', get_icon('SublimeText 3'), fixInfo['Sublime Text 3']]

            # Qt Designer
            if os.path.exists(qtDesigner):
                trackKeys['QtDesigner'] = ['QtDesigner', get_icon('QtDesigner'), qtDesigner]

            # Snipping tool.
            if 'Snipping Tool' in fixInfo:
                trackKeys['Snipping Tool'] = ['Snipping Tool', get_icon('Snipping Tool'), fixInfo['Snipping Tool']]

            # Database browser.
            if os.path.exists(dbBrowserPth):
                trackKeys['Database Browser'] = ['Database Browser', get_icon('SQliteTool'), dbBrowserPth]

            # Advance Renamer.
            if os.path.exists(advanceRenamerPth):
                trackKeys['Advance Renamer'] = ['Advance Renamer 3.8', get_icon('AdvanceRenamer'), advanceRenamerPth]

        info['pipeline'] = trackKeys
        pipelineConfig_yaml = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'config', 'main_config.yml')
        pipelineConfig_json = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData', 'config', 'main_config.json')
        dataHandle('yaml', 'w', pipelineConfig_yaml, trackKeys)
        dataHandle('json', 'w', pipelineConfig_json, trackKeys)
        info['icon'] = iconInfo
        # iconConfig = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData/icon_config.yml')
        #
        # if not os.path.exists(iconConfig):
        #     dataHandle('yaml', 'w', iconConfig, iconInfo)

        # envKeys = {}
        # for key in os.environ.keys():
        #     envKeys[key] = os.getenv(key)

        # pth = os.path.join(os.getenv('PIPELINE_TOOL'), 'appData/sysPath_config.yml')
        #
        # if not os.path.exists(pth):
        #     dataHandle('yaml', 'w', pth, envKeys)

    def deleteKey(self, keys, n=True):
        if not n:
            return self.appInfo
        else:
            for key in keys:
                try:
                    self.appInfo[key]
                except KeyError:
                    continue
                else:
                    del self.appInfo[key]

        return self.appInfo
# ----------------------------------------------------------------------------------------------------------- #

def check_blank(data, *args):
    if len(data) == 0 or data == "" or data is None:
        return False
    else:
        return True

def check_match(data1, data2, *args):

    if len(data1) == len(data2):
        count = len(data1) - 1
        for i in range(len(data1)):
            if data1[i] == data2[i]:
                count = count - 1
            else:
                count = count + 1
            i += 1

        if count == 1:
            return True
        else:
            return False
    else:
        return False

# --------------------------------------------------------------------------------------------------------
"""                                                END OF CODE                                         """
# --------------------------------------------------------------------------------------------------------
