# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------

import platform, subprocess, os, sys
from PLM.configs        import __pkgsReq__

from psutil             import cpu_percent, virtual_memory, disk_usage
from GPUtil             import getGPUs
from .converts         import byte2gb, mb2gb


def obj_properties_setting(directory, mode):
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
            print("ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
    else:
        print("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root,d) for d in dirs]:
            os.chmod(dir, mode)
    for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, mode)

def batch_obj_properties_setting(listObj, mode):

    for obj in listObj:
        if os.path.exists(obj):
            obj_properties_setting(obj, mode)
        else:
            print('Could not find the specific path: %s' % obj)

def install_py_packages(name):
    """
    Install python package via command prompt
    :param name: name of component
    :return:
    """
    # print('Using pip to install %s' % name)
    if os.path.exists(name):
        subprocess.Popen('python %s install' % name)
    else:
        subprocess.Popen('python -m pip install %s' % name, shell=True).wait()

def install_require_package(package=__pkgsReq__):
    try:
        import package
    except ImportError as err:
        print("installing {0}".format(package))
        command = "start python -m pip install {0}".format(package)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        status = p.wait()
        print("Command output: {0}".format(output))

def uninstall_all_required_package():
    for pkg in __pkgsReq__:
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
""" Command Prompt """

def cmd_execute_py(name, directory):
    """
    Executing a python file
    :param name: python file name
    :param directory: path to python file
    :return: executing in command prompt
    """
    print("Executing {name} from {path}".format(name=name, path=directory))
    pth = os.path.join(directory, name)
    if os.path.exists(pth):
        return subprocess.call([sys.executable, pth])
    else:
        print("Path: {} does not exist".format(directory))

def system_call(args, cwd="."):
    print("Running '{}' in '{}'".format(str(args), cwd))
    return subprocess.call(args, cwd=cwd)

def run_cmd(pth):
    return subprocess.Popen(pth)

def open_cmd():
    return os.system("start /wait cmd")


# -------------------------------------------------------------------------------------------------------------
""" PC performance """

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