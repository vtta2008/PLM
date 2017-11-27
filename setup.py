# coding=utf-8

"""



"""

from distutils.core import setup

setup(
    name='PipelineTool',
    version='13',
    packages=['', 'tk', 'ui', 'sql_tk', 'Mari_tk', 'Maya_tk', 'Maya_tk.modules', 'Maya_tk.modules.Modeling',
              'Maya_tk.modules.Sufacing', 'Maya_tk.plugins', 'Maya_tk.userLibrary',
              'Maya_tk.userLibrary.controllerLibrary', 'Nuke_tk', 'ZBrush_tk', 'Houdini_tk'],
    url='https://github.com/vtta2008/PipelineTool',
    license='internal share',
    author='Trinh Do (aka. Jimmy)',
    author_email='dot@damgteam.com',
    description='soft package manager in custom pipeline'
)
