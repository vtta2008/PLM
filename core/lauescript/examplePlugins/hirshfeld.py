"""
Created on Jun 1, 2014

@author: Jens Luebben

Plugin implementing the Hirshfeld test testing the
rigidity of a structure model.
"""
KEY = 'H'
OPTION_ARGUMENTS = {'compound': 'exp'}

import numpy as np



def get_adp_as_matrix(adp):
    if adp is None:
        return None
    return np.matrix([[adp[0], adp[3], adp[4]],
                      [adp[3], adp[1], adp[5]],
                      [adp[4], adp[5], adp[2]]])


#===============================================================================
# def get_aligned_axis(adp1,adp2):
#     bestcheck=0
#     besti=None
#     eigval1,eigvec1=np.linalg.eig(adp1)
#     eigval2,eigvec2=np.linalg.eig(adp2)
#     for i in range(3):
#         for j in range(3):
#             check=np.dot(eigvec1[:,i],eigvec2[:,j])
#             if check < 0: check=check *-1
#             if check > bestcheck: besti=(i,j)
#     return eigvec[:,besti1[0]],eigvec2[:,besti[1]],bestcheck
#===============================================================================


def get_difference(atom1, atom2, use):
    """
    Returns the difference of two sets of ADP along the bond vector
    between atom1 and atom2.
    """
    line = atom1.cart - atom2.cart
    line /= np.linalg.norm(line)
    try:
        int1 = np.dot(np.dot(line.transpose(), get_adp_as_matrix(atom1.adp[use])), line)
        int2 = np.dot(np.dot(line.transpose(), get_adp_as_matrix(atom2.adp[use])), line)
        difference = np.linalg.norm(int1 - int2)
    except:
        difference = 1.2

    return difference


def get_difference_diff(atom1, atom2, use):
    """
    Returns the difference of two sets of ADP along the bond vector
    between atom1 and atom2.
    """
    if atom1.element == 'H' or atom2.element == 'H':
        return 1.2 / 10000
    line = atom1.cart - atom2.cart
    line /= np.linalg.norm(line)

    try:
        adp1 = get_adp_as_matrix(atom1.adp['cart_meas']) - get_adp_as_matrix(atom1.adp['cart_int'])
        adp2 = get_adp_as_matrix(atom2.adp['cart_meas']) - get_adp_as_matrix(atom2.adp['cart_int'])
        adp1 = get_adp_as_matrix(atom1.adp['cart_meas'])
        adp2 = get_adp_as_matrix(atom2.adp['cart_meas'])
    except:
        return None

    int1 = np.dot(np.dot(line.transpose(), adp1), line)
    int2 = np.dot(np.dot(line.transpose(), adp2), line)
    difference = np.linalg.norm(int1 - int2)
    #===========================================================================
    # print
    # print atom1.name,atom2.name,difference
    # print atom1.adp['cart_meas'],atom2.adp['cart_meas']
    #===========================================================================
    return difference


def get_bonds(name='exp'):
    """
    Determines the atoms bound to every atom. Hydrogens bond partners
    are set to None.
    """
    for atom in data[name].atoms:
        atom.bonds = []
        if not 'H(' in atom.name:
            for atom2 in atom.partner[1:]:
                if np.linalg.norm(atom.cart - atom2.cart) < 1.75:
                    atom.bonds.append(atom2)
        else:
            atom.bonds = None


def get_all_differences(use, name='exp'):
    """
    Calculates the differences in the mean square amplitudes of
    displacement for every unique pair of bound atoms.
    """
    get_bonds()
    difference_list = []
    black_list = []
    for atom1 in data[name].atoms:
        if atom1.bonds:
            for atom2 in atom1.bonds:
                difference = get_difference(atom1, atom2, use)
                if not (atom2, atom1) in black_list:
                    difference_list.append((atom1.name, atom2.name, float(difference)))
                    black_list.append((atom1, atom2))
                    #===========================================================
                    # if not 'A' in argv:
                    #     print '{:7s} {:7s} {:-4e}'.format(difference_list[-1][0],difference_list[-1][1],difference_list[-1][2])
                    #===========================================================
    return difference_list


def get_full_matrix():
    """
    Performing a full hirshfeld test by calculating the hirshfeld
    test values for all atom pairs, not only directly bound pairs.

    The results are stored in a square matrix containing one line
    and one column for every atom.
    """
    global data
    matrix = [[0 for i in range(len(data['exp'].atoms))] for _ in range(len(data['exp'].atoms))]
    for i in range(len(data['exp'].atoms)):
        for j in range(len(data['exp'].atoms)):
            atom1 = data['exp'].atoms[i]
            atom2 = data['exp'].atoms[j]
            if not i == j:
                val = get_difference_diff(atom1, atom2, 'cart_ext')
                if val is None:
                    matrix[i][j] = None
                else:
                    matrix[i][j] = int(val * 10000)
    data['exp'].hirshfeld_matrix = matrix


def write_table(difference_list, use):
    """
    Writes the Hirshfeld-Test results as a Latex formated table.
    """
    filepointer = open('hirshfeld_' + use + '.tex', 'w')
    filepointer.write('\\begin{table}\n\\centering\n\
\\caption{Hirshfeld Test results (' + use + ').}\n\
\\begin{tabular}{ccc}\n\\hline\nAtom 1&Atom 2\
&$\Delta U_z$ [$A^2$]\\\\\n\\hline\n')
    for line in difference_list:
        filepointer.write('{:7s}&{:7s}&${:-4e}$\\\\\n'.format(line[0], line[1], line[2]))
    filepointer.write('\\hline\n\\end{tabular}\n\\end{table}')


def run(configurator, **kwargs):
    """
    Main interface function called by the plugin manager.

    The 'use' argument specifies which ADP contribution
    should be tested. The options are: 'cart_int', 'cart_ext'
    , 'cart_sum' 'cart_meas'.

    The 'tex' argument specifies whether a latex format
    table should be written to 'hirshfeld_'use'.tex'.

    The 'full' argument specifies if the hirshfeld test
    should be applied to all atom pairs or only to
    directly bound pairs.
    """
    global indent, printer
    printer = configurator.setup()
    global data, compoundKey
    data = configurator.get_variable()
    compoundKey = configurator.arg('compound')
    usearg = configurator.arg('use')
    if not usearg:
        use = 'cart_meas'
    else:
        use = usearg

    if not configurator.arg('full'):
        printer('Performing hirshfeld test for directly bound atoms.')
        difference_list = get_all_differences(use)
        data['exp'].hirshfeld_list = difference_list
        if configurator.arg('tex'):
            printer('Writing file: \'hirshfeld.tex\'.')
            write_table(difference_list, use)
    else:
        printer('Performing hirshfeld test for all atom pairs.')
        get_full_matrix()
        difference_list = get_all_differences(use)
        data['exp'].hirshfeld_list = difference_list


