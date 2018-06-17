__author__ = 'jens'

KEY = 'rigdat'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt'}  # Edit this to define cmd line options for
# the plugin and their default values.

from numpy import mean, std

from lauescript.cryst.crystgeom import Uiso
from lauescript.cryst.tables import atomicmass


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
    data = pluginManager.get_variable()
    loader = pluginManager.get_variable('loader')
    iop = loader.get_IOP()
    temp = iop.get_temperature()
    values = []
    for atom in data.iter_atoms():
        # if 'cart_ext' in atom.adp.keys():
            asum = Uiso(atom.adp['cart_sum'])
            aint = Uiso(atom.adp['cart_int'])
            if aint > 0. and asum > 0.:
                values.append(aint / asum * atomicmass[atom.element])
    printer.register_file('../rigdat.dat', keyword='rigdat', mode='a')
    printer('Average U_prop: {:4.2f} +- {:4.2f} at {} K'.format(mean(values), std(values), temp))
    printer('{} {:4.2f} {:4.2f}'.format(temp, mean(values), std(values)), use=['rigdat'])