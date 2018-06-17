"""
Created on Apr 1, 2013

@author: jens

This module is used for the fitting of TLS Parameters to the measured
data. This implementation of the TLS-Fit sets the matrix element
S_33 is arbitrarily to zero.

"""

KEY = 'T'

import numpy as np

import lauescript.cryst.crystgeom as cg


def raw_rotation_matrix(data, axis, rigid_group):
    """
    Determines an 'empty' rotation matrix suitable for fitting the
    rotation angle by a least squares method.
    """
    print('\n\n\n\n Am I really used???????????\n\n\n\n')
    axis /= np.linalg.norm(axis)
    a, b, c = axis[0], axis[1], axis[2]
    raw_matrix = []
    for atom in rigid_group:
        x, y, z = atom.cart[0], atom.cart[1], atom.cart[2]
        raw_matrix.append([0, x - 2 * x * b * b - 2 * x * c * c])
        raw_matrix.append([-2 * x * c, 2 * x * a * b])
        raw_matrix.append([2 * x * b, 2 * x * a * c])

        raw_matrix.append([2 * y * c, 2 * y * a * b])
        raw_matrix.append([0, y - 2 * y * a * a - 2 * y * c * c])
        raw_matrix.append([-2 * y * a, 2 * y * b * c])

        raw_matrix.append([-2 * z * b, 2 * z * a * c])
        raw_matrix.append([2 * z * a, 2 * z * b * c])
        raw_matrix.append([0, z - 2 * z * a * a - 2 * z * b * b])

        data['exp'][atom.name].raw_matrix = raw_matrix


def prep_data2ls(data, useH=False):
    """
    Prepares the data for the least square optimization. The useH option
    can be set to True to force the usage of hydron atoms. This is not
    recommendet for the actual fit but for the application of the
    fitted Parameters to the atoms.

    This function is used when a rigid body fit is selected.
    """
    y = []
    A = []
    for atom in data['exp'].atoms:
        if not atom.name[0] == 'H' or useH:
            if useH or atom.adp['cart_meas'] is not None:

                xlist = atom.cart.tolist()

                x1 = (xlist[0])
                x2 = (xlist[1])
                x3 = (xlist[2])
                A.append(np.array([1, 0, 0, 0, 0, 0, 0, x3 * x3, x2 * x2, 0, 0, -2 * x2 * x3, 0
                    , 0, 0, 0, 2 * x3, 0, 0, 0]))
                A.append(np.array([0, 1, 0, 0, 0, 0, x3 * x3, 0, x1 * x1, -2 * x1 * x3, 0, 0, 0
                    , 0, -2 * x3, 0, 0, 0, 0, 2 * x1]))
                A.append(np.array([0, 0, 1, 0, 0, 0, x2 * x2, x1 * x1, 0, -2 * x1 * x2, 0, 0, 0
                    , 0, 0, 2 * x2, 0, -2 * x1, 0, 0]))
                A.append(np.array([0, 0, 0, 1, 0, 0, 0, 0, -x1 * x2, -x3 * x3, x2 * x3, x1 * x3
                    , -x3, x3, 0, 0, 0, 0, x1, -x2]))
                A.append(np.array([0, 0, 0, 0, 1, 0, 0, -x1 * x3, 0, x2 * x3, -x2 * x2, x1 * x2
                    , x2, 0, 0, 0, -x1, x3, 0, 0]))
                A.append(np.array([0, 0, 0, 0, 0, 1, -x2 * x3, 0, 0, x1 * x3, x1 * x2, -x1 * x1
                    , 0, -x1, x2, -x3, 0, 0, 0, 0]))

                adplist_sum = atom.adp['cart_meas']
                adplist_int = atom.adp['cart_int']
                adplist = []
                if not atom.adp['cart_meas'] is None:
                    for m in range(len(adplist_sum)):
                        if uncorrelate:
                            adplist.append(adplist_sum[m] - adplist_int[m])
                        else:
                            adplist.append(adplist_sum[m])

                    for i in range(len(adplist)):
                        y.append(adplist[i])
    A = np.array(A)
    return A, y


def prep_data2ls_srb(data, rigid_groups, rigid_namess, axiss, useH=False):
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

    for atom in data['exp'].atoms:
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
                row = [1, 0, 0, 0, 0, 0, 0, x3 * x3, x2 * x2, 0, 0, -2 * x2 * x3, 0, 0, 0, 0, 2 * x3, 0, 0, 0]
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
                row = [0, 1, 0, 0, 0, 0, x3 * x3, 0, x1 * x1, -2 * x1 * x3, 0, 0, 0, 0, -2 * x3, 0, 0, 0, 0, 2 * x1]
                for g in range(num_groups):
                    if not atom in rigid_group:
                        for _ in range(7): row.append(0)
                    else:
                        row2 = [V[g][1] * V[g][1], -2 * x3 * V[g][1], 0, 2 * x1 * V[g][1], 0, 2 * V[g][1], 0]
                        row = row + row2
                A.append(np.array(row))
                indexlist.append(len(A) - 1)

                #33
                row = [0, 0, 1, 0, 0, 0, x2 * x2, x1 * x1, 0, -2 * x1 * x2, 0, 0, 0, 0, 0, 2 * x2, 0, -2 * x1, 0, 0]
                for g in range(num_groups):
                    if not atom in rigid_group:
                        for _ in range(7): row.append(0)
                    else:
                        row2 = [V[g][2] * V[g][2], 2 * x2 * V[g][2], -2 * x1 * V[g][2], 0, 0, 0, 2 * V[g][2]]
                        row = row + row2
                A.append(np.array(row))
                indexlist.append(len(A) - 1)

                #12
                row = [0, 0, 0, 1, 0, 0, 0, 0, -x1 * x2, -x3 * x3, x2 * x3, x1 * x3, -x3, x3, 0, 0, 0, 0, x1, -x2]
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
                row = [0, 0, 0, 0, 1, 0, 0, -x1 * x3, 0, x2 * x3, -x2 * x2, x1 * x2, x2, 0, 0, 0, -x1, x3, 0, 0]
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
                row = [0, 0, 0, 0, 0, 1, -x2 * x3, 0, 0, x1 * x3, x1 * x2, -x1 * x1, 0, -x1, x2, -x3, 0, 0, 0, 0]
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
        A, y, _ = prep_data2ls_srb(data, rigid_groups, rigid_namess, axiss)
    else:
        A, y = prep_data2ls(data)

    v = np.linalg.lstsq(A, y)
    v = v[0]



    # ===========================================================================
    # T=np.matrix([[v[0],v[3],v[4]],[v[3],v[1],v[5]],[v[4],v[5],v[2]]])
    # L=np.matrix([[v[6],v[9],v[10]],[v[9],v[7],v[11]],[v[10],v[11],v[8]]])
    # S=np.matrix([[v[12],v[14],v[15]],[v[16],v[13],v[17]],[v[18],v[19],0]])
    #===========================================================================
    rest = np.array(v[20:])
    R = []
    for g in range(len(rest) / 7):
        #=======================================================================
        # R.append(np.matrix([[v[20+1+g*7],v[20+4+g*7],v[20+5+g*7]],[v[20+4+g*7],v[20+2+g*7],v[20+6+g*7]],[v[20+5+g*7],v[20+6+g*7],v[20+3+g*7]]]))
        #=======================================================================
        R.append([v[20 + 1 + g * 7], v[20 + 2 + g * 7], v[20 + 3 + g * 7], v[20 + 4 + g * 7], v[20 + 5 + g * 7],
                  v[20 + 6 + g * 7]])
    #R=np.matrix()
    #R=np.array(v[20:])
    indexlist = None
    if srb:
        A, y, indexlist = prep_data2ls_srb(data, rigid_groups, rigid_namess, axiss, useH=True)
    else:
        A, y = prep_data2ls(data, useH=True)
    Utls = np.dot(A, v)

    printer('\nFitted TLS parameters:\n')
    printer('    | {T[0]:+4.2e}  {T[3]:+4.2e}  {T[4]:+4.2e} |' \
            '\n T  | {T[3]:+4.2e}  {T[1]:+4.2e}  {T[5]:+4.2e} |' \
            '\n    | {T[4]:+4.2e}  {T[5]:+4.2e}  {T[2]:+4.2e} |\n' \
            .format(T=v))
    printer('    | {T[6]:+4.2e}  {T[9]:+4.2e}  {T[10]:+4.2e} |' \
            '\n L  | {T[9]:+4.2e}  {T[7]:+4.2e}  {T[11]:+4.2e} |' \
            '\n    | {T[10]:+4.2e}  {T[11]:+4.2e}  {T[8]:+4.2e} |\n' \
            .format(T=v))
    printer('    | {T[12]:+4.2e}  {T[14]:+4.2e}  {T[15]:+4.2e} |' \
            '\n S  | {T[16]:+4.2e}  {T[13]:+4.2e}  {T[17]:+4.2e} |' \
            '\n    | {T[18]:+4.2e}  {T[19]:+4.2e}  {z:+4.2e} |\n' \
            .format(T=v, z=0))
    for index, R in enumerate(R):
        printer('    | {T[0]:+4.2e}  {T[3]:+4.2e}  {T[4]:+4.2e} |' \
                '\n R{index} | {T[3]:+4.2e}  {T[1]:+4.2e}  {T[5]:+4.2e} |' \
                '\n    | {T[4]:+4.2e}  {T[5]:+4.2e}  {T[2]:+4.2e} |\n' \
                .format(T=R, index=index + 1))

    apply_tls(Utls, indexlist, srb)


def apply_tls(Utls, indexlist=None, srb=False):
    """
    Uses the calculated TLS-Parameter to calculate the displacements
    for all atoms based on those parameters.
    """

    if srb:
        pass
    # m=np.linalg.pinv(data['exp'].frac2cartmatrix)
    for i in range(len(Utls) / 6):
        data['exp'].atoms[i].adp['cart_ext'] = Utls[i * 6:i * 6 + 6]
        data['exp'].atoms[i].adp['cart_sum'] = data['exp'].atoms[i].adp['cart_int'] \
                                               + data['exp'].atoms[i].adp['cart_ext']
        #===============================================================================
        #         if not data['exp'].atoms[i].element == 'H':
        #
        #             data['exp'].atoms[i].adp['cart_int']=data['exp'].atoms[i].adp['cart_sum']\
        #                                     -data['exp'].atoms[i].adp['cart_ext']
        #             data['exp'].atoms[i].adp['frac_int']=cg.rotate_adp3(data['exp']\
        #                                     .atoms[i].adp['cart_int'],\
        #                                     data['exp'].cart2fracmatrix,\
        #                                     data['exp'].cell)
        #===============================================================================


        data['exp'].atoms[i].adp['frac_ext'] = cg.rotate_adp3(data['exp']
                                                              .atoms[i].adp['cart_ext'],
                                                              data['exp'].cart2fracmatrix,
                                                              data['exp'].cell)

        data['exp'].atoms[i].adp['frac_sum'] = cg.rotate_adp3(data['exp']
                                                              .atoms[i].adp['cart_sum'],
                                                              data['exp'].cart2fracmatrix,
                                                              data['exp'].cell)


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
        #raw_matrix=raw_rotation_matrix(data,axis,rigid_group)
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
        #sys.exit()
        print([i for i in sorted_rigid_names])

    else:
        sorted_rigid_groups = rigid_groups
        sorted_rigid_names = rigid_names
        sorted_axiss = axiss

    return sorted_rigid_groups, sorted_rigid_names, sorted_axiss


def get_user_input(srb):
    """
    Calls the tls interface function of the gui.py module to
    get user defined input for the TLS-Fit.
    """
    # ===========================================================================
    # if srb=='gui':
    #     from gui import get_tls_definition
    #     return get_tls_definition()
    # elif srb=='auto':
    #     from autosegment import get_tls_definition_auto
    #     return get_tls_definition_auto()
    #===========================================================================
    # from autosegment import get_tls_definition_auto

    # return get_tls_definition_auto()


def run(configurator, srb=None, **kwargs):
    """
    Interface function for the main.py module.

    If srb (Segmented Rigid Body) is True, a segmented
    rigid body analysis is performed. Otherwise a rigid
    body model is applied.
    """

    global indent, printer, uncorrelate, mo
    printer = configurator.setup()
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
    # ===========================================================================
    # indent=5
    #===========================================================================


    #srb=True
    fit_tls(data, srb)
    return True

