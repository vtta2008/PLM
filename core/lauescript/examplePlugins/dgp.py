__author__ = 'jens'

KEY = 'GG'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt'}  # Edit this to define cmd line options for
# the plugin and their default values.

import imp

def run(pluginManager):
    """
    This is the entry point for the plugin manager.
    The plugin manager will pass a reference to itself
    to the function.
    Use the APD_Printer instance returned by
    pluginManager.setup() instead of the 'print'
    statement to generate autoformated cmd line output.
    :param pluginManager: Reference to the plugin manager
    instance.
    """
    printer = pluginManager.setup()

    # Clear sys.argv to avoid interference with the gui library.
    pluginManager.clearSystemArgs()

    plugin = imp.load_source('main', pluginManager.get_plugin_path() + '/demoguiplugin/main.py')
    plugin.run(pluginManager)
