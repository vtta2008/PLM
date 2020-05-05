# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------


import platform, subprocess, os, sys, re, json
from PLM.configs import __pkgsReq__



def _loadConfig(filePath):
    with open(filePath, 'r') as myfile:
        fileString = myfile.read()
        cleanString = re.sub('//.*?\n|/\*.*?\*/', '', fileString, re.S)
        data = json.loads(cleanString)
    return data

def _saveData(filePath, data):
    f = open(filePath, "w")
    f.write(json.dumps(data,
                       sort_keys = True,
                       indent = 4,
                       ensure_ascii=False))
    f.close()
    print("Data successfully saved !")

def _loadData(filePath):
    with open(filePath) as json_file:
        j_data = json.load(json_file)
    json_file.close()
    print("Data successfully loaded !")
    return j_data

def _swapListIndices(inputList, oldIndex, newIndex):
    if oldIndex == -1:
        oldIndex = len(inputList)-1
    if newIndex == -1:
        newIndex = len(inputList)
    value = inputList[oldIndex]
    inputList.pop(oldIndex)
    inputList.insert(newIndex, value)


def _zoom_in(graph):
    """
    Set the node graph to zoom in by 0.1
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    zoom = graph.get_zoom() + 0.1
    graph.set_zoom(zoom)


def _zoom_out(graph):
    """
    Set the node graph to zoom in by 0.1
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    zoom = graph.get_zoom() - 0.2
    graph.set_zoom(zoom)


def _reset_zoom(graph):
    graph.reset_zoom()


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
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved