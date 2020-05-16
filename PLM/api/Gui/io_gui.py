# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
from PLM import globals


if globals.qtBindingMode == 'PyQt5':
        from PyQt5.QtGui        import (QBrush, QColor, QCursor, QFont, QFontMetrics, QIcon, QImage,
                                        QIntValidator, QKeySequence, QPaintDevice, QPainter, QPainterPath, QPalette, QPen, QPixmap,
                                        QPolygon, QTransform, QTextTableFormat, QTextCharFormat, )
elif globals.qtBindingMode == 'PySide2':
        from PySide2.QtGui      import (QBrush, QColor, QCursor, QFont, QFontMetrics, QIcon, QImage,
                                        QIntValidator, QKeySequence, QPaintDevice, QPainter, QPainterPath, QPalette, QPen, QPixmap,
                                        QPolygon, QTransform, QTextFormat, QTextCharFormat, )



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved