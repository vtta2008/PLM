"""
Created on 19.06.2014

@author: Jens Luebben

Plugin for building complete molecules from the
asymmetric unit and the corresponding symmertry
operations.
"""
from lauescript.cryst.symmetry import SymmetryElement

KEY = 'expand'
# OPTION_ARGUMENTS=['load']

def run(config):
    printer = config.setup()
    loader = config.get_variable('loader')
    active_id = loader.get_active_id()
    if not active_id.startswith('shelx'):
        printer.highlight('Error: Wrong input file ID: {}.'.format(active_id))
        printer('Molecule expansion currently only works with \'Shelxl\' type files.')
        printer('Note: CIFs written by \'Shelxl\' will be supported very soon.')
        return
    symmetry_elements = loader.get_symmetry()
    lattice = float(loader.get_lattice())
    if lattice > 0:
        centric = True
    else:
        centric = False
    # centric = True
    data = config.get_variable()
    symms = []
    for symm in symmetry_elements:
        symm = SymmetryElement(symm, centric=False)
        symms.append(symm)
    if centric:
        symms.append(SymmetryElement(['-X', '-Y', '-Z']))
        for symm in symmetry_elements:
            symm = SymmetryElement(symm, centric=True)
            symms.append(symm)
    newatoms = []
    asymunits = {str(symm): [] for symm in symms}
    for atom in data.iter_atoms():
        for symm in symms:
            newatom = symm + atom
            newatom.normalize()
            newatoms.append(newatom)
            asymunits[str(symm)].append(newatom)
            # print '{} {:8.3} {:8.3} {:8.3} {:8.3} {:8.3} {:8.3} {:8.3} {:8.3} {:8.3}'.format(newatom.get_element(), newatom.get_cart()[0],
            #                                                                                  newatom.get_cart()[1],newatom.get_cart()[2],
            #                                                                                  *newatom.adp['cart_meas'])

    for atom in newatoms:
        data['exp'] += atom

    # for unit in asymunits.values():
    #     mol = MOLECULE('test')
    #     for atom in unit:
    #         mol.atoms.append(atom)
    #     print get_center_of_mass(mol, 'frac')

    # for symm in symms:
    #     print
    #     print symm







