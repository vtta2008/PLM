# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from .utils             import (clean_file_ext, resize_image, data_handler, create_signal_slot, autoRename, wait,
                               get_repr, ensure_valid)

from .types             import is_button, is_string, is_action, is_url, url_valid, detect_url

from .nets              import filenameFromUrl, filenameFromHeader

from .converts          import str2bool, text_to_hex, bool2str, byte2gb, tuple2Qcolor, bytes2str, format_bytes

from .inspects          import (getToken, getUnix, getTime, getDate, get_screen_resolution, get_pointer_bounding_box,
                                check_blank, check_match, check_preset)

from .nodes             import setup_context_menu

from .paths             import get_file_path

from .procs             import (get_ram_useage,  get_gpu_useage, get_disk_useage, get_cpu_useage, install_pyPackage,
                                uninstall_pyPackage)