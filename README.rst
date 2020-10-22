PIPELINE MANAGER (PLM)
######################

.. sidebar:: APPLICATION
    :subtitle: PIPELINE MANAGER (PLM)

    :Name: Pipeline Manager
    :Built: `Python 3 <https://www.python.org/>`_, PySide2
    :Authors: `Trinh Do <www.dot.damgteam.com>`_, `Duong Minh Duc <www.up.damgteam.com>`_
    :Version: 13.0.0 Beta
    :Platforms: Windows (planned for cross-platform)


.. sidebar:: SERVER
    :subtitle: VanilaServer (local server)

    :Name: `VanilaServer <https://github.com/vtta2008/VanilaServer>`_
    :Built: NodeJs
    :Authors: `Trinh Do <www.dot.damgteam.com>`_, `Duong Minh Duc <www.up.damgteam.com>`_
    :Version: NA
    :Platforms: cross-platform


INTRODUCTION
------------

.. Topic:: Pipeline Manager (PLM) v13.0.0

    This application aimed to build, manage, and optimise vfx pipelines using Python 3 and PyQt5/PySide2. The current
    version is compatible with Windows 10. The idea is managing and setup a workplace for everyone and handling
    communication between all department throughout PLM. The main intension of this project is to create a online pipline
    which is suitable for a group working online together.

.. Topic:: Intension Features

    - Pipeline designer
    - Auto config software bundle by.
    - Flexible user configurations.
    - Optional use PyQt5 or PySide2 for layout.
    - Flexible implimentation.
    - Realtime monitoring PC performance.
    - Tools for planning, scheduling, tasking and supervising with reminder.

.. note::

    Due to VFX Reference Platform and the large invention, we need to stay with python 2.7 but expect to migrate to
    python 3 in 2019 (Delayed to 2020). See `details <http://www.vfxplatform.com>`_

    - Hips of work to do.

    - Lots of functions were designed but not planned, please do not expected much.

    - Things could be changed along development process.


PREREQUISITE
------------

    PLM is mainly built by Python 3

    - `Python 3.7+ <https://www.python.org/>`_ or `Anaconda Python 3.7+ <https://www.anaconda.com/products/individual>`_

    - Python package requirement

        #. General
            * PyQtWebEngine>=5.14.0
            * Pyside2>=5.14.1
            * Shiboken2>=5.14.1
            * cx_Freeze>=6.1
            * pytest==5.3.2
            * pytest-cov==2.8.1
            * msgpack>=0.6.2
            * pip>=19.3.1
            * winshell>=0.6.0
            * helpdev>=0.6.10
            * deprecate>=1.0.5
            * argparse>=1.4.0
            * green>=3.1.0
            * GPUtil>=1.4.0
            * playsound>=1.2.2
            * python-resize-image>=1.1.19
            * sphinx == 3.0.2
            * sphinx_rtd_theme == 0.4.3
            * reportlab == 3.5.42
            * zopfli==0.1.6
            * fs==2.4.11


        #. Windows

            * WMI>=1.4.9

PIPELINE SOFTWARE BUNDLE
------------------------

.. list-table::
    :widths: 100 100 100 100 100
    :header-rows: 1

    * - Name
      - Version
      - Recommend
      - Plugin(s)
      - Note

    * - `Python <https://www.python.org>`_
      - 3.7
      - `Anaconda <https://www.anaconda.com/products/individual>`_
      -
      - conda config

    * - `Autodesk Maya <https://www.autodesk.com/education/free-software/maya>`_
      - 2017+
      - 2017, 2019
      - `Vray <https://www.chaosgroup.com/vray/maya>`_, `VMM <https://www.mediafire.com/#gu9s1tbb2u4g9>`_
      -

    * - `Houdini FX <https://www.sidefx.com/download/>`_
      - 16.5.496, 17.5.425
      -
      -
      -

    * - `Mari <https://www.foundry.com/products/mari>`_
      - 4.0v1, 4.1v1, 4.6v1
      -
      -
      -

    * - `Substance Painter <https://www.substance3d.com/products/substance-painter/>`_
      - All
      -
      -
      -

    * - `NukeX <https://www.foundry.com/products/nuke>`_
      - 11.1v1, 11.2v1, 12.0v1
      -
      -
      -

    * - `Hiero <https://www.foundry.com/products/hiero>`_
      - 11.1v1, 11.2v1, 12.0v1
      -
      -
      -

    * - `Katana <https://www.foundry.com/products/katana>`_
      - 2.6v3, 3.5v2
      -
      -
      -

    * - `ZBrush <https://pixologic.com/zbrush/downloadcenter/>`_
      - 4R7, 4R8, 2020
      -
      -
      -

    * - `Davinci Resolve <https://www.blackmagicdesign.com/nz/products/davinciresolve/>`_
      - 14
      -
      -
      - Disabled

    * - `Photoshop <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
      - CC 2018, CC 2019
      -
      -
      - Overpriced

    * - `Illustrator <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
      - CC 2018, CC 2019
      -
      -
      - Overpriced

    * - `Premiere Pro <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
      - CC 2018, CC 2019
      -
      -
      -

    * - `After Effects <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
      - CC 2018, CC 2019
      -
      -
      - Overpriced

    * - `Krita <https://krita.org/en/>`_
      -
      -
      -
      - 64bit only

    * - `Storyboarder <https://wonderunit.com/storyboarder/>`_
      -
      -
      -
      -

.. note::

    - For VMM for maya, remember to configure the path once it is opened in Maya. (sadly, the author has stopped
      developing the plugin.

.. topic:: Screenshot

    .. image:: https://github.com/vtta2008/PLM/blob/master/bin/screenshots/layout.PNG
