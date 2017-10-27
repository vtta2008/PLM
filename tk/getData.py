# coding=utf-8
"""
Script Name: getData.py
Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script will find all the path of modules, icons, images ans store them to a file
"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
import json, logging, os, sys, re, platform, winshell

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

from tk import defaultVariable as var
from tk import appFuncs as func

# ------------------------------------------------------
# DEFAULT VARIABLES
# ------------------------------------------------------
PACKAGE = var.MAIN_PACKPAGE
# List of file name
NAMES = var.MAIN_NAMES

# ----------------------------------------------------------------------------------------------------------- #
"""                MAIN CLASS: GET MODULE INFO - GET ALL INFO OF MODULES, ICONS, IMAGES                     """
# ----------------------------------------------------------------------------------------------------------- #
class GetData( object ):
    """
    This class will find all the info of python, icon, image files and folders then store them to info files in
    info folder
    """
    def __init__(self, package, names):
        """
        Initialize the main class functions
        :param package: the package of many information stored from default variable
        :param names: the dictionary of names stored from default variable
        :returns: all installed app info, package app info, icon info, image info, pc info.
        """
        logger.info('Updating data paths')

        func.proc('')

        self.createAllInfoFiles(package, names)

    def getPCinfo(self, package):
        """
        It will get all the info of section and store in an info file
        :param package: the package of many information stored from default variable
        :return: info file
        """
        # python version
        pythonVersion = sys.version
        # os
        windowOS = platform.system()
        # os version
        windowVersion = platform.version()
        # create dictionary to store info in
        sysInfo = {}
        # store python info
        sysInfo[ 'python' ] = pythonVersion
        # store os info
        sysInfo[ 'os' ] = windowOS + "|" + windowVersion
        # check if info folder exists, if not, create one
        values = {}
        cache = os.popen2( "SYSTEMINFO" )
        source = cache[ 1 ].read()
        sysOpts = package['sysOpts']
        sysInfo['artist name'] = platform.node()
        sysInfo['operating system'] = platform.system() + "/" + platform.platform()
        sysInfo['python version'] = platform.python_version()

        for opt in sysOpts:
            values[opt] = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % (opt), source, re.IGNORECASE)][0]

        for item in values:
            #self.createLog('stored %s: %s into sysInfo' % (item, values[item]))
            sysInfo[item] = values[item]

        return sysInfo

    def getModuleInfo(self, package):
        """
        Get all the info of modules
        :param package: the package of many information stored from default variable
        :param names: the dictionary of names stored from default variable
        :return: modules.info
        """
        # Create info module dictionary
        moduleInfo = {}
        # root path
        moduleInfo['root'] = package['root']
        # module path
        moduleInfo['app module'] = os.path.join(package['root'], package['py'][0])
        #self.createLog('adding %s to moduleInfo' % moduleInfo['app module'])
        # ui path
        moduleInfo['app ui'] = os.path.join(package['root'], package['py'][1])
        #self.createLog('adding %s to moduleInfo' % moduleInfo['app ui'])
        # loop to store all the python files found root's content to dictionary
        for pyFol in package['py']:
            pyPth = os.path.join(package['root'], pyFol)
            if os.path.exists(pyPth):
                sys.path.append(pyPth)
            files = [f for f in os.listdir(pyPth) if f.endswith('PipelineTool.py')]
            for file in files:
                # do not need __init__.py
                if '__init__' in file:
                    pass
                else:
                    pth = os.path.join( pyPth, file )
                    moduleInfo[file.split('PipelineTool.py')[0]] = pth
        # return the dictionary
        return moduleInfo

    def getIconInfo(self, package, names):
        """
        Get all the info of icons
        :param package: the package of many information stored from default variable
        :param names: the dictionsary of names stored from default variable
        :return: icons.info
        """
        # Create dictionary for icon info
        iconInfo = {}
        # Store unusual info
        iconInfo['Sep'] = 'separato.png'
        iconInfo['File'] = 'file.png'
        # store path info to dictionary
        iconInfo['iconPth'] = os.path.join(package['root'], package['image'][0])
        # get all the icon file in folder
        icons = [f for f in os.listdir(iconInfo['iconPth']) if '.icon' in f]
        # check if there is no files in folder
        if len(icons)==0:
            iconInfo['icons'] = None
        # if there is, make a loop to store them to info file one by one
        else:
            for i in icons:
                iconInfo[i.split('.icon')[0]] = os.path.join(iconInfo['iconPth'], i)
        #Get list of icon name
        iconNames = [f for f in iconInfo]
        # Create dictionary to story icon name in
        icons ={}
        # Store icon name into it
        icons['name'] = iconNames
        # return icons info
        return iconInfo

    def getImgInfo(self, package):
        """
        Get all the info of images
        :param package: the package of many information stored from default variable
        :return: imgs.info
        """
        # create dictionary for image info
        imgInfo = {}
        # store basic info into dictionary
        imgInfo['imgPth'] = os.path.join(package['root'], package['image'][1])
        # get list of image files in folder
        imgs = [f for f in os.listdir(imgInfo['imgPth']) if '.img' in f]
        # check if there is no image file
        if len(imgs)==0:
            imgInfo['imgs'] = None
        # if there is, store them one by one by a loop to info file
        else:
            for i in imgs:
                imgInfo[i.split('.png')[0]] = os.path.join(imgInfo['imgPth'], i)
        # return the info file
        return imgInfo

    def getAllAppInfo(self, package):
        """
        It will find and put all the info of installed apps to two list: appname and path
        :param filters: self.appName, self.appPath
        :return: self.appName, self.appPath
        """
        shortcuts = {}
        appName = []
        appPth = []
        # get list of all programmes installed in local pc
        all_programs = winshell.programs(common=1)
        # loop to store info to shortcut, path, filename.
        for dirpath, dirnames, filenames in os.walk(all_programs):
            relpath = dirpath[1+ len(all_programs):]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(dirpath, f)) for f in filenames])
        # loop to store all the app names, paths to a dictionary
        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                appName.append(name)
                appPth.append(lnk.path)
                #self.createLog('Found %s: %s' % (name, lnk.path))
        appInfo = {}
        # fix the encoding convention
        for name in appName:
            pth = appPth[appName.index(name)]
            pth = func.encode(pth, 'utf8')
            name = func.encode(name, 'utf8')
            appInfo[name] = pth
        # return data
        return appInfo

    def getPackageAppInfo(self, package, names):
        """
        It will Check if there is more than 1 version is installed
        :param package: the package of many information stored from default variable
        :param names: the dictionary of names stored from default variable
        :return: final app info
        """
        # Take app info return from function
        self.appInfo = self.getAllAppInfo(package)
        # logger.info(self.appInfo)
        # filter 1: find .exe path
        keys = [k for k in self.appInfo if not self.appInfo[k].endswith(package['ext'][0])]
        self.appInfo = self.deleteKey(keys, '1')
        # logger.info(self.appInfo)
        # filter 2: filter app name
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

        # logger.info(self.appInfo )
        # filter 3: filter keywords

        for k in package['filter']:
            for key in keys:
                if k in key:
                    # logger.info('%s: %s' % (k, key))
                    del self.appInfo[key]
        #return
        return self.appInfo

    def createAllInfoFiles(self, package, names):
        """
        Run all the functions inside class and take all the return info then store them to files
        :param package: the package of many information stored from default variable
        :return: info files
        """
        info = {}
        # check if info folder exists, if not, create one
        scrPth = package['appData']
        # logger.info('Checking path available: %s' % scrPth)
        if not os.path.exists(package['appData']):
            # logger.info('False, creating path %s' % package['appData'])
            os.mkdir(package['appData'])
        # take info return from modules
        # logger.info('collecting modules pth')
        info['modules'] = self.getModuleInfo(package)
        # take info return from icons
        # logger.info( 'collecting info pth' )
        iconInfo = self.getIconInfo(package, names)
        # take info return from image
        # logger.info( 'collecting images and icons pth' )
        info['image'] = self.getImgInfo(package)
        # take info return from sys
        # logger.info( 'collecting local computer configuration pth' )
        info['sys'] = self.getPCinfo(package)
        # take info return from all apps
        # logger.info('collecting installed apps pth')
        info['apps'] = self.getAllAppInfo(package)
        # take info return from apps
        # logger.info( 'collecting pipeline package apps pth' )
        self.appInfo = self.getPackageAppInfo(package, names)
        # logger.info( 'Fix paths which is not corrected' )
        for key in self.appInfo:
            # fix nukeX path
            if 'NukeX' in key:
                # logger.info( 'Fix Nukex path' )
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
            # fix Hiero path
            if 'Hiero' in key:
                # logger.info( 'Fix Hiero path' )
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
            # fix UVLayout path
            if 'UVLayout' in key:
                # logger.info( 'Fix UVLayout path' )
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"
        # take info and arrange them to pipeline
        trackKeys = {}
        for icon in iconInfo:
            for key in self.appInfo:
                if icon in key:
                    trackKeys[icon] = [key, iconInfo[icon], self.appInfo[key]]
                    # logger.info('%s, %s' % (key, icon))

        # insert info which is not in installed apps
        trackKeys['Logo'] = ['pipeline manager', iconInfo['Logo'], '']
        trackKeys['Sep'] = ['separator', iconInfo['Sep'], 'separator']
        trackKeys['File'] = ['File', iconInfo['File'], '']
        trackKeys['Exit'] = ['Exit application', iconInfo['Exit'], '']
        trackKeys['About'] = ['About pipeline tool', iconInfo['About'], 'About pipeline tool']
        trackKeys['Credit'] = ['Credit', iconInfo['Credit'], 'Thanks to all of you']
        trackKeys['Help'] = ['Introduction', iconInfo['Help'], '']
        # make a loop to store all info to files one by one
        # logger.info(iconInfo)

        info['pipeline'] = trackKeys
        info['icon'] = iconInfo
        # Save all info to directory
        logger.info( 'creating Info file' )
        self.createInfo(info, names, package)
        logger.info( 'creating environment variable file' )
        self.getSysPth(package=PACKAGE, names=NAMES)

    def getSysPth(self, package, names):
        envKeys = {}
        for key in os.environ.keys():
            envKeys[key] = os.getenv(key)

        pth = os.path.join(package['appData'], names['sysEnv'])
        logger.info('Saving file to %s' % pth)
        with open(pth, 'w') as f:
            json.dump(envKeys, f, indent=4)

        func.proc('update')

    def deleteKey(self, keys, n):
        for key in keys:
            try:
                self.appInfo[key]
            except KeyError:
                continue
            else:
                del self.appInfo[key]

        return self.appInfo

    def createInfo(self, info, names, package):
        with open(os.path.join(package['appData'], names['info']), 'w') as f:
            json.dump(info, f, indent=4)

def initialize(package=PACKAGE, names=NAMES):
    """
    This function will import all the variables which need to run the class
    :param package: the package of many information stored from default variable
    :param names: the dictionsary of names stored from default variable
    :return: info file, log file
    """
    GetData( package, names )

if __name__=='__main__':
    initialize(PACKAGE, NAMES)

# ----------------------------------------------------------------------------------------------------------- #
"""                                             END OF CODE                                                 """
# ----------------------------------------------------------------------------------------------------------- #