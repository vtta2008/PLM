# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:

    Base text widgets for statusbar.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """


from pyPLM.Widgets import TextLabel
from pyPLM.Gui import Painter
from PLM.options                import ELIDE_RIGHT, ELIDE_NONE, SiPoPre, SiPoMin, TEXT_MENEOMIC
from PLM.utils                  import get_repr, ensure_valid


class TextBase(TextLabel):

    key                         = 'TextBase'

    def __init__(self, parent=None, elidemode=ELIDE_RIGHT):
        super(TextBase, self).__init__(parent)

        self.setSizePolicy(SiPoPre, SiPoMin)
        self._elidemode         = elidemode
        self._elided_text       = ''

    def __repr__(self):
        return get_repr(self, text=self.text())

    def setText(self, txt):
        super(TextBase, self).setText(txt)
        if self._elidemode != ELIDE_NONE:
            self._update_elided_text(self.width())

    def _update_elided_text(self, width):
        if self.text():
            self._elided_text   = self.fontMetrics().elidedText(self.text(), self._elidemode, width, TEXT_MENEOMIC)
        else:
            self._elided_text   = ''

    def resizeEvent(self, e):
        super(TextBase, self).resizeEvent()
        size = e.size()
        ensure_valid(size)
        self._update_elided_text(size.width())

    def paintEvent(self, e):
        if self._elidemode == ELIDE_NONE:
            super(TextBase, self).paintEvent(e)
        else:
            e.accept()
            painter = Painter(self)
            geom = self.geometry()
            ensure_valid(geom)
            painter.drawText(0, 0, geom.width(), geom.height(), int(self.alignment()), self._elided_text)


# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved