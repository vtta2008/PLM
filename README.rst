PIPELINE MANAGER (PLM)
######################

.. sidebar:: DAMGTEAM PROFILE
    :subtitle: PLM

    :Name: Pipeline Manager
    :Built: `Python 3 <https://www.python.org/>`_, PyQt5/PySide2 (optional)
    :Authors: `Trinh Do <www.dot.damgteam.com>`_, `Duong Minh Duc <www.up.damgteam.com>`_
    :Version: 13.0.0 Beta
    :Platforms: Windows (planned for cross-platform)


.. sidebar:: DAMGTEAM PROFILE
    :subtitle: VanilaServer (test server)

    :Name: VanilaServer
    :Built: NodeJs
    :Authors: `Trinh Do <www.dot.damgteam.com>`_, `Duong Minh Duc <www.up.damgteam.com>`_
    :Version: NA
    :Platforms: cross-platform


INTRODUCTION
------------

.. Topic:: About PLM

    This application aimed to build, manage, and optimise vfx pipelines using Python 3 and PyQt5/PySide2. The current
    version is compatible with Windows 10. The idea is managing and setup a workplace for everyone and handling
    communication between all department throughout PLM.

.. note::

    Due to VFX Reference Platform and the large invention, we need to stay with python 2.7 but expect to migrate to
    python 3 in 2019 (Delayed to 2020). See `details <http://www.vfxplatform.com>`_

.. warning::

    - Some of stuff is planned but not built yet, please do not expected much.

    - Things could be changed along development process.

.. topic:: Prerequisite

    - `Python 3.7 <https://www.python.org/>`_ or `Anaconda Python 3.7 <https://www.anaconda.com/products/individual>`_


.. topic:: App Bundle


    .. list-table::
        :widths: 100 100 10 50 50 100
        :header-rows: 1

        * - Name
          - Version
          - Recommend
          - Config
          - Plugin(s)
          - Note

        * - `Python <https://www.python.org>`_
          - 3.7
          - `Anaconda <https://www.anaconda.com/products/individual>`_
          - Yes
          -
          - conda config

        * - `Autodesk Maya <https://www.autodesk.com/education/free-software/maya>`_
          - 2017+
          - 2017, 2019
          - Yes
          - `Vray <https://www.chaosgroup.com/vray/maya>`_, `VMM <https://www.mediafire.com/#gu9s1tbb2u4g9>`_
          -

        * - `Houdini FX <https://www.sidefx.com/download/>`_
          - 16.5.496, 17.5.425
          -
          - Yes
          -
          -

        * - `Mari <https://www.foundry.com/products/mari>`_
          - 4.0v1, 4.1v1, 4.6v1
          -
          - Yes
          -
          -

        * - `Substance Painter <https://www.substance3d.com/products/substance-painter/>`_
          -
          -
          - Yes
          -
          -

        * - `NukeX <https://www.foundry.com/products/nuke>`_
          - 11.1v1, 11.2v1, 12.0v1
          -
          - Yes
          -
          -

        * - `Hiero <https://www.foundry.com/products/hiero>`_
          - 11.1v1, 11.2v1, 12.0v1
          -
          - Yes
          -
          -

        * - `ZBrush <https://pixologic.com/zbrush/downloadcenter/>`_
          - 4R7, 4R8, 2020
          -
          - Yes
          -
          -

        * - `Davinci Resolve <https://www.blackmagicdesign.com/nz/products/davinciresolve/>`_
          -
          -
          - Yes
          -
          - Disabled

        * - `Photoshop <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
          - CC 2018, CC 2019
          -
          - Yes
          -
          - Overpriced

        * - `Illustrator <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
          - CC 2018, CC 2019
          -
          - Yes
          -
          - Overpriced

        * - `Premiere Pro <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
          - CC 2018, CC 2019
          -
          - Yes
          -
          -

        * - `After Effects <https://www.adobe.com/creativecloud/catalog/desktop.html>`_
          - CC 2018, CC 2019
          -
          - Yes
          -
          - Overpriced

        * - `Krita <https://krita.org/en/>`_
          -
          -
          - Yes
          -
          - Free

        * - `Storyboarder <https://wonderunit.com/storyboarder/>`_
          -
          -
          - Yes
          -
          - Free

.. note::

    - For VMM for maya, remember to configure the path once it is opened in Maya. (sadly, the author has stopped
      developing the plugin.

.. topic:: Screenshot

    update later
