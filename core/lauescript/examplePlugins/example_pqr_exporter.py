__author__ = 'jens'

from lauescript.laueio.pdb_iop import PDBIOP

KEY = '2pqr'
OPTION_ARGUMENTS = {'write': 'apd.pqr'}


def run(configx):
    """
    Entry point for the plugin manager
    :param configx: plugin manager instance
    :return: None
    """
    global config, data
    config = configx
    printer = config.setup()
    pdbiop = PDBIOP('test.test')
    pdbiop.setup(new=True)
    data = config.get_variable()
    pdbiop.set(['cart', 'serial_numbers', 'name_prefixes', 'occupancies',
                'adp_cart', 'residue_numbers', 'vdw_radii', 'point_charges'],
               provide, new=True)
    printer(pdbiop.export('PQR'))
    with open(config.arg('write'), 'w') as fp:
        fp.write(pdbiop.export('PQR'))
    printer('\nPQR formatted output written to {}.'.format(config.arg('write')))




def provide():
    """
    Iterator iterating over all atoms yielding the attributes specified above.
    :return:
    """
    for i, atom in enumerate(data.iter_atoms()):
        yield [atom.get_name(), atom.get_cart(), i, atom.get_element(), 1, atom.adp['cart_meas'], 1, None, 1]
