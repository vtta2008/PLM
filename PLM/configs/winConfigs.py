# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import subprocess, re, uuid, socket
from wmi                    import WMI


from .                      import CPU_TYPE, RAM_TYPE, FORM_FACTOR, DRIVE_TYPE
from pyPLM.Widgets import Application

PIPE                        = subprocess.PIPE
STDOUT                      = subprocess.STDOUT

sysKey                      = 'SYSTEMINFO'
optKey1                     = 'OS Configuration'
igCase                      = re.IGNORECASE
scr                         = subprocess.Popen(sysKey, stdin=PIPE, stdout=PIPE).communicate()[0].decode('utf-8')
optInfo1                    = re.findall("{0}:\w*(.*?)\n".format(optKey1), scr, igCase)

wmiObj                      = WMI()

baseBoardSys                = wmiObj.Win32_BaseBoard()
computerSys                 = wmiObj.Win32_ComputerSystem()
biosSys                     = wmiObj.Win32_BIOS()
operatingSys                = wmiObj.Win32_OperatingSystem()
processorSys                = wmiObj.Win32_Processor()
displaySys                  = wmiObj.Win32_DisplayControllerConfiguration()
memorySys                   = wmiObj.Win32_PhysicalMemory()
logicalDiskSys              = wmiObj.Win32_LogicalDisk()
cdromSys                    = wmiObj.Win32_CDROMDrive()
diskDriveSys                = wmiObj.Win32_DiskDrive()
pciSys                      = wmiObj.Win32_IDEController()
networkSys                  = wmiObj.Win32_NetworkAdapter()
keyboardSys                 = wmiObj.Win32_Keyboard()
miceSys                     = wmiObj.Win32_PointingDevice()
totalRam                    = computerSys[0].TotalPhysicalMemory


def osInfo(**info):

    count = 1
    for o in operatingSys:
        ops = {}
        key = 'os {0}'.format(count)
        ops['brand'] = o.Manufacturer
        ops['os name'] = o.Caption
        ops['device name'] = computerSys[0].DNSHostName
        ops['device type'] = [item.strip() for item in optInfo1][0]
        ops['registered email'] = o.RegisteredUser
        ops['organisation'] = o.Organization
        ops['version'] = o.Version
        ops['os architecture'] = o.OSArchitecture
        ops['serial number'] = o.SerialNumber
        ops['mac adress'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info[key] = ops
        count += 1

    return info

def biosInfo( **info):

    count = 1
    for b in biosSys:
        bios = {}
        key = 'bios {0}'.format(count)
        bios['brand'] = computerSys[0].Manufacturer
        bios['name'] = b.Manufacturer
        bios['model'] = baseBoardSys[0].Product
        bios['type'] = computerSys[0].SystemType
        bios['version'] = b.BIOSVersion
        bios['sockets'] = computerSys[0].NumberOfProcessors
        info[key] = bios
        count += 1
    return info

def cpuInfo(**info):

    count = 1
    for c in processorSys:
        cpu = {}
        key = 'cpu {0}'.format(count)
        cpu['name'] = c.Name
        cpu['cores'] = c.NumberOfCores
        cpu['threads'] = c.NumberOfLogicalProcessors
        cpu['family'] = c.Caption
        cpu['max speed'] = '{0} GHz'.format(int(c.MaxClockSpeed) / 1000)
        cpu['type'] = CPU_TYPE[c.ProcessorType]
        cpu['l2 size'] = '{0} MB'.format(c.L2CacheSize)
        cpu['l3 size'] = '{0} MB'.format(c.L3CacheSize)
        info[key] = cpu
        count += 1
    return info

def gpuInfo(**info):
    count = 1
    for g in displaySys:
        gpu = {}
        key = 'gpu {0}'.format(count)
        gpu['name'] = g.Name
        gpu['refresh rate'] = g.RefreshRate
        gpu['bit rate'] = g.BitsPerPixel
        info[key] = gpu
        count += 1
    return info

def screenInfo(**info):

    allScreens = Application.screens()
    count = 1
    for index, screen_no in enumerate(allScreens):
        screenInfo = {}
        key = 'screen {0}'.format(count)
        screen = allScreens[index]
        screenInfo['resolution'] = '{0}x{1}'.format(screen.size().width(), screen.size().height())
        screenInfo['depth'] = screen.depth()
        screenInfo['serial'] = screen.serialNumber()
        screenInfo['brand'] = screen.manufacturer()
        screenInfo['model'] = screen.model()
        screenInfo['name'] = screen.name()
        screenInfo['dpi'] = screen.physicalDotsPerInch()
        info[key] = screenInfo
        count += 1
    return info

def ramInfo(**info):
    rams = []
    count = 1
    for r in memorySys:
        ram = {}
        key = 'ram {0}'.format(count)
        ram['capacity'] = '{0} GB'.format(round(int(r.Capacity) / (1024.0 ** 3)))
        ram['bus'] = r.ConfiguredClockSpeed
        ram['location'] = r.DeviceLocator
        ram['form'] = FORM_FACTOR[r.FormFactor]
        ram['type'] = RAM_TYPE[r.MemoryType]
        ram['part number'] = r.PartNumber
        rams.append(ram['capacity'])
        info[key] = ram
        count += 1

    info['total'] = '{0} GB'.format(round(int(totalRam) / (1024.0 ** 3)))
    info['details'] = rams
    info['rams'] = len(memorySys)
    return info

def driverInfo(**info):

    usbCount = 1
    pttCount = 1
    hddCount = 1
    dvdCount = 1

    for physical_disk in diskDriveSys:

        try:
            physical_disk.associators("Win32_DiskDriveToDiskPartition")
        except Exception:
            print('Error occur due to the use of multi thread')
            import psutil
            disk = {}
            key = 'Hard Drive'
            for partition in psutil.disk_partitions():
                disk[partition.mountpoint] = (partition.fstype, partition.device)
            info[key] = disk
        else:
            if physical_disk.associators("Win32_DiskDriveToDiskPartition") == []:
                disk = {}
                key = 'USB drive {0}'.format(usbCount)
                disk['brand'] = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                disk['index'] = physical_disk.Index
                disk['name'] = physical_disk.Name.replace('\\\\.\\', '')
                disk['model'] = physical_disk.Model
                disk['partition'] = physical_disk.Partitions
                disk['size'] = '0 GB'
                disk['type'] = DRIVE_TYPE[2]
                for d in logicalDiskSys:
                    if d.DriveType == 2:
                        disk['path'] = '{0}/'.format(d.Caption)

                disk['firmware'] = physical_disk.FirmwareRevision
                info[key] = disk
                usbCount += 1
            else:
                for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
                    if partition.associators("Win32_LogicalDiskToPartition") == []:
                        disk = {}
                        key = 'partition {0}'.format(pttCount)
                        disk['brand'] = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                        disk['firmware'] = physical_disk.FirmwareRevision
                        disk['index'] = '{0} - {1}'.format(partition.DiskIndex, partition.Index)
                        disk['name'] = partition.Name
                        disk['model'] = physical_disk.Model
                        disk['partition'] = partition.Caption
                        disk['size'] = '{0} GB'.format(round(int(partition.size) / (1024.0 ** 3)))
                        disk['block'] = '{0} MB'.format(round(int(partition.NumberOfBlocks) / (1024.0 ** 2)))
                        disk['offset'] = '{0} GB'.format(round(int(partition.StartingOffset) / (1024.0 ** 3)))
                        disk['type'] = partition.Type
                        info[key] = disk
                        pttCount += 1
                    else:
                        for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                            disk = {}
                            key = 'harddrive {0}'.format(hddCount)
                            disk['brand'] = \
                            (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                            disk['path'] = '{0}/'.format(logical_disk.Caption)
                            disk['index'] = physical_disk.Index
                            disk['name'] = '{0} ({1})'.format(logical_disk.VolumeName, logical_disk.Caption)
                            disk['model'] = physical_disk.Model
                            disk['partition'] = partition.Caption
                            disk['size'] = '{0} GB'.format(round(int(logical_disk.size) / (1024.0 ** 3)))
                            disk['free size'] = '{0} GB'.format(round(int(logical_disk.FreeSpace) / (1024.0 ** 3)))
                            disk['type'] = DRIVE_TYPE[logical_disk.DriveType]
                            disk['firmware'] = physical_disk.FirmwareRevision
                            disk['setup type'] = logical_disk.FileSystem
                            info[key] = disk
                            hddCount += 1

    if not cdromSys is []:
        disk = {}
        key = 'CD drive {0}'.format(dvdCount)
        disk['brand'] = (cdromSys[0].DeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
        disk['path'] = '{0}/'.format(cdromSys[0].Drive)
        disk['index'] = cdromSys[0].Id
        disk['name'] = cdromSys[0].Name
        disk['model'] = cdromSys[0].Caption
        disk['type'] = cdromSys[0].MediaType
        info[key] = disk
        dvdCount += 1

    return info

def pciInfo(**info):
    count = 1
    for p in pciSys:
        pci = {}
        key = 'PCI rack {0}'.format(count)
        pci['name'] = p.Name
        pci['id'] = p.DeviceID
        pci['status'] = p.Status
        info[key] = pci
        count += 1
    return info

def networkInfo(**info):
    count = 1
    info['LAN ip'] = socket.gethostbyname(socket.gethostname())
    for n in networkSys:
        if n.AdapterType:
            network = {}
            key = 'network device {0}'.format(count)
            network['name'] = n.Name
            network['brand'] = n.Manufacturer
            network['id'] = n.DeviceID
            network['uid'] = n.GUID
            network['index'] = n.Index
            network['MacAdress'] = n.MACAddress
            network['connect id'] = n.NetConnectionID
            network['service name'] = n.ServiceName
            network['speed'] = n.Speed
            network['type'] = n.AdapterType
            network['type id'] = n.AdapterTypeID
            info[key] = network
            count += 1
    return info

def keyboardInfo(**info):
    count = 1
    for k in keyboardSys:
        keyboard = {}
        key = 'keyboard {0}'.format(count)
        keyboard['name'] = k.Name
        keyboard['id'] = k.DeviceID
        keyboard['status'] = k.Status
        info[key] = keyboard
        count += 1
    return info

def miceInfo(**info):
    count = 1
    for m in miceSys:
        mice = {}
        key = 'mice {0}'.format(count)
        mice['brand'] = m.Manufacturer
        mice['name'] = m.Name
        mice['id'] = m.DeviceID
        mice['status'] = m.Status
        info[key] = mice
        count += 1

    return info


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved