__author__ = 'jens'

import numpy as np
from numpy.linalg import LinAlgError
from lauescript.laueio.loader import Loader

KEY = 'compare'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'apd.res',
                    'use': ['cart_sum', 'cart_sum']}  # Edit this to define cmd line options for
NAME = 'Compare'
INFO = """Plugin for quantitativly comparing two sets of ADPs.
Example usage:
apd load <firstmodel.res> -compare load <secondmodel.res> use cart_meas:cart_meas
-> Compare the measured ADPs (Those read from the file) of 'firstmodel' and 'secondmodel'.
"""
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
    global printer
    printer = pluginManager.setup()
    data = pluginManager.get_variable()


    molecule2 = load(pluginManager)
    use = pluginManager.arg('use')
    printer('Comparing: ## {} vs. {} ##\n'.format(*use))

    method = ws06
    vals = []
    hlist = []
    nlist = []
    for atom in data.iter_atoms(sort=True):

        atom2 = molecule2[atom.get_name()]
        try:
            vals.append(method(atom.adp[use[0]], atom2.adp[use[1]]))
            #pass
        except LinAlgError:
            vals.append(999)
        size = sum(atom.adp[use[0]][:3]) - sum(atom2.adp[use[1]][:3])
        if size > 0:
            relSize = '+'
        elif size == 0:
            relSize = '='
        else:
            relSize = '-'
        relSizeComp = ''.join(['+' if (atom.adp[use[0]][i]-atom2.adp[use[1]][i]) > 0 else '-' for i in range(3)])
        printer('{:7s}{:10f}      {}({})'.format(atom.name, vals[-1], relSize, relSizeComp))
        if atom.element == 'H':
            hlist.append(vals[-1])
        else:
            nlist.append(vals[-1])

    printer('\nAverage difference:               {:5.3f}'.format(sum(vals) / len(vals)))
    printer('\nAverage heavy atom difference:    {:5.3f}'.format(sum(nlist) / len(nlist)))
    hav = sum(hlist) / len(hlist)
    std = np.std(hlist) * 3
    nh = []
    for h in hlist:
        if not h - hav > std:
            nh.append(h)
    nhav = sum(nh) / len(nh)
    printer('Average hydrogen atom difference: {:5.3f}'.format(hav))
    printer('Average difference ( < 3 sigma ): {:5.3f}'.format(nhav))


def ws06(adp1, adp2):
    """
    Compare method as introduced by Whitten & Spackman 2006

    The function calculates the overlap 'R' of two ADP's ellipsoid
    representations. The functions returns the similarity index 'S'
    which is given by 'S=100(1-R)'.
    :param adp1: List/Array type of length 6.
    :param adp2: List/Array type of length 6.
    :returns: Float representing similarity of adp1 and adp2.
    """
    adp1 = get_matrix(adp1)
    adp2 = get_matrix(adp2)
    adp1i = np.linalg.inv(adp1)
    adp2i = np.linalg.inv(adp2)
    a = 2 ** 1.5
    b = np.dot(adp1i, adp2i)
    c = np.linalg.det(b)
    d = c ** 0.25
    up = a * d

    x = adp1i + adp2i
    y = np.linalg.det(x)
    z = y ** 0.5
    R = up / z
    return 100 * (1 - R)

def get_matrix(adp):
    """
    Transforms an ADP to its matrix representation.
    :param adp: List/Array type of length 6.
    :return: 3x3 np.matrix
    """
    adp = np.matrix([[float(adp[0]), float(adp[3]), float(adp[4])],
                    [float(adp[3]), float(adp[1]), float(adp[5])],
                    [float(adp[4]), float(adp[5]), float(adp[2])]])
    return adp

def load(pluginManager):
    loader = Loader(pluginManager.get_active_printer())
    filename = pluginManager.arg('load')
    loader.create(filename)
    mol = loader.load('compare')
    printer('Using file {} for comparison.'.format(filename))
    return mol