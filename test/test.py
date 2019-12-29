# -*- coding: utf-8 -*-
"""

Script Name: test.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
import platform, sys, re, subprocess, psutil, os, socket, uuid, pprint

from bin.Cpuinfo    import cpu
from bin            import DAMGDICT

try:
    import wmi
except ImportError:
    subprocess.Popen('python -m pip install wmi --user', shell=True).wait()
    import wmi

RAMTYPE = {
    0: 'Unknown',
    1: 'Other',
    2: 'DRAM',
    3: 'Synchronous DRAM',
    4: 'Cache DRAM',
    5: 'EDO',
    6: 'EDRAM',
    7: 'VRAM',
    8: 'SRAM',
    9: 'RAM',
    10: 'ROM',
    11: 'Flash',
    12: 'EEPROM',
    13: 'FEPROM',
    14: 'EPROM',
    15: 'CDRAM',
    16: '3DRAM',
    17: 'SDRAM',
    18: 'SGRAM',
    19: 'RDRAM',
    20: 'DDR',
    21: 'DDR2',
    22: 'DDR2 FB-DIMM',
    24: 'DDR3',
    25: 'FBD2',
}

FORMFACTOR = {
    0: 'Unknown',
    1: 'Other',
    2: 'SIP',
    3: 'DIP',
    4: 'ZIP',
    5: 'SOJ',
    6: 'Proprietary',
    7: 'SIMM',
    8: 'DIMM',
    9: 'TSOP',
    10: 'PGA',
    11: 'RIMM',
    12: 'SODIMM',
    13: 'SRIMM',
    14: 'SMD',
    15: 'SSMP',
    16: 'QFP',
    17: 'TQFP',
    18: 'SOIC',
    19: 'LCC',
    20: 'PLCC',
    21: 'BGA',
    22: 'FPBGA',
    23: 'LGA',
    24: 'FB-DIMM',
}

CPUTYPE = {

    1: 'Other',
    2: 'Unknown',
    3: 'Central Processor',
    4: 'Math Processor',
    5: 'DSP Processor',
    6: 'Video Processor',
}

DRIVE_TYPES = {
  0 : "Unknown",
  1 : "No Root Directory",
  2 : "Removable Disk",
  3 : "Local Disk",
  4 : "Network Drive",
  5 : "Compact Disc",
  6 : "RAM Disk"
}

deviceInfo                      = DAMGDICT()
usbCount = dvdCount = hddCount = pttCount = gpuCount = pciCount = keyboardCount = netCount = ramCount = miceCount = 1
cpuCount = biosCount = osCount = 1

com                             = wmi.WMI()
source                          = subprocess.Popen("SYSTEMINFO", stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

for s in com.CIM_OperatingSystem():
    print(s)
#
# for d in com.Win32_ComputerSystem():
#     print(d)

# Owner
deviceInfo['type']              = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % ('OS Configuration'), source, re.IGNORECASE)][0]


# print(deviceInfo['type'])

# os info
osInfo                          = {}
for o in com.Win32_OperatingSystem():
    ops                         = {}
    key                         = 'os {0}'.format(osCount)
    ops['brand']                = o.Manufacturer
    ops['os name']              = o.Caption
    ops['device name']          = com.Win32_ComputerSystem()[0].DNSHostName
    ops['device type']          = o
    ops['registered email']     = o.RegisteredUser
    ops['organisation']         = o.Organization
    ops['version']              = o.Version
    ops['os architecture']      = o.OSArchitecture
    ops['serial number']        = o.SerialNumber
    ops['mac adress']           = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    osInfo                      = ops
    osCount += 1


# Bios info
biosInfo                        = {}
for b in com.Win32_BIOS():
    bios                        = {}
    key                         = 'bios {0}'.format(biosCount)
    bios['brand']               = com.Win32_ComputerSystem()[0].Manufacturer
    bios['name']                = b.Manufacturer
    bios['model']               = com.Win32_BaseBoard()[0].Product
    bios['type']                = com.Win32_ComputerSystem()[0].SystemType
    bios['version']             = b.BIOSVersion
    bios['sockets']             = com.Win32_ComputerSystem()[0].NumberOfProcessors
    biosInfo[key]               = bios
    biosCount += 1

# CPU info
cpuInfo                         = {}

for c in com.Win32_Processor():
    cpu                         = {}
    key                         = 'cpu {0}'.format(cpuCount)
    cpu['name']                 = c.Name
    cpu['cores']                = c.NumberOfCores
    cpu['threads']              = c.NumberOfLogicalProcessors
    cpu['family']               = c.Caption
    cpu['max speed']            = '{0} GHz'.format(int(c.MaxClockSpeed)/1000)
    cpu['type']                 = CPUTYPE[c.ProcessorType]
    cpu['l2 size']              = '{0} MB'.format(c.L2CacheSize)
    cpu['l3 size']              = '{0} MB'.format(c.L3CacheSize)

    cpuInfo[key]                = cpu
    cpuCount += 1

# RAM info
ramInfo                         = {}
rams                            = []
for r in com.Win32_PhysicalMemory():
    ram                         = {}
    key                         = 'physical ram {0}'.format(ramCount)
    ram['capacity']             = '{0} GB'.format(round(int(r.Capacity)/(1024.0 ** 3)))
    ram['bus']                  = r.ConfiguredClockSpeed
    ram['location']             = r.DeviceLocator
    ram['form']                 = FORMFACTOR[r.FormFactor]
    ram['type']                 = RAMTYPE[r.MemoryType]
    ram['part number']          = r.PartNumber
    rams.append(ram['capacity'])
    ramInfo                     = ram
    ramCount += 1

ramInfo['total']                = '{0} GB'.format(round(int(com.Win32_ComputerSystem()[0].TotalPhysicalMemory)/(1024.0 ** 3)))
ramInfo['details']              = rams
ramInfo['rams']                 = len(com.Win32_PhysicalMemory())

# GPU Info
gpuInfo                         = {}
for g in (com.Win32_DisplayControllerConfiguration()):
    gpu                         = {}
    key                         = 'gpu {0}'.format(gpuCount)
    gpu['name']                 = g.Name
    gpu['refresh rate']         = g.RefreshRate
    gpu['bit rate']             = g.BitsPerPixel
    gpuInfo[key]                = gpu
    gpuCount += 1

# Drives Info
driversInfo                     = {}
for physical_disk in com.Win32_DiskDrive():
    # USB drive
    if physical_disk.associators("Win32_DiskDriveToDiskPartition") == []:
        disk                            = {}
        key                             = 'USB drive {0}'.format(usbCount)
        disk['brand']                   = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
        disk['index']                   = physical_disk.Index
        disk['name']                    = physical_disk.Name.replace('\\\\.\\', '')
        disk['model']                   = physical_disk.Model
        disk['partition']               = physical_disk.Partitions
        disk['size']                    = '0 GB'
        disk['type']                    = DRIVE_TYPES[2]
        for d in com.Win32_LogicalDisk():
            if d.DriveType == 2:
                disk['path']            = '{0}/'.format(d.Caption)

        disk['firmware']                = physical_disk.FirmwareRevision
        driversInfo[key]              = disk
        usbCount += 1
    else:
        for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
            if partition.associators("Win32_LogicalDiskToPartition") == []:
                disk                    = {}
                key                     = 'partition {0}'.format(pttCount)
                disk['brand']           = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                disk['firmware']        = physical_disk.FirmwareRevision
                disk['index']           = '{0} - {1}'.format(partition.DiskIndex, partition.Index)
                disk['name']            = partition.Name
                disk['model']           = physical_disk.Model
                disk['partition']       = partition.Caption
                disk['size']            = '{0} GB'.format(round(int(partition.size)/(1024.0 ** 3)))
                disk['block']           = '{0} MB'.format(round(int(partition.NumberOfBlocks)/(1024.0 ** 2)))
                disk['offset']          = '{0} GB'.format(round(int(partition.StartingOffset)/(1024.0 ** 3)))
                disk['type']            = partition.Type
                driversInfo[key]      = disk
                pttCount += 1
            else:
                key = 'harddrive {0}'.format(hddCount)
                for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                    disk                = {}
                    disk['brand']       = (physical_disk.PNPDeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
                    disk['path']        = '{0}/'.format(logical_disk.Caption)
                    disk['index']       = physical_disk.Index
                    disk['name']        = '{0} ({1})'.format(logical_disk.VolumeName, logical_disk.Caption)
                    disk['model']       = physical_disk.Model
                    disk['partition']   = partition.Caption
                    disk['size']        = '{0} GB'.format(round(int(logical_disk.size) / (1024.0 ** 3)))
                    disk['free size']   = '{0} GB'.format(round(int(logical_disk.FreeSpace) / (1024.0 ** 3)))
                    disk['type']        = DRIVE_TYPES[logical_disk.DriveType]
                    disk['firmware']    = physical_disk.FirmwareRevision
                    disk['setup type']  = logical_disk.FileSystem
                    driversInfo[key]  = disk
                    hddCount += 1

# DVD drive
if not com.Win32_CDROMDrive() is []:
    disk                                = {}
    key = 'CD drive {0}'.format(dvdCount)
    disk['brand']                       = (com.Win32_CDROMDrive()[0].DeviceID).replace('SCSI\\DISK&VEN_', '').split('&PROD')[0]
    disk['path']                        = '{0}/'.format(com.Win32_CDROMDrive()[0].Drive)
    disk['index']                       = com.Win32_CDROMDrive()[0].Id
    disk['name']                        = com.Win32_CDROMDrive()[0].Name
    disk['model']                       = com.Win32_CDROMDrive()[0].Caption
    disk['type']                        = com.Win32_CDROMDrive()[0].MediaType
    dvdCount += 1
    driversInfo[key]                  = disk

# PCI Info
pciInfo                         = {}
for p in com.Win32_IDEController():
    pci                         = {}
    key                         = 'PCI rack {0}'.format(pciCount)
    pci['name']                 = p.Name
    pci['id']                   = p.DeviceID
    pci['status']               = p.Status
    pciInfo[key]                = pci
    pciCount += 1

# Keyboard Info
keyboardInfo                    = {}
for k in com.Win32_Keyboard():
    keyboard                    = {}
    key                         = 'keyboard {0}'.format(keyboardCount)
    # keyboard['brand']           = k.Manufacturer
    keyboard['name']            = k.Name
    keyboard['id']              = k.DeviceID
    keyboard['status']          = k.Status
    keyboardInfo[key]           = keyboard
    keyboardCount += 1

# Mice Info
miceInfo                        = {}
for m in com.Win32_PointingDevice():
    mice                        = {}
    key                         = 'mice {0}'.format(miceCount)
    mice['brand']               = m.Manufacturer
    mice['name']                = m.Name
    mice['id']                  = m.DeviceID
    mice['status']              = m.Status
    miceInfo[key]               = mice
    miceCount += 1

# Network
networkInfo                     = {}
networkInfo['LAN ip']           = socket.gethostbyname(socket.gethostname())
for n in com.Win32_NetworkAdapter():
    if n.AdapterType:
        network                     = {}
        key                         = 'network device {0}'.format(netCount)
        network['name']             = n.Name
        network['brand']            = n.Manufacturer
        network['id']               = n.DeviceID
        network['uid']              = n.GUID
        network['index']            = n.Index
        network['MacAdress']        = n.MACAddress
        network['connect id']       = n.NetConnectionID
        network['service name']     = n.ServiceName
        network['speed']            = n.Speed
        network['type']             = n.AdapterType
        network['type id']          = n.AdapterTypeID
        networkInfo[key]            = network
        netCount += 1

# Collect Info
deviceInfo['os']                = osInfo
deviceInfo['bios']              = biosInfo
deviceInfo['cpu']               = cpuInfo
deviceInfo['gpu']               = gpuInfo
deviceInfo['ram']               = ramInfo
deviceInfo['drivers']           = driversInfo
deviceInfo['PCIs']              = pciInfo
deviceInfo['keyboard']          = keyboardInfo
deviceInfo['network']           = networkInfo

# pprint.pprint(deviceInfo)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:38 AM
# © 2017 - 2018 DAMGteam. All rights reserved