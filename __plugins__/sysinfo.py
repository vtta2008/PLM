# -*- coding: utf-8 -*-
"""

Script Name: sysinfo.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""

# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import subprocess
import os
import sys
import re

os.geteuid()
os.getuid()

def sh(cmd, in_shell=False, get_str=True):
    output = subprocess.check_output(cmd, shell=in_shell)
    if get_str:
        return str(output, 'utf-8')
    return output

class Hwinfo:
    @classmethod
    def product(cls):
        """
        detect information about product
        """
        cmd = 'dmidecode -s system-product-name | head -1'
        output = sh(cmd, True)
        return Info('Product', output.strip())

    @classmethod
    def distro(cls):
        """
        detect information about distribution
        """
        cmd = 'lsb_release -sirc'
        output = sh(cmd, True)
        return Info('Distro', output.strip().replace('\n', ' '))

    @classmethod
    def kernel(cls):
        """
        detect information about kernel
        """
        cmd = ['uname', '-or']
        output = sh(cmd)
        return Info('Kernel', output.strip())

    @classmethod
    def processor(cls):
        """
        detect information about CPU
        """
        cmd = 'dmidecode -s processor-version | head -1'
        output = sh(cmd, True)
        return Info('Processor', output.strip())

    @classmethod
    def baseboard(cls):
        """
        detect information about baseboard
        """
        vendor = sh('cat /sys/devices/virtual/dmi/id/board_vendor', True)
        name = sh('cat /sys/devices/virtual/dmi/id/board_name', True)
        chipset = sh('lspci | grep ISA | sed -e "s/.*: //" -e "s/LPC.*//" -e "s/Controller.*//"', True)
        desc = vendor + name + chipset
        return Info('BaseBoard', desc.replace('\n', ' ', 2).strip())

    def __init__(self):
        """
        execute shell command and get information about hardware
        """
        infos = [
            Hwinfo.product(), Hwinfo.distro(), Hwinfo.kernel(),
            Hwinfo.processor(), Hwinfo.baseboard(), Rom(),
            Memory(), Disk(), OnboardDevice()
            ]
        self.info_list = infos

    def __str__(self):
        return ''.join([i.msg() for i in self.info_list])

class Info:
    """
    represent any hardware information
    """
    WIDTH = 10
    INDENT = '│──'

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.subInfo = []

    def msg(self):
        """
        generate the message to print
        """
        if self.desc == 'noop':
            return ''
        msg = []
        margin = ' ' * (Info.WIDTH - len(self.name))
        main_msg = '{0}{1}: {2}\n'.format(self.name, margin, self.desc)
        msg.append(main_msg)
        sub_msg = [ self.indent_subInfo(i) for i in self.subInfo if i]
        if sub_msg:
            sub_msg[-1] = sub_msg[-1].replace('│', '└')
        return ''.join(msg + sub_msg)

    def addSubInfo(self, subInfo):
        self.subInfo.append(subInfo)

    def indent_subInfo(self, line):
        return Info.INDENT + line

    def __str__(self):
        return  '"name": {0}, "description": {1}'.format(self.name, self.desc)

class Rom(Info):
    def __init__(self):
        self.rom_list = self.roms()
        Info.__init__(self, 'Rom', self.getDesc() if self.rom_list else 'noop')
    def getDesc(self):
        roms = [self.transform(i) for i in self.rom_list]
        roms_msg = ['{0} {1}'.format(i['VENDOR'], i['MODEL']) for i in roms]
        return ' '.join(roms_msg)

    def transform(self, line):
        rom = {}
        for line in re.split(r'(?<=") ', line):
            if '=' in line:
                key, value = line.split('=')
                if key in 'VENDOR' or key in 'MODEL':
                    rom[key] = value.replace('"', '').strip()
        return rom
    def roms(self):
        cmd = """lsblk -dP -o VENDOR,TYPE,MODEL | grep 'TYPE="rom"'"""
        try:
            output = sh(cmd, True)
            rom_list = [x for x in output.split('\n') if x]
            return rom_list
        except Exception:
            # no rom
            return []

class OnboardDevice(Info):
    def __init__(self):
        self.ob_devices = self.onboardDevices()
        Info.__init__(self, 'Onboard', '' if self.ob_devices else 'noop')
        info = [self.obToStr(i) for i in self.ob_devices]
        for i in info:
            self.addSubInfo(i)

    def onboardDevices(self):
        cmd = ['dmidecode', '-t', '41']
        parsing = False
        ob_list = []
        splitter = ': '
        attrs = ['Reference Designation', 'Type']
        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              bufsize = 1, universal_newlines = True) as p:
            for i in p.stdout:
                line = i.strip()
                if not parsing and line == 'Onboard Device':
                    parsing = True
                    ob = {}
                if parsing and splitter in line:
                    (key, value) = line.split(splitter, 1)
                    if key in attrs:
                        ob[key] = value
                elif parsing and not line:
                    parsing = False
                    ob_list.append(ob)
        return ob_list

    def obToStr(self, ob):
        tvalue = ob['Type']
        desvalue = ob['Reference Designation']
        ret = '{0}: {1}\n'.format(tvalue, desvalue)
        return ret

class Disk(Info):
    def __init__(self):
        self.disks = self.diskList()
        Info.__init__(self, 'Disks', '{0} {1} GB Total'.format(' '.join(self.disks), self.countSize()))
        self.details = self.disksDetail(self.disks)
        detail_strs = [ self.extractDiskDetail(i) for i in self.details]
        for i in detail_strs:
            self.addSubInfo(i)

    def countSize(self):
        sum = 0
        for i in self.disks:
            cmd = 'blockdev --getsize64 ' + i
            output = sh(cmd, True)
            sum += int(output) // (10 ** 9)
        return sum
    def diskList(self):
        """
        find out how many disk in this machine
        """
        sds = sh('ls -1d /dev/sd[a-z]', in_shell=True)
        sd_list = [x for x in sds.split('\n') if x]
        return sd_list

    def disksDetail(self, sd_list):
        cmd = ['smartctl', '-i']
        parsing = False
        splitter = ':'
        disk_list = []
        try:
            for i in sd_list:
                new_cmd = cmd[:]
                new_cmd.append(i)
                with subprocess.Popen(new_cmd, stdout=subprocess.PIPE,
                                      bufsize = 1, universal_newlines=True) as p:
                    for j in p.stdout:
                        line = j.strip()
                        if not parsing and 'START OF INFORMATION' in line:
                            parsing = True
                            disk = {}
                        if parsing and splitter in line:
                            key, value = line.split(splitter, 1)
                            value = value.strip()
                            if key in 'Model Family':
                                disk['model'] = value
                            elif key in 'Device Model':
                                disk['device'] = value
                            elif key in 'User Capacity':
                                p = re.compile('\[.*\]')
                                m = p.search(value)
                                disk['capacity'] = m.group()
                        elif parsing and not line:
                            parsing = False
                            disk['node'] = i
                            disk_list.append(disk)
        except Exception:
            pass
        return disk_list

    def extractDiskDetail(self, disk):
        line = '{node}: {device} {capacity}\n'.format(
            node=disk['node'], device=disk['device'],
            capacity=disk['capacity'])
        return line


class Memory(Info):
    def __init__(self):
        self.memory = self.memory()
        Info.__init__(self, 'Memory', self.getDesc(self.memory))
        detail_strs = [ self.extractMemDetail(i) for i in self.memory]
        for i in detail_strs:
            self.addSubInfo(i)

    def memory(self):
        cmd = ['dmidecode', '-t', 'memory']
        parsing = False
        splitter = ': '
        attrs = ['Size', 'Type', 'Speed', 'Manufacturer', 'Locator']
        mem_list = []
        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              bufsize = 1, universal_newlines = True) as p:
            for i in p.stdout:
                line = i.strip()
                if not parsing and line == 'Memory Device':
                    parsing = True
                    mem = {}
                if parsing and splitter in line:
                    (key, value) = line.split(splitter, 1)
                    if key in attrs:
                        mem[key] = value

                # read a empty, end the parsing
                elif parsing and not line:
                    parsing = False
                    mem_list.append(mem)
        return mem_list

    def extractMemDetail(self, mem):
        # maybe no memory in this slot
        if 'Unknown' in mem['Type'] and 'No Module Installed' in mem['Size']:
            return ''
        line = '{slot}: {manufa} {type} {speed}\n'.format(
            slot=mem['Locator'], manufa=mem['Manufacturer'],
            type=mem['Type'], speed=mem['Speed'])
        return line

    def getDesc(self, mem_list):
        mem_size = [self.convertMemSize(i['Size']) for i in mem_list]
        total = sum(mem_size)
        return '{0} MB Total'.format(total)

    def convertMemSize(self, size_str):
        (size, unit) = size_str.split(' ', 1);
        try:
            return int(size)
        except ValueError:
            return 0

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 20/08/2018 - 5:46 AM
# © 2017 - 2018 DAMGteam. All rights reserved