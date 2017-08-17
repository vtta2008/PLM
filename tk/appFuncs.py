# coding=utf-8
"""
Script Name: appFuncs.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script will find all the path of modules, icons, images ans store them to a file
"""

import os, sys, logging, json, subprocess, pip

DATA_KEY = "PIPELINE_TOOL"

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

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

    pkgInfo = os.path.join(os.getenv(DATA_KEY), os.path.join('scrInfo', 'packages.info'))

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
def checkPlugin(name, *args):
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
        logger.info('package "%s" is not installed, execute package installation procedural' % name)
        install_package(name)


# Create environment variable by custom key
def createKey(key, scrInstall, toolName, *args):
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
    toolPth = os.path.join(scrInstall, toolName)
    if not os.path.exists(toolPth):
        os.mkdir(toolPth)
    os.environ[key] = toolPth

# Check the value of environment variable
def checkEnvKey(key, scrInstall, toolName, *args):
    try:
        pth = os.getenv(key)
        if pth == None or pth == '':
            createKey(key, scrInstall, toolName)
    except KeyError:
        createKey(key, scrInstall, toolName)
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
def saveCurrentUserLogin(userName, *args):
    userDataPth = os.path.join(os.getenv(DATA_KEY), os.path.join('scrInfo', 'user.info'))

    with open(userDataPth, 'r') as f:
        userData = json.load(f)

    curUser = {}
    curUser[userName] = userData[userName]
    currentUserLoginPth = os.path.join(os.getenv(DATA_KEY), 'user.tempLog')
    with open(currentUserLoginPth, 'w') as f:
        json.dump(curUser, f, indent=4)

    logger.info('save file to %s' % currentUserLoginPth)