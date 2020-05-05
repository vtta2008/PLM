# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
from psutil             import cpu_percent, virtual_memory, disk_usage
from GPUtil             import getGPUs
from .converter         import byte2gb, mb2gb

def get_cpu_useage(interval=1, percpu=False):
    return cpu_percent(interval, percpu)

def get_ram_total():
    return byte2gb(virtual_memory()[0])

def get_ram_useage():
    return virtual_memory()[2]

def get_gpu_total():
    gpus = getGPUs()
    total = 0.0
    for gpu in gpus:
        total += float(gpu.memoryTotal)
    return mb2gb(total)

def get_gpu_useage():
    gpus = getGPUs()
    used = 0.0
    for gpu in gpus:
        used += float(gpu.memoryUsed/gpu.memoryTotal*100)
    rate = used/len(gpus)
    return round(rate, 2)

def get_disk_total():
    disk = disk_usage('/')
    return round(disk.total/(1024**3))

def get_disk_used():
    disk = disk_usage('/')
    return round(disk.used/(1024**3))

def get_disk_free():
    disk = disk_usage('/')
    return round(disk.free/(1024**3))

def get_disk_useage():
    disk = disk_usage('/')
    return disk.percent


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved