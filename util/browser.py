import json
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import *

import variables as var

PACKAGE = var.MAIN_PACKPAGE
NAMES = var.MAIN_NAMES
CURPTH = var.MAIN_ROOT
pthInfo = os.path.join(CURPTH, NAMES['appdata'])
infoData = NAMES['info']
with open(os.path.join(pthInfo, infoData), 'r') as f:
    info = json.load(f)
# Get app path
APPINFO = info['pipeline']
LOGO = info['icon']['Logo']
iconPth = os.path.join(CURPTH, 'icons/Web.icon')
keys = [k.split('.icon')[0] for k in os.listdir(iconPth) if k.endswith('.png')]

info = {}
icons = {}

for key in keys:
    icons[key] = os.path.join(iconPth, key + '.icon.png')

info['icons'] = icons
info['homePage'] = 'https://www.google.com.vn'

with open(os.path.join(PACKAGE['appData'], NAMES['web']), 'w') as f:
    json.dump(info, f, indent=4)

with open(os.path.join(PACKAGE['appData'], NAMES['web']), 'r') as f:
    web = json.load(f)

icons = web['icons']


class DAMGwebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(DAMGwebBrowser, self).__init__(*args, **kwargs)

        self.setWindowTitle('DAMG web browser')

        self.setWindowIcon(QIcon(LOGO))

        self.buildUI()

        self.setCentralWidget(self.browser)

        self.show()

    def buildUI(self):
        self.browser = QWebView()
        self.browser.setUrl(QUrl(web['homePage']))

        navtb = QToolBar('Navigation')
        homeBtn, backBtn, forwardBtn, reloadBtn, stopBtn = self.toolBarBtns()
        navtb.addAction(homeBtn)
        navtb.addAction(backBtn)
        navtb.addAction(forwardBtn)
        navtb.addAction(stopBtn)
        navtb.addAction(reloadBtn)

        urltb = QToolBar('URL')

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(icons['https']))
        self.httpsicon.resize(16, 16)
        urltb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigateUrl)
        urltb.addWidget(self.urlbar)

        self.addToolBar(navtb)
        self.addToolBar(urltb)

        self.browser.urlChanged.connect(self.updateUrlBar)

    def toolBarBtns(self):
        homeBtn = QAction(QIcon(icons['home']), 'Home', self)
        homeBtn.setToolTip('Go to homepage')
        homeBtn.triggered.connect(self.homepage)

        backBtn = QAction(QIcon(icons['back']), 'Back', self)
        backBtn.setToolTip('Back to previous page')
        backBtn.triggered.connect(self.browser.back)

        forwardBtn = QAction(QIcon(icons['forward']), 'Forward', self)
        forwardBtn.setToolTip('Forward to next page')
        forwardBtn.triggered.connect(self.browser.forward)

        reloadBtn = QAction(QIcon(icons['refresh']), 'Reload', self)
        reloadBtn.setToolTip('Reload the current page')
        reloadBtn.triggered.connect(self.browser.reload)

        stopBtn = QAction(QIcon(icons['stop']), 'Stop', self)
        stopBtn.setToolTip('Stop loading page')
        stopBtn.triggered.connect(self.browser.stop)

        return homeBtn, backBtn, forwardBtn, reloadBtn, stopBtn

    def updateUrlBar(self, q):
        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(icons['https']))
        else:
            self.httpsicon.setPixmap(QPixmap(icons['http']))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def navigateUrl(self):
        q = QUrl(self.urlbar.text())

        if q.scheme() == '':
            q.setScheme('https')

        self.browser.setUrl(QUrl(q))

    def homepage(self):
        self.browser.setUrl(QUrl('https://www.google.com.vn'))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    web = DAMGwebBrowser()

    app.exec_()
