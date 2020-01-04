#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: ImageViewer.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

    This is UI which can view any type of image.

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, glob
from functools import partial

# PyQt5
from PyQt5                  import QtSql
from PyQt5.QtCore           import Qt, QDir, pyqtSignal
from PyQt5.QtGui            import QPixmap, QTransform, QIcon
from PyQt5.QtWidgets        import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QMenu, QFileDialog, QHBoxLayout

from devkit.Widgets         import Widget
from devkit.Gui             import AppIcon
from utils                  import get_screen_resolution
from appData                import LOCAL_DB

# Plt

# -------------------------------------------------------------------------------------------------------------
""" Graphic View class """

class ImageViewing(QGraphicsView):

    viewerCloseSig          = pyqtSignal(bool)
    viewRealImageSizeSig    = pyqtSignal(bool)
    toggleFullscreenSig     = pyqtSignal(bool)
    vertMaxSig              = pyqtSignal(bool)
    horizMaxSig             = pyqtSignal(bool)
    zoomInSig               = pyqtSignal(bool)
    zoomOutSig              = pyqtSignal(bool)
    zoomResetSig            = pyqtSignal(bool)
    rotateImgSig            = pyqtSignal(int)
    dirBrowseSig            = pyqtSignal(int)
    fitViewSig              = pyqtSignal(bool)
    goToLocationSig         = pyqtSignal(bool)

    def emit_close(self):
        self.viewerCloseSig.emit(True)

    def viewRealImageSize(self):
        self.viewRealImageSizeSig.emit(True)

    def toggleFullscreen(self):
        self.toggleFullscreenSig.emit(True)

    def vertMax(self):
        self.vertMaxSig.emit(True)

    def horizMax(self):
        self.horizMaxSig.emit(True)

    def zoomIn(self):
        self.zoomInSig.emit(True)

    def zoomOut(self):
        self.zoomOutSig.emit(True)

    def zoomReset(self):
        self.zoomResetSig.emit(True)

    def rotateImg(self, value):
        self.rotateImgSig.emit(value)

    def dirBrowse(self, value):
        self.dirBrowseSig.emit(value)

    def fitView(self):
        self.fitViewSig.emit(True)

    def goToLocation(self):
        self.goToLocationSig.emit(True)

    def wheelEvent(self, event):
        moose = event.angleDelta().y() / 120
        if moose > 0:
            self.zoomIn()
        elif moose < 0:
            self.zoomOut()

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addSeparator()
        menu.addAction('Real Image Size             F10', self.viewRealImageSize)
        menu.addSeparator()
        menu.addAction('Toggle fullscreen           F11', self.toggleFullscreen)
        menu.addAction('Vertically max.                 V', self.vertMax)
        menu.addAction('HoriZontally max.           Z', self.horizMax)
        menu.addSeparator()
        menu.addAction('Zoom in                         +, e', self.zoomIn)
        menu.addAction('Zoom out                       -, d', self.zoomOut)
        menu.addAction('Reset zoom                      1', self.zoomReset)
        menu.addSeparator()
        menu.addAction('Rotate CCW                     r', partial(self.rotateImg, 1))
        menu.addAction('Spin CW                          s', partial(self.rotateImg, -1))
        menu.addAction('Next image                   SPACE', partial(self.dirBrowse, 1))
        menu.addAction('Previous image            BACKSPACE', partial(self.dirBrowse, -1))
        menu.addAction('Fit image                         f', self.fitView)
        menu.addSeparator()
        menu.addAction('Go to file location', self.goToLocation)
        menu.addSeparator()
        menu.addAction('Quit                             Ctrl + Q', self.emit_close)

        menu.exec_(event.globalPos())

# -------------------------------------------------------------------------------------------------------------
""" Main Window Class """

class ViewerWindow(QMainWindow):

    resizeSig = pyqtSignal(int, int)

    def resizeEvent(self, resizeEvent):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        # self.view.resize(width + 2, height + 2)
        # self.resizeSig.emit(width + 4, height + 4)

    def closeEvent(self, event):

        ImageInitUI().winState()
        if self.inshuft == 0:
            ImageInitUI().dbInsert()
            self.db.close()
        else:
            ImageInitUI().dbUpdate()
            self.db.close()

        QApplication.instance().quit()

# -------------------------------------------------------------------------------------------------------------
""" Image UI main class """

class ImageInitUI(ViewerWindow):

    def __init__(self, key=None, parent=None):
        super(ImageInitUI, self).__init__(parent)

        self.dbfile = LOCAL_DB
        self.dbdir = os.path.dirname(self.dbfile)

        if not os.path.isfile(self.dbfile):
            self.createDB()

        self.key = key

        # Set common window attributes
        self.path, self.title = os.path.split(self.key)

        self.dbSanitise()

        self.formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.pbm', '.pgm', '.ppm', '.xbm', '.xpm', '.dds',
                        '.icns', '.jp2', '.mng', '.tga', '.tiff', '.wbmp', '.webp')
        try:
            open(self.key, 'r')
        except IOError:
            # print('There was an error opening the file')
            # sys.exit(1)
            pass

        if self.key.lower().endswith(self.formats):
            # If inshuft = 0, the image is not in shufti's image database
            self.inshuft = 0
            self.rotval = 0
            self.rotvals = (0, -90, -180, -270)

            self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.dbfile)
            self.db.open()
            self.query = QtSql.QSqlQuery()
            self.dbSearch(self.dbkey)

            self.img = QPixmap(self.key)
            self.scene = QGraphicsScene()
            self.scene.addPixmap(self.img)

            self.view = ImageViewing(self.scene)
            self.setCentralWidget(self.view)

            closeSig = self.view.viewerCloseSig
            realSizeSig = self.view.viewRealImageSizeSig
            fullScreenSig = self.view.toggleFullscreenSig
            vertMaxSig = self.view.vertMaxSig
            horizMaxSig = self.view.horizMaxSig
            zoomInSig = self.view.zoomInSig
            zoomOutSig = self.view.zoomOutSig
            zoomResetSig = self.view.zoomResetSig
            rotateImgSig = self.view.rotateImgSig
            dirBrowserSig = self.view.dirBrowseSig
            fitViewSig = self.view.fitViewSig
            localtionSig = self.view.goToLocationSig

            closeSig.connect(self.closeLayout)
            realSizeSig.connect(self.viewRealImageSize)
            fullScreenSig.connect(self.toggleFullscreen)
            vertMaxSig.connect(self.vertMax)
            horizMaxSig.connect(self.horizMax)
            zoomInSig.connect(self.zoomIn)
            zoomOutSig.connect(self.zoomOut)
            zoomResetSig.connect(self.zoomReset)
            rotateImgSig.connect(self.getValueRotate)
            dirBrowserSig.connect(self.getValueDirBrowser)
            fitViewSig.connect(self.fitView)
            localtionSig.connect(self.goToLocation)

            self.view.setDragMode(QGraphicsView.ScrollHandDrag)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # Create array of images in current image dir
            self.imgfiles = []
            for filename in glob.glob(str(self.path) + '/*'):
                base, ext = os.path.splitext(filename)
                if ext.lower() in self.formats:
                    self.imgfiles.append(filename)

            # Find location of current image in imgfiles array
            self.dirpos = 0
            while self.dirpos < len(self.imgfiles) and self.imgfiles[self.dirpos] != self.key:
                self.dirpos += 1
            # If we have no inshuftery, we use the defaults
            if self.inshuft == 0:
                self.newImage()
            else:
                self.oldImage()
        else:
            # print("Unsupported file format")
            # sys.exit(1)
            pass

    def getValueRotate(self, value):
        self.rotateImg(value)

    def getValueDirBrowser(self, value):
        self.dirBrowse(value)

    def viewRealImageSize(self):
        self.resize(self.img.height(), self.img.width())

    def newImage(self):

        self.getScreenRes()
        self.imgw = self.img.width()
        self.imgh = self.img.height()
        self.zoom = 1
        self.rotate = 0
        if self.imgw > self.screenw or self.imgh > self.screenh:
            self.resize(self.screenw, self.screenh)
            self.show()
            self.resetScroll()
            self.fitView()
        else:
            self.resize(self.imgw + 2, self.imgh + 2)
            self.show()
            self.resetScroll()

    def oldImage(self):

        if self.rotate == -90:
            self.rotval = 1
        elif self.rotate == -180:
            self.rotval = 2
        elif self.rotate == -270:
            self.rotval = 3
        self.resize(self.img.size())
        self.updateView()
        self.show()
        self.setGeometry(self.winposx, self.winposy, self.winsizex, self.winsizey)
        self.view.verticalScrollBar().setValue(self.vscroll)
        self.view.horizontalScrollBar().setValue(self.hscroll)

    def goToLocation(self):
        os.startfile(self.path)

    def toggleFullscreen(self):

        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_F11:
            self.toggleFullscreen()
        elif event.key() == Qt.Key_Equal or event.key() == Qt.Key_E:
            self.zoomIn()
        elif event.key() == Qt.Key_Minus or event.key() == Qt.Key_D:
            self.zoomOut()
        elif event.key() == Qt.Key_1:
            self.zoomReset()
        elif event.key() == Qt.Key_S:
            self.rotateImg(-1)
        elif event.key() == Qt.Key_R:
            self.rotateImg(1)
        elif event.key() == Qt.Key_F:
            self.fitView()
        elif event.key() == Qt.Key_Space:
            self.dirBrowse(1)
        elif event.key() == Qt.Key_Backspace:
            self.dirBrowse(-1)
        elif event.key() == Qt.Key_V:
            self.vertMax()
        elif event.key() == Qt.Key_Z:
            self.horizMax()
        elif event.key() == Qt.Key_Q:
            self.close()

    def mouseDoubleClickEvent(self, event):

        self.toggleFullscreen()

    def createDB(self):

        if not os.path.exists(self.dbdir):
            os.makedirs(self.dbdir)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbfile)
        self.query = QtSql.QSqlQuery()
        self.db.open()
        self.query.exec_("create table shuftery(filename text primary configKey, "
                         "zoom real, winposx int, winposy int, winsizex int, winsizey int, "
                         "hscroll int, vscroll int, rotate int)")
        return True

    def zoomIn(self):

        self.zoom *= 1.05
        self.updateView()

    def zoomOut(self):

        self.zoom /= 1.05
        self.updateView()

    def zoomReset(self):

        self.zoom = 1
        self.updateView()

    def rotateImg(self, clock):

        self.rotval += clock
        if self.rotval == 4:
            self.rotval = 0
        elif self.rotval < 0:
            self.rotval = 3
        self.rotate = self.rotvals[self.rotval]
        self.updateView()

    def fitView(self):

        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        if self.rotate == 0:
            self.zoom = self.view.transform().m11()
        elif self.rotate == -90:
            self.zoom = (self.view.transform().m12()) * -1
        elif self.rotate == -180:
            self.zoom = (self.view.transform().m11()) * -1
        else:
            self.zoom = self.view.transform().m12()

    def updateView(self):
        self.view.setTransform(QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))

    def winState(self):

        self.winsizex = self.geometry().width()
        self.winsizey = self.geometry().height()
        self.vscroll = self.view.verticalScrollBar().value()
        self.hscroll = self.view.horizontalScrollBar().value()
        self.winposx = self.pos().x()
        self.winposy = self.pos().y()

    def dbInsert(self):

        self.query.exec_("insert into shuftery values('%s" % self.dbkey +
                         "', " + str(self.zoom) + ", " + str(self.winposx) + ", " + str(self.winposy) +
                         ", " + str(self.winsizex) + ", " + str(self.winsizey) + ", " + str(self.hscroll) +
                         ", " + str(self.vscroll) + ", " + str(self.rotate) + ")")

    def dbUpdate(self):

        self.query.exec_("update shuftery set zoom=" + str(self.zoom) +
                         ", winposx=" + str(self.winposx) + ", winposy=" + str(self.winposy) +
                         ", winsizex=" + str(self.winsizex) + ", winsizey=" + str(self.winsizey) +
                         ", hscroll=" + str(self.hscroll) + ", vscroll=" + str(self.vscroll) +
                         ", rotate=" + str(self.rotate) + " where filename='%s'" % self.dbkey)

    def dbSearch(self, field):

        self.query.exec_("SELECT * FROM shuftery WHERE filename='%s'" % field)
        # If the image is found in shufti.db, load the previous view glsetting
        while self.query.next() and self.inshuft == 0:
            self.zoom = self.query.value(1)
            self.winposx = self.query.value(2)
            self.winposy = self.query.value(3)
            self.winsizex = self.query.value(4)
            self.winsizey = self.query.value(5)
            self.hscroll = self.query.value(6)
            self.vscroll = self.query.value(7)
            self.rotate = self.query.value(8)
            self.inshuft = 1

    def dbSanitise(self):

        self.dbkey = self.key.replace("\"", "\"\"")
        self.dbkey = self.dbkey.replace("\'", "\'\'")
        self.dbkey = self.dbkey.replace("\\", "\\\\")

    def dirBrowse(self, direc):

        if len(self.imgfiles) > 1:
            self.dirpos += direc
            if self.dirpos > (len(self.imgfiles) - 1):
                self.dirpos = 0
            elif self.dirpos < 0:
                self.dirpos = (len(self.imgfiles) - 1)

            self.winState()
            if self.inshuft == 0:
                self.dbInsert()
            else:
                self.dbUpdate()

            self.key = self.imgfiles[self.dirpos]
            self.dbSanitise()

            self.path, self.title = os.path.split(self.key)
            self.setWindowTitle(str("Image Viewer: " + self.title))
            self.setWindowIcon(QIcon(AppIcon(32, "ImageViewer")))

            self.inshuft = 0
            self.dbSearch(self.dbkey)
            self.scene.clear()
            self.view.resetTransform()
            self.img = QPixmap(self.key)
            self.scene.addPixmap(self.img)
            if self.inshuft == 0:
                self.newImage()
            else:
                self.oldImage()

    def vertMax(self):

        self.getScreenRes()
        self.winsizex = self.geometry().width()
        self.winposx = self.pos().x()
        self.setGeometry(self.winposx, 0, self.winsizex, self.screenh)

    def horizMax(self):

        self.getScreenRes()
        self.winsizey = self.geometry().height()
        self.winposy = self.pos().y()
        self.setGeometry(0, self.winposy, self.screenw, self.winsizey)

    def resetScroll(self):

        self.view.verticalScrollBar().setValue(0)
        self.view.horizontalScrollBar().setValue(0)

    def getScreenRes(self):
        self.screenw, self.screenh = get_screen_resolution()

    def closeLayout(self, param):
        if param:
            QApplication.instance().quit()

# -------------------------------------------------------------------------------------------------------------
""" Image Viewer class """

class ImageViewer(Widget):

    key = 'ImageViewer'

    def __init__(self, key=None, parent=None):
        super(ImageViewer, self).__init__(parent)
        if key == None or not os.path.exists(key) or os.path.isdir(key):
            # configKey = self.loadImageFromFile()
            key = " "

        self._key = key
        self.layout = QHBoxLayout()
        self.buildUI()
        self.setLayout(self.layout)

    def buildUI(self):

        viewer = ImageInitUI(self._key)
        resizeSig = viewer.resizeSig
        resizeSig.connect(self.resizeUI)

        self.title = viewer.title

        self.setWindowTitle("Image Viewer: " + str(self.title))
        self.setWindowIcon(AppIcon(32, "ImageViewer"))

        self.layout.addWidget(viewer)

    def loadImageFromFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose an image", QDir.currentPath(),
                                                  "All Files (*)"
                                                  ";;Img Files (*.jpg);;Img Files (*.jpeg);;Img Files (*.png)"
                                                  ";;Img Files (*.gif);;Img Files (*.bmp);;Img Files (*.pbm)"
                                                  ";;Img Files (*.pgm);;Img Files (*.pgm);;Img Files (*.ppm)"
                                                  ";;Img Files (*.xbm);;Img Files (*.xpm);;Img Files (*.dds)"
                                                  ";;Img Files (*.icns);;Img Files (*.jp2);;Img Files (*.mng)"
                                                  ";;Img Files (*.tga);;Img Files (*.tiff);;Img Files (*.wbmp)"
                                                  ";;Img Files (*.webp)",
                                                  options=options)

        if fileName:
            return fileName
        elif str(type(fileName)) == "NoneType":
            return " "
        else:
            return " "

    def resizeUI(self, w, h):
        self.resize(w, h)