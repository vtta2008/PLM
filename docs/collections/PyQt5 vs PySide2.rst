
PyQt5 vs PySide2: What's the difference between the two Python Qt libraries?
############################################################################

...and what's exactly the same (most of it)
===========================================

If you start building Python application with Qt5 you'll soon discover that there are in fact two packages which you
can use to do this — PyQt5 and PySide2.

In this short guide I'll run through why exactly this is, whether you need to care (spoiler: you really don't), what the
few differences are and how to work around them. By the end you should be comfortable re-using code examples from both
PyQt5 and PySide2 tutorials to build your apps, regardless of which package you're using yourself.

Background
==========

#. Why are there two packages?

PyQt has been developed by Phil Thompson of `Riverbank Computing Ltd <https://www.riverbankcomputing.com/software/pyqt/intro>`_.
for a very long time — supporting versions of Qt going back to 2.x. Back in 2009 Nokia, who owned the Qt toolkit at the
time, wanted to have Python bindings for Qt available under the LGPL license (like Qt itself). Unable to come to
agreement with Riverbank (who would lose money from this, so fair enough) they then released their own bindings as PySide
(also, fair enough).

.. note::

    Edit: it's called PySide because "side" is Finnish for "binder" — thanks to Renato Araujo Oliveira Filho in the comments.

The two interfaces were comparable at first but PySide ultimately development lagged behind PyQt. This was particularly
noticeable following the release of Qt 5 — the Qt5 version of PyQt (PyQt5) was available from mid-2016, while the first
stable release of PySide2 was 2 years later.

It is this delay which explains why many Qt 5 on Python examples use PyQt5 rather than PySide2 — it's not necessarily
better, but it existed. However, the Qt project has recently adopted PySide as the official `Qt for Python release <https://wiki.qt.io/Qt_for_Python>`_
which should ensure its viability and increase it's popularity going forward.

.. list-table:: OVERVIEW
    :widths: 100 100 100
    :header-rows: 1

    * - Criteria
      - PyQt5
      - PySide2

    * - Current stable version (2019-06-23)
      - 5.12
      - 5.12

    * - First stable release
      - Apr 2016
      - Jul 2018

    * - Developed by
      - Riverbank Computing Ltd.
      - Qt

    * - License
      - GPL or commercial
      - LGPL

    * - Platforms
      - Python 3
      - Python 3 and Python 2.7 (Linux and MacOS only)

Which should you use? Well, honestly, it doesn't really matter.

Both packages are wrapping the same library — Qt5 — and so have 99.9% identical APIs (see below for the few differences).
Code that is written for one can often be used as-is with other, simply changing the imports from **PyQt5** to **PySide2**.
Anything you learn for one library will be easily applied to a project using the other.

Also, no matter with one you choose to use, it's worth familiarising yourself with the other so you can make the best
use of all available online resources — using PyQt5 tutorials to build your PySide2 applications for example, and vice
versa.

In this short chapter I'll run through the few notable differences between the two packages and explain how to write
code which works seamlessly with both. After reading this you should be able to take any PyQt5 example online and
convert it to work with PySide2.

#. Licensing

The key difference in the two versions — in fact the entire reason PySide2 exists — is licensing. PyQt5 is available
under a GPL or commercial license, and PySide2 under a LGPL license.

If you are planning to release your software itself under the GPL, or you are developing software which will not be
distributed, the GPL requirement of PyQt5 is unlikely to be an issue. However, if you plan to distribute your software
without distributing the source you will either need to purchase a commercial license from Riverbank for PyQt5 or use
PySide2.

The LGPL license does not require you to share the source code of your own applications, even if they are bundled with
PySide2. You only need to ensure that the source code covered by the LGPL is made available, including modifications
you have made to it, if any. In normal use there will not be any modifications and the standard distributions of
PySide2/Qt5 source code will already cover this for you.

.. note::

    Qt itself is available under a Qt Commercial License, GPL 2.0, GPL 3.0 and LGPL 3.0 licenses.

#. Python versions

    *   PyQt5 is Python 3 only.

    *   PySide2 is available for Python3 and Python 2.7, but Python 2.7 builds are only available for 64 bit versions of MacOS
        and Linux. Windows 32 bit is supported on Python 2 only.

4. UI files

Both packages use slightly different approaches for loading .ui files exported from Qt Creator/Designer. PyQt5 provides
the uic submodule which can be used to load UI files directly, to produce an object. This feels pretty Pythonic (if you
ignore the camelCase).

PYTHON
------

.. code-block:: python

    import sys
    from PyQt5 import QtWidgets, uic

    app = QtWidgets.QApplication(sys.argv)

    window = uic.loadUi("mainwindow.ui")
    window.show()
    app.exec()


The equivalent with PySide2 is one line longer, since you need to create a QUILoader object first. Unfortunately the api
of these two interfaces is different too (.load vs .loadUI) and take different parameters.

.. code-block:: python

    import sys
    from PySide2 import QtCore, QtGui, QtWidgets
    from PySide2.QtUiTools import QUiLoader

    loader = QUiLoader()

    app = QtWidgets.QApplication(sys.argv)
    window = loader.load("mainwindow.ui", None)
    window.show()
    app.exec_()


To load a UI onto an object in PyQt5, for example in your ``QMainWindow.__init__``, you can call ``uic.loadUI`` passing
in ``self`` (the target widget) as the second parameter.

.. code-block:: python

    import sys
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5 import uic


    class MainWindow(QtWidgets.QMainWindow):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            uic.loadUi("mainwindow.ui", self)


    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


The PySide2 loader does not support this — the second parameter to ``.load`` is the parent widget of the widget you're
creating. This prevents you adding custom code to the ``__init__`` block of the widget, but you can work around this with a
separate function.

.. code-block:: python

    import sys
    from PySide2 import QtWidgets
    from PySide2.QtUiTools import QUiLoader

    loader = QUiLoader()

    def mainwindow_setup(w):
        w.setTitle("MainWindow Title")

    app = QtWidgets.QApplication(sys.argv)

    window = loader.load("mainwindow.ui", None)
    mainwindow_setup(window)
    window.show()
    app.exec()


#. Converting UI files to Python

Both libraries provide identical scripts to generate Python importable modules from Qt Designer ``.ui`` files. For PyQt5
the script is named ``pyuic5``.

.. code-block:: BASH

    pyuic5 mainwindow.ui -o MainWindow.py

You can then import the UI_MainWindow object, subclass using multiple inheritance from the base class you're using (e.g.
QMainWIndow) and then call self.setupUI(self) to set the UI up.

.. code-block:: python

    import sys
    from PyQt5 import QtWidgets
    from MainWindow import Ui_MainWindow

    class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.setupUi(self)


    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

For PySide2 it is named ``pyside2-uic`` —

.. code-block:: BASH

    pyside2-uic mainwindow.ui -o MainWindow.py

The subsequent setup is identical.

.. code-block:: python

    import sys
    from PySide2 import QtWidgets
    from MainWindow import Ui_MainWindow

    class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setupUi(self)


    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

.. note::

    For more information on using Qt Designer with either PyQt5 or PySide2 see the Qt Creator tutorial.

#. exec() or exec_()

The .exec() method is used in Qt to start the event loop of your QApplication or dialog boxes. In Python 2.7 exec was a
keyword, meaning it could not be used for variable, function or method names. The solution used in both PyQt4 and PySide
was to rename uses of .exec to .exec_() to avoid this conflict.

Python 3 removed the exec keyword, freeing the name up to be used. As PyQt5 targets only Python 3 it could remove the
workaround, and .exec() calls are named just as in Qt itself. However, the .exec_() names are maintained for backwards
compatibility.

PySide2 is available on both Python 3 and Python 2.7 and so still uses .exec_(). It is however only available for 64bit
Linux and Mac.

If you're targeting both PySide2 and PyQt5 use .exec_()

Slots and Signals
Defining custom slots and signals uses slightly different syntax between the two libraries. PySide2 provides this
interface under the names Signal and Slot while PyQt5 provides these as pyqtSignal and pyqtSlot respectively. The
behaviour of them both is identical for defining and slots and signals.

The following PyQt5 and PySide2 examples are identical —

.. code-block:: python

    my_custom_signal = pyqtSignal()  # PyQt5
    my_custom_signal = Signal()  # PySide2

    my_other_signal = pyqtSignal(int)  # PyQt5
    my_other_signal = Signal(int)  # PySide2

Or for a slot —

.. code-block:: python

    @pyqtslot
    def my_custom_slot():
        pass

    @Slot
    def my_custom_slot():
        pass

If you want to ensure consistency across PyQt5 and PySide2 you can use the following import pattern for PyQt5 to use
the Signal and @Slot style there too.

.. code-block:: python

    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

.. list-table::

    * - You could of course do the reverse from PySide2.QtCore import Signal as pyqtSignal, Slot as pyqtSlot although
        that's a bit confusing.

#. Supporting both in libraries

.. list-table::

    * - You don't need to worry about this if you're writing a standalone app, just use whichever API you prefer.

If you're writing a library, widget or other tool you want to be compatible with both PyQt5 and PySide2 you can do so
easily by adding both sets of imports.

.. code-block:: python

    import sys

    if 'PyQt5' in sys.modules:
        # PyQt5
        from PyQt5 import QtGui, QtWidgets, QtCore
        from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

    else:
        # PySide2
        from PySide2 import QtGui, QtWidgets, QtCore
        from PySide2.QtCore import Signal, Slot

This is the approach used in our custom widgets library, where we support for PyQt5 and PySide2 with a single library
import. The only caveat is that you must ensure PyQt5 is imported before (as in on the line above or earlier) when
importing this library, to ensure it is in sys.modules.

.. list-table::

    * - An alternative would be to use an environment variable to switch between them — see QtPy later.

If you're doing this in multiple files it can get a bit cumbersome. A nice solution to this is to move the import logic
to its own file, e.g. named qt.py in your project root. This module imports the Qt modules (QtCore, QtGui, QtWidgets,
etc.) from one of the two libraries, and then you import into your application from there.

The contents of the qt.py are the same as we used earlier —

.. code-block:: python

    import sys

    if 'PyQt5' in sys.modules:
        # PyQt5
        from PyQt5 import QtGui, QtWidgets, QtCore
        from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot

    else:
        # PySide2
        from PySide2 import QtGui, QtWidgets, QtCore
        from PySide2.QtCore import Signal, Slot

You must remember to add any other PyQt5 modules you use (browser, multimedia, etc.) in both branches of the if block.
You can then import Qt5 into your own application with —

.. code-block:: python

    from .qt import QtGui, QtWidgets, QtCore

…and it will work seamlessly across either library.

#. QtPy

If you need to target more than just Qt5 support (e.g. including PyQt4 and PySide v1) take a look at QtPy. This
provides a standardised PySide2-like API for PyQt4, PySide, PyQt5 and PySide2. Using QtPy you can control which API to
load from your application using the QT_API environment variable e.g.

.. code-block:: python

    import os
    os.environ['QT_API'] = 'pyside2'
    from qtpy import QtGui, QtWidgets, QtCore  # imports PySide2.

That's really it
There's not much more to say — the two are really very similar. With the above tips you should feel comfortable taking
code examples or documentation from PyQt5 and using it to write an app with PySide2. If you do stumble across any PyQt5
or PySide2 examples which you can't easily convert, drop a note in the comments and I'll update this page with advice.