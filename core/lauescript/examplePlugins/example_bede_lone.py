__author__ = 'jens'

from lauescript.laueio.loader import Loader
from lauescript.laueio.inout import FlexLoad
from lauescript.types.data import DATA

KEY = 'bede'
OPTION_ARGUMENTS = {'load': 'myFile.txt'}


def run(pluginManager):
    """
    Entry point for the plugin manager
    :param pluginManager: plugin manager instance
    :return: None
    """
    printer = pluginManager.setup()
    loader = Loader(printer)
    data = DATA()
    dabapath = pluginManager.get_databasepath()
    FlexLoad(data, loader, dabapath, pluginManager, pluginManager.arg('load'))
    shelxliop = loader.get_IOP()

    atomsWithInvariomName = {}
    for atom in data['exp'].atoms:
        try:
            atomsWithInvariomName[atom.get_active_invariom()].append(atom.name)
        except KeyError:
            atomsWithInvariomName[atom.get_active_invariom()] = [atom.name]

    for invariomName, atomNames in atomsWithInvariomName.items():
        printer()
        printer(invariomName)
        for atomName in atomNames:
            printer('  {}'.format(atomName))
            for bede in shelxliop.atoms[atomName].getBedeInstructions():
                printer('      {}'.format(str(bede)))

