SHORT FILM PIPELINE
===================

This application can be used to build, manage, and optimise film making pipelines. The latest version is compatible
with Windows 10 and may run on earlier versions. It does not run in Maya 2016 or lower.

Due to VFX Reference Platform and the large invention, we need to stay with python 2.7 but expect to migrate to python 3 in 2019 (Delayed to 2020).
Details are `here <http://www.vfxplatform.com>`_

NOTE:

    - It is still under developing, some function will not be working yet.
    - Really struggling at compling to executable file as well as build the installation.

REQUIREMENTS
============

    - Anaconda Python 3+ for Windows: download `64bit <https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe>`_ or `32bit <https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86.exe>`_

    Software & plugins available:

    - `Maya 2017+ <https://www.autodesk.com/education/free-software/maya>`_
    - `Vray <https://www.chaosgroup.com/vray/maya>`_, `Phoenix FD for Maya <https://www.chaosgroup.com/phoenix-fd/maya>`_
    - `VMM for maya <https://www.mediafire.com/#gu9s1tbb2u4g9>`_
    - `Houdini <https://www.sidefx.com/download/>`_
    - `Mari <https://www.foundry.com/products/mari>`_
    - `Nuke <https://www.foundry.com/products/nuke>`_
    - `ZBrush <https://pixologic.com/zbrush/downloadcenter/>`_
    - `Davinci Resolve <https://www.blackmagicdesign.com/nz/products/davinciresolve/>`_

NOTE:

    - You can install Photoshop, Premiere, After Effects or anything you want with `Adobe Creative Cloud <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
    - For VMM for maya, remember to configure the path once it is opened in Maya. (sadly, the author has stopped developing the plugin.)

LIBRARY SUPPORT
===============

I spent many years to build this library for texturing and referencing. The library is now freely availalbe to everyone.
You may also find the following libraries useful, You will need an `mediafie <https://mediafire.com>`_ account to be able to download.

    - `ALPHA library <https://www.mediafire.com/#21br3oz8gf44j>`_
    - `HDRI library <https://www.mediafire.com/#33moon9n0qagc>`_
    - `TEXTURE library <https://www.mediafire.com/#v5t32j935afg7>`_

HOW TO USE PIPELINE MANAGER
===========================

Go to the diretory of 'PipelineTool' folder, hold down Shift + right-click -> Open PowerShell window here/Open command window here
In CommandPrompt/WindowShell:

Run directly:

.. code:: bash

    start python main.py

Complie executable file:

.. code:: bash

    python setup.py build

REFERENCE
=========

For Plugins/Files that I am using, you can see `here <appData/docs/reference>`_.

Copyright (C) 2017 - 2019 by DAMGTEAM - `details <appData/docs/copyright>`_.