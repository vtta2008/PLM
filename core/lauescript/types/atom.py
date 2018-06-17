"""
Created on Nov 1, 2013

@author: jens

Module containing definitions for atom related data types.
"""
from numpy import dot, array, matrix, cos
from numpy.linalg import eig
from numpy.linalg import norm
from lauescript.cryst.transformations import ADP_to_matrix, ADP_to_XD_list, frac2cart, cart2frac, frac2cart_ADP, cart2frac_ADP
from lauescript.cryst.transformations import frac2cart_ADP, cart2frac_ADP
from lauescript.cryst.tables import halogens, elementofnumber, proton_number
from lauescript.cryst.geom import get_framework_neighbors
import lauescript.cryst.crystgeom as cg
from lauescript.core.core import apd_exit
from lauescript.types.adp import ADP


class NoADPError(Exception):
    pass


class AtomInterface(object):
    """
    Interface definition of the Atom data type.

    Atom does currently not inherit from AtomInterface.
    """

    def __init__(self,
                 name=None,
                 cart=None,
                 frac=None,
                 element=None,
                 residue=None,
                 molecule=None):
        self.name = name
        self.cart = cart
        self.frac = frac
        self.adp = None
        self.element = element
        self.residue = residue
        self.custom_attributes = {}
        self.adp_updated = False
        self.special_position = False

    def set_custom_attribute(self, name, value):
        self.custom_attributes[name] = value

    def get_custom_attribute(self, name):
        return self.custom_attributes[name]

    def set_name(self, value):
        self.name = value

    def set_id(self, value):
        self.set_name(value)

    def set_adp_frac(self, value):
        self.adp_frac = value

    def set_adp_cart(self, value):
        self.adp_cart = value

    def set_cart(self, value):
        self.cart = value

    def set_frac(self, value):
        # self.cart = frac2cart(value, self.molecule.cell)
        self.frac = value

    def set_element(self, value):
        self.element = value

    def set_residue(self, value):
        self.residue = value

    def set_cell(self, value):
        self.cell = value

    def set_occupancy(self, value):
        self.occupancy = value

    def set_molecule(self, value):
        self.molecule = value

    def get_name(self):
        return self.name

    def get_cell(self):
        return self.cell

    def get_id(self):
        return self.get_name()

    def get_cart(self):
        return self.cart

    def get_frac(self):
        return self.frac

    def get_element(self):
        return self.element

    def get_residue(self):
        return self.residue

    def get_molecule(self):
        return self.molecule

    def get_occupancy(self):
        return self.occupancy

    def get_adp_frac(self):
        return self.adp_frac

    def get_adp_cart(self):
        return self.adp_cart

    def updated(self):
        self.adp_updated = True

    def is_updated(self):
        if self.adp_updated:
            return True

    def get_adp(self):
        if self.adp:
            return self.adp
        else:
            raise NoADPError

    def set_special(self, value):
        self. special_position = value

    def __sub__(self, other):
        pass



class ATOM(AtomInterface):
    """
    Class representing an atom. The ATOM methods
    should not be called directly. Rather the
    MOLECULE class or the DATA class should be
    used as interfaces.
    """

    def __init__(self,
                 name=None,
                 element=None,
                 cart=None,
                 frac=None,
                 molecule=None,
                 model_compound=None):
        """
        Everything that is known about the molecule can
        be specified on initilization. Otherwise the attributes
        can be set later by calling the corresponding methods.
        """
        self.tolerated = False
        self.molecule_id = None
        self.invariom_code = None
        self.invariom_code = None
        self.adp_updated = False
        self.orientation = []
        self.name = name
        self.element = element
        self.cart = cart
        self.frac = frac
        self.molecule = molecule
        self.model_compound = model_compound
        self.partner = None
        self.keep = ['cart', 'disps', 'element']
        self.invarioms = {}
        self.invariom_name = None
        self.orientation = None
        self.unique = True
        self.adp = ADP(flag='anis')
        # self.adp = {'flag': 'anis'}

        if self.molecule:
            if frac is not None and self.molecule.frac2cartmatrix is not None:
                self.frac2cart(self.molecule.frac2cartmatrix)
            elif cart is not None and  self.molecule.cart2fracmatrix is not None:
                self.cart2frac(self.molecule.cart2fracmatrix)

    def add_invariom(self, name, orientation):
        if not name in self.invarioms.keys():
            self.invarioms[name] = orientation

    def __sub__(self, atom):
        try:
            x, y, z = self.get_frac()
        except TypeError:
            return abs(norm(self.cart - atom.get_cart()))
        try:
            xx, yy, zz = atom.get_frac() + 99.5
        except TypeError:
            xx, yy, zz = array(atom.get_frac()) + 99.5
        dx = (xx - x) % 1 - 0.5
        dy = (yy - y) % 1 - 0.5
        dz = (zz - z) % 1 - 0.5
        a, b, c, alpha, beta, gamma = self.molecule.get_cell(False)
        dd = a**2*dx**2 + b**2*dy**2 + c**2*dz**2 + 2*b*c*cos(alpha)*dy*dz + 2*a*c*cos(beta)*dx*dz + 2*a*b*cos(gamma)*dx*dy
        return dd**.5
        # return norm(self.cart - atom.cart)

    def shortDistance(self, atom, cell):
        x, y, z = self.frac
        xx, yy, zz = atom.get_frac() + 99.5
        dx = (xx - x) % 1 - 0.5
        dy = (yy - y) % 1 - 0.5
        dz = (zz - z) % 1 - 0.5
        a, b, c, alpha, beta, gamma = cell
        dd = a**2*dx**2 + b**2*dy**2 + c**2*dz**2 + 2*b*c*cos(alpha)*dy*dz + 2*a*c*cos(beta)*dx*dz + 2*a*b*cos(gamma)*dx*dy
        return dd**.5

    def cartDistance(self, other):
        return norm(self.cart - other.cart)

    def set_active_invariom(self, name):
        self.invariom_name = name
        self.orientation = self.invarioms[name]

    def get_active_invariom(self):
        return self.invariom_name

    def set_invariom_atom(self, atom):
        self.invariom = atom


    def set_molecule_id(self, ID):
        """
        Sets an integer for identifying which chemical
        molecule the atom belongs to
        """
        self.molecule_id = ID

    def get_molecule_id(self):
        """
        Returns the molecule ID of the atom.
        """
        return self.molecule_id

    def strip_atom(self, keep):
        """
        Strips the atom instance of all unnecessary data
        to minimize the size of the serialized file.
        all attributes specified in the 'self.keep' list will
        be preserved.
        """
        types = [type(self.strip_atom),
                 type(self.__class__)]

        for attr in dir(self):
            if not type(getattr(self, attr)) in types:
                if any(i in attr for i in self.keep) \
                        or any(i in attr for i in keep) \
                        or attr[0:2] == '__':
                    continue
                else:
                    pass

    def __str__(self):
        return self.name

    def update_coordinates(self, frac2cartmatrix, cart2fracmatrix):
        """
        Calculates the atom's fractional respectively cartesian coordinates
        depending on what data is available.
        """
        if self.cart is not None:
            self.cart2frac(cart2fracmatrix)
        elif self.frac is not None:
            self.frac2cart(frac2cartmatrix)

    def update_H_ADP(self):
        if self.adp['flag'] == 'iso':
            return
        try:
            # self.adp['cart_meas'] = array(self.partner[0].adp['cart_meas'] * 1.2)
            self.adp['flag'] = 'riding'
            uiso = cg.Uiso(self.partner[0].adp['cart_meas'] * 1.2)
            self.adp['cart_meas'] = array([uiso, uiso, uiso, 0, 0, 0])
        except:
            apd_exit('error in ATOM.update_H_ADP')
            self.adp['cart_meas'] = None

    def frac2cart(self, matrix):
        """
        Calculate the atom's cartesian coordinates.
        """
        self.cart = array(dot(matrix, self.frac).tolist()[0])

    def cart2frac(self, matrix):
        """
        Calculates the atom's fractional coordinates.
        """
        self.frac = array(dot(matrix, self.cart).tolist()[0])

    def give_adp(self, key, value, error=None):
        if value is not None:
            self.adp[key] = array(value)
            if type(value) == float:
                self.adp['flag'] = 'iso'
            if error:
                self.adp[key + '_error'] = array(error)
        else:
            self.adp['flag'] = 'riding'

    def give_Uiso(self, value):
        self.adp['iso_meas'] = value

    def get_unique_neighbors(self):
        """
        Determines 2 unique atoms in the enviroment of the atom.
        """

        code_list = []

        for i in range(len(self.invariom_code) / 19):
            neighbor_code = self.invariom_code[i * 19:(i + 1) * 19]

            neighbor_code = neighbor_code[:12] + neighbor_code[13:]
            code_list.append(neighbor_code)
        unique_code_list = []
        for i in range(2):
            for code in reversed(code_list):
                if code_list.count(code) == 1:
                    full_code = code[:12] + '0' + code[12:]
                    unique_code_list.append(full_code)
                    code_list.remove(code)
                    break
        return unique_code_list

    def give_code_atom_links(self, links):
        """
        Sets the code_atom_link attribute uses it to
        create the invariom_fragment attribute.
        """
        self.code_atom_links = links
        self.invariom_fragment = [self] + [atom for atom in self.molecule.atoms if atom.name in links.values()]

    def get_prochirality(self):
        """
        Determines whether its necessary to differentiate between
        two sides of the molecule. For example Protons in R-O-CH2-N-R.

        If the atom is prochiral, the side (re/si) is determined.
        """
        if self.element in halogens:
            self.prochiral = False
            return
        if self.invariom_name[1] is '@':
            self.prochiral = False
            if self.invariom_name[2] is '3':
                print('Warning! Approximating ADP in 3 membered ring for atom {}.'.format(self.name))
            return
        if not get_framework_neighbors(atom=self, useH=True):
            self.prochiral = False
            return
        neighbor0 = get_framework_neighbors(self, useH=True)
        if len(neighbor0) > 1:
            self.prochiral = False
            return
        neighbor0 = neighbor0[0]
        neighbors = [atom.element for atom in get_framework_neighbors(neighbor0,
                                                                          useH=True) if not atom == self]
        if any(self.element == i for i in neighbors):
            neighbors.remove(self.element)
            if not any(self.element == i for i in neighbors):
                if len(neighbors) > 1:
                    if not neighbors[0] == neighbors[1]:
                        self.prochiral = True
                        pos1 = self.cart
                        pos2 = neighbor0.cart
                        pos3 = cg.get_closest_atom_of_element(self.element, neighbor0, exclude=self).cart
                        plane_vector = cg.get_normal_vector_of_plane(pos1, pos2, pos3)
                        ref_element = max([proton_number[i] for i in neighbors])
                        ref_atom = cg.get_closest_atom_of_element(elementofnumber[ref_element], neighbor0,
                                                                  exclude=self)
                        ref_vector = neighbor0.cart - ref_atom.cart
                        ref_vector /= norm(ref_vector)
                        if dot(ref_vector, plane_vector) > 0:
                            self.side = 're'
                        else:
                            self.side = 'si'
                        return
        self.prochiral = False

    def get_distances(self):
        """
        Calculates all intramolecular distances.
        """
        if not self.molecule:
            print('ERROR in atom.get_distances(): Atom {} is not part of ' \
                  'a molecule.'.format(self.name))
            exit()
        neighbors = []
        for atom2 in self.molecule.atoms:
            if not self == atom2:
                try:
                    neighbors.append((atom2, self-atom2))
                except KeyError:
                    neighbors.append((atom2, self - atom2))
        neighbors = sorted(neighbors, key=lambda value: value[1])
        self.partner = [neighbor[0] for neighbor in neighbors]


    def averageADP(self):
        cartAdp = array([0]*6)
        for atom in get_framework_neighbors(self):
            cartAdp += atom.adp['cart_int']
        self.adp['cart_int'] = cartAdp

    def transfer_adp(self):
        """
        Transfers the ADP of the invarioms to the atoms of interest by
        rotating the invraiom's ADP as defined by the orientation vectors.
        """
        if self.tolerated:
            return self
            # adp = array([0]*6)
            # for atom in get_framework_neighbors(self):
            #     adp +=

        if not self.invariom:
            print(self.invariom, self, 'Error in atom.transfer_adp()')
            exit()
        elif self.orientation[0] is not None and len(self.invariom.orientation) == 2 and len(
                self.orientation) == 2:
            if self.prochiral and not self.molecule.daba:
                if not self.side is self.invariom.side:
                    self.orientation[0] *= -1
                    self.orientation[1] *= -1
            cg.rotate_3D(self, self.invariom)
            # self.turn()
        else:
            print('Warning: Using U_eq for {}'.format(self.name))
            Uiso = cg.Uiso(self.invariom.adp['cart_int'])
            self.adp['cart_int'] = array([Uiso, Uiso, Uiso, 0, 0, 0])

    def transfer_matched_ADP(self, matched_atom, transformation):
        """
        Transfers the ADP from 'matched_atom' to self by
        applying the transformation matrix 'transformation'.
        """
        self.adp['cart_int'] = ADP_to_XD_list(
            dot(dot(transformation.T, ADP_to_matrix(matched_atom.adp['cart_int'])), transformation))
        if any([num > 1 or num < -1 for num in self.adp['cart_int']]):
            print('Warning!: atom.py: {} ADP too large. Using average of all values.'.format(self.name))
            adps = [atom.invariom.adp['cart_int'] for atom in self.molecule.atoms if
                    all([num < 1 or num > -1 for num in self.adp['cart_int']])]
            self.adp['cart_int'] = sum(adps) / len(adps)

    def add_disps(self, freq, disps):
        """
        Adds the polarisation vectors for every internal vibration
        frequency to the atom.
        """
        # print freq, disps
        # raw_input()
        try:
            self.disps[str(freq)] = disps
        except:
            self.disps = {str(freq): disps}

    def turn(self):
        return
        adp = self.adp['cart_int']
        adp = matrix([[float(adp[0]), float(adp[3]), float(adp[4])],
                      [float(adp[3]), float(adp[1]), float(adp[5])],
                      [float(adp[4]), float(adp[5]), float(adp[2])]])
        w, v = eig(adp)

        keep = w.tolist().index(min(w))
        vectors = [array((w[i] * v[:, i]).flatten().tolist()[0]) for i in range(3)]
        # print(vectors)

        value = 0
        for i in range(3):
            if not i == keep:
                value += w[i]
        value *= 0.5
        for i in range(3):
            if not i == keep:
                w[i] = value
        v = [array((w[i] * v[:, i]).flatten().tolist()[0]) for i in range(3)]
        # print vectors
        adp = matrix([[v[0][0], v[1][0], v[2][0]],
                      [v[0][1], v[1][1], v[2][1]],
                      [v[0][2], v[1][2], v[2][2]]])
        adp = (adp + adp.T) / 2
        # print adp

        w, v = eig(adp)

        keep = w.tolist().index(min(w))
        vectors = [array((w[i] * v[:, i]).flatten().tolist()[0]) for i in range(3)]
        # print vectors

    def iter_bound_atoms(self):
        return get_framework_neighbors(self)


    def normalize(self):
        """
        Moves the atom in the unit cell if necessary
        :return: None
        """
        self.set_frac([frac % 1 if frac > 0 else (1 + frac)%1 for frac in self.frac])

    def set_frac(self, frac):
        self.frac = frac
        self.cart = frac2cart(frac, self.molecule.get_cell())

    def tolerate(self):
        self.tolerated = True

    def isTolerated(self):
        return self.tolerated














