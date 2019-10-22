# -*- coding: utf-8 -*-
"""

Script Name: serverTest2.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

"""
A small GUI tool to test async serial access withing a Qt application.
:author: Stefan Lehmann <stefan.st.lehmann@gmail.com
:license: MIT license, see license.txt for details
:created on 2018-02-08 11:29:49
:last modified by:   Stefan Lehmann
:last modified time: 2018-02-28 14:12:53
"""
import asyncio
import serial
from typing import Iterator, Tuple
from serial.tools.list_ports import comports
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QGridLayout, \
    QPushButton, QMessageBox, QApplication, QLineEdit, QPlainTextEdit
from PyQt5.QtGui import QCloseEvent
from quamash import QEventLoop


# Object for access to the serial port
ser = serial.Serial(timeout=0)
SER_BAUDRATE = 9600

# Setting constants
SETTING_PORT_NAME = 'port_name'
SETTING_MESSAGE = 'message'


def gen_serial_ports() -> Iterator[Tuple[str, str]]:
    """Return all available serial ports."""
    ports = comports()
    return ((p.description, p.device) for p in ports)


def send_serial_async(msg: str) -> None:
    """Send a message to serial port (async)."""
    ser.write(msg.encode())


# noinspection PyArgumentList
class RemoteWidget(QWidget):
    """Main Widget."""

    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)

        # Port Combobox
        self.port_label = QLabel(self.tr('COM Port:'))
        self.port_combobox = QComboBox()
        self.port_label.setBuddy(self.port_combobox)
        self.update_com_ports()

        # Connect and Disconnect Buttons
        self.connect_btn = QPushButton(self.tr('Connect'))
        self.disconnect_btn = QPushButton(self.tr('Disconnect'))
        self.disconnect_btn.setVisible(False)
        self.connect_btn.pressed.connect(self.on_connect_btn_pressed)
        self.disconnect_btn.pressed.connect(self.on_disconnect_btn_pressed)

        # message line edit
        self.msg_label = QLabel(self.tr('Message:'))
        self.msg_lineedit = QLineEdit()
        self.msg_label.setBuddy(self.msg_label)
        self.msg_lineedit.setEnabled(False)
        self.msg_lineedit.returnPressed.connect(self.on_send_btn_pressed)

        # send message button
        self.send_btn = QPushButton(self.tr('Send'))
        self.send_btn.setEnabled(False)
        self.send_btn.pressed.connect(self.on_send_btn_pressed)

        # received messages
        self.received_label = QLabel(self.tr('Received:'))
        self.received_textedit = QPlainTextEdit()
        self.received_textedit.setReadOnly(True)
        self.received_label.setBuddy(self.received_textedit)

        # Arrange Layout
        layout = QGridLayout()
        layout.addWidget(self.port_label, 0, 0)
        layout.addWidget(self.port_combobox, 0, 1)
        layout.addWidget(self.connect_btn, 0, 2)
        layout.addWidget(self.disconnect_btn, 0, 2)
        layout.addWidget(self.msg_label, 1, 0)
        layout.addWidget(self.msg_lineedit, 1, 1)
        layout.addWidget(self.send_btn, 1, 2)
        layout.addWidget(self.received_label, 2, 0)
        layout.addWidget(self.received_textedit, 2, 1, 1, 2)
        self.setLayout(layout)

        self._load_settings()

    def _load_settings(self) -> None:
        """Load settings on startup."""
        settings = QSettings()

        # port name
        port_name = settings.value(SETTING_PORT_NAME)
        if port_name is not None:
            index = self.port_combobox.findData(port_name)
            if index > -1:
                self.port_combobox.setCurrentIndex(index)

        # last message
        msg = settings.value(SETTING_MESSAGE)
        if msg is not None:
            self.msg_lineedit.setText(msg)

    def _save_settings(self) -> None:
        """Save settings on shutdown."""
        settings = QSettings()
        settings.setValue(SETTING_PORT_NAME, self.port)
        settings.setValue(SETTING_MESSAGE, self.msg_lineedit.text())

    def show_error_message(self, msg: str) -> None:
        """Show a Message Box with the error message."""
        QMessageBox.critical(self, QApplication.applicationName(), str(msg))

    def update_com_ports(self) -> None:
        """Update COM Port list in GUI."""
        for name, device in gen_serial_ports():
            self.port_combobox.addItem(name, device)

    @property
    def port(self) -> str:
        """Return the current serial port."""
        return self.port_combobox.currentData()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle Close event of the Widget."""
        if ser.is_open:
            ser.close()

        self._save_settings()

        event.accept()

    def on_connect_btn_pressed(self) -> None:
        """Open serial connection to the specified port."""
        if ser.is_open:
            ser.close()
        ser.port = self.port
        ser.baudrate = SER_BAUDRATE

        try:
            ser.open()
        except Exception as e:
            self.show_error_message(str(e))

        if ser.is_open:
            self.connect_btn.setVisible(False)
            self.disconnect_btn.setVisible(True)
            self.port_combobox.setDisabled(True)
            self.msg_lineedit.setEnabled(True)
            self.send_btn.setEnabled(True)
            loop.create_task(self.receive_serial_async())

    def on_disconnect_btn_pressed(self) -> None:
        """Close current serial connection."""
        if ser.is_open:
            ser.close()

        if not ser.is_open:
            self.connect_btn.setVisible(True)
            self.disconnect_btn.setVisible(False)
            self.port_combobox.setEnabled(True)
            self.msg_lineedit.setEnabled(False)
            self.send_btn.setEnabled(False)

    def on_send_btn_pressed(self) -> None:
        """Send message to serial port."""
        msg = self.msg_lineedit.text() + '\r\n'
        loop.call_soon(send_serial_async, msg)

    async def receive_serial_async(self) -> None:
        """Wait for incoming data, convert it to text and add to Textedit."""
        while True:
            msg = ser.readline()
            if msg != b'':
                text = msg.decode().strip()
                self.received_textedit.appendPlainText(text)
            await asyncio.sleep(0)


if __name__ == '__main__':
    app = QApplication([])
    loop = QEventLoop()
    asyncio.set_event_loop(loop)

    app.setOrganizationName('KUZ')
    app.setApplicationName('Dosierstation')
    w = RemoteWidget()
    w.show()

    with loop:
        loop.run_forever()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 5:05 AM
# © 2017 - 2018 DAMGteam. All rights reserved