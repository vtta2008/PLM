__author__ = 'jens'

try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle
from os.path import join
from lauescript.cryst.geom import get_framework_neighbors


def database(pluginManager, asDict=False, overridePath=None):
    if not overridePath:
        path = pluginManager.config.get('APD', 'DatabasePath')
    else:
        path = overridePath
    picklepointer = open(join(path, 'database.pkl'), 'rb')
    try:
        data = pickle.load(picklepointer, encoding='latin1')
    except TypeError:
        data = pickle.load(picklepointer)
    picklepointer.close()
    if not asDict:
        return data.values()
    else:
        return data


def atoms_of_element(molecule, element='H'):
    """
    Returns a list of all atoms of a given element.
    """
    try:
        return [atom for atom in molecule.atoms if atom.element == element]
    except AttributeError:
        return [atom for atom in molecule if atom.element == element]

def atoms_with_attribute(molecule, attribute, value=None):
    """
    Returns a list of all atoms that either have a certain attribute if
    'value' is None or all atoms where the attribute has the value 'value'
    """
    atoms = [atom for atom in molecule.atoms if hasattr(atom, attribute)]
    if not value:
        return atoms
    return [atom for atom in atoms if getattr(atom,attribute) == value]

def selected_atoms(molecule, function, value):
    """
    Returns a list of atoms selected by a selector function.
    Each atom is passed to the function and the return value is compared
    to 'value'. If return value and 'value' are equal, the atom is
    'selected'.
    """
    return[atom for atom in molecule.atoms if function(atom) == value]


def iter_atoms(molecule, sort=False):
    return molecule.iter_atoms(sort)


def iter_atom_pairs(molecule, bound=True, unique=True, sort=True):
    return molecule.iter_atom_pairs(bound, unique, sort=sort)


def iter_riding_hydrogen_atoms(atom):
    return atoms_of_element(get_framework_neighbors(atom=atom, useH=True))

