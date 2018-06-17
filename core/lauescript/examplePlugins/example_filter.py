__author__ = 'jens'

import lauescript.cryst.filter as filter
from lauescript.cryst.filter import filter_atom, filter_atom_pair
from lauescript.core.core import *
from lauescript.cryst.iterators import iter_atoms, iter_atom_pairs

KEY = 'filter'
OPTION_ARGUMENTS = {'load': 'myFile.txt',
                    'atomfilter': False,
                    'secondfilter': False,
                    'customfilter': False}


def run(pluginManager):
    """
    Entry point for the plugin manager
    :param pluginManager: plugin manager instance
    :return: None
    """
    printer = pluginManager.setup()
    molecule = quickLoad(pluginManager, pluginManager.arg('load'))
    printer('Filtering Atoms:')
    for atom in iter_atoms(molecule):
        if filter_atom(pluginManager, atom, 'atomfilter'):
            printer(atom)
    printer.spacer()
    printer('\nFiltering Atom Pairs:')
    for atom1, atom2 in iter_atom_pairs(molecule, bound=False, unique=False):
        if filter_atom_pair(pluginManager, atom1, atom2, 'atomfilter', 'secondfilter'):
            printer('{} {}'.format(atom1.get_name(), atom2.get_name()))

    printer.spacer()
    printer('\nUsing Custom Filter Function:')
    filter.register_custom_fuction('firstOf', firstOfElement)
    for atom in iter_atoms(molecule):
        if filter_atom(pluginManager, atom, 'customfilter'):
            printer(atom)


def firstOfElement(atomName):
    if atomName[-1] == '1' and atomName[-2] not in '1234567890':
            return True
    return False