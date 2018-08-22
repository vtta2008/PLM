SHORT FILM PIPELINE
===================

.. image:: https://github.com/vtta2008/DAMGTEAM/blob/master/__rc__/imgs/tags/python.tag.png
    :target: https://www.anaconda.com/download/

.. image:: https://github.com/vtta2008/DAMGTEAM/blob/master/__rc__/imgs/tags/version.tag.png
    :target: https://github.com/vtta2008/PipelineTool/releases

.. image:: https://github.com/vtta2008/DAMGTEAM/blob/master/__rc__/imgs/tags/licence.tag.png
    :target: https://github.com/vtta2008/PipelineTool/blob/master/LICENSE

This application can be used to build, manage, and optimise film making pipelines. The latest version is compatible
with Windows 10 and may run on earlier versions. It does not run in Maya 2016 or lower.

Due to VFX Reference Platform and the large invention, we need to stay with python 2.7 but expect to migrate to python 3 in 2019 (Delayed to 2020).
Details are `here <http://www.vfxplatform.com>`_

NOTE:

    - It is still under developing, some function will not be working yet.

REQUIREMENTS
============

Python 3.6 for Windows:

    - 64 bit `download <https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe>`_

    - 32 bit `download <https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86.exe>`_

Also require extra python packages (will update more)   || To install extra packages, run command in CMD:

.. code:: bash

    PyQt5       >= 5.11.2       deprecate   >= 1.0.5    || python -m pip install {packagename} --user --upgrade
    msgpack     >=0.5.6         winshell    >= 11.0.6   ||
    pip         >=18            pandas      >=0.23.4    ||
    wheel       >=0.31.1        appdirs     >=1.4.3     ||
    argparse    >=1.4.0         green       >=2.12.1    ||

LIST SOFTWARE PACKAGE
======================

    - `Maya 2017 and/or Maya 2018 <https://www.autodesk.com/education/free-software/maya>`_
    - `Vray 3.6 <https://www.chaosgroup.com/vray/maya>`_
    - `Phoenix FD 3.0 <https://www.chaosgroup.com/phoenix-fd/maya>`_
    - `VMM for maya <https://www.mediafire.com/#gu9s1tbb2u4g9>`_
    - `Houdini <https://www.sidefx.com/download/>`_
    - `Mari <https://www.foundry.com/products/mari>`_
    - Mari extension: "Will update later"
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

Run directly:                                       Complie executable file:

.. code:: bash

    start python PLM.py                             python setup.py build

REFERENCE
=========

For Plugins/Files that I am using, you can see `here <appData/docs/reference>`_.
Copyright (C) 2017 - 2018 by DAMGteam - `details <appData/docs/copyright>`_.