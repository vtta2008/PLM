# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
# import subprocess, pkg_resources
#
# installed_packages = pkg_resources.working_set
# installed = sorted(["%s" % i.key for i in installed_packages])
#
# for p in installed:
#     cmd = "pip install {0} --upgrade".format(p)
#     subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE).wait()
#
# print('finish')

from subprocess import PIPE, Popen
from GPUtil import GPUtil
import os
from distutils import spawn

nvidia_smi = spawn.find_executable('nvidia-smi')
print(nvidia_smi)
if nvidia_smi is None:
    nvidia_smi = "%s/Program Files/NVIDIA Corporation/NVSMI/nvidia-smi.exe" % os.environ['systemdrive']

print(nvidia_smi, os.path.exists(nvidia_smi))

p = Popen([nvidia_smi,"--query-gpu=index,uuid,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu", "--format=csv,noheader,nounits"], stdout=PIPE)
stdout, stderror = p.communicate()


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
