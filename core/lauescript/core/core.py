__author__ = 'Arrahed'
"""
Module for core functions.
"""

#from apd.main import get_plugin_manager
from lauescript.core.pluginmanager import get_plugin_manager
from traceback import format_exc
import socket

from lauescript.core.pluginmanager import get_plugin_manager
import lauescript.core.error as error


def apd_exit(value=1, message=None, verbose=True):
    """
    Function for terminating the APD-Toolkit.
    :param value: Integer specifying the value that is returned to the program caller. Defaults to '1'
    :param message: String that is printed before termination. Defaults to a standard message if 'value' is not
    '0'.
    :param verbose: Boolean controlling whether the message is printed. Defaults to True.
    :return: None
    """
    import lauescript.laueio.loader as loader
    config = get_plugin_manager()
    printer = config.get_active_printer()
    printer.unmute()
    if not message:
        if value:
            message = ['The application terminated unexpectedly.',
                       '\n\n{}'.format(format_exc())]
        else:
            message = ['']

    dosend = config.config.getboolean('Errors', 'reporterrors')
    plusfiles = config.config.getboolean('Errors', 'includeinput')
    files = ''
    if plusfiles:
        filenames = loader.Loader.get_read_files()
        for filename in filenames:
            fp = open(filename, 'r')
            files += fp.read()
            fp.close()
        files = files.replace('\'', '###').replace('\"', '####')

    if dosend and value:
        report = error.createReport(format_exc(), fileContent=files)
        try:
            error.sendReport(report, config)
            try:
                message = ['An error report was send to the developer.'] + message
            except TypeError:
                message = ['An error report was send to the developer.'] + [message]
        except socket.error:
            try:
                message = ['Sending an error report to the developer failed.'] + message
            except TypeError:
                message = ['Sending an error report to the developer failed.'] + [message]

    if verbose:
        if not type(message) == list:
            message = [message]
        printer(*message)
    config.exit(value)


def quickLoad(pluginManager, filename=None):
    """
    Utility function for quickly creating a molecule object from a
    data file provided. The loading procedure is carried out with
    default values and returns a 'Molecule' instance with the name
    'quickloadedMolecule'.
    :param pluginManager: Reference to an PluginManager Instance.
    :param filename: String representing the filename that is supposed
    to be used.
    :return: Instance of an 'Molecule' object.
    """
    from lauescript.laueio.loader import Loader
    loader = Loader(pluginManager.get_active_printer())
    loader.create(filename)
    mol = loader.load('quickloadedMolecule')
    return mol

def storeData(data, filename='laue.dat'):
    """
    Utility function for serializing data.
    :param data: Reference to the object to be stored.
    :param filename: String representing the filename that will be used.
    Defaults to 'laue.dat'.
    :return: None
    """
    import cPickle
    with open(filename, 'wb') as fp:
        cPickle.dump(data, fp)

def restoreData(filename='laue.dat'):
    """
    Utility function for restoring a previously serialized data state.
    :param filename: String representing the the filename of the stored data.
    Defaults to 'laue.dat'.
    :return: Reference to the restored object.
    """
    import cPickle
    with open(filename, 'rb') as fp:
        return cPickle.load(fp)





