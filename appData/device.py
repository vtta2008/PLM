# -*- coding: utf-8 -*-
"""

Script Name: device.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import platform, subprocess, re, uuid, socket

from bin import DAMGDICT
from .types import CPUTYPE, RAMTYPE, FORMFACTOR, DRIVETYPE

if platform.system() == 'Windows':
    try:
        import wmi
    except ImportError:
        subprocess.Popen('python -m pip install wmi --user', shell=True).wait()
        import wmi

PIPE = subprocess.PIPE
com = wmi.WMI()

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

        # pprint.pprint(self)

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


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 03/01/2020 - 01:52
# © 2017 - 2019 DAMGteam. All rights reserved