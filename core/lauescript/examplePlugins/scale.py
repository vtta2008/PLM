"""
Created on Jun 1, 2013

@author: jens

Plugin for scaling Neutron diffraction derived ADPs to the
size of X-ray diffraction derived ADPs.
"""

import numpy as np

from lauescript.laueio.loader import Loader


KEY = 'S'
OPTION_ARGUMENTS = {'load': None,
                    'use': ['cart_meas', 'cart_neut']}


def build_ls_matrices(data):
    """
    Prepares the data for the least square optimization. The useH option
    can be set to True to force the usage of hydron atoms. This is not
    recommendet for the actual fit but for the application of the
    fitted Parameters to the atoms.

    :param data: Instance of the DATA class containing all necessary data.
    """
    loader = Loader(printer)
    filename = config.arg('load')
    if not filename:
        filename = 'neut.res'
    printer('Using file \'{}\' for target ADPs.\n'.format(filename))
    loader.create(filename)
    global mol
    mol = loader.load('neutron')
    printer('Scaling \'{}\' from \'exp\' model to\n\'cart_meas\' of target model.\n'.format(use[0]))



    y = []
    A = []
    for atom in data['exp'].atoms:
        if not atom.name[0] == 'H':
            name = atom.name.replace('(', '').replace(')', '')
            adpN = mol[name].adp['cart_meas']
            adpX = atom.adp[use[0]]

            A.append(np.array([adpX[0], 1, 0, 0, 0, 0, 0]))
            A.append(np.array([adpX[1], 0, 1, 0, 0, 0, 0]))
            A.append(np.array([adpX[2], 0, 0, 1, 0, 0, 0]))
            A.append(np.array([adpX[3], 0, 0, 0, 1, 0, 0]))
            A.append(np.array([adpX[4], 0, 0, 0, 0, 1, 0]))
            A.append(np.array([adpX[5], 0, 0, 0, 0, 0, 1]))

            for i in range(len(adpN)):
                y.append(adpN[i])

    A = np.array(A)
    return A, y


def fit_scale(data):
    """
    Carries out the Fit of the scale factor to scale the neutron data
    to the x-ray data.

    :param data: Instance of the DATA class containing all necessary data.
    """

    A, y = build_ls_matrices(data)

    v = np.linalg.lstsq(A, y)
    v = v[0]
    config.register_variable(v, 'scale2X')


def apply_scale(data):
    """
    Applies the fitted scaling paramters to the ADPs.

    :param data: Instance of the DATA class containing all necessary data.
    """
    scale = config.get_variable('scale2X')
    printer('  Scaling parameters:\n')
    printer('           |{1:6.3f} {4:6.3f} {5:6.3f} |\n *{0:6.3f} + |{4:6.3f} {2:6.3f} {6:6.3f} |\n'
            '           |{5:6.3f} {4:6.3f} {3:6.3f} |\n'.format(*scale))
    printer('Storing scaled ADPs in key \'{}\'.'.format(use[1]))
    for xatom in data['exp'].atoms:
        name = xatom.name.replace('(', '').replace(')', '')
        # atom = mol[name]
        try:
            adp = xatom.adp[use[0]]
        except KeyError:
            printer('Missing ADP for atom: {}'.format(xatom.get_name()))
            adp = [1, 1, 1, 0, 0, 0]
        adp[0] = adp[0] * scale[0] + scale[1]
        adp[1] = adp[1] * scale[0] + scale[2]
        adp[2] = adp[2] * scale[0] + scale[3]
        adp[3] = adp[3] * scale[0] + scale[4]
        adp[4] = adp[4] * scale[0] + scale[5]
        adp[5] = adp[5] * scale[0] + scale[6]
        xatom.adp[use[1]] = adp


def run(configurator):
    """
    Interface function for the main.py module.

    :param configurator: Instance of the plugin manager.
    """
    global printer, config, use
    config = configurator
    printer = config.setup()
    data = config.get_variable()
    use = config.arg('use')
    fit_scale(data)

    apply_scale(data)