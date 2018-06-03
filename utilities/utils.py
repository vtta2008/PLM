#!/usr/bin/env python3
# coding=utf-8
"""
Script Name: utils.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Here is where a lot of function need to use multiple times overall
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, requests, platform, shutil, subprocess, urllib, winshell, yaml, json, pip, re, datetime, time, uuid, \
    win32api, cv2

from pyunpack import Archive

# Plt
import appData as app

# ----------------------------------------------------------------------------------------------------------- #
""" Simple log """

logger = app.set_log()

# ----------------------------------------------------------------------------------------------------------- #
""" Preset """

def preset_setup_config_data(*args):
    # setup local database
    if not os.path.exists(app.DBPTH):
        from appData import baseRC as base
        base.GenerateResource()

    # Set up app config directories
    for dirPth in [app.DAMGDIR, app.APPDIR, app.CONFIGDIR, app.SETTINGDIR, app.LOGODIR]:
        if not os.path.exists(dirPth):
            os.mkdir(dirPth)

def preset_load_appInfo(*args):
    if not os.path.exists(app.mainConfig):
        Collect_info()
    # Load info from file
    with open(app.mainConfig, 'r') as f:
        appInfo = json.load(f)
    return appInfo

def preset_implement_maya_tanker(*args):
    tk = os.path.join(os.getenv(app.__envKey__), 'tankers', 'pMaya')

    tranker = dict(modules = ['anim', 'lib', 'modeling', 'rendering', 'simulating', 'surfacing', ],
                     QtPlugins = [], )

    pVal = ""
    pyList = [os.path.join(tk, k) for k in tranker] + [os.path.join(tk, "modules", p) for p in tranker["modules"]]

    for p in pyList:
        pVal += p + ';'
    os.environ['PYTHONPATH'] = pVal

    # Copy userSetup.py from source code to properly maya folder
    usScr = os.path.join(os.getenv(app.__envKey__), 'packages', 'maya', 'userSetup.py')
    if os.path.exists(usScr):
        mayaVers = [os.path.join(tk, v) for v in app.autodeskVer if os.path.exists(os.path.join(tk, v))] or []
        if not len(mayaVers) == 0 or not mayaVers == []:
            for usDes in mayaVers:
                shutil.copy(usScr, usDes)

def preset_load_iconInfo(*args):
    with open(app.appIconCfg, 'r') as f:
        iconInfo = json.load(f)
    return iconInfo

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

def read_package_variable(key):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join('appData', '__init__.py')
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ')
            if parts and parts[0] == key:
                return parts[-1].strip("'")
    assert 0, "'{0}' not found in '{1}'".format(key, module_path)

# -------------------------------------------------------------------------------------------------------------
""" shotcut """

def create_shotcut(target, icon, shortcut, description):
    winshell.CreateShortcut(
        Path=os.path.join(winshell.desktop(), shortcut),
        Target=target,
        Icon=(icon, 0),
        Description=description
    )
# -------------------------------------------------------------------------------------------------------------
""" Error handle """

def handle_path_error(directory=None):
    if not os.path.exists(directory) or directory is None:
        try:
            raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
        except IsADirectoryError as error:
            pass
            # logger.info('Caught error: ' + repr(error))

# -------------------------------------------------------------------------------------------------------------
""" Installation """

def install_py_packages(name, *args):
    """
    Install python package via command prompt
    :param name: name of component
    :return:
    """
    # logger.info('Using pip to install %s' % name)
    if os.path.exists(name):
        subprocess.Popen('python %s install' % name)
    else:
        subprocess.Popen('python -m pip install %s' % name, shell=True).wait()

def install_required_package():
    for pkg in app.__pkgsReq__:
        try:
            subprocess.Popen("python -m pip install %s" % pkg)
        except FileNotFoundError:
            subprocess.Popen("pip install %s" % pkg)
        finally:
            subprocess.Popen("python -m pip install --upgrade %s" % pkg)

def uninstall_all_required_package():
    __pkgsReq__ = app.__pkgsReq__
    for pkg in app.__pkgsReq__:
        try:
            subprocess.Popen("python -m pip uninstall %s" % pkg)
        except FileNotFoundError:
            subprocess.Popen("pip uninstall %s" % pkg)
            __pkgsReq__.remove(pkg)

    if len(__pkgsReq__)==0:
        return True
    else:
        return False

# -------------------------------------------------------------------------------------------------------------
""" Inspect info """

def get_python_pkgs():
    pyPkgs = {}
    pyPkgs['__mynote__'] = 'import pip; pip.get_installed_distributions()'

    for package in pip.get_installed_distributions():
        name = package.project_name  # SQLAlchemy, Django, Flask-OAuthlib
        key = package.key  # sqlalchemy, django, flask-oauthlib
        module_name = package._get_metadata("top_level.txt")  # sqlalchemy, django, flask_oauthlib
        location = package.location  # virtualenv lib directory etc.
        version = package.version  # version number

        pyPkgs[name] = [key, version, location]

    pkgConfig = os.path.join(app.dtDir.split('appData')[0], 'appData', 'pkgs_config.yml')

    with open(pkgConfig, 'w') as f:
        yaml.dump(pyPkgs, f, default_flow_style=False)

    return pyPkgs

def inspect_package(name):
    """
    check python component, if false, it will install component
    :param name:
    :return:
    """
    # logger.info( 'Trying to import %s' % name )
    allPkgs = get_python_pkgs()
    if name in allPkgs:
        # logger.info('package "%s" is already installed' % name)
        pass
    else:
        # logger.info('package "%s" is not installed, '
        #             'execute package installation procedural' % name)
        install_py_packages(name)

def get_all_env_key(key, path):
    try:
        pth = os.getenv(key)
        if pth == None or pth == '':
            # logger.info('install new environment variable')
            os.environ[key] = path
    except KeyError:
        # logger.info('install new environment variable')
        os.environ[key] = path
    else:
        pass

def get_all_path_from_dir(directory):
    """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    filePths = []   # List which will store all of the full file paths.
    dirPths = []    # List which will store all of the full folder paths.

    # Walk the tree.
    for root, directories, files in os.walk(directory, topdown=False):
        for filename in files:
            filePths.append(os.path.join(root, filename))  # Add to file list.
        for folder in directories:
            dirPths.append(os.path.join(root, folder)) # Add to folder list.
    return [filePths, dirPths]

def get_file_path(directory):
    handle_path_error(directory)
    return get_all_path_from_dir(directory)[0]

def get_folder_path(directory):
    handle_path_error(directory)
    return get_all_path_from_dir(directory)[1]

def get_base_folder(path):
    return os.path.dirname(path)

def get_base_name(path):
    return os.path.basename(path)

# -------------------------------------------------------------------------------------------------------------
""" Functions content """

def download_single_file(url, path_to, *args):
    execute_download = urllib.urlretrieve(url, path_to)
    # logger.info(execute_download)
    # logger.info("Downloaded to: %s" % str(path_to))

def download_image_from_url(link, *args):
    fileName = os.path.basename(link)
    imgPth = os.path.join(app.dtDir.split('appData')[0], 'avatar')
    avatarPth = os.path.join(imgPth, fileName)

    if not os.path.exists(avatarPth):
        download_single_file(link, avatarPth)

    return avatarPth

def extract_files(inDir, file_name, outDir, *args):
    Archive(os.path.join(inDir, file_name)).extractall(outDir)

def fix_image_files(root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for dir in dirs:
            system_call("mogrify *.png", "{}".format(os.path.join(path, dir)))

def obj_properties_setting(directory, mode, *args):
    if platform.system() == "Windows" or platform.system() == "Darwin":
        if mode == "h":
            if platform.system() == "Windows":
                subprocess.call(["attrib", "+H", directory])
            elif platform.system() == "Darwin":
                subprocess.call(["chflags", "hidden", directory])
        elif mode == "s":
            if platform.system() == "Windows":
                subprocess.call(["attrib", "-H", directory])
            elif platform.system() == "Darwin":
                subprocess.call(["chflags", "nohidden", directory])
        else:
            logger.debug("ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
    else:
        logger.debug("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

def batch_obj_properties_setting(listObj, mode, *args):

    for obj in listObj:
        if os.path.exists(obj):
            obj_properties_setting(obj, mode)
        else:
            pass
            # logger.info('Could not find the specific path: %s' % obj)

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
        # logger.info('The source folder: %s is not exists' % imgDir)
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
    info = {}
    if type == 'json':
        if mode == 'r' or mode == 'r+':
            with open(filePath, mode) as f:
                info = json.load(f)
        elif mode == 'w' or mode == 'w+':
            with open(filePath, mode) as f:
                info = json.dump(data, f, indent=4)
        else:
            with open(filePath, mode) as f:
                info = json.dump(data, f, indent=4)
    else:
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

def cmd_execute_py(name, path, *args):
    """
    Executing a python file
    :param name: python file name
    :param path: path to python file
    :return: executing in command prompt
    """
    # logger.info("Executing {name} from {path}".format(name=name, path=path))
    pth = os.path.join(path, name)
    if os.path.exists(pth):
        subprocess.call([sys.executable, pth])

def system_call(args, cwd="."):
    logger.info("Running '{}' in '{}'".format(str(args), cwd))
    subprocess.call(args, cwd=cwd)
    pass

def open_plt_browser(url, *args):
    from ui import Browser
    web = Browser.WebBrowser(url)
    web.show()
    web.exec_()

def reconfig_data(*args):
    pass

# -------------------------------------------------------------------------------------------------------------
""" Collecting info user """

def get_local_pc(*args):

    package = app.KEYPACKAGE
    pythonVersion = sys.version
    windowOS = platform.system()
    windowVersion = platform.version()

    sysOpts = package['sysOpts']
    cache = os.popen2("SYSTEMINFO")
    source = cache[1].read()

    sysInfo = {}

    sysInfo['python'] = pythonVersion
    sysInfo['os'] = windowOS + "|" + windowVersion
    sysInfo['pcUser'] = platform.node()
    sysInfo['operating system'] = platform.system() + "/" + platform.platform()
    sysInfo['python version'] = platform.python_version()

    values = {}

    for opt in sysOpts:
        values[opt] = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % (opt), source, re.IGNORECASE)][0]
    for item in values:
        sysInfo[item] = values[item]

    return sysInfo

def get_screen_resolution(*args):
    resW = win32api.GetSystemMetrics(0)
    resH = win32api.GetSystemMetrics(1)
    return resW, resH

def get_window_taskbar_size(*args):
    resW, resH = get_screen_resolution()
    monitors = win32api.EnumDisplayMonitors()
    display1 = win32api.GetMonitorInfo(monitors[0][0])
    tbH = resH - display1['Work'][3]
    tbW = resW
    return tbW, tbH

def get_datetime(*args):
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def get_date(*args):
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[0]

def get_time(*args):
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[1]

def get_token(*args):
    return str(uuid.uuid4())

def get_unix(*args):
    return (str(uuid.uuid4())).split('-')[-1]

def get_pc_location(*args):
    r = requests.get('https://api.ipdata.co').json()

    for key in r:
        k = (str(key))
        if k == 'ip':
            ip = str(r[key])
        elif k == 'city':
            city = str(r[key])
        elif k == 'country_name':
            country = str(r[key])
        else:
            ip = city = country = 'unknown'

    return ip, city, country

# -------------------------------------------------------------------------------------------------------------
""" Layout setting """

def set_buffer_and_offset(offsetX=5, offsetY=5, *args):
    tbW, tbH = get_window_taskbar_size()
    resW, resH = get_screen_resolution()
    if tbW == resW:
        bufferX = 0
    elif tbW > resW:
        bufferX = resW - tbW
    else:
        bufferX = tbW - resW
    bufferY = tbH
    return bufferX, bufferY, offsetX, offsetY

# ----------------------------------------------------------------------------------------------------------- #
""" Plt app functions """

def screenshot(*args):
    from ui import Screenshot
    screen = Screenshot.Screenshot()
    screen.exec_()

def run(pth, *args):
    subprocess.Popen(pth)

# ----------------------------------------------------------------------------------------------------------- #
""" Quick find path """

def getAppIcon(size=32, iconName="AboutPlt"):
    iconPth = os.path.join(os.getenv(app.__envKey__), 'imgs', 'icons', "x" + str(size))
    return os.path.join(iconPth, iconName + ".icon.png")

def getLogo(size=32, name="DAMG", *args):
    if name == "Logo":
        logoPth = os.path.join(os.getenv(app.__envKey__), 'imgs', 'logo', 'Plt', 'icons')
    elif name == 'DAMG':
        logoPth = os.path.join(os.getenv(app.__envKey__), 'imgs', 'logo', 'DAMGteam', 'icons')
    else:
        logoPth = os.path.join(os.getenv(app.__envKey__), 'imgs', 'logo', 'Plt', 'icons')

    return os.path.join(logoPth, str(size) + "x" + str(size) + ".png")

def getWebIcon(name, *args):
    webiconPth = os.path.join(os.getenv(app.__envKey__), 'imgs', 'web')
    icons = [i for i in get_file_path(webiconPth) if ".avatar" in i]
    for i in icons:
        if name in i:
            return i

def getAvatar(name, *args):
    avatars = [a for a in get_file_path(os.path.join(os.getenv(app.__envKey__), 'imgs', 'avatar')) if '.avatar' in a]
    for a in avatars:
        if name in a:
            return a

def getTag(name, *args):
    tags = [t for t in get_file_path(os.path.join(os.getenv(app.__envKey__), 'imgs', 'tags')) if '.tag' in t]
    for t in tags:
        if name in t:
            return t

# ----------------------------------------------------------------------------------------------------------- #
""" Encode, decode, convert """

def text_to_utf8(input):
    return input.encode('utf-8')

def text_to_hex(text):
    return ''.join(["%02X" % ord(x) for x in str(text)])

def hex_to_text(hex):
    bytes = []
    hexStr = ''.join(str(hex).split(" "))
    for i in range(0, len(hexStr), 2):
        bytes.append(chr(int(hexStr[i:i + 2], 16)))
    outPut = ''.join(bytes)
    return outPut

def str2bool(arg):
    return str(arg).lower() in ['true', 1, '1', 'ok', '2']

def bool2str(arg):
    if arg:
        return "True"
    else:
        return "False"

# ----------------------------------------------------------------------------------------------------------- #
""" Checking info """

def check_blank(data, *args):
    if len(data) == 0 or data == "" or data is None:
        return False
    else:
        return True

def check_match(data1, data2, *args):
    check = []
    if len(data1) == len(data2):
        for i in range(len(data1)):
            if data1[i] is data2[i]:
                continue
            else:
                check.append('False')
    else:
        check.append('False')

    if len(check) == 0:
        return True
    else:
        return False

# ----------------------------------------------------------------------------------------------------------- #
""" Math """
def check_odd(num):
    return str2bool(num%2)

def get_all_odd(numLst):
    return [i for i in numLst if check_odd(i)]

def get_all_even(numLst):
    return [i for i in numLst if not check_odd(i)]

# ----------------------------------------------------------------------------------------------------------- #
""" Remove data """

def del_key(key, dict = {}):
    try:
        del dict[key]
        # logger.info("key deleted: {key}".format(key=key))
    except KeyError:
        dict.pop(key, None)
        # logger.info("key poped: {key}".format(key=key))

# ----------------------------------------------------------------------------------------------------------- #
""" Remove data """

def clean_pyc_file(var, *args):
    fileNames = [f for f in get_file_path(app.dtDir.split('appData')[0]) if var in f] or []
    if not fileNames == []:
        for filePth in fileNames:
            os.remove(filePth)

def config_info(*args):
    Collect_info()

def shutdown(*args):
    os.system("shutdown /p")

def open_cmd(*args):
    os.system("start /wait cmd")

# ----------------------------------------------------------------------------------------------------------- #
""" Collecting all info. """

class Collect_info():
    """
    Initialize the main class functions
    :param package: the package of many information stored from default variable
    :param names: the dictionary of names stored from default variable
    :returns: all installed app info, package app info, icon info, image info, pc info.

    """
    def __init__(self):

        super(Collect_info, self).__init__()

        self.collect_env_variables()
        self.collect_icon_path()
        self.collect_all_app()
        self.collect_main_app()

    def collect_env_variables(self):
        envKeys = {}
        for key in os.environ.keys():
            envKeys[key] = os.getenv(key)
        self.create_config_file('envKeys', envKeys)

    def collect_icon_path(self):
        # Create dictionary for icon info
        self.iconInfo = {}
        self.iconInfo['Logo'] = app.PLTLOGO
        self.iconInfo['DAMG'] = app.DAMGLOGO
        # Custom some info to debug
        self.iconInfo['Sep'] = 'separato.png'
        self.iconInfo['File'] = 'file.png'
        # Get list of icons in imgage folder
        iconlst = [i for i in get_file_path(app.ICONDIR32) if i.endswith(".png")]
    
        for i in iconlst:
            self.iconInfo[os.path.basename(i).split('.icon')[0]] = i

        self.create_config_file('icon', self.iconInfo)

    def collect_all_app(self):
        """
        It will find and put all the info of installed apps to two list: appname and path
        return: self.appName, self.appPath
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

        self.appInfo = {}

        for name in appName:
            self.appInfo[str(name)] = str(appPth[appName.index(name)])

        self.create_config_file("app", self.appInfo)

    def collect_main_app(self):

        self.mainInfo = {}

        delKeys = []
        for key in self.appInfo:
            for k in app.KEYDETECT:
                if k in key:
                    delKeys.append(key)

        for key in delKeys:
            del_key(key, self.appInfo)

        keepKeys = [k for k in app.KEYPACKAGE if k in self.appInfo and k in self.iconInfo]

        # Custom functions
        self.mainInfo['Exit'] = ['Exit Pipeline Tool', self.iconInfo['Exit'], 'Func: Exit']
        self.mainInfo['CleanPyc'] = ['Clean ".pyc" files', self.iconInfo['CleanPyc'], 'Func: CleanPyc']
        self.mainInfo['ClearData'] = ['Clean Config data', self.iconInfo['CleanConfig'], 'Func: CleanConfigData']
        self.mainInfo['ReConfig'] = ['Re configuring data', self.iconInfo['Reconfig'], 'Func: Config']
        self.mainInfo['Command Prompt'] = ['Open command prompt', self.iconInfo['Command Prompt'], 'Func: open_cmd']
        self.mainInfo['Plt wiki'] = ['Plt wiki', self.iconInfo['Plt wiki'], "Url: {key}".format(key=app.__pltWiki__)]
        self.mainInfo['PltBrowser'] = ['PltBrowser', self.iconInfo['PltBrowser'], "UI: PltBrowser"]
        self.mainInfo['OpenConfig'] = ['Open config folder', self.iconInfo['OpenConfig'], '']

        for key in self.appInfo:
            if 'NukeX' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
            elif 'Hiero' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
            elif 'UVLayout' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"

        # Extra app come along with plt but not be installed in local.
        dbBrowserPth = os.path.join(os.getenv(app.__envKey__), 'tankers', 'sqlbrowser', 'SQLiteDatabaseBrowserPortable.exe')

        advanceRenamerPth = os.path.join(os.getenv(app.__envKey__), 'tankers', 'batchRenamer', 'ARen.exe')

        qtDesigner = os.path.join(os.getenv('PROGRAMDATA'), 'Anaconda3', 'Library', 'bin', 'designer.exe')

        davinciPth = os.path.join(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')

        eVal = [dbBrowserPth, advanceRenamerPth, qtDesigner, davinciPth]

        eKeys = ['Database Browser', 'Advance Renamer', 'QtDesigner', 'Davinci Resolve 14']

        for key in eKeys:
            if os.path.exists(eVal[eKeys.index(key)]):
                self.mainInfo[key] = [key, getAppIcon(32, key), "App: {key}".format(key=eVal[eKeys.index(key)])]

        for key in keepKeys:
            self.mainInfo[key] = [key, getAppIcon(32, key), "App: {key}".format(key=self.appInfo[key])]

        for key in app.CONFIG_APPUI:
            self.mainInfo[key] = [key, getAppIcon(32, key), "UI: {key}".format(key=key)]

        for key in app.CONFIG_SYSTRAY:
            self.mainInfo[key] = [key, getAppIcon(32, key), "Func: {key}".format(key=key)]

        self.create_config_file('main', self.mainInfo)

    def create_config_file(self, name, data):
        if name == 'envKeys':
            filePth = app.pyEnvCfg
        elif name == "main":
            filePth = app.mainConfig
        elif name=='icon':
            filePth = app.appIconCfg
        elif name == 'app':
            filePth = app.appConfig
        else:
            filePth = app.webIconCfg

        dataHandle('json', 'w', filePth, data)

# ----------------------------------------------------------------------------------------------------------- #