__author__ = 'jens'

from numpy import mean

from lauescript.cryst.iterators import database, atoms_of_element


KEY = 'dbiter'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt'}  # Edit this to define cmd line options for
# the plugin and their default values.


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
    printer('Reading database file...')
    for molecule in database(pluginManager):
        h_atoms = atoms_of_element(molecule, 'H')
        if not len(h_atoms) == 0:
            average_bond_length = mean([atom - atom.partner[0] for atom in h_atoms])
        else:
            average_bond_length = 0

        printer('\nName: {}\nInvariom Priority: {}'
                '\nNumber of H atoms: {}'
                '\nAverage H-bond length: {:5.3f}'.format(molecule, molecule.criterion.replace('  ', ''),
                                                          len(h_atoms), average_bond_length))
