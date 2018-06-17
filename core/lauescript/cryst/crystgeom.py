"""
Created on Feb 10, 2013

@author: jens

Deprecated module for crystallogrphy related geometry operations. And a lot
of other stuff that I put here.
"""

import numpy as np


atomtable = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
             'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
             'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22,
             'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29,
             'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36}

covalence_radius = {'H': .37, 'He': .0, 'Li': 1.23, 'Be': .90, 'B': .80, 'C': .77,
                    'N': .74, 'O': .71, 'F': .72, 'Ne': 0., 'Na': 1.54, 'Mg': 1.36,
                    'Al': 1.18, 'Si': 1.11, 'P': 1.06, 'S': 1.02, 'Cl': .99, 'Ar': 0.,
                    'K': 2.03, 'Ca': 1.74, 'Sc': 1.44, 'Ti': 1.32, 'V': 1.22,
                    'Cr': 1.18, 'Mn': 1.17, 'Fe': 1.17, 'Co': 1.16, 'Ni': 1.15,
                    'Cu': 1.17, 'Zn': 1.25, 'Ga': 1.26, 'Ge': 1.22, 'As': 1.20,
                    'Se': 1.16, 'Br': 1.14, 'Kr': 0.,
                    'Rb': 2.18}  # , 191, 162, 145, 134, 130, 127, 125, 125, 128, 134, 148, 144, 141, 140, 136, 133, 0, 235, 198, 169, 165, 165, 164, 164, 162, 185, 161, 159, 159, 157, 157, 156, 170, 156, 144, 134, 130, 128, 126, 127, 130, 134, 149, 148, 147, 146, 146, 145, 0, 0, 0, 188, 165, 161, 142, 130, 151, 182, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}

electro_negativ = {'H': 2.20, 'He': 5.50, 'Li': .97, 'Be': 1.47, 'B': 2.01, 'C': 2.50,
                   'N': 3.07, 'O': 3.50, 'F': 4.40, 'Ne': 4.80, 'Na': 1.01, 'Mg': 1.23,
                   'Al': 1.47, 'Si': 1.74, 'P': 2.06, 'S': 2.44, 'Cl': 2.83, 'Ar': 3.20,
                   'K': .91, 'Ca': 1.04, 'Sc': 1.20, 'Ti': 1.32, 'V': 1.45,
                   'Cr': 1.56, 'Mn': 1.60, 'Fe': 1.64, 'Co': 1.70, 'Ni': 1.75,
                   'Cu': 1.75, 'Zn': 1.66, 'Ga': 1.82, 'Ge': 2.02, 'As': 2.20,
                   'Se': 2.48, 'Br': 2.74, 'Kr': 2.90,
                   'Rb': .89}  # , 99, 111, 122, 123, 130, 136, 142, 145, 130, 142, 146, 149, 172, 182, 201, 221, 240, 86, 97, 108, 108, 107, 107, 107, 107, 110, 111, 110, 110, 110, 111, 111, 106, 114, 123, 133, 140, 146, 152, 155, 142, 142, 144, 144, 155, 167 }

proton_number = {'H': '001', 'He': '002', 'Li': '003', 'Be': '004', 'B': '005', 'C': '006', 'N': '007', 'O': '008',
                 'F': '009', 'Ne': '010', 'Na': '011', 'Mg': '012', 'Al': '013', 'Si': '014', 'P': '015',
                 'S': '016', 'Cl': '017', 'Ar': '018', 'K': '019', 'Ca': '020', 'Sc': '021', 'Ti': '022',
                 'V': '023', 'Cr': '024', 'Mn': '025', 'Fe': '026', 'Co': '027', 'Ni': '028', 'Cu': '029',
                 'Zn': '030', 'Ga': '031', 'Ge': '032', 'As': '033', 'Se': '034', 'Br': '035', 'Kr': '036'}

number_proton = dict([[v, k] for k, v in proton_number.items()])

priority = {'3': '5',
            '2': '4',
            '1.5': '3',
            '6': '2',
            '5': '1',
            '1': '0'}


def frac2cart(coords, matrix):
    coords = np.dot(matrix, coords).flatten().tolist()[0]
    return coords


def xd_element(name):
    """
    Return the element of an atom as defined in it's label.
    """
    try:
        name = name[:2]
    except:
        pass
    try:
        covalence_radius[name]
    except:
        name = name[0]
    return name


def Uiso(adp, mean='geometric'):
    try:
        adp = get_adp_as_matrix(adp)
        eigvals = np.linalg.eigvals(adp)
        if mean == 'geometric':
            return (abs(eigvals[0]) * abs(eigvals[1]) * abs(eigvals[2])) ** (1. / 3.)
        elif mean == 'arithmetic':
            return sum(eigvals) / 3.
        else:
            print('crystgeom: Error: please specify mean as \'geometric\' or \'arithmetic\'')
            exit()
    except:
        return adp


def get_adp_as_matrix(adp):
    if adp is None:
        return None
    return np.matrix([[adp[0], adp[3], adp[4]],
                      [adp[3], adp[1], adp[5]],
                      [adp[4], adp[5], adp[2]]])


def get_compound_properties(path):
    """
    Reads a *.FChk file and returns a list containing the charge of
    the compound, the number of electrons in the compound, the overall
    lengths of the dipole moment vector and the total HF energy.
    """
    filepointer = open(path)
    charge = None
    NE = None
    E_HF = None
    dipole = None
    read_dipole = False
    for line in filepointer:
        if read_dipole:
            read_dipole = False
            dipole = [float(value) for value in line.split(' ') if '.' in value]
            dipole = np.linalg.norm(dipole)
        elif 'Charge' in line and not charge:
            charge = line.split(' ')[-1].rstrip('\n')
        elif 'Number of electrons' in line and not NE:
            NE = line.split(' ')[-1].rstrip('\n')
        elif 'Total Energy' in line and not E_HF:
            E_HF = line.split(' ')[-1].rstrip('\n')
        elif 'Dipole Moment' in line and not dipole:
            read_dipole = True
        if charge and NE and E_HF and dipole:
            break
    return [charge, NE, dipole, E_HF]


def center_molecule(atom_coords):
    center = get_geom_center(atom_coords)
    atom_coords = move_center_to_point(atom_coords, center)
    return atom_coords


def get_pair_list(atom_elements_1, atom_coords_1,
                  atom_elements_2, atom_coords_2):
    pair_list = []
    for i in range(len(atom_coords_1)):
        best_hit = (9, None)
        for j in range(len(atom_coords_2)):
            dist = np.linalg.norm(atom_coords_1[i] - atom_coords_2[j])
            if dist < best_hit[0] and atom_elements_1[i] == atom_elements_2[j]:
                best_hit = (dist, j)
        pair_list.append(best_hit[1])
    # ===========================================================================
    # print
    # for i in range(len(pair_list)):
    #     print atom_atoms_1[i],atom_atoms_2[pair_list[i]]
    #===========================================================================
    return pair_list


def bond_order(bondxi,
               threshold_single_meso=0.0847,
               # ================================================================
               # threshold_meso_double=0.184,
               #================================================================
               threshold_meso_double=0.0847,
               threshold_double_triple=0.27):
    """
    Returns the bond order between two atoms.
    """
    if bondxi < threshold_single_meso:
        order = '1'
    elif bondxi < threshold_meso_double:
        order = '1.5'
    elif bondxi < threshold_double_triple:
        order = '2'
    else:
        order = '3'
    return order


# ===============================================================================
# def rotate_3D_symmetric(atom,source_atom):
#     '''
#     Rotates the ADP of 'atom' to match the orientation
#     of 'source_atom.
#     '''
#     cosangle=np.dot(atom.orientation[0],source_atom.orientation[0])
#     angle=np.arccos(cosangle)
#     axis=np.cross(atom.orientation[0],source_atom.orientation[0])
#     axis=axis/np.linalg.norm(axis)
#     matrix=get_3drotation_matrix(axis,angle)
#     orientation0_new=np.dot(source_atom.orientation[0],matrix)
#     if np.linalg.norm(orientation0_new-atom.orientation[0])<0.00001:
#         pass
#     else:
#         angle=angle*-1
#         matrix=get_3drotation_matrix(axis,angle)
#
#     atom.adp['cart_int']=rotate_adp(source_atom.adp['cart_int'],matrix)
#===============================================================================




def rotate_3D(atom, source_atom):
    """
    Rotates the ADP of 'atom' to match the orientation
    of 'source_atom.
    """
    from lauescript.cryst.match import get_transform

    lst2 = [np.array([0, 0, 0]), source_atom.orientation[0], source_atom.orientation[1]]
    lst1 = [np.array([0, 0, 0]), atom.orientation[0], atom.orientation[1]]

    matrix = get_transform(lst1, lst2, matrix=True)

    adp = source_atom.adp['cart_int']

    atom.adp['cart_int'] = rotate_adp(adp, matrix)


def xi(element1, element2, distance):
    """
    Calculates the bond distinguishing parameter Xi.
    """
    return (float(covalence_radius[element1]) + float(covalence_radius[element2]) -
            (0.08 * float(abs(electro_negativ[element1] - electro_negativ[element2]))) - distance)


def get_orientation_vector(atom1, atom2):
    v = atom1.cart - atom2.cart
    return v / np.linalg.norm(v)


def framework_crawler2(atom, direction, rigid_group_old=None):
    """
    Function to identify atoms belonging to a previosly defined rigid
    group.
    Arguments:
        atom:            the name of the first atom of the rigid group.
        direction:       the name of the second atom of the rigid group.
        rigid_group_old: used by the function itself for consecutive calls.

    Returns a list of atom names belonging to the rigid group.
    """
    print(1)
    if not rigid_group_old:
        rigid_group = [atom, direction]
    else:
        rigid_group = rigid_group_old
    for atom in get_framework_neighbours(direction):
        if not atom in rigid_group and not atom.element == 'H':
            rigid_group.append(atom)
            framework_crawler2(rigid_group[0], atom, rigid_group)
    if not rigid_group_old:
        #=======================================================================
        # print '    Determined rigid group:', [i.name for i in rigid_group]
        #=======================================================================
        return rigid_group


def get_closest_atom_of_element(element, atom, exclude=None):
    """
    Returns the atom with the shortest distance to the given atom.
    """
    for atom2 in atom.partner:
        if (element == atom2.element or not element) and not atom2 == exclude:
            return atom2


def get_atom_with_longest_bond(element, atom):
    hit = None
    for atom2 in atom.partner:
        if element in atom2.name:
            if np.linalg.norm(atom.cart - atom2.cart) < 1.8:
                hit = atom2
            else:
                break
    return hit


def get_framework_neighbours(atom, useH=True):
    """
    Needs a ATOM.atom instance as argument.
    Returns the names of the framework atoms bound to that atom.
    """
    neighbourlist = []
    for atom2 in atom.partner[:5]:
        #if not 'H(' in atom2.name and np.linalg.norm(atom.cart-atom2.cart)<=1.6:
        if np.linalg.norm(atom.cart - atom2.cart) <= float(covalence_radius[atom.element]) + float(
                covalence_radius[atom2.element]) + .1:
            if not 'H' == atom2.element or useH:
                neighbourlist.append(atom2)
    return neighbourlist


#===============================================================================
# def get_framework_neighbours(atom,useH=True):
#     """
#     Needs a classes.atom instance as argument.
#     Returns the names of the framework atoms bound to that atom.
#     """
#     neighbourlist=[]
#     for atom2 in atom.partner[atom.molecule.name][1:5]:
#         #if not 'H(' in atom2.name and np.linalg.norm(atom.cart-atom2.cart)<=1.6:
#         if np.linalg.norm(atom.cart-atom2.cart)<=1.6:
#             if not 'H(' in atom2.name or useH:
#                 neighbourlist.append(atom2)
#     return neighbourlist
#===============================================================================

def read_meas_adp(data, path='xd.res', use='meas'):
    """
    Reads the measured ADP from the xd.res file.
    The parameters are stored in atom.adp['frac_meas'] and
    atom.adp['cart_meas']
    """
    use2 = 'frac_' + use
    switch = False
    filepointer = open(path, 'r')
    atomname = None
    for line in filepointer:
        if switch:
            split = [i for i in line.split(' ') if len(i) > 0]
            if not len(split) == 6:
                print('WARNING!!! Inconsistend number of floats while\
                       reading measured ADP.')
            data['exp'][atomname].adp[use2] = split
            switch = False
        if '(' in line:
            split = [i for i in line.split(' ') if len(i) > 0]
            if split[0][-1] == ')':
                switch = True
                atomname = split[0]
    use = 'cart_' + use
    for atom in data['exp'].atoms:
        # if use == 'cart_neut': print(atom)
        atom.adp[use] = rotate_adp2(atom.adp[use2],
                                    atom.molecule.frac2cartmatrix,
                                    atom.molecule.cell)
    return data


def reflect_adp(adp, planev):
    """
    Returns the ADP after reflection on the plane defined by its normal
    vector 'planev'.
    """
    M = np.identity(4)
    M[:3, :3] -= 2.0 * np.outer(planev, planev)
    M[:3, 3] = (2.0 * np.dot(np.array([0, 0, 0]), planev)) * planev

    return rotate_adp(adp, M[:3, :3])


def eigenv2tensor(axis):
    """
    Calculates the tensor representation of ADP from its priciple axis.
    """
    vec = np.ones((3, 3))
    vecval = np.ones((3, 3))
    for i in range(len(axis)):
        vmag = np.linalg.norm(axis[i])
        v = axis[i] / vmag
        #print v
        vec[:, i] = v
        vecval[:, i] = axis[i]
    adp = np.linalg.solve(vec, vecval)
    return adp


def get_adp_from_calc(vx, vy, vz):
    """
    Calculates an ADP in its matrix representation from the three
    principle axis representing the displacement ellipsoid.

    The three principle axis of the ellipsoid are needed as arguments.
    A Matrix representation of the ADP is returned.
    """
    ##    lx=np.linalg.norm(vx)
    ##    ly=np.linalg.norm(vy)
    ##    lz=np.linalg.norm(vz)
    lx = vx
    ly = vy
    lz = vz
    L = np.matrix([[lx, 0, 0],
                   [0, ly, 0],
                   [0, 0, lz]])


    ##    Vx=vx/lx
    ##    Vy=vy/ly
    ##    Vz=vz/lz
    Vx = np.array([1, 0, 0])
    Vy = np.array([0, 1, 0])
    Vz = np.array([0, 0, 1])
    V = np.matrix([[Vx[0], Vy[0], Vz[0]],
                   [Vx[1], Vy[1], Vz[1]],
                   [Vx[2], Vy[2], Vz[2]]])
    Vinv = np.linalg.inv(V)
    #print V,Vinv
    M = np.dot(np.dot(Vinv, L), V)
    #print M
    return M


#===============================================================================
#
#
# def get_general_distances(coordlist1,coordlist2,atomlist1,atomlist2):
#     """
#     Calculates a distance dictionary between two sets of atoms.
#     Returns a dictionary entry for every atom in atomlist1 with the inter atom
#     distances and the corresponding atom name keyed to their atom type.
#
#     This function is used by the get_best_point() function.
#     """
#     maindict={}
#     for i in range(len(atomlist1)):
#         distdict={}
#         for j in range(len(atomlist2)):
#             if not atomlist2[j][0] in distdict.keys():
#                 distdict[atomlist2[j][0]]=[[np.linalg.norm(coordlist1[i]-coordlist2[j]),atomlist2[j]]]
#             else:
#                 distdict[atomlist2[j][0]].append([np.linalg.norm(coordlist1[i]-coordlist2[j]),atomlist2[j]])
# ##        print atomlist1[i],'aaaaaaaaaaa'
#         maindict[atomlist1[i]]=distdict
#     return maindict
#===============================================================================



def get_best_quaternion(coordlist1, coordlist2):
    """
    Determines the the quaternion representing the best possible
    transformation of two coordinate systems into each other using
    a least sqare approach.

    This function is used by the get_refined_rotation() function.
    """
    M = np.matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    if len(coordlist1) <= len(coordlist2):
        number = len(coordlist1)
    else:
        number = len(coordlist2)
    for i in range(number):
        aaa = np.matrix(np.outer(coordlist1[i], coordlist2[i]))
        M = M + aaa

    N11 = float(M[0][:, 0] + M[1][:, 1] + M[2][:, 2])
    N22 = float(M[0][:, 0] - M[1][:, 1] - M[2][:, 2])
    N33 = float(-M[0][:, 0] + M[1][:, 1] - M[2][:, 2])
    N44 = float(-M[0][:, 0] - M[1][:, 1] + M[2][:, 2])
    N12 = float(M[1][:, 2] - M[2][:, 1])
    N13 = float(M[2][:, 0] - M[0][:, 2])
    N14 = float(M[0][:, 1] - M[1][:, 0])
    N21 = float(N12)
    N23 = float(M[0][:, 1] + M[1][:, 0])
    N24 = float(M[2][:, 0] + M[0][:, 2])
    N31 = float(N13)
    N32 = float(N23)
    N34 = float(M[1][:, 2] + M[2][:, 1])
    N41 = float(N14)
    N42 = float(N24)
    N43 = float(N34)

    N = np.matrix([[N11, N12, N13, N14],
                   [N21, N22, N23, N24],
                   [N31, N32, N33, N34],
                   [N41, N42, N43, N44]])

    values, vectors = np.linalg.eig(N)
    w = list(values)
    quat = vectors[:, w.index(max(w))]
    quat = np.array(quat).reshape(-1, ).tolist()
    return quat, max(w)


def get_rotation_matrix_from_quaternion(q):
    """
    Returns the rotation matrix equivalent of the given quaternion.

    This function is used by the get_refined_rotation() function.
    """
    R = np.matrix([[q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3],
                    2 * (q[1] * q[2] - q[0] * q[3]),
                    2 * (q[1] * q[3] + q[0] * q[2])],
                   [2 * (q[2] * q[1] + q[0] * q[3]),
                    q[0] * q[0] - q[1] * q[1] + q[2] * q[2] - q[3] * q[3],
                    2 * (q[2] * q[3] - q[0] * q[1])],
                   [2 * (q[3] * q[1] - q[0] * q[2]),
                    2 * (q[3] * q[2] + q[0] * q[1]),
                    q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]]])
    return R


def get_geom_center(coordlist):
    """
    Calculates the geometrical center of a set of points.
    """
    return sum(coordlist) / len(coordlist)


def move_center_to_point(atomlist, point):
    """
    Moves the geometrical center of the atoms in atomlist to the given point.
    """
    for atom in range(len(atomlist)):
        atomlist[atom] = atomlist[atom] - point
    return atomlist


def rotate_adp_reverse(adp, rotmat):
    """
    Rotates the adp with its corresponding rotation matrix.
    """

    adp = np.matrix([[float(adp[0]), float(adp[3]), float(adp[4])],
                     [float(adp[3]), float(adp[1]), float(adp[5])],
                     [float(adp[4]), float(adp[5]), float(adp[2])]])
    rotmatT = np.transpose(rotmat)
    adp = np.dot(rotmat, adp)
    adp = np.dot(adp, rotmatT)
    adp = np.array(adp).flatten().tolist()
    return [adp[0], adp[4], adp[8], adp[1], adp[2], adp[5]]


def rotate_adp(adp, rotmat):
    """
    Rotates the adp with its corresponding rotation matrix.
    """

    adp = np.matrix([[float(adp[0]), float(adp[3]), float(adp[4])],
                     [float(adp[3]), float(adp[1]), float(adp[5])],
                     [float(adp[4]), float(adp[5]), float(adp[2])]])
    rotmatT = np.transpose(rotmat)
    adp = np.dot(rotmatT, adp)
    adp = np.dot(adp, rotmat)
    #    print '=\n',adp,'\n-------------------------------------------------\n\n\n\n\n\n'
    adp = np.array(adp).flatten().tolist()
    return [adp[0], adp[4], adp[8], adp[1], adp[2], adp[5]]


def rotate_adp2(adp, rotmat, cell):
    """
    Rotates the adp with its corresponding rotation matrix.
    """
    adp = np.matrix([[float(adp[0]), float(adp[3]), float(adp[4])],
                     [float(adp[3]), float(adp[1]), float(adp[5])],
                     [float(adp[4]), float(adp[5]), float(adp[2])]])
    rotmat = np.linalg.inv(rotmat)
    rotmatT = np.transpose(rotmat)
    Nmat = np.matrix([[1 / cell[0], 0, 0],
                      [0, 1 / cell[1], 0],
                      [0, 0, 1 / cell[2]]])
    Nmat = np.linalg.inv(Nmat)
    NmatT = np.transpose(Nmat)

    adp = np.dot(rotmat, adp)
    adp = np.dot(adp, rotmatT)

    adp = np.dot(Nmat, adp)
    adp = np.dot(adp, NmatT)

    adp = np.array(adp).flatten().tolist()
    return [adp[0], adp[4], adp[8], adp[1], adp[2], adp[5]]


def rotate_adp3(adp, rotmat, cell):
    """
    Rotates the adp with its corresponding rotation matrix.
    """
    adp = np.matrix([[float(adp[0]), float(adp[3]), float(adp[4])],
                     [float(adp[3]), float(adp[1]), float(adp[5])],
                     [float(adp[4]), float(adp[5]), float(adp[2])]])
    rotmati = np.matrix(rotmat)
    rotmatiT = np.transpose(rotmati)
    rotmat = np.linalg.inv(rotmat)

    Nmat = np.matrix([[1 / cell[0], 0, 0],
                      [0, 1 / cell[1], 0],
                      [0, 0, 1 / cell[2]]])
    Nmat = np.linalg.inv(Nmat)
    NmatT = np.transpose(Nmat)
    adp = np.dot(rotmati, adp)
    adp = np.dot(adp, rotmatiT)

    adp = np.dot(Nmat, adp)
    adp = np.dot(adp, NmatT)

    adp = np.array(adp).flatten().tolist()
    return [adp[0], adp[4], adp[8], adp[1], adp[2], adp[5]]


def rotate_list_by(coordlist, R):
    """
    Returns a list of coordinates where every position is rotated by
    the the rotation matrix 'R'.
    """
    for coord in range(len(coordlist)):
        value = np.dot(R, coordlist[coord])
        value = np.array(value).reshape(-1, ).tolist()
        coordlist[coord] = value
    return coordlist


def write_xyz(coords, name):
    filepointer = open(name, 'w')
    filepointer.write(str(len(coords)))
    filepointer.write('\n' + name + '\n')
    for line in coords:
        filepointer.write('C ')
        for coord in line:
            filepointer.write(str(coord) + ' ')
        filepointer.write('\n')
    filepointer.close()


def write_xyzqt(coords, name):
    filepointer = open(name, 'a')
    filepointer.write(name + '\n')
    for line in coords:
        filepointer.write('C ')
        for coord in line:
            filepointer.write(' ' + str(coord))
        filepointer.write('\n')
    filepointer.close()


def get_3drotation_matrix(axis, angle):
    """
    Returns the rotation matrix that rotates a vector around the given axis
    by the given angle using the "Euler-Rodrigues formula".
    """
    angle = angle  #*-1
    norm = np.linalg.norm(np.array(axis))
    if norm > 0:
        axis /= norm
        ax, ay, az = axis[0], axis[1], axis[2]
        cos, sin = np.cos(angle), np.sin(angle)
        rotmat = np.array([[cos + ax * ax * (1 - cos), ax * ay * (1 - cos) - az * sin, ax * az * (1 - cos) + ay * sin],
                           [ay * ax * (1 - cos) + az * sin, cos + ay * ay * (1 - cos), ay * az * (1 - cos) - ax * sin],
                           [az * ax * (1 - cos) - ay * sin, az * ay * (1 - cos) + ax * sin, cos + az * az * (1 - cos)]])
        return rotmat


def get_normal_vector_of_plane(p1, p2, p3):
    """
    Returns the normal vector of a plane defined by the points p1,p2 and p3.
    """
    v12 = np.array(p1) - np.array(p2)
    v13 = np.array(p1) - np.array(p3)
    nvec = np.cross(v12, v13)
    ##    print 'norm: '+str(np.linalg.norm(nvec))
    return nvec / np.linalg.norm(nvec)


def read_gaussian_coords():
    atomlist = []
    filepointer = open('g98.out', 'r')
    for line in filepointer.readlines():
        if 'Distance' in line: break
        try:
            newline = [float(i) for i in line.split(' ') if len(i) > 0]
            newline = [newline[:2], np.array(newline[3:])]
            atomlist.append(newline)
        except:
            pass
    return atomlist


def get_closest_neighbours(atomlist, neighbours=2):
    """
    Returns a list where every element is a list of three atomnames. The second and third
    names are the closest neighbours of the first names.
    The argument is a list as returned by frac_to_cart and the number of neighbours to be
    returned.
    """
    print('atomlist', atomlist)
    neighbourlist = []
    for atom in atomlist:
        listline = [atom[0][0]]
        dists = []
        distsc = []
        for partner in atomlist:
            dists.append(np.linalg.norm(atom[1] - partner[1]))
            distsc.append(np.linalg.norm(atom[1] - partner[1]))
        dists.remove(min(dists))
        for _ in range(neighbours):
            if min(dists) < 2.5:
                listline.append(atomlist[distsc.index(min(dists))][0][0])
                dists.remove(min(dists))
        #listline.append(atomlist[distsc.index(min(dists))][0][0])
        neighbourlist.append(listline)
    return neighbourlist


def calculate_distance_matrix(atomlist):
    """
    Calculates for every atom the distances to all other atoms
    in atomlist.
    Returns a list where every element is a list of all distances.
    """
    distlist = []
    for atom in atomlist:
        atomdict = {}
        for partner in atomlist:
            if not str(int(partner[0][1])) in atomdict.keys():
                atomdict[str(int(partner[0][1]))] = []
                atomdict[str(int(partner[0][1]))].append(np.linalg.norm(atom[1] - partner[1]))
            else:
                atomdict[str(int(partner[0][1]))].append(np.linalg.norm(atom[1] - partner[1]))
            atomdict[str(int(partner[0][1]))].sort()

        distlist.append(atomdict)

    return distlist


def link_atoms_by_distance(distlist1, atomlist1, distlist2, atomlist2, keys):
    """
    The function is able to identify equal atoms of one molecule in different
    coordinate systems independent of the molecule's orientaion.
    """
    hitlist = []

    for atom in distlist1:
        atomtype = int(atomlist1[distlist1.index(atom)][0][1])
        valuelist = []
        for partner in distlist2:
            partnertype = int(atomlist2[distlist2.index(partner)][0][1])
            if atomtype == partnertype:
                partnervalue = 0
                keylist = partner.keys()
                for key in keylist:
                    for element in range(len(atom[key])):
                        partnervalue += abs(atom[key][element] - partner[key][element])
            else:
                partnervalue = 9999999
            valuelist.append(partnervalue)
        minvalue = min(valuelist)
        besthit = valuelist.index(minvalue)
        hitlist.append(besthit)


def make_list_unique(seq, idfun=None):
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)

        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result


def get_influence_atoms(atomlist):
    """
    Determines the atoms defining the chemical enviroment of a given atom by checking
    their bonding partners. Only the first and second neighbours are considered.
    """
    enviromentlist = []
    trunclist = []
    neighbourlist = get_closest_neighbours(atomlist, 4)
    for neighbours in neighbourlist:
        if neighbours[0][0] == "H":
            neighbours = neighbours[:2]
        if neighbours[0][0] == "O":
            neighbours = neighbours[:3]
        trunclist.append(neighbours)
    for atom in trunclist:
        newatom = []
        for atom1partner in atom[1:]:
            for partner in trunclist:
                if partner[0] == atom1partner:
                    counter = 0

                    for atomi in partner:
                        if atomi[0] == 'H':
                            counter += 1

                    if counter < 2 or (partner[0] in atom and atom[0][0] == 'H'):
                        newatom += atom + partner[1:]

        newatom = make_list_unique(newatom)
        newatom.sort()
        enviromentlist.append(newatom)
    return enviromentlist


def link_atoms_by_distance_diff(distlist1, atomlist1, distlist2, atomlist2, keys):
    """
    The function is able to identify equivalent atoms in different molecules in different
    coordinate systems independent of the molecule's orientaion.
    """
    hitlist = []

    for atom in distlist1:
        atomtype = int(atomlist1[distlist1.index(atom)][0][1])
        valuelist = []
        for partner in distlist2:
            partnertype = int(atomlist2[distlist2.index(partner)][0][1])
            if atomtype == partnertype:
                partnervalue = 0
                keylist = partner.keys()
                for key in keylist:
                    for element in range(len(atom[key])):
                        value = abs(atom[key][element] - partner[key][element])
                        partnervalue += value
            else:
                partnervalue = 9999999
            valuelist.append(partnervalue)
        minvalue = min(valuelist)
        besthit = valuelist.index(minvalue)
        hitlist.append(besthit)


def read_multiple_coordinates(fragmentnames):
    """
    Calls read_coordinates and frac_to_cart for every path=name in fragmentnames and returns a
    dictionary where every returnvalue of frac_to_cart is keyed to its fragment name.
    """
    fragdict = {}
    for name in fragmentnames:
        path = name + '/'
        cell, pos = read_coordinates(path)
        atomlist = frac_to_cart(cell, pos)
        atomdict = {}
        for atom in atomlist:
            atomdict[atom[0][0]] = atom[1]
        fragdict[name] = atomlist
    return fragdict


##def read_coordinates(path=''):
##    """
##    Reads the cell parameters from a 'xd.mas' file and the atomic positions
##    from a 'xd.res' file.
##    The function returns a list with the cell parameters and an dictionary which
##    keys the atom name to its fractional coordinates.
##    """
##    maspointer=open(path+'xd.mas','r')
##    respointer=open(path+'xd.res','r')
##    positions={}
##    keylist=[]  #Needed to keep the atomlist order. This is important for the frequency read function.
##    for line in maspointer.readlines():
##        if 'CELL' in line:
##            cell=[float(i) for i in line.split(" ") if '.' in i]
##    for line in respointer.readlines():
##        if '(' in line and not '!' in line:
##            coords=[float(i) for i in line.split(" ") if '.' in i]
##            coords=coords[:-1]
##            key=line.split(" ")[0]
##            keylist.append(key)
##            positions[key]=coords
##    sortkeylist=[]
##    for i in range(len(keylist)):
##        j=i+1
##        for key in keylist:
##            if j==int(key[2:-1]):
##                sortkeylist.append(key)
##    return cell,positions,sortkeylist

def read_xd_master_file(path, errorpointer):
    """
    Returns the compound name and the cell parameters from a xd.mas style
    file specified by 'path'.
    """
    filepointer = open(path, 'r')
    for line in filepointer.readlines():
        if 'TITLE' in line:
            compound_name = line.partition('!')[2].lstrip().rstrip()
        if 'CELL' in line:
            cell = [float(i) for i in line.split(" ") if '.' in i]
            break
    filepointer.close()
    try:
        return compound_name, cell
    except:
        errorpointer.write(path + '\n')
        return None, None


def read_xd_parameter_file(path, sort=False):
    respointer = open(path, 'r')
    positions = {}
    keylist = []
    for line in respointer.readlines():
        if '(' in line and not '!' in line:
            coords = [float(i) for i in line.split(" ") if '.' in i]
            coords = coords[:-1]
            key = line.split(" ")[0]
            keylist.append(key)
            positions[key] = coords
    if sort:
        sortkeylist = []
        for i in range(len(keylist)):
            j = i + 1
            for key in keylist:
                number = get_number(key)
                if j == int(number):
                    sortkeylist.append(key)
    else:
        sortkeylist = keylist
    return positions, sortkeylist


def read_coordinates(path='', sort=True):
    """
    Reads the cell parameters from a 'xd.mas' file and the atomic positions
    from a 'xd.res' file.
    The function returns a list with the cell parameters and an dictionary which
    keys the atom name to its fractional coordinates.
    """
    maspointer = open(path + 'xd.mas', 'r')
    respointer = open(path + 'xd.res', 'r')

    positions = {}
    keylist = []  #Needed to keep the atomlist order. This is important for the frequency read function.
    for line in maspointer.readlines():
        if 'CELL ' in line:
            cell = [float(i) for i in line.split(" ") if '.' in i]
            break
    for line in respointer.readlines():
        if '(' in line and not '!' in line:
            coords = [float(i) for i in line.split(" ") if '.' in i]
            coords = coords[:-1]
            key = line.split(" ")[0]
            keylist.append(key)
            positions[key] = coords
    if sort:
        sortkeylist = []
        for i in range(len(keylist)):
            j = i + 1
            for key in keylist:
                number = get_number(key)
                if j == int(number):
                    sortkeylist.append(key)
    else:
        sortkeylist = keylist
    return cell, positions, sortkeylist


def get_number(atomname):
    """
    Returns the number in the brackets of an atomname.
    """
    switch = False
    number = ''
    for char in atomname:
        if char == ')':
            switch = False
        if switch:
            number += char
        if char == '(':
            switch = True
    return number


def frac_to_cart(cell, positions):
    """
    Transforms a set of given fractional coordinates to cartesian coordinates.
    Needs a list containing the cell parameters as its first argument and the dictionary
    returned by read coordinates().
    Returns a dictionary with cartesian coordinates analog to fractional dictionary.
    """
    atomlist = []
    counter = 1
    a, b, c = cell[0], cell[1], cell[2]
    alpha, beta, gamma = cell[3] / 180 * np.pi, cell[4] / 180 * np.pi, cell[5] / 180 * np.pi
    v = np.sqrt(1 - np.cos(alpha) * np.cos(alpha) - np.cos(beta) * np.cos(beta) - np.cos(gamma) * np.cos(gamma) \
                + 2 * np.cos(alpha) * np.cos(beta) * np.cos(gamma))
    transmatrix = np.matrix([[a, b * np.cos(gamma), c * np.cos(beta)],
                             [0, b * np.sin(gamma), c * (np.cos(alpha) - np.cos(beta) * np.cos(gamma)) / np.sin(gamma)],
                             [0, 0, c * v / np.sin(gamma)]])

    for atom in positions:
        coordmatrix = np.dot(transmatrix, positions[str(atom)])
        coordmatrix = np.array(coordmatrix).flatten().tolist()
        atomlist.append([])
        atomlist[-1].append([atom, atomtable[atom[0]]])
        counter += 1
        atomlist[-1].append(np.array(coordmatrix))
    return atomlist


def list_to_dict(atomlist, full=False):
    """
    Keys the coordinates of the atoms read from xd.res to the numerical part of its name.
    """
    atomdict = {}
    if full:
        for atom in atomlist:
            atomdict[atom[0]] = atom[1]
    else:
        for atom in atomlist:
            atomdict[atom[0][0]] = atom[1]
    return atomdict


#===============================================================================
# def link_atoms(gatomlist,xatomdict):
#     """
#     Returns a list of pairs of equivalten atoms.
#     """
#     linklist=[]
#     keylist=xatomdict.keys()
#     for atom in range(len(gatomlist)):
#         for key in keylist:
#             if int(key)==atom+1:
#                 linklistline=[atomlist[atom][1],xatomdict[key]]
#                 linklist.append(linklistline)
#                 break
#     return linklist
#===============================================================================

#===============================================================================
# def get_random_plane(linklist):
#     """
#     Randomly picks three atoms to build a plane from.
#     """
#     planepoints=random.sample(linklist,3)
#     gplanenorm=get_normal_vector_of_plane(planepoints[0][0],planepoints[1][0],planepoints[2][0])
#     gplanedir=np.linalg.norm(planepoints[0][0]-planepoints[1][0])
#     xplanenorm=get_normal_vector_of_plane(planepoints[0][1],planepoints[1][1],planepoints[2][1])
#     xdplanedir=np.linalg.norm(planepoints[0][1]-planepoints[1][1])
#     return gplanenorm,xplanenorm
#===============================================================================

def get_angle(v1, v2):
    """
    Returns the angle between two vectors.
    """
    return np.arccos(np.dot(v1, v2))


def read_invout_database(path):
    path += 'Invariome.out'
    filepointer = open(path, 'r')
    invnames = {}
    for line in filepointer.readlines():
        splitted = line.split(' ')
        invnames[splitted[0][:-1]] = splitted[1][:-1]
    return invnames


