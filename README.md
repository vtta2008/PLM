## **SHORT FILM PIPELINE**

This applications is to build, manage, and optimise a pipeline to make a short film.

Now it's compatible with Windows 10 (may also work with earlier version but I have not tested yet) and will not work with Maya 2016 or lower.

Regard to VFX Reference Platform, due to large invention we will stay with python 2.7 but will update to python 3 on 2019.
Details are here:

    http://www.vfxplatform.com/

**SOFTWARE INSTALL**

Python standalone:

    - Anaconda python 2.7: https://www.anaconda.com/download

Maya 2017/2018(it's up to you):

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

After years of research and accumulation, I can share you some library which is good for texturing and/or reference.

You will need this for V-ray material preset in maya (VMM for maya).

    VMM for maya: https://www.mediafire.com/#gu9s1tbb2u4g9
    After downloading, please remember config the path to it when you open inside Maya.
    It is really sadly that the author has stop developing this app.

Otherwise, here is something you may (or may not) like it.

Alpha library:

    ALPHA library: https://www.mediafire.com/#21br3oz8gf44j

Hdri library:

    HDRI library: https://www.mediafire.com/#33moon9n0qagc

Texture library:

    TEXTURE library: https://www.mediafire.com/#v5t32j935afg7

**RUN PIPELINE TOOL**

Download and extract zip file to your pc, remember to rename the folder to 'PipelineTool'.

Go to PipelineTool folder in your explorer, hold Shift + right-click -> Open PowerShell window here/Open command window here

In CommandPrompt/WindowShell window:

    "start python main.py" then enter to run.

A user login window will show up, login with your username and password.

If you do not have login account, simply create one. I have updated register function.

* Update sql, now data is being stored to database file.
* Tranfering configurations of the pipeline into database, not using yml.

**REFERENCE**

Here is Plugins/Files that I use for my code in Maya

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
