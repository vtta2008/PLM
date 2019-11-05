# -*- coding: utf-8 -*-
"""

Script Name: myRadio.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

import os
import sys
import wget
import encodings
from urllib import request
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, Qt, QMimeData, QSize, QPoint, QProcess, QStandardPaths, QFile, QDir, \
    QSettings
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QSlider, QStatusBar, QMainWindow, QFileDialog,
                             QListView, QMenu, qApp, QAction,
                             QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QSpacerItem, QSizePolicy, QMessageBox,
                             QPlainTextEdit, QSystemTrayIcon)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem, QVideoWidget
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QCursor, QStandardItem, QClipboard


changed = pyqtSignal(QMimeData)
btnwidth = 80


class Editor(QMainWindow):
    def __init__(self):
        super(Editor, self).__init__()
        self.isModified = False
        self.radio_editor = QPlainTextEdit(self)
        self.radio_editor.textChanged.connect(self.setModified)
        self.close_btn = QPushButton("Close", self)
        self.close_btn.setFixedWidth(btnwidth)
        self.close_btn.setIcon(QIcon.fromTheme("window-close"))
        self.close_btn.clicked.connect(self.closeWin)  ###(lambda: self.hide())
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.radio_editor)
        self.layout.addWidget(self.close_btn)
        self.wid = QWidget()
        self.wid.setLayout(self.layout)
        self.setCentralWidget(self.wid)
        self.setGeometry(0, 0, 800, 600)
        self.show()

    def closeWin(self):
        if self.isModified == True:
            with open(MainWin().radiofile, 'w') as f:
                if sys.version[0] == "2":
                    f.write(self.radio_editor.toPlainText().encode('utf8', 'replace'))
                elif sys.version[0] == "3":
                    f.write(str(self.radio_editor.toPlainText()))
                f.close()
                print("saved, closing editor")
                os.execv(sys.argv[0], sys.argv)
        else:
            print("closing editor")
            self.hide()

    #    def closeEvent(self, e):
    #        if self.isModified == True:
    #            with open(MainWin().radiofile, 'r+') as f:
    #                f.write(str(self.radio_editor.toPlainText().encode('utf-8')))
    #                f.close()
    #                print("saved, closing editor")
    #                os.execv(sys.argv[0], sys.argv)
    #                self.close()
    #        else:
    #            print("closing editor")
    #            self.close()

    def setModified(self):
        self.isModified = True


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.settings = QSettings("myRadio", "settings")
        self.setStyleSheet(mystylesheet(self))
        self.radioNames = []
        self.radiolist = []
        self.channels = []
        self.radiofile = ""
        self.radioStations = ""
        self.wg = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 2, 10, 2)
        self.player = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.layout1 = QHBoxLayout()

        self.outfile = QStandardPaths.standardLocations(QStandardPaths.TempLocation)[0] + "/radio.mp3"
        self.recording_enabled = False
        self.is_recording = False
        ### combo box
        self.urlCombo = QComboBox(self)

        self.play_btn = QPushButton("Play", self)
        self.play_btn.setFixedWidth(btnwidth)
        self.play_btn.setFlat(True)
        self.play_btn.setIcon(QIcon.fromTheme("media-playback-start"))
        self.layout1.addWidget(self.play_btn)

        self.pause_btn = QPushButton("Pause", self)
        self.pause_btn.setFixedWidth(btnwidth)
        self.pause_btn.setFlat(True)
        self.pause_btn.setIcon(QIcon.fromTheme("media-playback-pause"))
        self.layout1.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("Stop", self)
        self.stop_btn.setFixedWidth(btnwidth)
        self.stop_btn.setFlat(True)
        self.stop_btn.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.layout1.addWidget(self.stop_btn)
        ### record
        self.rec_btn = QPushButton("Record", self)
        self.rec_btn.setFixedWidth(btnwidth)
        self.rec_btn.setFlat(True)
        self.rec_btn.setIcon(QIcon.fromTheme("media-record"))
        self.rec_btn.clicked.connect(self.recordRadio1)
        self.rec_btn.setToolTip("Record Station")
        self.layout1.addWidget(self.rec_btn)
        ### stop record
        self.stoprec_btn = QPushButton("Stop Rec", self)
        self.stoprec_btn.setFixedWidth(btnwidth)
        self.stoprec_btn.setFlat(True)
        self.stoprec_btn.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.stoprec_btn.clicked.connect(self.stop_recording)
        self.stoprec_btn.setToolTip("Stop Recording")
        self.layout1.addWidget(self.stoprec_btn)
        ### edit Radiio List
        self.edit_btn = QPushButton("", self)
        self.edit_btn.setFixedWidth(26)
        self.edit_btn.setFlat(True)
        self.edit_btn.setToolTip("Channel Editor")
        self.edit_btn.setIcon(QIcon.fromTheme("preferences-system"))
        self.edit_btn.clicked.connect(self.edit_Channels)
        self.layout1.addWidget(self.edit_btn)

        spc1 = QSpacerItem(6, 10, QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.level_sld = QSlider(self)
        self.level_sld.setTickPosition(1)
        self.level_sld.setOrientation(Qt.Horizontal)
        self.level_sld.setValue(65)
        self.level_lbl = QLabel(self)
        self.level_lbl.setAlignment(Qt.AlignHCenter)
        self.level_lbl.setText("Volume 65")
        self.layout.addWidget(self.urlCombo)
        self.layout.addLayout(self.layout1)
        self.layout.addItem(spc1)
        self.layout.addWidget(self.level_sld)
        self.layout.addWidget(self.level_lbl)
        self.player = RadioPlayer(self)
        self.player.metaDataChanged.connect(self.metaDataChanged)
        self.play_btn.clicked.connect(self.playRadioStation)
        self.pause_btn.clicked.connect(self.pause_preview)
        self.stop_btn.clicked.connect(self.stop_preview)
        self.level_sld.valueChanged.connect(self.set_sound_level)
        self.urlCombo.currentIndexChanged.connect(self.url_changed)
        self.current_station = ""

        self.process = QProcess()
        self.process.started.connect(self.getPID)

        self.wg.setLayout(self.layout)
        self.setCentralWidget(self.wg)

        self.stoprec_btn.setVisible(False)
        self.readStations()

        self.createStatusBar()
        self.setAcceptDrops(True)
        self.setWindowTitle("Radio")
        self.tIcon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), "radio_bg.png"))
        self.setWindowIcon(self.tIcon)
        self.stationActs = []

        self.setMinimumHeight(180)
        self.setFixedWidth(460)
        self.move(0, 30)
        self.findExecutable()

        self.readSettings()

        # Init tray icon
        trayIcon = QIcon(self.tIcon)

        self.trayIcon = QSystemTrayIcon()
        #        self.trayIcon.activated.connect(self.showMain)
        self.trayIcon.setIcon(trayIcon)
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.on_systray_activated)
        #        self.trayIcon.setToolTip("Welcome")
        qApp.setStyleSheet(
            "QSystemTrayIcon::message { font-size: 10pt; color: #2e3436; background: #c4a000; border: 1px solid #1f3c5d; }");
        self.metaLabel = QLabel()

        #        self.show()
        self.geo = self.geometry()
        self.editAction = QAction(QIcon.fromTheme("preferences-system"), "edit Channels", triggered=self.edit_Channels)
        self.showWinAction = QAction(QIcon.fromTheme("view-restore"), "show Main Window", triggered=self.showMain)
        self.recordAction = QAction(QIcon.fromTheme("media-record"), "record channel", triggered=self.recordRadio1)
        self.stopRecordAction = QAction(QIcon.fromTheme("media-playback-stop"), "stop recording",
                                        triggered=self.stop_recording)

    def getURLfromPLS(self, inURL):
        response = request.urlopen(inURL)
        html = response.read().splitlines()

        t = str(html[1])
        url = t.partition("=")[2].partition("'")[0]
        #        print(url)
        return (url)

    def getURLfromM3U(self, inURL):
        response = request.urlopen(inURL)
        html = response.read().splitlines()

        t = str(html[1])
        url = t.partition("'")[2].partition("'")[0]
        print(url)
        return (url)

    def on_systray_activated(self, i_reason):
        buttons = qApp.mouseButtons()
        if buttons == Qt.LeftButton:
            self.leftMenu()
        elif buttons == Qt.RightButton:
            self.showMain()

    def leftMenu(self):
        menuSectionIcon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), "radio_bg.png"))
        self.tray_menu = QMenu()
        ##################
        for i in range(self.urlCombo.count() - 1):
            text = self.urlCombo.itemData(i, Qt.DisplayRole)
            data = self.urlCombo.itemData(i, Qt.DisplayRole)
            if text.startswith("--"):
                self.stationActs.append(text)
            else:
                self.stationActs.append(QAction(QIcon.fromTheme("browser"), text, triggered=self.openTrayStation))
                self.stationActs[i].setData(str(i))
            if not text.startswith("--"):
                self.tray_menu.addAction(self.stationActs[i])
            else:
                self.tray_menu.addSection(menuSectionIcon, text.replace("--", ""))
        ##################
        self.tray_menu.addSeparator()
        if self.is_recording == False:
            if not self.urlCombo.currentText().startswith("--"):
                self.tray_menu.addAction(self.recordAction)
                self.recordAction.setText("%s %s: %s" % ("record", "channel", self.urlCombo.currentText()))
        if self.is_recording == True:
            self.tray_menu.addAction(self.stopRecordAction)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.editAction)
        self.tray_menu.addAction(self.showWinAction)
        self.tray_menu.addSeparator()
        exitAction = self.tray_menu.addAction(QIcon.fromTheme("application-exit"), "exit")
        exitAction.triggered.connect(self.exitApp)
        self.tray_menu.exec_(QCursor.pos())

    def showMain(self):
        if self.isVisible() == False:
            self.showWinAction.setText("hide Main Window")
            self.setVisible(True)
        elif self.isVisible() == True:
            self.showWinAction.setText("show Main Window")
            self.setVisible(False)

    def openTrayStation(self):
        action = self.sender()
        if action:
            ind = action.data()
            print("%s %s %s" % ("switch to station:", ind, self.urlCombo.currentText()))
            self.urlCombo.setCurrentIndex(int(ind))

    def exitApp(self):
        self.close()

    def message(self):
        QMessageBox.information(
            None, 'Systray Message', 'Click Message')

    def closeEvent(self, e):
        print("writing settings ...\nGoodbye ...")
        self.writeSettings()

    def readSettings(self):
        print("reading settings ...")
        if self.settings.contains("pos"):
            pos = self.settings.value("pos", QPoint(200, 200))
            self.move(pos)
        else:
            self.move(0, 26)
        if self.settings.contains("index"):
            index = int(self.settings.value("index"))
            self.urlCombo.setFocus()
            self.urlCombo.setCurrentIndex(index)
            if self.urlCombo.currentIndex() == 0:
                self.url_changed()
        else:
            self.urlCombo.setCurrentIndex(0)
            self.url_changed()

    def writeSettings(self):
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("index", self.urlCombo.currentIndex())

    def readStations(self):
        menuSectionIcon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), "radio_bg.png"))
        self.urlCombo.clear()
        self.radiolist = []
        self.channels = []
        dir = os.path.dirname(sys.argv[0])
        self.radiofile = os.path.join(dir, "myradio.txt")
        import codecs
        with open(self.radiofile, 'r') as f:
            self.radioStations = f.read()
            f.close()
            self.radioStations = self.remove_last_line_from_string(self.radioStations)
            for t in self.radioStations:
                self.channels.append(t)
            for lines in self.radioStations.split("\n"):
                if not lines.startswith("--"):
                    self.urlCombo.addItem(QIcon.fromTheme("browser"), lines.partition(",")[0])
                else:
                    m = QStandardItem(menuSectionIcon, lines.partition(",")[0])
                    m.setEnabled(False)
                    self.urlCombo.model().appendRow(m)
                self.radiolist.append(lines.partition(",")[2])
        self.urlCombo.setCurrentIndex(0)

    def edit_Channels(self):
        self.edWin = Editor()
        #        self.show()
        with open(self.radiofile, 'r') as f:
            t = f.read()
            f.close()
        self.edWin.radio_editor.setPlainText(t)
        self.edWin.isModified = False

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            self.playURL()
        elif e.key() == Qt.Key_F1:
            QMessageBox.information(self, "Information", "F5 -> play URL from Clipboard").exec_()
        else:
            e.accept()

    def msgbox(self, message):
        QMessageBox.warning(self, "Message", message)

    def findExecutable(self):
        wget = QStandardPaths.findExecutable("wget")
        if wget != "":
            print("%s %s %s" % ("wget found at ", wget, " *** recording enabled"))
            self.msglbl.setText("recording enabled")
            self.recording_enabled = True
        else:
            self.msgbox("wget not found\nrecording disabled")
            self.recording_enabled = False

    def remove_last_line_from_string(self, s):
        return s[:s.rfind('\n')]

    def createStatusBar(self):
        self.msglbl = QLabel()
        self.msglbl.setWordWrap(True)
        self.msglbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.msglbl)
        self.msglbl.setText("Ready")

    def metaDataChanged(self):
        if self.player.isMetaDataAvailable():
            trackInfo = (self.player.metaData("Title"))
            trackInfo2 = (self.player.metaData("Comment"))
            if not trackInfo == None:
                if not trackInfo2 == None:
                    self.msglbl.setText("%s %s" % (trackInfo, trackInfo2))
                    self.metaLabel.setText("%s %s" % (trackInfo, trackInfo2))
                    self.trayIcon.showMessage("Radio", "%s %s" % (trackInfo, trackInfo2), self.tIcon, 5000)
                else:
                    self.msglbl.setText(trackInfo)
                    self.trayIcon.showMessage("Radio", trackInfo, self.tIcon, 5000)
                    self.msglbl.adjustSize()
                    self.adjustSize()
            else:
                self.msglbl.setText("%s %s" % ("playing", self.urlCombo.currentText()))
        else:
            self.msglbl.setText("%s %s" % ("playing", self.urlCombo))

    def url_changed(self):
        if self.urlCombo.currentIndex() < self.urlCombo.count() - 1:
            if not self.urlCombo.currentText().startswith("--"):
                ind = self.urlCombo.currentIndex()
                url = self.radiolist[ind]
                print("%s %s" % ("playing", url))
                self.current_station = url
                self.player.stop()
                self.rec_btn.setVisible(True)
                self.stop_btn.setVisible(True)
                self.play_btn.setVisible(True)
                self.pause_btn.setVisible(True)
                self.playRadioStation()
            else:
                self.rec_btn.setVisible(False)
                self.stop_btn.setVisible(False)
                self.play_btn.setVisible(False)
                self.pause_btn.setVisible(False)

    def playRadioStation(self):
        if self.player.is_on_pause:
            self.set_running_player()
            self.player.start()
            self.pause_btn.setFocus()
            return

        if not self.current_station:
            return

        self.player.set_media(self.current_station)
        self.set_running_player()
        self.player.start()
        self.msglbl.setText("%s %s" % ("playing", self.urlCombo.currentText()))
        self.setWindowTitle(self.urlCombo.currentText())

    def playURL(self):
        clip = QApplication.clipboard()
        if not clip.text().endswith(".pls") and not clip.text().endswith(".m3u"):
            self.current_station = clip.text()
        elif clip.text().endswith(".pls"):
            print("is a pls")
            url = self.getURLfromPLS(clip.text())
            self.current_station = url
        elif clip.text().endswith(".m3u"):
            print("is a pls")
            url = self.getURLfromM3U(clip.text())
            self.current_station = url
        print(self.current_station)

        if self.player.is_on_pause:
            self.set_running_player()
            self.player.start()
            self.pause_btn.setFocus()
            return

        if not self.current_station:
            return

        self.player.set_media(self.current_station)
        self.set_running_player()
        self.player.start()
        self.msglbl.setText("%s %s" % ("playing", self.urlCombo.currentText()))

    def set_running_player(self):
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.rec_btn.setEnabled(True)

    def pause_preview(self):
        self.player.set_on_pause()
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.rec_btn.setEnabled(False)
        self.play_btn.setFocus(True)
        self.msglbl.setText("Pause")

    def stop_preview(self):
        self.player.finish()
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.rec_btn.setEnabled(False)
        self.msglbl.setText("Stopped")

    def set_sound_level(self, level):
        self.player.set_sound_level(level)
        self.level_lbl.setText("Volume " + str(level))

    def update_volume_slider(self, level):
        self.level_lbl.setText("Volume " + str(level))
        self.level_sld.blockSignals(True)
        self.level_sld.setValue(value)
        self.level_lbl.setText("Volume " + str(level))
        self.level_sld.blockSignals(False)

    def recordRadio(self):
        if self.is_recording == False:
            self.deleteOutFile()
            cmd = ("wget -q " + self.current_station + " -O " + self.outfile)
            print(cmd)
            self.is_recording = True
            self.process.startDetached(cmd)
            #            wget.download (self.current_station, self.outfile)
            self.rec_btn.setVisible(False)
            self.stoprec_btn.setVisible(True)
        else:
            self.msgbox("Recording is still in progress")

    def recordRadio1(self):
        if self.is_recording == False:
            self.deleteOutFile()
            cmd = ("timeout 1h wget -q " + self.current_station + " -O " + self.outfile)
            print(cmd)
            self.is_recording = True
            self.process.startDetached(cmd)
            #            wget.download (self.current_station, self.outfile)
            self.rec_btn.setVisible(False)
            self.stoprec_btn.setVisible(True)
        else:
            self.msgbox("Recording is still in progress")

    def stop_recording(self):
        if self.is_recording == True:
            self.showMain()
            self.process.close()
            print("stopping recording")
            self.is_recording = False
            QProcess.execute("killall wget")
            if self.isVisible() == False:
                self.showWinAction.setText("hide Main Window")
                self.setVisible(True)
            self.saveMovie()
            self.stoprec_btn.setVisible(False)
            self.rec_btn.setVisible(True)
            self.showMain()
        else:
            self.msgbox("Recording is not in progress")

    def saveMovie(self):
        if self.is_recording == False:
            print("saving audio")
            #            self.setWindowTitle("myRadio")
            infile = QFile(self.outfile)
            path, _ = QFileDialog.getSaveFileName(self, "Save as...", QDir.homePath() + "/Musik/" \
                                                  + self.urlCombo.currentText().replace("-", " ").replace(" - ",
                                                                                                          " ") + ".mp3",
                                                  "Audio (*.mp3)")
            if (path != ""):
                savefile = path
                if QFile(savefile).exists:
                    QFile(savefile).remove()
                print("%s %s" % ("saving", savefile))
                if not infile.copy(savefile):
                    QMessageBox.warning(self, "Error",
                                        "Cannot write file %s:\n%s." % (path, infile.errorString()))
                #                self.deleteOutFile()
                #                self.process.setProcessState(0)
                print("%s %s" % ("process state: ", str(self.process.state())))
                if QFile(self.outfile).exists:
                    print("exists")
                    QFile(self.outfile).remove()

    def deleteOutFile(self):
        if QFile(self.outfile).exists:
            print("%s %s" % ("deleting file", self.outfile))
            if QFile(self.outfile).remove:
                print("%s %s" % (self.outfile, "deleted"))
            else:
                print("%s %s" % (self.outfile, "not deleted"))

    def getPID(self):
        print("%s %s" % (self.process.pid(), self.process.processId()))


class RadioPlayer(QMediaPlayer):
    def __init__(self, driver):
        super(RadioPlayer, self).__init__()
        self.driver = driver
        self.url = None
        self.auto_sound_level = True
        self.is_running = False
        self.is_on_pause = False
        self.volumeChanged.connect(self.on_volume_changed)
        self.stateChanged.connect(self.on_state_changed)

    def set_media(self, media):
        if isinstance(media, QUrl):
            self.url = media

        elif isinstance(media, str):
            self.url = QUrl(media)

        self.setMedia(QMediaContent(self.url))

    def start(self):
        self.is_running = True
        self.is_on_pause = False
        self.play()

    def set_on_pause(self):
        self.is_running = False
        self.is_on_pause = True
        self.pause()

    def finish(self):
        self.is_running = False
        self.is_on_pause = False
        self.stop()

    def set_sound_level(self, level):
        self.auto_sound_level = False
        self.setVolume(level)

    def on_volume_changed(self, value):
        if self.auto_sound_level:
            self.update_volume_slider(value)
        self.auto_sound_level = True

    def on_state_changed(self, state):
        if not state:
            self.driver.stop_preview()


def mystylesheet(self):
    return """
QPushButton
{
color: #1f3c5d;
}
QComboBox
{
height: 18px;
background: #d3d7cf;
color: #2e3436;
font-size: 8pt;
}
QComboBox::item
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #729fcf, stop: 1.0 #204a87);
selection-color: #eeeeec;
}
QStatusBar
{
height: 32px;
color: #888a85;
font-size: 8pt;
background: transparent;
}
QLabel
{
border: 0px;
color: #1f3c5d;
font-size: 9pt;
}
QMainWindow
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}
QSlider::handle:horizontal 
{
background: transparent;
width: 8px;
}
QSlider::groove:horizontal {
border: 1px solid #444;
height: 8px;
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #babdb6, stop: 1.0 #D3D3D3);
border-radius: 4px;
}
QSlider::sub-page:horizontal {
background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
    stop: 0 #66e, stop: 1 #bbf);
background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
    stop: 0 #bbf, stop: 1 #55f);
border: 1px solid #777;
height: 8px;
border-radius: 4px;
}
QSlider::handle:horizontal:hover {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #fff, stop:1 #ddd);
border-radius: 4px;
}
QSlider::sub-page:horizontal:disabled {
background: #bbb;
border-color: #999;
}
QSlider::add-page:horizontal:disabled {
background: #eee;
border-color: #999;
}
QSlider::handle:horizontal:disabled {
background: #eee;
border-radius: 4px;
}
    """


if __name__ == "__main__":
    app = QApplication([])
    win = MainWin()
    win.show()
    win.setVisible(False)
    sys.exit(app.exec_())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved