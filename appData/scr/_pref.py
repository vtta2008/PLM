# -*- coding: utf-8 -*-
"""

Script Name: _pref.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
LOGGING_LEVELS = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}

# node connection property types
PROPERTY = dict(
    simple=['FLOAT', 'STRING', 'BOOL', 'INT'],
    arrays=['FLOAT2', 'FLOAT3', 'INT2', 'INT3', 'COLOR'],
    data_types=['FILE', 'MULTI', 'MERGE', 'NODE', 'DIR'],
)

# Default preferences
PREFERENCES = {
    "ignore_scene_prefs": {"default": False, "desc": "Use user prefences instead of scene preferences.",
                           "label": "Ignore scene preferences", "class": "global"},
    "use_gl": {"default": False, "desc": "Render graph with OpenGL.", "label": "Use OpenGL", "class": "scene"},
    "edge_type": {"default": "bezier", "desc": "Draw edges with bezier paths.", "label": "Edge style",
                  "class": "scene"},
    "render_fx": {"default": False, "desc": "Render node drop shadows and effects.", "label": "render FX",
                  "class": "scene"},
    "antialiasing": {"default": 2, "desc": "Antialiasing level.", "label": "Antialiasing", "class": "scene"},
    "logging_level": {"default": 30, "desc": "Verbosity level.", "label": "Logging level", "class": "global"},
    "autosave_inc": {"default": 90000, "desc": "Autosave delay (seconds x 1000).", "label": "Autosave time",
                     "class": "global"},
    "stylesheet_name": {"default": "default", "desc": "Stylesheet to use.", "label": "Stylesheet", "class": "global"},
    "palette_style": {"default": "default", "desc": "Color palette to use.", "label": "Palette", "class": "global"},
    "font_style": {"default": "default", "desc": "font style to use.", "label": "Font style", "class": "global"},
    "viewport_mode": {"default": "smart", "desc": "viewport update mode.", "label": "Viewport Mode", "class": "global"}
}

VALID_FONTS = dict(
    ui=['Arial', 'Cantarell', 'Corbel', 'DejaVu Sans', 'DejaVu Serif', 'FreeSans', 'Liberation Sans',
        'Lucida Sans Unicode', 'MS Sans Serif', 'Open Sans', 'PT Sans', 'Tahoma', 'Verdana'],
    mono=['Consolas', 'Courier', 'Courier 10 Pitch', 'Courier New', 'DejaVu Sans Mono', 'Fixed',
          'FreeMono', 'Liberation Mono', 'Lucida Console', 'Menlo', 'Monaco'],
    nodes=['Consolas', 'DejaVu Sans Mono', 'Menlo', 'DejaVu Sans']
)

EDGE_TYPES = ['bezier', 'polygon']

VIEWPORT_MODES = dict(
    full='QGraphicsView.FullViewportUpdate',
    smart='QGraphicsView.SmartViewportUpdate',
    minimal='QGraphicsView.MinimalViewportUpdate',
)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 17/06/2018 - 12:51 AM
# © 2017 - 2018 DAMGteam. All rights reserved