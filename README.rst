SHORT FILM PIPELINE
====================

This applications can be used to build, manage, and optimise film making pipelines. The latest version is compatible
with Windows 10 and may run on earlier versions. It does not run in Maya 2016 or lower.

Due to VFX Reference Platform and the large invention, we need to stay with python 2.7 but expect to migrate to python 3 in 2019.
Details are `here <http://www.vfxplatform.com>`_

NOTE:
    - Currently I am working on setup a server and working on it, some functions may not work.

**SOFTWARE TO INSTALL**
=======================

Python 3.6 for Windows:
    - 64 bit `download <https://repo.anaconda.com/archive/Anaconda3-5.1.0-Windows-x86_64.exe>`_

    - 32 bit `download <https://repo.anaconda.com/archive/Anaconda3-5.1.0-Windows-x86.exe>`_

    - Also require extra python packages (will update more):

.. code:: bash

    deprecated, jupyter-console, ipywidgets,'pywinauto, winshell, pandas,
    notebook, juppyter, opencv-python, pyunpack, argparse, qdarkgraystyle,
    asyncio, websockets, cx_Freeze,

To install extra packages, run command in CMD:

.. code:: bash
    python -m pip install {packagename}

**LIST SOFTWARES PACKAGE**
==========================

    - `Maya 2017 <https://www.autodesk.com/education/free-software/maya>`_
    - `Vray 3.6 <https://www.chaosgroup.com/vray/maya>`_
    - `Phoenix FD 3.0 <https://www.chaosgroup.com/phoenix-fd/maya>`_
    - `VMM for maya <https://www.mediafire.com/#gu9s1tbb2u4g9>`_
    - `Houdini <https://www.sidefx.com/download/>`_
    - `Mari download <https://www.foundry.com/products/mari>`_
    - Mari extension: "Will update later"
    - `Nuke download <https://www.foundry.com/products/nuke>`_
    - `ZBrush download <https://pixologic.com/zbrush/downloadcenter/>`_
    - `Creative Cloud download <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
    - `Davinci Resolve <https://www.blackmagicdesign.com/nz/products/davinciresolve/>`_

NOTE:
    - You can install Photoshop, Premiere, After Effects or anything you want with Adobe Creative Cloud

    - For VMM for maya, remember to configure the path once it is opened in Maya. (sadly, the author has stopped developing the plugin.)

**LIBRARY SUPPORT**
===================

I spent many years to build this library for texturing and referencing. The library is now freely availalbe to everyone.
You may also find the following libraries useful:

    - `ALPHA library <https://www.mediafire.com/#21br3oz8gf44j>`_
    - `HDRI library <https://www.mediafire.com/#33moon9n0qagc>`_
    - `TEXTURE library <https://www.mediafire.com/#v5t32j935afg7>`_

**HOW TO USE PIPELINE TOOL**
============================

Go to the diretory of 'PipelineTool' folder, hold down Shift + right-click -> Open PowerShell window here/Open command window here
In CommandPrompt/WindowShell:

Run directly:

.. code:: bash
    start python main.py

Complie executable file:

.. code:: bash
    python setup.py build

**REFERENCE**
=============

Here is the Plugins/Files that I am using:

.. code:: bash

    GitHub - mottosso/Qt.py: Minimal Python 2 & 3 shim around all Qt bindings - PySide, PySide2, PyQt4 and PyQt5. (n.d.).
    Retrieved from https://github.com/mottosso/Qt.py

    mstuttgart/qdarkgraystyle. (n.d.). A dark gray style sheet for PyQt5 application.
    Retrieved from https://github.com/mstuttgart/qdarkgraystyle

    sqlitebrowser/sqlitebrowser. (2017, November 30).
    Retrieved from https://github.com/sqlitebrowser/sqlitebrowser

    Advanced Renamer - Free and fast batch rename utility for files and folders. (n.d.).
    Retrieved from https://www.advancedrenamer.com/

Copyright (C) 2016-2018 by Trinh Do