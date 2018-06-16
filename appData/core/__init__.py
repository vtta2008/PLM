# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
import appData as app
logger = app.logger

import appData.core.attributes as atributes
# attributes
Attribute               = attributes.Attribute


from appData.core import events
# events
EventHandler            = events.EventHandler


from appData.core import metadata
# Parsers/Managers
MetadataParser          = metadata.MetadataParser


# Plugin Manager
from appData.core import plugins
PluginManager           = plugins.PluginManager


from appData.core import graph
# graph class
Graph                   = graph.Graph

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 15/06/2018 - 8:26 PM
# © 2017 - 2018 DAMGteam. All rights reserved