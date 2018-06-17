"""
Module for generating an init script.
"""
__author__ = 'jens'

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
from os.path import expanduser, join
from sys import argv
import inspect
import os


def interactive():
    """
    Interactive script asking for user input.
    :return: string representing file path, boolean, boolean
    """
    data_path_def = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))[:-3] + 'data'
    data_path = raw_input('Path to data directory [{}]:\n\r'.format(data_path_def))
    if not data_path:
        data_path = data_path_def
    report = raw_input('Should occuring errors be reported automatically [True]:\n\r')
    if report is '' or report.lower() is 'true':
        report = True
    else:
        report = False
    files = bool(raw_input('Should input files be included in reports [False]:\n\r'))
    if files.lower() is 'true':
        files = True
    else:
        files = False
    return data_path, report, files


def run(outputName=None, data_path=None, plugin_path=None):
    """
    Generates a default INI file in the user's home directory
    :return: None
    """
    if not outputName:
        expanduser(join('~', '.apd.ini'))
    if not data_path:
        data_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))[:-3] + 'data'
    if not plugin_path:
        plugin_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))[:-3] + 'examplePlugins'
    report = 'false'
    files = 'false'
    if '-i' in argv:
        data_path, report, files = interactive()
    conf = ConfigParser()
    conf.add_section('APD')
    conf.add_section('Database')
    conf.add_section('Errors')
    conf.set('APD', 'DatabasePath', data_path)
    conf.set('APD', 'PluginPath', plugin_path)
    conf.set('APD', 'newH', 'true')
    conf.set('Errors', 'ReportErrors', report)
    conf.set('Errors', 'IncludeInput', files)
    conf.set('Errors', 'ServerAddress', '134.76.64.183')
    conf.set('Errors', 'Port', '7235')
    conf.set('Database', 'Frequency_cutoff', '200')
    conf.set('Database', 'ModelcompountRootdirectory', 'Not used')
    conf.set('Database', 'frequency_scale', '1')
    with open(expanduser(outputName), 'w') as fp:
        conf.write(fp)

if __name__ == '__main__':
    run()
