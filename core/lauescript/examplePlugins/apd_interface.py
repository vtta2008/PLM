"""
Created on Feb 12, 2014

@author: Jens Luebben

Plugin providing an interface to call the APD-Toolkit's
main functions.

When calling the 'apd' executable, the plugin manager
will get configured to call this plugin automatically.
"""

KEY = 'apd'
OPTION_ARGUMENTS = {'load': None}
HEADLINE = 'Loading Files and Transfering ADPs'


def run(config):
    """
    Asks the plugin manager for user input and executes
    the APD-Toolkit's main functions.
    """
    from lauescript.laueio.inout import FlexLoad
    from lauescript.laueio.loader import Loader

    printer = config.setup()
    data = config.get_variable()
    loader = Loader(printer)
    config.register_variable(loader, 'loader')
    data.register_config(config)
    dabapath = config.get_databasepath()

    filename = config.arg('load')
    if filename:
        if filename.endswith('.apd'):
            printer('APD-Script file found. Executing script.')
            from lauescript.core.scripting import Parser

            parser = Parser(filename, indent=5, config=config)
            printer.enter()
            parser()
            printer.exit()
            exit()
        FlexLoad(data, loader, dabapath, config, filename)
    else:
        FlexLoad(data, loader, dabapath, config)
    printer('Loading successful.')
    data.update()