"""
Created on 08.02.2014

@author: Jens Luebben

This is a template for a plugin for the APD-Toolkit.

To be recognized as a plugin by the plugin manager
the module must implement the global 'KEY' variable.
The value of the variable defines how the plugin will
be addressed by the cmdline. In this case the module
will be executed if '-test' is given as a cmdline
argument.
The global variable OPTION_ARGUMENTS is optional.
It is a list containing all keywords that
represent options that need additional arguments.
In this case the first occurrence of 'load' after
'-test' will be considered an option with an
additional argument. The cmdline argument after
'load' will be assigned to the option 'load'.

A plugin must also implement a 'run()'function taking
one argument. The plugin manager passes itself when
calling the run() function. Before anything else
the run() function should call the 'config.setup()'
function which returns:
    - printer: An instance of the apd_printer class.
      The instance is created with the correct
      indentation level. The plugin manager also
      calls the 'enter(), headline(), bottomline()
      and exit()' methods.
"""
KEY = 'test'
OPTION_ARGUMENTS = {'load': 'test.test'}


def run(config):
    printer = config.setup()
    printer('\nThe sample_plugin has been successfully'
            ' started.\nNow I can do whatever I want.')

    printer('\nAsking config for value of option \'load\': {}'.format(config.arg('load')))
    printer('Asking config for value of option \'x\': {}'.format(config.arg('x')))
