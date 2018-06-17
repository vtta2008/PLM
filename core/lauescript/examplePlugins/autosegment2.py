"""
Created on Okt 1, 2014

@author: Jens Luebben

Plugin for automatically segementing a rigid molecule
body into attached rigid groups.
"""

KEY = 'A'
OPTIONS = ['noforce']
NAME = 'Auto'

import numpy as np

import lauescript.cryst.crystgeom as cg
from lauescript.cryst.geom import get_framework_neighbors

MIMIMUM_SIZE = 4
MIMIMUM_SIZE = 5
MIMIMUM_SIZE = 8


def autosegment():
    """
    Checks the availability of the required data and calls the
    hirshfeld test module if necessary.
    Subsequently the autosegmentation functions are called.
    """

    printer('\nStarting the automatic segmentation procedure.')

    try:
        matrix = data['exp'].hirshfeld_matrix
        hirshfeld_list = data['exp'].hirshfeld_list
    except:
        printer('\nNo hirshfeld test data found. Calling hirshfeld'
                ' test module.')
        options = {'full': True}
        config.call('H', options)
        matrix = data['exp'].hirshfeld_matrix
        hirshfeld_list = data['exp'].hirshfeld_list
    set_threshold(hirshfeld_list, matrix)

    groups = get_potential_axis(matrix)
    # ===========================================================================
    # groups+=segment_chemical_molecules()
    #===========================================================================
    start_fit(groups)


def set_threshold(hirshfeld_list, matrix):
    """
    Determines appropriate thresholds for the rigidity evaluation based
    on the results of the hirshfeld test.

    This function is a dummy right now.
    """
    # ===============================================================================
    #     printer=cg.apd_printer(indent)
    #     rigid_values=[i[2]*10000 for i in hirshfeld_list if not any('H' in j for j in i[:2])]
    #     ref_values=list(rigid_values)
    #     rigid_values.remove(max(rigid_values))
    #     rigid_values.remove(min(rigid_values))
    #     rigid_mean=np.mean(rigid_values)
    #     rigid_std=np.std(rigid_values)
    #     for v in rigid_values:
    #         if abs(v-rigid_mean)>2*rigid_std:
    #             rigid_values.remove(v)
    #     rigid_mean=np.mean(rigid_values)
    #     rigid_std=np.std(rigid_values)
    #     #===========================================================================
    #     # printer(rigid_mean)
    #     # printer( rigid_std)
    #     #===========================================================================
    #
    #     #===========================================================================
    #     # for line in matrix:
    #     #     printer( line)
    #     #===========================================================================
    #
    #     norid_values=[j[i] for j in matrix for i in range(len(matrix[0])) if  j[i] > 1]
    #     norid_values.remove(max(norid_values))
    #     norid_values.remove(min(norid_values))
    #
    #     #===========================================================================
    #     # printer(norid_values)
    #     #===========================================================================
    #     norid_mean=np.mean(norid_values)
    #     norid_std=np.std(norid_values)
    #===============================================================================
    #===============================================================================
    #     printer()
    #     printer( norid_mean)
    #     printer( norid_std)
    #     printer('hello\nworld')
    #     printer('I am a test number {}.\nI hope I get printed correctly.'.format(norid_std))
    #
    #     printer( (rigid_mean**2-norid_mean)*-1)
    #===============================================================================


    global RIGIDITY_THRESHOLD
    RIGIDITY_THRESHOLD = 0


def start_fit(groups):
    """
    Prepares the accepted groups for the fitting procedure and
    calls the tls fit module with the appropriate options.
    """
    printer('\nAutomatic segmentation completed successfully.\n\n\n'
            'Starting TLS-Fitting procedure.\n')
    global tls_definitions
    tls_definitions = []
    for group in groups:
        axis = group[0].cart - group[1].cart
        axis /= np.linalg.norm(axis)
        tls_definitions.append((axis, group[0], group[1]))

    for i, mol in enumerate(data['exp'].get_all_chem_molecules()):
        global current_molecule
        current_molecule = mol

        if len([a for a in mol if not a.get_element() == 'H']) > 4:
            rigid = True
            for definition in tls_definitions:
                if any([atom in mol for atom in definition[1:]]):
                    rigid = False
                    options = {'auto': True, 'molecule': '{}'.format(i + 1)}
                    config.call('T2', options)
                    break
            if rigid:
                options = {'molecule': '{}'.format(i + 1)}
                config.call('T2', options)

        else:
            for atom in mol:
                atom.adp['cart_sum'] = atom.adp['cart_meas']


# ===============================================================================
#         if len(tls_definitions)>0:
#             #=======================================================================
#             # print tls_definitions
#             # options={'options':['auto'],'molecule':['0']}
#             # config.call('T2',options)
#             #=======================================================================
#
#             for i,mol in enumerate(data['exp'].get_all_chem_molecules()):
#                 if len([a for a in mol if not a.get_element()=='H'])> 4:
#                     options={'options':['auto'],'molecule':['{}'.format(i+1)]}
#                     config.call('T2',options)
#                 else:
#                     for atom in mol:
#                         atom.adp['cart_sum']=atom.adp['cart_meas']
#
#         else:
#             for i,mol in enumerate(data['exp'].get_all_chem_molecules()):
#                 if len([a for a in mol if not a.get_element()=='H'])> 4:
#                     options={'options':[],'molecule':['{}'.format(i+1)]}
#                     config.call('T2',options)
#                 else:
#                     for atom in mol:
#                         atom.adp['cart_sum']=atom.adp['cart_meas']
#===============================================================================


def get_tls_definition_auto():
    """
    Interface function for the TLS-Fitting module.
    """
    return [definition for definition in tls_definitions if any(atom in current_molecule for atom in definition[1:])]


def get_potential_axis(matrix):
    """
    Determines potential rotation axis within the molecule.
    """
    namelist = []
    axislist = []
    for atom in data['exp'].atoms:
        atomtypes = parse_inv_name(atom.invariom_name)
        frame_atoms = get_framework_neighbours(atom)
        if len(atomtypes) > 1:
            for atom2 in frame_atoms:
                if atom2.name[0] in atomtypes and cg.get_atom_with_longest_bond(atom2.name[0], atom):
                    pair = [atom.name, atom2.name]
                    pair = sorted(pair)
                    if not pair in namelist:
                        axislist.append((atom, atom2))
                        namelist.append(pair)
    printer('\n{} potential rotation axis found:'.format(len(namelist)))
    for pair in namelist:
        printer('AXIS: {0:5>s}---{1:4<s}'.format(pair[0], pair[1]))
    printer('\nGenerate associated rigid groups.')

    return generate_rigid_groups(axislist, matrix)


def generate_rigid_groups(axislist, matrix):
    """
    Generates rigid groups from the list of rotation axis and checks
    every group's suitability for an attached rigid group
    """
    rigid_groups = []
    for axis in axislist:
        rigid_groups.append(cg.framework_crawler(axis[0], axis[1]))
    vals = []
    printer('\nChecking potential groups\' rigidity.')
    for group in rigid_groups:
        printer()
        vals.append(check_rigidity(group, matrix))
    accepted_groups = []
    printer('\n')
    for _ in range(len(vals)):
        bestgroup = min(vals)
        if bestgroup > RIGIDITY_THRESHOLD:
            if len(accepted_groups) == 0:
                printer('No suitable rigid groups detected.')
            break
        i = vals.index(bestgroup)
        potential_group = rigid_groups[i]
        print
        if too_close(potential_group, accepted_groups):
            printer('\nKill too similar group:', [k.name for k in potential_group])
            vals[i] = 999
            continue
        accepted_groups.append(potential_group)
        printer('Accepted rigid group:', [k.name for k in potential_group])
        vals[i] = 999

    return accepted_groups


def too_close(group, groups, threshold=3):
    """
    Checks whether an additional group would imply a new group that is
    too small to be considered.
    """
    counter = 0
    supergroup = list(group)
    for group2 in groups:
        for atom in group:
            if atom in group2:
                counter += 1
        if len(group) - counter < threshold:
            return True
        supergroup += group2
    counter = 0
    for atom in data['exp'].atoms:
        if not atom in supergroup and not atom.element == 'H':
            counter += 1
    if counter <= threshold:  # and len(groups)>0:
        return True

    return False


def check_rigidity(group, matrix):
    """
    Checks whether a generated group can be considered rigid
    in comparison with the rest of the molecule. Also, groups
    too small for TLS-Analysis are deleted.
    """
    if len(group) < MIMIMUM_SIZE:
        printer('\nKill too small group: ', [i.name for i in group])
        return 999
    if len(data['exp'].atoms) - len(group) < MIMIMUM_SIZE:
        printer('\nKill too small group: ', [i.name for i in group])
        return 999

    rigidcounter = 0
    rigidsum = 0
    nonrigidcounter = 0
    nonrigidsum = 0
    #===========================================================================
    # print matrix
    # exit()
    #===========================================================================
    for atom in group:
        i = data['exp'].atoms.index(atom)
        deltaline = matrix[i]
        for atom2 in group:
            if not atom == atom2:
                #===============================================================
                # print
                # print atom,atom2
                # print deltaline
                #===============================================================
                j = data['exp'].atoms.index(atom2)
                delta = deltaline[j]
                #===============================================================
                # print delta
                #===============================================================
                rigidsum += delta
                rigidcounter += 1
    #===========================================================================
    # exit()
    #===========================================================================
    for atom2 in data['exp'].atoms:
        if not atom2 in group:
            j = data['exp'].atoms.index(atom2)
            delta = deltaline[j]
            try:
                nonrigidsum += delta
                nonrigidcounter += 1
            except:
                #===========================================================
                # Ignore values of non anisotropic ADP.
                #===========================================================
                pass

    rigidval = rigidsum / rigidcounter
    nonrigidval = nonrigidsum / nonrigidcounter
    val = rigidval * 2 - nonrigidval
    printer('\nChecking group:', [i.name for i in group])
    printer('Average Delta z^2 for atoms within the rigid group: {}'.format(rigidval))
    printer('Average Delta z^2 for atoms not within the rigid group: {}'.format(nonrigidval))
    printer('Rigidity index: {}'.format(val * -1))
    if val > RIGIDITY_THRESHOLD:
        printer('Rigidity index too small.\nKill group:', [i.name for i in group])
    return val


def parse_inv_name(invname):
    """
    Analyses the invariom string to find single bonds in
    the molecule
    """
    try:
        _ = int(invname[0])
        return []
    except:
        if 'H' == invname[0]:
            return []
        switch = False
        bswitch = True
        atomlist = []
        planeswitch = False
        if '=' == invname[0]:
            planeswitch = True
        for char in invname:
            if '[' == char:
                bswitch = False
            if ']' == char:
                bswitch = True
            if bswitch:
                if switch and '.' == char:
                    switch = False
                if switch:
                    try:
                        _ = int(char)
                        continue
                    except:
                        if not 'h' == char:
                            atomlist.append(char.swapcase())
                        switch = False
                if '1' == char or ('@' == char and not planeswitch):
                    switch = True
        return atomlist


def segment_chemical_molecules():
    groups = []
    i = -1
    if not noforce:
        printer('\nBuilding rigid groups for isolated molecules in the\nasymmetric unit.')
        for i, chem_mol in enumerate(data['exp'].get_all_chem_molecules()[:-1]):
            groups.append(chem_mol)
        printer('\n{} rigid group added.'.format(i + 1))
    return groups


def run(configurator, **kwargs):
    """
    Call me!!! Call me!!!

    Interface function for the APD-Toolkit's plugin manager.
    """
    global printer, config, noforce
    config = configurator
    noforce = config.arg('noforce')
    printer = configurator.setup()
    global data
    data = configurator.get_variable()
    autosegment()
    return 0

