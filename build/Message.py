# -*- coding: utf-8 -*-
"""

Script Name: Message.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import sys
import subprocess

# PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon

# Plm
from core.Loggers import SetLogger
# logger = SetLogger()

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# -------------------------------------------------------------------------------------------------------------
""" Message """

class Message(QTableWidget):
    """The list of messages."""

    # useful columns (to not use just numbers in the code), and titles
    text_col = 1
    media_col = 2
    check_col = 3
    titles = ("When", "Text", "Media", "Done")

    def __init__(self, storage, systray):
        self._messages = storage.get_elements()
        self._storage = storage
        self._systray = systray
        super(Message, self).__init__(len(self._messages), len(self.titles))

        item_builders = [
            self._build_item_datetime,
            self._build_item_text,
            self._build_item_media,
            self._build_item_checkbox,
        ]

        for row, msg in enumerate(self._messages):
            logger.debug("Set message for row %d: %s", row, msg)
            for col in range(len(self.titles)):
                builder = item_builders[col]            # get the builder according to the column and build the item
                item = builder(msg)
                if item is None:                        # if no specific item, build and empty one, and add a tooltip in any case
                    item = QTableWidgetItem()
                    item.setToolTip(self.tooltips_missing[col])
                else:
                    item.setToolTip(self.tooltips_present[col])

                item.setFlags(item.flags() & Qt.ItemIsEditable)     # set it to not editable and put it in the table
                self.setItem(row, col, item)

        self.setHorizontalHeaderLabels(self.titles)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSizeAdjustPolicy(2)

        # enable user to move columns
        header = self.horizontalHeader()
        header.setSectionsMovable(True)

        # load configuration & put columns in saved order
        for fr, to in enumerate(config.COL_ORDER):
            header.moveSection(self.visualColumn(fr), to)

        self.itemClicked.connect(self._item_clicked)
        self.itemDoubleClicked.connect(self._item_doubleclicked)
        self.show()


    def _build_item_datetime(self, msg):
        """Build the item for the datetime column."""
        return QTableWidgetItem(str(msg.sent_at))


    def _build_item_text(self, msg):
        """Build the item for the text column."""
        if msg.text is not None:
            return QTableWidgetItem(msg.text)


    def _build_item_media(self, msg):
        """Build the item for the media column."""
        if msg.extfile_path is not None:
            # build the icon according to the media type, if known
            if msg.media_type == msg.MEDIA_TYPE_IMAGE:
                icon = QIcon(func.getAppIcon("Radio"))
            elif msg.media_type == msg.MEDIA_TYPE_AUDIO:
                icon = QIcon(func.getAppIcon("Audio"))
            else:
                icon = QIcon()

            item = QTableWidgetItem()
            item.setIcon(icon)
            return item


    def _build_item_checkbox(self, msg):
        """Build the item for the checkbox column."""
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.Unchecked)
        return item


    def closeEvent(self, event):
        """Intercept closing and delete marked messages."""
        messages_to_remove = []
        for row in range(self.rowCount()):
            if self.item(row, self.check_col).checkState() == Qt.Checked:
                # note, we can access the message like this because the table can not be reordered
                messages_to_remove.append(self._messages[row])
        if messages_to_remove:
            self._storage.delete_elements(messages_to_remove)
            self._systray.set_message_number()

        # saves column order configuration
        col_order = []
        for col in range(self.columnCount()):
            col_order.append(self.visualColumn(col))
        config.COL_ORDER = col_order
        config.save()
        super().closeEvent(event)


    def _item_clicked(self, widget):
        """An item in the table was clicked."""
        column = widget.column()
        row = widget.row()

        if column == self.check_col:
            # click in the checkbox column disable or enable the whole row
            disable = widget.checkState() == Qt.Checked
            for column in range(len(self.titles) - 1):  # -1 to not strike out checkbox
                item = self.item(row, column)
                if disable:
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                else:
                    item.setFlags(item.flags() | Qt.ItemIsEnabled)
                font = item.font()
                font.setStrikeOut(disable)
                item.setFont(font)


    def _item_doubleclicked(self, widget):
        """An item in the table was clicked."""
        column = widget.column()
        row = widget.row()

        if column == self.media_col:
            # click in the media column, execute externally
            msg = self._messages[row]
            if msg.extfile_path is not None:
                logger.debug("Opening external file %r", msg.extfile_path)
                subprocess.call(['/usr/bin/xdg-open', msg.extfile_path])

        elif column == self.text_col:
            # click in the text column, copy to clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(widget.text())

def main():
    app = QApplication(sys.argv)
    layout = Message()
    layout.show()
    app.exec_()


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 16/06/2018 - 4:39 AM
# © 2017 - 2018 DAMGteam. All rights reserved