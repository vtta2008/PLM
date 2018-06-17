"""
Created on Jul 24, 2014

@author: jens
"""

KEY = 'descent'
OPTION_ARGUMENTS = {'file': 'apd.descent'}


def run(config):
    printer = config.setup()
    filename = config.arg('file')
    file_pointer = open(filename, 'w')
    printer('Writing output to {}'.format(filename))
    for atom in config.get_variable().iter_atoms(sort=True):
        file_pointer.write('{}: {} from: {}\n'.format(atom.name,
                                                      atom.invariom_name,
                                                      atom.model_compound.name))
