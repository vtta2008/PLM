"""
Created on 09.02.2014

@author: Jens Luebben

Plugin providing an interface to the database generator.
This plugin is usually called by the APD-Toolkit automatically
if necessary but can also be manually called to compile
database files for certain temperatures.
"""

KEY = 'D'
# OPTION_ARGUMENTS = 'T'
HEADLINE = '             APD-Toolkit Database Generator           '
BOTTOMLINE = '             Database generation completed            '


def run(configurator):
    """
    Called by the plugin manager. Accesses the 'data'
    instance returned by the plugin manager and generates
    a database file based on the attributs of 'data'
    """
    global printer, config
    config = configurator
    printer = config.setup()
    data = config.get_variable()
    generate(data)


def generate(data):
    """
    Sets up the database generator depending on the use input
    provided by the plugin manager.
    """
    import lauescript.database as db
    from lauescript.types.data import GENERATOR

    if config.arg('clean'):
        clean = True
    else:
        clean = False
    temperatures = []
    # ===========================================================================
    # for arg in mo['options']:
    #     try:
    #         temperatures.append(float(arg))
    #     except:
    #         pass
    #===========================================================================
    if not clean:
        db.generate_database(data,
                             config.get_frequency_cutoff(),
                             clean=False,
                             temperatures=temperatures,
                             path=config.config.DatabasePath,
                             root=config.get_config_value('Database', 'modelcompountrootdirectory'),
                             newh=config.get_config_value('APD', 'newH'))
        return

    if config.arg('save'):
        save = True
    else:
        save = False
    data = GENERATOR(temperatures, save)
    db.generate_database(data, config.get_frequency_cutoff(),
                         root=config.get_config_value('Database', 'modelcompountrootdirectory'),
                         frequency_scale=config.get_config_valueFloat('Database', 'frequency_scale'),
                         newh=config.get_config_value('APD', 'newH'))