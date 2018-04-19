## **SHORT FILM PIPELINE**

This applications can be used to build, manage, and optimise film making pipelines.

The latest version is compatible with Windows 10 and may run on earlier versions. It does not run in Maya 2016 or lower.

Due to VFX Reference Platform and the large invention, we need to stay with python 2.7 but expect to migrate to python 3 in 2019.

Details are as follows:

    http://www.vfxplatform.com/

**SOFTWARE TO INSTALL**

Python standalone:

    - Anaconda python 2.7: https://www.anaconda.com/download

Maya 2017/2018(Optional):

    - Maya education: https://www.autodesk.com/education/free-software/maya
    - Vray 3.6: https://www.chaosgroup.com/vray/maya
    - Phoenix FD 3.0: https://www.chaosgroup.com/phoenix-fd/maya

Houdini:

    - Houdini download: https://www.sidefx.com/download/

Mari:

    - Mari download: https://www.foundry.com/products/mari
    - Mari extension: "Will update later"

Nuke:

    - Nuke download: https://www.foundry.com/products/nuke

ZBrush:

    - ZBrush download: https://pixologic.com/zbrush/downloadcenter/

Adobe:

    - Creative Cloud download: https://www.adobe.com/creativecloud/catalog/desktop.html
    You can install Photoshop, Premiere, After Effects or anything you want with Adobe Creative Cloud

Davinci Resolve:

    - Davinci Resolve download: https://www.blackmagicdesign.com/nz/products/davinciresolve/

**LIBRARY SUPPORT**

I spent many years to build this library for texturing and referencing. The library is now freely availalbe to everyone.

For V-ray Materials in Maya, you will need this plugin:

    VMM for maya: https://www.mediafire.com/#gu9s1tbb2u4g9
    After downloading it, remember to configure the path once it is opened in Maya.
    Unfortunately, the original author has stopped developing the plugin.

You may also find the following libraries useful:

Alpha library:

    ALPHA library: https://www.mediafire.com/#21br3oz8gf44j

Hdri library:

    HDRI library: https://www.mediafire.com/#33moon9n0qagc

Texture library:

    TEXTURE library: https://www.mediafire.com/#v5t32j935afg7

**RUN PIPELINE TOOL**

Download and extract the zip file, remember to rename the folder as 'PipelineTool'.

Go to the diretory of 'PipelineTool' folder, hold down Shift + right-click -> Open PowerShell window here/Open command window here

In CommandPrompt/WindowShell:

    "start python main.py" then enter to run.

A user login window will show up. Login with your username and password.

If you do not have login account, simply create one. I have updated register function.

* Update sql, now data is being stored to database file.
* Tranfering configurations of the pipeline into database, not using yml.

**REFERENCE**

Here is the Plugins/Files that I use in Maya:

    GitHub - mottosso/Qt.py: Minimal Python 2 & 3 shim around all Qt bindings - PySide,
    PySide2, PyQt4 and PyQt5. (n.d.). Retrieved from https://github.com/mottosso/Qt.py

Database browser:

    sqlitebrowser/sqlitebrowser. (2017, November 30).
    Retrieved from https://github.com/sqlitebrowser/sqlitebrowser

Advance Renamer:

    Advanced Renamer - Free and fast batch rename utility for files and folders. (n.d.).
    Retrieved from https://www.advancedrenamer.com/

**TODO LIST**

- Add pycharm, sublime into app *Done
- Redesign database
- Optimise configuration procedures *Working
