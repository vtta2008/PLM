"""
Created on Feb 12, 2014

@author: Jens Luebben

Module for generating a micro database file based on an ONIOM
calculation.
"""
KEY = 'micro'
OPTION_ARGUMENTS = {'load': None,
                    'cluster': 15}
HEADLINE = ' Using micro mode  '
BOTTOMLINE = ' Exiting micro mode'


def run(config):
    """
    Called by the plugin manager.
    Asks the plugin manager for user input and
    configures the database generator to generate
    the desired database file.
    """
    import lauescript.database as db
    from lauescript.types.data import GENERATOR
    from lauescript.laueio.inout import FlexLoad
    from lauescript.laueio.loader import Loader
    from lauescript.core.core import apd_exit

    printer = config.setup()
    dabapath = '.'
    match = 'geom'
    if config.arg('generate'):
        printer('Generating new micro database.')
        data = GENERATOR([], True)
        path = config.arg('load')
        db.generate_micro_database(data, config.get_frequency_cutoff(), path=path,
                                   printer=printer, clustersize=int(config.arg('cluster')),
                                   frequency_scale=config.get_config_valueFloat('Database', 'frequency_scale'))
        apd_exit(0)
    data = config.get_variable()
    printer('Loading data.')
    filename = config.arg('load')
    printer('Setting ADP transfer mode to pattern matching.\n')
    loader = Loader(printer)
    config.register_variable(loader, 'loader')
    if filename:
        if '.apd' in filename:
            printer('APD-Script file found. Executing script.')
            from lauescript.scripting import Parser

            parser = Parser(filename, indent=5)
            printer.enter()
            parser()
            printer.exit()
            exit()
        FlexLoad(data, loader, dabapath, config, filename)
    else:
        FlexLoad(data, loader, dabapath, config)
    printer('Loading successful.')

    data.update(match=match)