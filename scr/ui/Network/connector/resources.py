#!/usr/bin/python

# Copyright (c) 2018 Thomas Grime http://www.radiandynamics.com

import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)