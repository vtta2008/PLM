# -*- coding: utf-8 -*-
"""

Script Name: _data.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, platform, subprocess, json, shutil, pkg_resources, requests, uuid, socket, pprint
from platform import system

PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT

try:
    from importlib import reload
except ImportError:
    pass

PLATFORM = 'Windows'
API_MINIMUM = 0.64

from appData                        import metadatas as m
from .dirs                          import *
from .pths                          import *
from .text                          import *
from .keys                          import *
from .types                         import *
from .formats                       import *
from .options                       import *

from bin.data.localSQL              import SQLS
from bin                            import DAMGDICT

try:
    import winshell
except ImportError:
    subprocess.Popen('python -m pip install winshell --user', shell=True).wait()
    import winshell

try:
    import wmi
except ImportError:
    subprocess.Popen('python -m pip install wmi --user', shell=True).wait()
    import wmi
finally:
    com = wmi.WMI()

from cores.EnvVariableManager       import EnvVariableManager
envVar                              = EnvVariableManager()

# -------------------------------------------------------------------------------------------------------------
""" Environment configKey """

__envKey__              = m.__envKey__
PLMAPPID                = m.PLMAPPID
VERSION                 = m.VERSION
COPYRIGHT               = m.COPYRIGHT

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__copyright__           = m.COPYRIGHT
__organization__        = m.__organization__
__groupname__           = m.__groupname__
__damgSlogan__          = m.__damgSlogan__
__website__             = m.__website__
__author1__             = m.__author1__
__author2__             = m.__author2__
__Founder__             = m.__author1__
__CoFonder1__           = m.__author2__
__email1__              = m.__email1__
__email2__              = m.__email2__

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__             = m.__project__
__appname__             = m.__appname__
__appShortcut__         = m.__appShortcut__
__version__             = m.__version__
__versionFull__         = m.VERSION
__cfgVersion__          = m.__cfgVersion__
__verType__             = m.__verType__
__reverType__           = m.__reverType__
__about__               = m.__about__
__homepage__            = m.__homepage__
__plmSlogan__           = m.__plmSlogan__
__plmWiki__             = m.__plmWiki__

# -------------------------------------------------------------------------------------------------------------
""" Server """

__globalServer__        = m.__globalServer__
__globalServerCheck__   = m.__globalServerCheck__
__globalServerAutho__   = m.__globalServerAutho__

__localPort__           = m.__localPort__
__localHost__           = m.__localHost__
__localServer           = m.__localServer__
__localServerCheck__    = m.__localServerCheck__
__localServerAutho__    = m.__localServerAutho__

__google__              = m.__google__
__googleVN__            = m.__googleVN__
__googleNZ__            = m.__googleNZ__

__email__               = m.__email__

__packages_dir__        = m.__packages_dir__
__classifiers__         = m.__classifiers__
__download__            = m.__download__
__description__         = m.__description__
__readme__              = m.__readme__
__modules__             = m.__modules__
__pkgsReq__             = m.__pkgsReq__


class ConfigPython(DAMGDICT):

    key                 = 'ConfigPython'

    def __init__(self):
        super(ConfigPython, self).__init__()

        self['python'] = platform.python_build()
        self['python version'] = platform.python_version()

        pths = [p.replace('\\', '/') for p in os.getenv('PATH').split(';')[0:]]
        sys.path = [p.replace('\\', '/') for p in sys.path]

        for p in pths:
            if os.path.exists(p):
                if not p in sys.path:
                    sys.path.insert(-1, p)

        self['PATH']    = sys.path
        envVar.create_envVariable('PATH', sys.path)

        for py in pkg_resources.working_set:
            self[py.project_name] = py.version

        pprint.pprint(self)


class ConfigMachine(DAMGDICT):

    key                                 = 'ConfigMachine'

    usbCount = dvdCount = hddCount = pttCount = gpuCount = pciCount = keyboardCount = netCount = ramCount = miceCount \
    = cpuCount = biosCount = osCount = 1

    def __init__(self):
        super(ConfigMachine, self).__init__()

        self['os']                      = self.osInfo()
        self['bios']                    = self.biosInfo()
        self['cpu']                     = self.cpuInfo()
        self['gpu']                     = self.gpuInfo()
        self['ram']                     = self.ramInfo()
        self['drivers']                 = self.driverInfo()
        self['PCIs']                    = self.pciInfo()
        self['network']                 = self.networkInfo()
        self['keyboard']                = self.keyboardInfo()
        self['mice']                    = self.miceInfo()

        pprint.pprint(self)

    def osInfo(self, **info):
        source = subprocess.Popen("SYSTEMINFO", stdin=PIPE, stdout=PIPE).communicate()[0].decode('utf-8')
        for o in com.Win32_OperatingSystem():
            ops                         = {}
            key                         = 'os {0}'.format(self.osCount)
            ops['brand']                = o.Manufacturer
            ops['os name']              = o.Caption
            ops['device name']          = com.Win32_ComputerSystem()[0].DNSHostName
            ops['device type']          = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % ('OS Configuration'), source, re.IGNORECASE)][0]
            ops['registered email']     = o.RegisteredUser
            ops['organisation']         = o.Organization
            ops['version']              = o.Version
            ops['os architecture']      = o.OSArchitecture
            ops['serial number']        = o.SerialNumber
            ops['mac adress']           = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            info[key]                   = ops
            self.osCount += 1
        return info

    def biosInfo(self, **info):
        for b in com.Win32_BIOS():
            bios                        = {}
            key                         = 'bios {0}'.format(self.biosCount)
            bios['brand']               = com.Win32_ComputerSystem()[0].Manufacturer
            bios['name']                = b.Manufacturer
            bios['model']               = com.Win32_BaseBoard()[0].Product
            bios['type']                = com.Win32_ComputerSystem()[0].SystemType
            bios['version']             = b.BIOSVersion
            bios['sockets']             = com.Win32_ComputerSystem()[0].NumberOfProcessors
            info[key]                   = bios
            self.biosCount += 1
        return info

    def cpuInfo(self, **info):
        for c in com.Win32_Processor():
            cpu                         = {}
            key                         = 'cpu {0}'.format(self.cpuCount)
            cpu['name']                 = c.Name
            cpu['cores']                = c.NumberOfCores
            cpu['threads']              = c.NumberOfLogicalProcessors
            cpu['family']               = c.Caption
            cpu['max speed']            = '{0} GHz'.format(int(c.MaxClockSpeed) / 1000)
            cpu['type']                 = CPUTYPE[c.ProcessorType]
            cpu['l2 size']              = '{0} MB'.format(c.L2CacheSize)
            cpu['l3 size']              = '{0} MB'.format(c.L3CacheSize)
            info[key]                   = cpu
            self.cpuCount += 1
        return info

    def gpuInfo(self, **info):
        for g in (com.Win32_DisplayControllerConfiguration()):
            gpu                         = {}
            key                         = 'gpu {0}'.format(self.gpuCount)
            gpu['name']                 = g.Name
            gpu['refresh rate']         = g.RefreshRate
            gpu['bit rate']             = g.BitsPerPixel
            info[key]                   = gpu
            self.gpuCount += 1
        return info

    def ramInfo(self, **info):
        rams                            = []
        for r in com.Win32_PhysicalMemory():
            ram                         = {}
            key                         = 'physical ram {0}'.format(self.ramCount)
            ram['capacity']             = '{0} GB'.format(round(int(r.Capacity) / (1024.0 ** 3)))
            ram['bus']                  = r.ConfiguredClockSpeed
            ram['location']             = r.DeviceLocator
            ram['form']                 = FORMFACTOR[r.FormFactor]
            ram['type']                 = RAMTYPE[r.MemoryType]
            ram['part number']          = r.PartNumber
            rams.append(ram['capacity'])
            info[key]                   = ram
            self.ramCount += 1

        info['total'] = '{0} GB'.format(round(int(com.Win32_ComputerSystem()[0].TotalPhysicalMemory)/(1024.0 ** 3)))
        info['details'] = rams
        info['rams'] = len(com.Win32_PhysicalMemory())
        return info

    def driverInfo(self, **info):
        for physical_disk in com.Win32_DiskDrive():
            if physical_disk.associators("Win32_DiskDriveToDiskPartition") == []:
                disk                    = {}
                key                     = 'USB drive {0}'.format(self.usbCount)
                disk['brand']           = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                disk['index']           = physical_disk.Index
                disk['name']            = physical_disk.Name.replace('\\\\.\\', '')
                disk['model']           = physical_disk.Model
                disk['partition']       = physical_disk.Partitions
                disk['size']            = '0 GB'
                disk['type']            = DRIVETYPE[2]
                for d in com.Win32_LogicalDisk():
                    if d.DriveType == 2:
                        disk['path']    = '{0}/'.format(d.Caption)

                disk['firmware']        = physical_disk.FirmwareRevision
                info[key]               = disk
                self.usbCount += 1
            else:
                for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
                    if partition.associators("Win32_LogicalDiskToPartition") == []:
                        disk            = {}
                        key             = 'partition {0}'.format(self.pttCount)
                        disk['brand']   = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                        disk['firmware'] = physical_disk.FirmwareRevision
                        disk['index']   = '{0} - {1}'.format(partition.DiskIndex, partition.Index)
                        disk['name']    = partition.Name
                        disk['model']   = physical_disk.Model
                        disk['partition'] = partition.Caption
                        disk['size']    = '{0} GB'.format(round(int(partition.size) / (1024.0 ** 3)))
                        disk['block']   = '{0} MB'.format(round(int(partition.NumberOfBlocks) / (1024.0 ** 2)))
                        disk['offset']  = '{0} GB'.format(round(int(partition.StartingOffset) / (1024.0 ** 3)))
                        disk['type']    = partition.Type
                        info[key]       = disk
                        self.pttCount += 1
                    else:
                        for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                            disk        = {}
                            key         = 'harddrive {0}'.format(self.hddCount)
                            disk['brand'] = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                            disk['path'] = '{0}/'.format(logical_disk.Caption)
                            disk['index'] = physical_disk.Index
                            disk['name'] = '{0} ({1})'.format(logical_disk.VolumeName, logical_disk.Caption)
                            disk['model'] = physical_disk.Model
                            disk['partition'] = partition.Caption
                            disk['size'] = '{0} GB'.format(round(int(logical_disk.size) / (1024.0 ** 3)))
                            disk['free size'] = '{0} GB'.format(round(int(logical_disk.FreeSpace) / (1024.0 ** 3)))
                            disk['type'] = DRIVETYPE[logical_disk.DriveType]
                            disk['firmware'] = physical_disk.FirmwareRevision
                            disk['setup type'] = logical_disk.FileSystem
                            info[key] = disk
                            self.hddCount += 1

        if not com.Win32_CDROMDrive() is []:
            disk = {}
            key = 'CD drive {0}'.format(self.dvdCount)
            disk['brand'] = (com.Win32_CDROMDrive()[0].DeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
            disk['path'] = '{0}/'.format(com.Win32_CDROMDrive()[0].Drive)
            disk['index'] = com.Win32_CDROMDrive()[0].Id
            disk['name'] = com.Win32_CDROMDrive()[0].Name
            disk['model'] = com.Win32_CDROMDrive()[0].Caption
            disk['type'] = com.Win32_CDROMDrive()[0].MediaType
            info[key] = disk
            self.dvdCount += 1

        return info

    def pciInfo(self, **info):
        for p in com.Win32_IDEController():
            pci                         = {}
            key                         = 'PCI rack {0}'.format(self.pciCount)
            pci['name']                 = p.Name
            pci['id']                   = p.DeviceID
            pci['status']               = p.Status
            info[key]                   = pci
            self.pciCount += 1
        return info

    def networkInfo(self, **info):
        info['LAN ip']                  = socket.gethostbyname(socket.gethostname())
        for n in com.Win32_NetworkAdapter():
            if n.AdapterType:
                network                 = {}
                key                     = 'network device {0}'.format(self.netCount)
                network['name']         = n.Name
                network['brand']        = n.Manufacturer
                network['id']           = n.DeviceID
                network['uid']          = n.GUID
                network['index']        = n.Index
                network['MacAdress']    = n.MACAddress
                network['connect id']   = n.NetConnectionID
                network['service name'] = n.ServiceName
                network['speed']        = n.Speed
                network['type']         = n.AdapterType
                network['type id']      = n.AdapterTypeID
                info[key]               = network
                self.netCount += 1
        return info

    def keyboardInfo(self, **info):
        for k in com.Win32_Keyboard():
            print(k)
            keyboard                    = {}
            key                         = 'keyboard {0}'.format(self.keyboardCount)
            # keyboard['brand']           = k.Manufacturer
            keyboard['name']            = k.Name
            keyboard['id']              = k.DeviceID
            keyboard['status']          = k.Status
            info[key]                   = keyboard
            self.keyboardCount += 1
        return info

    def miceInfo(self, **info):
        for m in com.Win32_PointingDevice():
            mice                        = {}
            key                         = 'mice {0}'.format(self.miceCount)
            mice['brand']               = m.Manufacturer
            mice['name']                = m.Name
            mice['id']                  = m.DeviceID
            mice['status']              = m.Status
            info[key]                   = mice
            self.miceCount += 1
        return info


class ConfigDirectory(DAMGDICT):

    key                                 = 'ConfigDirectory'

    def __init__(self):
        super(ConfigDirectory, self).__init__()
        from . import dirs
        keys                            = [k for k in vars(dirs).keys() if not k in notKeys]
        for k in keys:
            self[k]                     = vars(dirs)[k].replace('\\', '/')

        mode = 0o770
        for path in self.values():
            if not os.path.exists(path):
                (head, tail) = os.path.split(path)
                res = self.create_folder(head, mode)
                try:
                    original_umask = os.umask(0)
                    os.makedirs(path, mode)
                finally:
                    os.umask(original_umask)

                os.chmod(path, mode)

        pprint.pprint(self)


class ConfigPath(DAMGDICT):

    key                                = 'ConfigPath'

    def __init__(self):
        super(ConfigPath, self).__init__()
        from . import pths
        keys                            = [k for k in vars(pths).keys() if not k in notKeys]
        for k in keys:
            self[k]                     = vars(pths)[k].replace('\\', '/')

        pprint.pprint(self)


class ConfigEnvVar(DAMGDICT):

    key                                 = 'ConfigEnvVar'

    def __init__(self):
        super(ConfigEnvVar, self).__init__()

        for k, v in os.environ.items():
            self[k]                     = v.replace('\\', '/')

        pprint.pprint(self)


class ConfigIcon(DAMGDICT):

    key                                 = 'ConfigIcon'

    def __init__(self):
        super(ConfigIcon, self).__init__()

        self['icon12'] = self.get_icons(ICON_DIR_12)
        self['icon16'] = self.get_icons(ICON_DIR_16)
        self['icon24'] = self.get_icons(ICON_DIR_24)
        self['icon32'] = self.get_icons(ICON_DIR_32)
        self['icon48'] = self.get_icons(ICON_DIR_48)
        self['icon64'] = self.get_icons(ICON_DIR_64)

        self['maya']   = self.get_icons(MAYA_ICON_DIR)

        self['node']   = self.get_icons(NODE_ICON_DIR)

        self['tag']    = self.get_icons(TAG_ICON_DIR)

        self['web32']  = self.get_icons(WEB_ICON_32)
        self['web128'] = self.get_icons(WEB_ICON_128)

        pprint.pprint(self)

    def get_icons(self, dir):
        icons = DAMGDICT()
        for root, dirs, names in os.walk(dir, topdown=False):
            for name in names:
                icons[name.split('.icon')[0]] = os.path.join(root, name).replace('\\', '/')
        return icons


class ConfigAvatar(DAMGDICT):

    key                                 = 'ConfigAvatar'

    def __init__(self):
        super(ConfigAvatar, self).__init__()

        for root, dirs, names in os.walk(AVATAR_DIR, topdown=False):
            for name in names:
                self[name.split('.avatar')[0]] = os.path.join(root, name).replace('\\', '/')

        pprint.pprint(self)


class ConfigLogo(DAMGDICT):

    key                                 = 'ConfigLogo'

    def __init__(self):
        super(ConfigLogo, self).__init__()

        damgLogos                       = DAMGDICT()
        plmLogos                        = DAMGDICT()

        for root, dirs, names in os.walk(DAMG_LOGO_DIR, topdown=False):
            for name in names:
                damgLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        for root, dirs, names in os.walk(PLM_LOGO_DIR, topdown=False):
            for name in names:
                plmLogos[name.split('.png')[0]] = os.path.join(root, name).replace('\\', '/')

        self['DAMGTEAM']                = damgLogos
        self['PLM']                     = plmLogos

        pprint.pprint(self)


class ConfigPics(DAMGDICT):

    key                                 = 'ConfigPics'

    def __init__(self):
        super(ConfigPics, self).__init__()

        for root, dirs, names, in os.walk(PIC_DIR, topdown=False):
            for name in names:
                self[name.split('.node')[0]] = os.path.join(root, name).replace('\\', '/')

        pprint.pprint(self)


class ConfigMaya(DAMGDICT):

    key                                 = 'ConfigMaya'

    def __init__(self):
        super(ConfigMaya, self).__init__()
        modules = ['anim', 'lib', 'modeling', 'rendering', 'simulating', 'surfacing']
        modulePth = os.path.join(MAYA_DIR, 'modules')
        paths = [os.path.join(modulePth, m) for m in modules]
        envVar.create_envVariable('PYTHONPATH', ';'.join(paths))

        usScr = os.path.join(MAYA_DIR, 'userSetup.py')

        if os.path.exists(usScr):
            mayaVers = [os.path.join(MAYA_DIR, v) for v in autodeskVer if os.path.exists(os.path.join(MAYA_DIR, v))] or []
            if not len(mayaVers) == 0 or not mayaVers == []:
                for usDes in mayaVers:
                    shutil.copy(usScr, usDes)


class ConfigApps(DAMGDICT):

    key                         = 'ConfigApps'

    def __init__(self):
        super(ConfigApps, self).__init__()

        shortcuts               = {}
        programs                = winshell.programs(common=1)

        for paths, dirs, names in os.walk(programs):
            relpath = paths[len(programs) + 1:]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(paths, n)) for n in names])

        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                self[str(name)] = lnk.path

        removeKeys = []
        for key in self.keys():
            for k in KEYDETECT:
                if k in key:
                    removeKeys.append(key)

        for k in removeKeys:
            self.del_key(k)

        pprint.pprint(self)

    def del_key(self, key):
        try:
            del self[key]
        except KeyError:
            self.pop(key, None)


class ConfigPipeline(DAMGDICT):

    key                         = 'ConfigPipeline'

    with open(iconCfg, 'r') as f:
        iconInfo = json.load(f)

    with open(appsCfg, 'r') as f:
        appInfo = json.load(f)

    def __init__(self):
        super(ConfigPipeline, self).__init__()

        qtDesigner = os.path.join(os.getenv('PROGRAMDATA'), 'Anaconda3', 'Library', 'bin', 'designer.exe')
        davinciPth = os.path.join(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')

        eVal = [qtDesigner, davinciPth]
        eKeys = ['QtDesigner', 'Davinci Resolve 14']

        for key in eKeys:
            if os.path.exists(eVal[eKeys.index(key)]):
                self[key] = [key, self.iconInfo['icon32'][key], "{0}".format(eVal[eKeys.index(key)])]

        keepKeys = [k for k in KEYPACKAGE if k in self.keys() and k in self.iconInfo['icon32']]

        for key in self.appInfo:
            if 'NukeX' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
            elif 'Hiero' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
            elif 'UVLayout' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"

        for key in keepKeys:
                    self[key] = [key, self.iconInfo['icon32'][key], "{0}".format(self.appInfo[key])]

        for key in CONFIG_APPUI:
            if key == 'UserSetting':
                self[key] = ['Profile', self.iconInfo['icon32'][key], 'User Profile']
            elif key == 'SignIn':
                self[key] = ['Sign In', self.iconInfo['icon32'][key], 'SignIn']
            elif key == 'SignUp':
                self[key] = ['New Account', self.iconInfo['icon32'][key], 'Create new account']
            elif key == 'SwtichAccount':
                self[key] = ['Change Account', self.iconInfo['icon32'][key], 'Change other account']
            elif key == 'SignOut':
                self[key] = ['Sign Out', self.iconInfo['icon32'][key], 'Log Out']
            else:
                self[key] = [key, self.iconInfo['icon32'][key], "{0}".format(key)]

        for key in CONFIG_SYSTRAY:
            if key in self.appInfo:
                self[key] = [key, self.iconInfo['icon32'][key], self.appInfo[key]]
            elif key in FIX_KEY.keys():
                self[key] = [key, self.iconInfo['icon32'][key], FIX_KEY[key]]
            else:
                self[key] = [key, self.iconInfo['icon32'][key], key]


        # show layout
        self['About']                  = ['About PLM', self.iconInfo['icon32']['About'], 'About']
        self['CodeOfConduct']          = ['Code of Conduct', self.iconInfo['icon32']['CodeOfConduct'], 'CodeOfConduct']
        self['Contributing']           = ['Contributing', self.iconInfo['icon32']['Contributing'], 'Contributing']
        self['ReConfig']               = ['Re configuring qssPths', self.iconInfo['icon32']['ReConfig'], 'ReConfig']
        self['Reference']              = ['Reference', self.iconInfo['icon32']['Reference'], 'Reference']
        self['PLM wiki']               = ['PLM wiki', self.iconInfo['icon32']['PLM wiki'], "{key}".format(key=__plmWiki__)]
        self['Browser']                = ['Browser', self.iconInfo['icon32']['Browser'], "Browser"]
        self['OpenConfig']             = ['Open config folder', self.iconInfo['icon32']['OpenConfig'], '']
        self['Version']                = ['Version Info', 'Version', 'Version']
        self['Licence']                = ['Licence Info', 'Licence', 'Licence Info']

        self['Organisation']           = ['Organisation', 'OrganisationManager', 'Organisation']
        self['Team']                   = ['Team', 'TeamManager', 'Team']
        self['Project']                = ['Project', 'ProjectManager', 'Project']
        self['Task']                   = ['Task', 'TaskManager', 'Task']

        self['SettingUI']              = ['PLM Settings', 'Settings', 'SettingUI']
        self['Configuration']          = ['PLM Configuration', 'Configuration', 'Configuration']
        self['Showall']                = ['showall', 'ShowAll', 'showall']

        self['Alpha']                  = ['Open Alpha Map Library', 'AlphaLibrary', 'AlphaLibrary']
        self['HDRI']                   = ['Open HDRI Map Library', 'HDRILibrary', 'HDRILibrary']
        self['Texture']                = ['Open Texture Map Library', 'TextureLibrary', 'TextureLibrary']

        self['Feedback']               = ['Feedback', 'Feedback', 'Feedback']
        self['ContactUs']              = ['Contact Us', 'ContactUs', 'ContactUs']

        self['Restore']                = ['Restore', 'Restore', 'PipelineManager']
        self['Maximize']               = ['Maximize', 'Maximize', 'PipelineManager']
        self['Minimize']               = ['Minimize', 'Minimize', 'PipelineManager']

        self['Apperance']              = ['Appearance', 'Appearance', 'Appearance']

        # Executing
        self['CleanPyc']               = ['Clean ".pyc" files', self.iconInfo['icon32']['CleanPyc'], 'CleanPyc']
        self['Debug']                  = ['Run PLM Debugger', self.iconInfo['icon32']['Debug'], 'Debug']
        self['Exit']                   = ['Exit PLM', self.iconInfo['icon32']['Exit'], 'Exit']
        self['ConfigFolder']           = ['Go To Config Folder', 'ConfigFolder', CFG_DIR]
        self['IconFolder']             = ['Go To Icon Folder', 'IconFolder', APP_ICON_DIR]
        self['SettingFolder']          = ['Go To Setting Folder', 'SettingFolder', SETTING_DIR]
        self['AppFolder']              = ['Go To PLM Folder', 'AppFolder', ROOT_DIR]
        self['Command Prompt']         = ['Open command prompt', self.iconInfo['icon32']['Command Prompt'], 'open_cmd']

        self['Cut']                    = ['Cut', 'Cut', 'Cut']
        self['Copy']                   = ['Copy', 'Copy', 'Copy']
        self['Paste']                  = ['Paste', 'Paste', 'Paste']

        self['bright']                 = ['bright', 'bright', 'bright']
        self['dark']                   = ['dark', 'dark', 'dark']
        self['chacoal']                = ['chacoal', 'chacoal', 'chacoal']
        self['nuker']                  = ['nuker', 'nuker', 'nuker']

        # Update link
        self['pythonTag']              = ['pythonLink', 'pythonTagIcon', 'https://docs.anaconda.com/anaconda/reference/release-notes/']
        self['licenceTag']             = ['licenceLink', 'licenceTagIcon', 'https://github.com/vtta2008/damgteam/blob/master/LICENCE']
        self['versionTag']             = ['versionLink', 'versionTagIcon', 'https://github.com/vtta2008/damgteam/blob/master/appData/documentations/version.rst']




# -------------------------------------------------------------------------------------------------------------
""" Config directories """

class ConfigManager(DAMGDICT):

    key                                 = 'Configurations'

    checkList                           = DAMGDICT()

    printOutput                         = False
    subprocess                          = False
    cfgs                                = True
    _pthInfo                            = False
    _iconInfo                           = False
    _mainPkgs                           = False
    _appInfo                            = False

    def __init__(self):
        super(ConfigManager, self).__init__()

        if not os.path.exists(LOCAL_DB):
            SQLS(LOCAL_DB)

        self.checkList['db']            = True

        self.deviceInfo                 = ConfigMachine()
        self.save_data(deviceCfg, self.deviceInfo)
        self.checkList['device']        = True

        self.dirInfo                    = ConfigDirectory()
        self.save_data(dirCfg, self.dirInfo)
        self.checkList['dirs']          = True

        self.pathInfo                   = ConfigPath()
        self.save_data(pthCfg, self.pthInfo)
        self.checkList['paths']         = True

        self.pyInfo                     = ConfigPython()
        self.save_data(pythonCfg, self.pyInfo)
        self.checkList['python']        = True

        self.envInfo                    = ConfigEnvVar()
        self.save_data(envVarCfg, self.envInfo)
        self.checkList['envVar']        = True

        self.iconInfo                   = ConfigIcon()
        self.save_data(iconCfg, self.iconInfo)
        self.checkList['icons']         = True

        self.avatarInfo                 = ConfigAvatar()
        self.save_data(avatarCfg, self.avatarInfo)
        self.checkList['avatars']       = True

        self.logoInfo                   = ConfigLogo()
        self.save_data(logoCfg, self.logoInfo)
        self.checkList['logos']         = True

        self.picInfo                    = ConfigPics()
        self.save_data(picCfg, self.picInfo)
        self.checkList['pictures']      = True

        self.mayaInfo                   = ConfigMaya()
        self.save_data(mayaIconCfg, self.mayaInfo)
        self.checkList['maya']          = True

        self.appInfo                    = ConfigApps()
        self.save_data(appsCfg, self.appInfo)
        self.checkList['apps']          = True

        self.pipelineInfo               = ConfigPipeline()
        self.save_data(pipelineCfg, self.pipelineInfo)
        self.checkList['pipeline']      = True


    def save_data(self, filePth, data):
        if os.path.exists(filePth):
            os.remove(filePth)

        with open(filePth, 'w+') as f:
            json.dump(data, f, indent=4)
            f.close()
        return True

configManager = ConfigManager()

# -------------------------------------------------------------------------------------------------------------
""" Config qssPths from text file """

def read_file(fileName):

    filePth = os.path.join(RAWS_DATA_DIR, fileName)

    if not os.path.exists(filePth):
        filePth = os.path.join(DOCUMENTATION_DIR, "{}.rst".format(fileName))

    if os.path.exists(filePth):
        with open(filePth, 'r') as f:
            data = f.read()
        return data

QUESTIONS = read_file('QUESTION')
ABOUT = read_file('ABOUT')
CREDIT = read_file('CREDIT')
CODECONDUCT = read_file('CODECONDUCT')
CONTRIBUTING = read_file('CONTRIBUTING')
REFERENCE = read_file('REFERENCE')
LICENCE_MIT = read_file('LICENCE_MIT')

actionTypes = ['DAMGACTION', 'DAMGShowLayoutAction', 'DAMGStartFileAction', 'DAMGExecutingAction', 'DAMGOpenBrowserAction', ]

layoutTypes = ['DAMGUI', 'DAMGWIDGET', ] + actionTypes

with open(pipelineCfg, 'r') as f:
    mainData = json.load(f)
    f.close()

CONFIG_OFFICE = [k for k in mainData.keys() if k in CONFIG_OFFICE]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
