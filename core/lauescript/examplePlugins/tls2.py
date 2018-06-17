"""
Created on Apr 1, 2013

@author: jens

This module is used for the fitting of TLS Parameters to the measured
data. This implementation of the TLS-Fit sets the matrix element
S_33 is arbitrarily to zero.

"""

KEY = 'T2'
OPTION_ARGUMENTS = {'molecule': 0}
OPTIONS = ['correlate']
NAME = 'TLS'

import numpy as np
import lauescript.cryst.crystgeom as cg
from math import copysign


def buildLSMatrix(data, useH=False):
    """
    Prepares the data for the least square optimization. The useH option
    can be set to True to force the usage of hydron atoms. This is not
    recommendet for the actual fit but for the application of the
    fitted Parameters to the atoms.

    This function is used when a rigid body fit is selected.
    """
    y = []
    A = []
    if molID >= 0 and not useH:
        printer('\nPerforming rigid body fit for molecule with ID: {}'.format(molID))
    for atom in data['exp'].get_chem_molecule(molID):
        if not useH:
            fitted_atoms.append(atom)
        if not atom.name[0] == 'H' or useH:
            if useH or atom.adp['cart_meas'] is not None:

                xlist = atom.cart.tolist()

                x1 = (xlist[0])
                x2 = (xlist[1])
                x3 = (xlist[2])
                                 # TTTTTTTTTTTTTTTT     LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL      SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
                                 # 1  2  3  1  1  2     1        2         3         1             1              2                  1  2    3    1        1       2       2        3         3
                                 # 1  2  3  2  3  3     1        2         3         2             3              3                  1  2    3    2        3       1       3        1         2
                A.append(np.array([1, 0, 0, 0, 0, 0,    0      , x3 * x3 , x2 * x2 , 0           , 0            , -2 * x2 * x3,      0, 0  , 0  , 0      , 0     , 2 * x3, 0      , -2 * x2 , 0     ]))
                A.append(np.array([0, 1, 0, 0, 0, 0,    x3 * x3, 0       , x1 * x1 , 0           , -2 * x1 * x3 , 0           ,      0, 0  , 0  , -2 * x3, 0     , 0     , 0      , 0       , 2 * x1]))
                A.append(np.array([0, 0, 1, 0, 0, 0,    x2 * x2, x1 * x1 , 0       , -2 * x1 * x2, 0            , 0           ,      0, 0  , 0  , 0      , 2 * x2, 0     , -2 * x1, 0       , 0     ]))

                A.append(np.array([0, 0, 0, 1, 0, 0,    0      , 0       , -x1 * x2, -x3 * x3    , x2 * x3      , x1 * x3     ,    -x3, x3 , 0  , 0      , 0     , 0     , 0      , x1      , -x2   ]))
                A.append(np.array([0, 0, 0, 0, 1, 0,    0      , -x1 * x3, 0       , x2 * x3     , -x2 * x2     , x1 * x2     ,     x2, 0  , -x2, 0      , 0     , -x1   , x3     , 0       , 0     ]))
                A.append(np.array([0, 0, 0, 0, 0, 1,   -x2 * x3,        0, 0       , x1 * x3     , x1 * x2      , -x1 * x1    ,      0, -x1, x1 , x2     , -x3   , 0     , 0      , 0       , 0     ]))

                adplist_sum = atom.adp['cart_meas']
                adplist_int = atom.adp['cart_int']
                adplist = []
                if atom.adp['cart_meas'] is not None:
                    for m in range(len(adplist_sum)):
                        if uncorrelate:
                            adplist.append(adplist_sum[m] - adplist_int[m])
                        else:
                            adplist.append(adplist_sum[m])

                    for i in range(len(adplist)):
                        y.append(adplist[i])
            else:
                np.array([copysign(100, x1) - 100])
    A = np.array(A)
    return A, y


def buildLSMatrix_SRB(data, rigid_groups, rigid_namess, axiss, useH=False):
    """
    Prepares the data for the least square optimization. The useH option
    can be set to True to force the usage of hydron atoms. This is not
    recommendet for the actual fit but for the application of the
    fitted Parameters to the atoms.

    This function is used when a segmented rigid body fit is selected.
    """

    # ===========================================================================
    # data=cg.read_meas_adp(data)
    #===========================================================================

    y = []
    A = []
    num_groups = len(axiss)
    indexlist = []

    if molID >= 0 and not useH:
        printer('\nPerforming rigid body fit for molecule with ID: {}'.format(molID))

    for atom in data['exp'].get_chem_molecule(molID):
        if not useH:
            fitted_atoms.append(atom)
        if not atom.name[0] == 'H' or useH:
            if atom.adp['cart_meas'] is not None or useH:
                xlist = atom.cart.tolist()

                x1 = (xlist[0])
                x2 = (xlist[1])
                x3 = (xlist[2])


                V = []
                for g in range(num_groups):
                    V.append(np.cross(axiss[g], atom.cart - rigid_groups[g][0].cart))

                #11
                row = [1, 0, 0, 0, 0, 0,    0      , x3 * x3 , x2 * x2 , 0           , 0            , -2 * x2 * x3,      0, 0  , 0  , 0      , 0     , 2 * x3, 0      , -2 * x2 , 0     ]
                for g in range(num_groups):
                    rigid_group = rigid_groups[g]
                    if not atom in rigid_group:
                        for _ in range(7): row.append(0)
                    else:
                        row2 = [V[g][0] * V[g][0], 0, 2 * x3 * V[g][0], -2 * x2 * V[g][0], 2 * V[g][0], 0, 0]
                        row = row + row2

                A.append(np.array(row))
                indexlist.append(len(A) - 1)

                #22
                row = [0, 1, 0, 0, 0, 0,    x3 * x3, 0       , x1 * x1 , 0           , -2 * x1 * x3 , 0           ,      0, 0  , 0  , -2 * x3, 0     , 0     , 0      , 0       , 2 * x1]
                for g in range(num_groups):
                    if not atom in rigid_group:
                        for _ in range(7): row.append(0)
                    else:
                        row2 = [V[g][1] * V[g][1], -2 * x3 * V[g][1], 0, 2 * x1 * V[g][1], 0, 2 * V[g][1], 0]
                        row = row + row2
                A.append(np.array(row))
                indexlist.append(len(A) - 1)

                #33
                row = [0, 0, 1, 0, 0, 0,    x2 * x2, x1 * x1 , 0       , -2 * x1 * x2, 0            , 0           ,      0, 0  , 0  , 0      , 2 * x2, 0     , -2 * x1, 0       , 0     ]
                for g in range(num_groups):
                    if not atom in rigid_group:
                        for _ in range(7): row.append(0)
                    else:
                        row2 = [V[g][2] * V[g][2], 2 * x2 * V[g][2], -2 * x1 * V[g][2], 0, 0, 0, 2 * V[g][2]]
                        row = row + row2
                A.append(np.array(row))
                indexlist.append(len(A) - 1)

                #12
                row = [0, 0, 0, 1, 0, 0,    0      , 0       , -x1 * x2, -x3 * x3    , x2 * x3      , x1 * x3     ,    -x3, x3 , 0  , 0      , 0     , 0     , 0      , x1      , -x2   ]
                for g in range(num_groups):
                    if not atom in rigid_group:
                        for _ in range(7): row.append(0)
                    else:
                        row2 = [V[g][0] * V[g][1], -x3 * V[g][0], 2 * x3 * V[g][1], x1 * V[g][0] - x2 * V[g][1],
                                V[g][1], V[g][0], 0]
                        row = row + row2
                A.append(np.array(row))
                indexlist.append(len(A) - 1)

                #13
                row = [0, 0, 0, 0, 1, 0,    0      , -x1 * x3, 0       , x2 * x3     , -x2 * x2     , x1 * x2     ,     x2, 0  , -x2, 0      , 0     , -x1   , x3     , 0       , 0     ]
                for g in range(num_groups):
                    if not atom in rigid_group:
                        for _ in range(7): row.append(0)
                    else:
                        row2 = [V[g][0] * V[g][2], x2 * V[g][0], x3 * V[g][2] - x1 * V[g][0], -x2 * V[g][2], V[g][2], 0,
                                V[g][0]]
                        row = row + row2
                A.append(np.array(row))
                indexlist.append(len(A) - 1)

                #23
                row = [0, 0, 0, 0, 0, 1,   -x2 * x3,        0, 0       , x1 * x3     , x1 * x2      , -x1 * x1    ,      0, -x1, x1 , x2     , -x3   , 0     , 0      , 0       , 0     ]
                for g in range(num_groups):
                    if not atom in rigid_group:
                        for _ in range(7): row.append(0)
                    else:
                        row2 = [V[g][1] * V[g][2], x2 * V[g][1] - x3 * V[g][2], -x1 * V[g][1], x1 * V[g][2], 0, V[g][2],
                                V[g][1]]
                        row = row + row2
                A.append(np.array(row))
                indexlist.append(len(A) - 1)

                if not useH:
                    adplist_sum = atom.adp['cart_meas']
                    adplist_int = atom.adp['cart_int']
                    adplist = []
                    for m in range(len(adplist_sum)):
                        if uncorrelate:
                            adplist.append(adplist_sum[m] - adplist_int[m])
                        else:
                            adplist.append(adplist_sum[m])

                    for i in range(len(adplist)):
                        y.append(adplist[i])

    A = np.array(A)
    return A, y, indexlist


def fit_tls(data, srb):
    """
    Carries out the TLS-Fit and stores the information the the atom.adp
    dictionary.
    The current version overwrites the internal ADP of heavy atoms
    by the difference of the external and measured ADP.
    """
    if srb:
        rigid_groups, rigid_namess, axiss = segment(srb)
        A, y, _ = buildLSMatrix_SRB(data, rigid_groups, rigid_namess, axiss)
    else:
        A, y = buildLSMatrix(data)

    v = np.linalg.lstsq(A, y)
    v = v[0]

    rest = np.array(v[21:])
    R = []
    for g in range(len(rest) / 7):
        R.append([v[20 + 1 + g * 7], v[20 + 2 + g * 7], v[20 + 3 + g * 7], v[20 + 4 + g * 7], v[20 + 5 + g * 7],
                  v[20 + 6 + g * 7]])
    indexlist = None
    if srb:
        A, y, indexlist = buildLSMatrix_SRB(data, rigid_groups, rigid_namess, axiss, useH=True)
    else:
        A, y = buildLSMatrix(data, useH=True)
    Utls = np.dot(A, v)

    printer('\nFitted TLS parameters:\n')
    printer('    | {T[0]:+4.2e}  {T[3]:+4.2e}  {T[4]:+4.2e} |'
            '\n T  | {T[3]:+4.2e}  {T[1]:+4.2e}  {T[5]:+4.2e} |'
            '\n    | {T[4]:+4.2e}  {T[5]:+4.2e}  {T[2]:+4.2e} |\n'
            .format(T=v))
    printer('    | {T[6]:+4.2e}  {T[9]:+4.2e}  {T[10]:+4.2e} |'
            '\n L  | {T[9]:+4.2e}  {T[7]:+4.2e}  {T[11]:+4.2e} |'
            '\n    | {T[10]:+4.2e}  {T[11]:+4.2e}  {T[8]:+4.2e} |\n'
            .format(T=v))
    printer('    | {T[12]:+4.2e}  {T[15]:+4.2e}  {T[16]:+4.2e} |'
            '\n S  | {T[17]:+4.2e}  {T[13]:+4.2e}  {T[18]:+4.2e} |'
            '\n    | {T[19]:+4.2e}  {T[20]:+4.2e}  {T[14]:+4.2e} |\n'
            .format(T=v, z=0))
    for index, R in enumerate(R):
        printer('    | {T[0]:+4.2e}  {T[3]:+4.2e}  {T[4]:+4.2e} |'
                '\n R{index} | {T[3]:+4.2e}  {T[1]:+4.2e}  {T[5]:+4.2e} |'
                '\n    | {T[4]:+4.2e}  {T[5]:+4.2e}  {T[2]:+4.2e} |\n'
                .format(T=R, index=index + 1))

    apply_tls(Utls, indexlist, srb)


def apply_tls(Utls, indexlist=None, srb=False):
    """
    Uses the calculated TLS-Parameter to calculate the displacements
    for all atoms based on those parameters.
    """

    if srb:
        pass
        # ===============================================================================
    #     for i in range(len(Utls)/6):
    #         data['exp'].atoms[i].adp['cart_ext']=Utls[i*6:i*6+6]
    #         data['exp'].atoms[i].adp['cart_sum']=data['exp'].atoms[i].adp['cart_int']\
    #                                        +data['exp'].atoms[i].adp['cart_ext']
    #
    #
    #         data['exp'].atoms[i].adp['frac_ext']=cg.rotate_adp3(data['exp']\
    #                                     .atoms[i].adp['cart_ext'],\
    #                                     data['exp'].cart2fracmatrix,\
    #                                     data['exp'].cell)
    #
    #         data['exp'].atoms[i].adp['frac_sum']=cg.rotate_adp3(data['exp']\
    #                                     .atoms[i].adp['cart_sum'],\
    #                                     data['exp'].cart2fracmatrix,\
    #                                     data['exp'].cell)
    #===============================================================================

    for i, atom in enumerate(fitted_atoms):
        if atom.get_element() == 'H':
            atom.adp['cart_ext'] = Utls[i * 6:i * 6 + 6]

            atom.adp['cart_sum'] = atom.adp['cart_int'] + atom.adp['cart_ext']

            atom.adp['frac_ext'] = cg.rotate_adp3(atom.adp['cart_ext'],
                                                  data['exp'].cart2fracmatrix,
                                                  data['exp'].cell)

            atom.adp['frac_sum'] = cg.rotate_adp3(atom.adp['cart_sum'],
                                                  data['exp'].cart2fracmatrix,
                                                  data['exp'].cell)
            atom.updated()
        else:
            atom.adp['cart_sum'] = atom.adp['cart_meas']
            atom.adp['cart_ext'] = Utls[i * 6:i * 6 + 6]
            atom.updated()


def segment(srb):
    """
    Function to segment a molecule in rigid groups that are allowed to
    rotate against each other arround a defined axis.
    """
    # atom1,atom2,axis=get_user_input()
    tls_definitions = get_user_input(srb)
    rigid_groups, rigid_namess, axiss = [], [], []
    for tls_definition in tls_definitions:
        rigid_groups.append(cg.framework_crawler(tls_definition[1], tls_definition[2]))
        axiss.append(tls_definition[0])
        rigid_names = []
        for atom in rigid_groups[-1]:
            rigid_names.append(atom.name)
        rigid_namess.append(rigid_names)

    if len(rigid_namess) > 100:
        namesets = []
        for group in rigid_namess:
            evalstring = '{'
            for string in group:
                evalstring += '\'' + string
                evalstring += '\','
            evalstring += '}'
            nameset = eval(evalstring)
            namesets.append(nameset)

        hierachy = []
        for i in range(len(namesets)):
            hierachy.append([0, i])
            group1 = namesets[i]
            for j in range(len(namesets)):
                group2 = namesets[j]
                if not group1 == group2:
                    if group1.issubset(group2):
                        hierachy[j][0] += 1

        hierachy = sorted(hierachy, key=lambda hierachy: hierachy[0], reverse=True)
        sorted_rigid_groups = []
        sorted_rigid_names = []
        sorted_axiss = []
        for hierach in hierachy:
            sorted_rigid_groups.append(rigid_groups[hierach[1]])
            sorted_rigid_names.append(rigid_names[hierach[1]])
            sorted_axiss.append(axiss[hierach[1]])
        exit()
        print([i for i in sorted_rigid_names])

    else:
        sorted_rigid_groups = rigid_groups
        sorted_rigid_names = rigid_names
        sorted_axiss = axiss

    return sorted_rigid_groups, sorted_rigid_names, sorted_axiss


# def get_user_input(srb):
#     """
#     Calls the tls interface function of the gui.py module to
#     get user defined input for the TLS-Fit.
#     """
#     # ===========================================================================
#     # if srb=='gui':
#     #     from gui import get_tls_definition
#     #     return get_tls_definition()
#     # elif srb=='auto':
#     #     from autosegment import get_tls_definition_auto
#     #     return get_tls_definition_auto()
#     #===========================================================================
#     from autosegment2 import get_tls_definition_auto
#
#     return get_tls_definition_auto()


def run(configurator, srb=None, **kwargs):
    """
    Interface function for the main.py module.

    If srb (Segmented Rigid Body) is True, a segmented
    rigid body analysis is performed. Otherwise a rigid
    body model is applied.
    """

    global indent, printer, uncorrelate, mo, molID, fitted_atoms
    printer = configurator.setup()
    molID = int(configurator.arg('molecule'))
    if molID is False:
        molID = -1
    else:
        molID -= 1
    fitted_atoms = []
    global data
    data = configurator.get_variable()
    if configurator.arg('auto'):
        srb = 'auto'
    if configurator.arg('user'):
        srb = 'user'
    if configurator.arg('correlate'):
        printer('Not correcting correlation between internal\nand external vibrations.')
        uncorrelate = False
    else:
        printer('Correcting correlation between internal\nand external vibrations.')
        uncorrelate = True

    fit_tls(data, srb)
    return True

