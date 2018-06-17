from __future__ import print_function
"""
Created on 01.04.2014

@author: Jens Luebben

Module for generating invariom names from molecular geometry data.
Use the 'get_invariom_names' function to get a generator that iterates
over several threshold sets.
Use the 'get_invariom_names_simple' functions if no iterator behavior
is desired.
"""
import numpy as np
from numpy.linalg import norm
from sys import stdout
from string import ascii_letters
from lauescript.cryst.rings import find_planar_rings
from lauescript.cryst.transformations import cart2frac
from sklearn.neighbors import NearestNeighbors


covalence_radius = {'H': .37, 'He': .0, 'Li': 1.23, 'Be': .90, 'B': .80, 'C': .77,
                    'N': .74, 'O': .71, 'F': .72, 'Ne': 0., 'Na': 1.54, 'Mg': 1.36,
                    'Al': 1.18, 'Si': 1.11, 'P': 1.06, 'S': 1.02, 'Cl': .99, 'Ar': 0.,
                    'K': 2.03, 'Ca': 1.74, 'Sc': 1.44, 'Ti': 1.32, 'V': 1.22,
                    'Cr': 1.18, 'Mn': 1.17, 'Fe': 1.17, 'Co': 1.16, 'Ni': 1.15,
                    'Cu': 1.17, 'Zn': 1.25, 'Ga': 1.26, 'Ge': 1.22, 'As': 1.20,
                    'Se': 1.16, 'Br': 1.14, 'Kr': 0.,
                    'Rb': 2.18}

electro_negativ = {'H': 2.20, 'He': 5.50, 'Li': .97, 'Be': 1.47, 'B': 2.01, 'C': 2.50,
                   'N': 3.07, 'O': 3.50, 'F': 4.40, 'Ne': 4.80, 'Na': 1.01, 'Mg': 1.23,
                   'Al': 1.47, 'Si': 1.74, 'P': 2.06, 'S': 2.44, 'Cl': 2.83, 'Ar': 3.20,
                   'K': .91, 'Ca': 1.04, 'Sc': 1.20, 'Ti': 1.32, 'V': 1.45,
                   'Cr': 1.56, 'Mn': 1.60, 'Fe': 1.64, 'Co': 1.70, 'Ni': 1.75,
                   'Cu': 1.75, 'Zn': 1.66, 'Ga': 1.82, 'Ge': 2.02, 'As': 2.20,
                   'Se': 2.48, 'Br': 2.74, 'Kr': 2.90,
                   'Rb': .89}

electron_number = {'H': '001', 'He': '002', 'Li': '003', 'Be': '004', 'B': '005', 'C': '006', 'N': '007', 'O': '008',
                   'F': '009', 'Ne': '010', 'Na': '011', 'Mg': '012', 'Al': '013', 'Si': '014', 'P': '015',
                   'S': '016', 'Cl': '017', 'Ar': '018', 'K': '019', 'Ca': '020', 'Sc': '021', 'Ti': '022',
                   'V': '023', 'Cr': '024', 'Mn': '025', 'Fe': '026', 'Co': '027', 'Ni': '028', 'Cu': '029',
                   'Zn': '030', 'Ga': '031', 'Ge': '032', 'As': '033', 'Se': '034', 'Br': '035', 'Kr': '036'}

tsm = 0.0847,
tmd = 0.184,
tdt = 0.27,

v = False

def get_invariom_names(names,
                       cart=None,
                       frac=None,
                       cell=None,
                       thresholds=None,
                       dictionary=True,
                       orientations=False,
                       compounds=False,
                       corrections=None,
                       verbose=True,
                       output=None,
                       dynamic=False,
                       classic=True,
                       newH=True,
                       planarityThreshold=.1):
    """
    Generator that returns the desired output once for every set
    of threshold values.

    :param names: is mandatory and must be a list of unique
    strings identifying each atom.

    Either the argument 'cart' or both the arguments 'frac' and 'cell'
    are mandatory.
    :param cart: must be a list of numpy arrays of the length
    three. Every list element represents an atom at a position in
    cartesian space. The list indices connect the corrdinate list
    to the name list.
    :param frac: must be an equivalent list with fractional coordinates.
    :param cell: must be a list of length six representing the cell paramters
    a, b, c, alpha, beta, gamma.

    :param thresholds: must be a list. Every list element must be a list of length
    three where each element represents a threshold for differentiating
    bond orders. The first value distinguishes single bonds from meso bonds,
    the second one meso bonds from double bonds and the third one double
    bonds from triple bonds.

    :param dictionary: must be a boolean specifying whether the invariomnames
    should be returned as a list sorted the same way as the 'names' list or
    as a dictionary where every invariom name is keyed to its name
    provided by the 'names' argument.

    :param compounds: must be a filepointer to the 'APD_MAP.txt' file int the
    database directory or None. If not None a dictionary is returned keying
    the name of the corresponding model compound to the invariom names.

    :param orientations: specifies whether a dictionary keying two orientation
    vectors to each atom name should be returned after the invariom name
    list/dictionary. Each set of orientation vectors uniquely defines
    an invarioms orientation in cartesian space.

    :param corrections: must be a filepointer to a file opened in 'read' mode
    containing empirical corrections of invariom names. See the file
    'empirical_corrections.txt' in the apd.data package for more
    information.

    :param verbose: specifies wheter any feedback should be given. The feedback
    is printed to sys.stdout by default.

    :param output: can be used to redirect the output produced when 'verbose' is
    True. The parameter can be every object that implements the 'write'
    method.

    :param dynamic: must be a boolean that can be used to set a standard set
    of three threshold values that are used to determine bond orders.
    The standard values can be overwritten with the 'thresholds' argument.

    :param classic: must be a boolean. If True, double bonded atoms do not
    imply that the next neighbor must also be considered.

    :return: The return value depends on the chosen parameters but is always
    a list with the same order. The first element contains the list/dict of
    invariom names. The following elements are present if the corresponding
    parameters are set to 'True'.
    """
    if verbose:
        global v
        v = True
    if not output:
        output = stdout
    global printer, classic_names
    printer = output
    classic_names = classic

    if dynamic:
        thresholds = [[0.0827, 0.184, 0.27], [0.0927, 0.194, 0.27], [0.07, 0.160, 0.27]]
    elif not thresholds:
        thresholds = [[0.0827, 0.0847, 0.27]]

    global invfilter
    invfilter = CorrectionFilter(corrections)

    generator = InvariomGenerator(thresholds)
    if cart:
        generator.populate(names, cart, system='cart', cell=cell, planarityThreshold=planarityThreshold)
    elif frac:
        generator.populate(names, frac, system='frac', cell=cell, planarityThreshold=planarityThreshold)

    if compounds:
        invariom_map = compounds.readlines()

    returnlists = []
    for l in range(len(thresholds)):
        returnlist = []
        name_dictionary = {}
        orientation_dictionary = {}
        for i, j, k, atom in generator.harvest(l):
            if newH:
                element = Atom.generateElement(i)
                if element == 'H':
                    j = newAge(generator.get_invariom_name_of(i, l), atom, generator, l)
            name_dictionary[i] = j
            orientation_dictionary[i] = k

        if dictionary:
            returnlist.append(name_dictionary)
        if orientations:
            returnlist.append(orientation_dictionary)
        if compounds:
            returnlist.append(get_compounds(invariom_map, name_dictionary.values()))
        returnlists.append(returnlist)
    for returnlist in returnlists:
        yield returnlist


def newAge(invariomName, atom, generator, i):
    # try:
        heavyAtom = list(atom.get_bonds().values())[0].get_partner(atom)
        return '&'.join([invariomName, generator.get_invariom_name_of(heavyAtom.get_name(), i)])
    # except IndexError:
    #     return invariomName
    # return '&'.join(['H', generator.get_invariom_name_of(heavyAtom.get_name(), i)])


def truncate_neighbors(invariom_name):
    """
    Removes potential next neighbors from the invariom name if
    the invariom name fits certain criteria.
    :param invariom_name: string representing an invariom name.
    :return: string representing the truncated invariom name.
    """
    remove_list = ['2c[', '2n[']
    if invariom_name.startswith('O2c'):
        return invariom_name
    for key in remove_list:
        invariom_name = _truncate_neighbor(invariom_name, key)
    return invariom_name


def _truncate_neighbor(invariom_name, key):
    while True:
        if not key in invariom_name:
            return invariom_name

        i = invariom_name.index(key)
        if all([char in invariom_name[i:] for char in ['[', ']']]):
            j = invariom_name[i:].index('[')
            k = invariom_name[i:].index(']')
            part1 = invariom_name[:i + j]
            invariom_name = part1 + invariom_name[i + k + 1:]
            # ===========================================================================
            # else:
            # return invariom_name
            #===========================================================================


def get_invariom_names_simple(names,
                              cart=None,
                              frac=None,
                              cell=None,
                              thresholds=None,
                              dictionary=True,
                              orientations=False,
                              compounds=False,
                              corrections=None,
                              verbose=True,
                              output=None,
                              dynamic=False,
                              classic=False,
                              newH=True,
                              planarityThreshold=.1):
    """
    Generator that returns the desired output once for every set
    of threshold values.

    :param names: is mandatory and must be a list of unique
    strings identifying each atom.

    Either the argument 'cart' or both the arguments 'frac' and 'cell'
    are mandatory.
    :param cart: must be a list of numpy arrays of the length
    three. Every list element represents an atom at a position in
    cartesian space. The list indices connect the corrdinate list
    to the name list.
    :param frac: must be an equivalent list with fractional coordinates.
    :param cell: must be a list of length six representing the cell paramters
    a, b, c, alpha, beta, gamma.

    :param thresholds: must be a list. Every list element must be a list of length
    three where each element represents a threshold for differentiating
    bond orders. The first value distinguishes single bonds from meso bonds,
    the second one meso bonds from double bonds and the third one double
    bonds from triple bonds.

    :param dictionary: must be a boolean specifying whether the invariomnames
    should be returned as a list sorted the same way as the 'names' list or
    as a dictionary where every invariom name is keyed to its name
    provided by the 'names' argument.

    :param compounds: must be a filepointer to the 'APD_MAP.txt' file int the
    database directory or None. If not None a dictionary is returned keying
    the name of the corresponding model compound to the invariom names.

    :param orientations: specifies whether a dictionary keying two orientation
    vectors to each atom name should be returned after the invariom name
    list/dictionary. Each set of orientation vectors uniquely defines
    an invarioms orientation in cartesian space.

    :param corrections: must be a filepointer to a file opened in 'read' mode
    containing empirical corrections of invariom names. See the file
    'empirical_corrections.txt' in the apd.data package for more
    information.

    :param verbose: specifies wheter any feedback should be given. The feedback
    is printed to sys.stdout by default.

    :param output: can be used to redirect the output produced when 'verbose' is
    True. The parameter can be every object that implements the 'write'
    method.

    :param dynamic: must be a boolean that can be used to set a standard set
    of three threshold values that are used to determine bond orders.
    The standard values can be overwritten with the 'thresholds' argument.

    :param classic: must be a boolean. If True, double bonded atoms do not
    imply that the next neighbor must also be considered.

    :return: The return value depends on the chosen parameters but is always
    a list with the same order. The first element contains the list/dict of
    invariom names. The following elements are present if the corresponding
    parameters are set to 'True'.
    """
    if verbose:
        pass
    if not output:
        output = stdout
    global printer, classic_names
    printer = output
    classic_names = classic

    if dynamic:
        thresholds = [[0.0827, 0.0847, 0.27], [0.0927, 0.0947, 0.27], [0.049, 0.0847, 0.27]]
    elif not thresholds:
        thresholds = [[0.0827, 0.0847, 0.27]]

    global invfilter
    invfilter = CorrectionFilter(corrections)

    generator = InvariomGenerator(thresholds)
    if cart:
        generator.populate(names, cart, system='cart', planarityThreshold=planarityThreshold)
    elif frac:
        generator.populate(names, frac, system='frac', cell=cell, planarityThreshold=planarityThreshold)

    if compounds:
        invariom_map = compounds.readlines()

    returnlists = []
    for l in range(len(thresholds)):
        returnlist = []
        name_dictionary = {}
        orientation_dictionary = {}
        for i, j, k, _ in generator.harvest(l):
            # ===================================================================
            # try:
            # name_dictionary[i].append(j)
            #     orientation_dictionary[i].append(k)
            #     #===============================================================
            #     # if not  name_dictionary[i][0]==name_dictionary[i][1]:
            #     #     print i,name_dictionary[i][0],j
            #     #===============================================================
            #===================================================================

            #===================================================================
            # except:
            #===================================================================

            #===================================================================
            # if classic:
            #     j=truncate_neighbors(j)
            #===================================================================
            name_dictionary[i] = j
            orientation_dictionary[i] = k

        if dictionary:
            returnlist.append(name_dictionary)
        if orientations:
            returnlist.append(orientation_dictionary)
        if compounds:
            invariom_map = compounds.readlines()
            returnlist.append(get_compounds(invariom_map, name_dictionary.values()))
        returnlists.append(returnlist)
        # =======================================================================
        # yield returnlist
        # =======================================================================
    if not dynamic:
        return returnlists[0]
    else:
        return returnlists


def get_compounds(invariom_map, invariom_names):
    """
    Links every invariom name to the name of the 'smallest'
    model compound that it occurs in.

    :param invariom_map: filepointer to the 'APD_MAP.txt' file
    in the database directory.

    :param invariom_names: list of invariom names ordered corresponding
    to the atom names list passed to the interface functions.

    :return: Dictionary keying model compound names to their
    corresponding invariom names.
    """
    compounds_dict = {}
    for line in invariom_map:
        line = line.partition(':')
        if any([line[0] == name for name in invariom_names]):
            compounds_dict[line[0]] = line[2].rstrip('\n')

    missing = []
    for name in invariom_names:
        if not name in compounds_dict.keys():
            missing.append(name)
    if len(missing) > 0 and v:
        printer('\nError: Not all invarioms found in Database.')
        for miss in missing:
            printer(miss)
        printer()
    return compounds_dict


class InvariomGenerator(object):
    """
    Class for generating invariom names and orientations
    from atomic positions.
    """

    def __init__(self, thresholds=None):
        """
        Initializes the InvariomGenerator.
        :param thresholds: must
        be a list where each element is a list of three floats.
        """
        self.tms = None
        if not thresholds:
            self.thresholds = [[0.0827, 0.0847, 0.27]]
        else:
            self.thresholds = thresholds
        self.neigh = NearestNeighbors(5, 0.4)
        self.names = None
        self.dist_result = None
        self.i = 0
        self.bonds = {}
        self.atoms = {}
        self.angles = {}
        self.invariom_names = {}
        self.orientations = {}
        self.anglehashes = []
        self.tsm = None
        self.tmd = None
        self.tdt = None

    def get_invariom_name_of(self, atom_name, i):
        return self.invariom_names[atom_name][i]

    def next(self):
        """
        Loads the next set of thesholds. Used for
        dynamic thresholds.
        """
        self.tsm = self.thresholds[self.i][0]
        self.tmd = self.thresholds[self.i][1]
        self.tdt = self.thresholds[self.i][2]
        self.i += 1

    def create_bond(self, atom1, atom2):
        """
        Creates a bond between atom1 and atom2.
        If the bond distance is not physically reasonable,
        the bond is deleted.
        :param atom1: Atom instance.
        :param atom2: Atom instance.
        """
        bond = Bond(atom1, atom2, self)
        if bond.get_id() in self.bonds or bond.no_bond():
            del bond
        else:
            self.bonds[bond.get_id()] = bond
            atom1.add_bond(bond)
            atom2.add_bond(bond)

    def create_atom(self, name, coord, system, cell):
        """
        Creates an atom based on the name and its coordinates.
        :param name: String representing the atom's name.
        :param coord: List of three floats representing the
        atom's position.
        :param system: String specifying whether the coordinate
        system is 'frac' for fractional or 'cart' for cartesian.
        :param cell: List of six floats representing cell parameters
        of the format [a, b, c, alpha, beta, gamma]
        """
        atom = Atom(name, cell)
        if system == 'cart':
            atom.set_cart(coord)
            atom.frac = cart2frac(coord, cell)
        elif system == 'frac':
            atom.set_frac(coord, cell)
        # =======================================================================
        # else:
        # print 'Error'
        #     exit()
        #=======================================================================
        self.atoms[atom.get_name()] = atom

    def populate(self, names, coordinates, system='cart', cell=None, planarityThreshold=.1):
        """
        Populates the generator instance with atoms and carries
        out all necessary computations.

        :param names: List of strings where each name represents an
        atom's name.
        :param coordinates: List of coordinate data containing of
        a list of six floats each.
        :param system: String specifying whether the coordinate
        system is 'frac' for fractional or 'cart' for cartesian.
        :param cell: List of six floats representing cell parameters
        of the format [a, b, c, alpha, beta, gamma]
        """
        self.names = names
        if system == 'frac' and not cell:
            print('invsting2.py: Error. Cell missing.')
            exit()

        if system == 'frac':
            samples2 = [cart2frac(i, cell) for i in coordinates]
        else:
            samples2 = coordinates
        samples = coordinates

        dist_results = []
        for pos1 in samples2:
            dists = []
            for i, pos2 in enumerate(samples2):
                d = Bond.dist(pos1, pos2, cell)
                dists.append((d, i))
            dists = sorted(dists, key=lambda pair: pair[0])
            dist_results.append([d[1] for d in dists])


        # self.neigh.fit(samples)
        # for n in names:
        #     print(n)
        # self.dist_result = self.neigh.kneighbors(samples, len(samples), return_distance=False)
        self.dist_result = dist_results
        # print(self.dist_result)

        for _ in range(len(self.thresholds)):
            self.next()
            self.atoms = {}
            for i, name in enumerate(names):
                self.create_atom(name, coordinates[i], system, cell)
            self.generate_bonds()
            self.generate_angles()
            self.find_rings(planarityThreshold, cell)
            self.grow_enviroments()
            for name, atom in self.atoms.items():
                if invfilter.correct(atom.enviroment):
                    orientation = [None, None]
                else:
                    orientation = atom.get_orientation()
                try:
                    self.invariom_names[name].append(atom.get_invariom_name())
                    self.orientations[name].append(orientation)
                except KeyError:
                    self.invariom_names[name] = [atom.get_invariom_name()]
                    self.orientations[name] = [orientation]

    def harvest(self, i):
        """
        Interface for accessing the computed data.

        :param i: Integer defining which set of parameters will be
        returned.
        """
        for key, value in self.invariom_names.items():
            yield key, value[i], self.orientations[key][i], self.atoms[key]

    def generate_bonds(self):
        """
        Iterates over all atom pairs for bond generation
        between them.
        """
        self.bonds = {}

        for atoms in self.dist_result:
            for neighbor in atoms[1:]:
                # printer('{}  -  {}'.format(atom_list[atoms[0]].get_name(), atom_list[neighbor].get_name()))
                self.create_bond(self.atoms[self.names[atoms[0]]], self.atoms[self.names[neighbor]])

    def generate_angles(self):
        """
        Iterates of all bond pairs for each atom to
        instantiate all angles within the molecule.
        """
        self.anglehashes = []
        for atom in self.atoms.values():
            for bond1, bond2 in atom.iter_bond_pairs():
                angle = Angle(atom, bond1.get_partner(atom), bond2.get_partner(atom))
                self.angles[angle.get_id()] = angle
                self.anglehashes.append(angle.hash)
                atom.add_angle(angle)

    def find_rings(self, planarityThreshold, cell):
        """
        Uses the RingFinder class to find rings in the molecule
        and communicates the obtained information to the
        corresponding atoms and bonds.
        """
        # finder = RingFinder(self.angles, self.anglehashes)
        # rings = finder.harvest()
        planarityThreshold = 9999999
        # print(self.dist_result)
        rings = find_planar_rings([self.atoms[name] for name in self.names], cell, self.dist_result, planarityThreshold)
        # print(rings)
        for ring in rings:
            length = len(ring)
            IDs = []
            for atom1 in ring:
                ring_id = '{}'.format(':'.join(sorted(ring)))
                self.atoms[atom1].add_ring(length, ring_id)
                for atom2 in ring:
                    if not atom1 == atom2:
                        ID = '{}{}'.format(*sorted([atom1, atom2]))
                        if not ID in IDs:
                            if ID in self.bonds.keys():
                                IDs.append(ID)
                                self.bonds[ID].add_ring(length)
        for atom in self.atoms.values():
            atom.update_ring_data()

    def grow_enviroments(self):
        """
        Triggers the grow_enviroment function for all atoms.
        """
        for atom in self.atoms.values():
            atom.grow_enviroment()

    def get_tsm(self):
        """
        Returns the Threshold_Single_Meso.
        :return: Float threshold single meso.
        """
        return self.tsm

    def get_tmd(self):
        """
        Returns the Threshold_Meso_Double.
        :return: Float threshold meso double.
        """
        return self.tmd

    def get_tdt(self):
        """
        Returns the Threshold_Double_Triple.
        :return: Float threshold double triple.
        """
        return self.tdt


class Bond(object):
    """
    Class representing a chemical bond.
    """

    def __init__(self, atom1, atom2, controller):
        """
        Initializes the bond instance. The bond is created
        between atom1 and atom2.

        :param atom1: Atom instance.
        :param atom2: Atom instance.
        :param controller: must be an
        instance of the InvariomGenerator class.
        """
        self.order = None
        self.priority = None
        self.id = None
        self.xi = None
        self.controller = controller
        self.rings = []
        self.at = False
        self.too_far = True
        self.atom1 = atom1
        self.atom2 = atom2
        self.set_id()
        self.grow = True
        self.length = Bond.dist(atom1.frac, atom2.frac, atom1.cell)
        if self.length < covalence_radius[atom1.get_element()] + covalence_radius[atom2.get_element()] + .1:
            self.too_far = False
            self.set_xi()
            self.set_bond_order()
            # if 'C(1)_2' in [self.atom1.get_name(), self.atom2.get_name()]:
            #     print(sorted([self.atom1.get_name(), self.atom2.get_name()]))
        else:
            pass

    @staticmethod
    def dist(pos1, pos2, cell):
        x, y, z = pos1
        try:
            xx, yy, zz = pos2 + 99.5
        except TypeError:
            xx, yy, zz = np.array(pos2) + 99.5
        dx = (xx - x) % 1 - 0.5
        dy = (yy - y) % 1 - 0.5
        dz = (zz - z) % 1 - 0.5
        a, b, c, alpha, beta, gamma = cell
        alpha = alpha / 180 * np.pi
        beta = beta / 180 * np.pi
        gamma = gamma / 180 * np.pi
        dd = a ** 2 * dx ** 2 + b ** 2 * dy ** 2 + c ** 2 * dz ** 2 + 2 * b * c * np.cos(
            alpha) * dy * dz + 2 * a * c * np.cos(beta) * dx * dz + 2 * a * b * np.cos(gamma) * dx * dy
        return dd ** .5

    def get_partner(self, atom):
        """
        Returns the atom that is used to define the bond and
        is not equal to 'atom'.

        :param atom: Atom instance whose neighbor is requested.

        :return: Atom instance that is the bond neighbor of 'atom'.
        """
        if atom == self.atom1:
            return self.atom2
        return self.atom1

    def set_id(self):
        """
        Generates an unique ID from the labels of atom1 and atom2.
        """
        namelist = sorted([i.name for i in [self.atom1, self.atom2]])
        self.id = '{}{}'.format(*namelist)

    def get_id(self):
        """
        :return: string representing the bond's unique ID.
        """
        return self.id

    def no_bond(self):
        """
        :return: Boolean: True if the distance between atom1 and atom2 is
        too large to represent a chemical bond.
        """
        if self.too_far:
            return True
        return None

    def set_xi(self):
        """
        Calculates Xi.
        """
        self.xi = (
            float(covalence_radius[self.atom1.get_element()]) + float(covalence_radius[self.atom2.get_element()]) -
            (0.08 * float(
                abs(electro_negativ[self.atom1.get_element()] - electro_negativ[
                    self.atom2.get_element()]))) - self.length)

    def set_bond_order(self):
        """
        Determines the bond order based on the thresholds
        provided by the InvariomGenerator. The bond gets also
        assigned a priority based on the bond order.

        The priority is used to realize the correct sorting
        of the invariom string.
        """
        if self.xi < self.controller.get_tsm():
            self.order = '1'
            self.priority = '000'
            self.grow = False
        elif self.xi < self.controller.get_tmd():
            self.order = '~'
            self.priority = '790'
            self.grow = True
        elif self.xi < self.controller.get_tdt():
            self.order = '2'
            self.priority = '800'
            self.grow = True
        else:
            self.order = '3'
            self.priority = '900'
        if self.atom1.get_element() == 'H' or self.atom2.get_element() == 'H':
            self.order = '1'
            self.priority = '000'
            self.grow = True
        if self.atom1.get_element() == 'S' or self.atom2.get_element() == 'S':
            self.grow = True
        if self.atom1.get_element() == 'P' or self.atom2.get_element() == 'P':
            self.grow = True

    def get_bond_priority(self):
        """
        :return: String representing the bond's priority.
        """
        return self.priority

    def does_grow(self):
        """
        :return: Boolean: True if the invariom definition requires
        the consideration of next next neighbors for a
        bond of this type.
        """
        if self.grow:
            return True
        return None

    def get_invariom_char(self):
        """
        :return: String: invariom string representation of the
        bond.
        e.g.: '3' for a triple bond
              '#6' for a bond in a six membered ring.
        """
        return self.order

    def add_ring(self, size):
        """
        Reevaluates the bonds properties based on the fact
        that the bond is part of a 'size' membered ring.

        :param size: Integer representing the number of ring atoms.
        """
        self.grow = True
        self.rings.append(str(size))
        self.rings = sorted(self.rings, reverse=True)
        self.priority = '{p:{f}<3}'.format(p=''.join(self.rings), f='0')
        self.order = '#' + self.priority.rstrip('0')

    def is_ring_bond(self):
        """
        :return: Boolean: True if the bond is part of a ring system.
        """
        if len(self.rings) > 0:
            return True

    def set_at_bond(self):
        """
        Flags the Bond as a bond between an atom that is
        part of a ring system and an atom that is not.
        """
        self.at = True
        self.priority = self.priority[0] + '5' + self.priority[2]

    def get_invariom_char_noring(self, atom):
        """
        Returns the correct string representation when
        the bond is connected to one atom that is part
        of a ring at to one atom that is not.

        :param atom: Atom instance defining whether the bond to
        this atom is an @-bond.

        :return: returns the correct string representing the atom
        in the invariom name.
        """
        if self.at:
            return '@' + ''.join(atom.get_rings())
        else:
            return self.order

    def is_at_bond(self):
        return self.at


class Atom(object):
    """
    Class for representing an atom.
    """
    f2c_matrix = None
    
    @staticmethod
    def generateElement(atomName):
        element = []
        for char in atomName:
            if not char in ascii_letters:
                break
            element.append(char)
        element = ''.join(element).capitalize()
        for _ in range(10):
            if not element in electron_number.keys():
                element = element[:-1]
            else:
                break
        return element.capitalize()

    def __init__(self, name, cell,  element=None):
        """
        Initializes the Atom instance.
        :param name: must be an unique
        string defining the atom.
        :param element: is its chemical element.
        If no element is given. The element is estimated by interpreting
        the atom name.
        """
        self.cart = None
        self.frac = None
        self.cell = cell
        self.enviroment = None
        self.get_id = self.get_name
        self.name = name
        self.grow = False
        self.rings = []
        self.ring_ids = []
        self.invariom_name = None
        self.invariom_code = None
        self.prefix = ''
        self.bonds = {}
        self.angles = {}
        if not element:
            self.element = Atom.generateElement(self.name)
        #     element = []
        #     for char in self.name:
        #         if not char in ascii_letters:
        #             break
        #         element.append(char)
        #     element = ''.join(element).capitalize()
        #     for _ in range(10):
        #         if not element in electron_number.keys():
        #             element = element[:-1]
        #         else:
        #             break
        # self.element = element.capitalize()
        self.priority = electron_number[self.element]

    def set_cart(self, cart):
        """
        Adds information about the atoms position in
        cartesian coordinates.

        :param cart: List of three floats representing the
        atom's position in cartesian coordinates.
        """
        self.cart = np.array(cart)

    def set_frac(self, frac, cell):
        """
        Uses the cell and the fractional coordinates to
        set the atoms position in cartesian coordinates.

        :param frac: List of three floats representing the
        atom's position in fractional coordinates.
        :param cell: List of 6 floats representing the cell
        parameter: [a, b, c, alpha, beta, gamma]
        """
        # if not Atom.f2c_matrix != None:
        if Atom.f2c_matrix is None:
            Atom.f2c_matrix = self._get_frac2cart_matrix(cell)
        self.cart = np.array(self._frac2cart(frac, Atom.f2c_matrix))

    def get_cart(self):
        """
        :return: List of three floats representing the atom's
        coordinates in cartesian coordinates.
        """
        return self.cart

    def get_name(self):
        """
        :return: string representing the atom's name.
        """
        return self.name

    def get_element(self):
        """
        :return: string representing the atom's element.
        """
        return self.element

    @staticmethod
    def _get_frac2cart_matrix(cell):
        """
        Calculates the matrix to transform fractional coordinates to
        cartesian coordinates.

        :param cell: List of six floats representing the unit cell
        parameters: [a, b, c, alpha, beta, gamma]

        :return: numpy matrix representing the tranformation matrix.
        """
        a, b, c = cell[0], cell[1], cell[2]
        alpha, beta, gamma = cell[3] / 180 * np.pi, cell[4] \
                             / 180 * np.pi, cell[5] / 180 * np.pi
        v = np.sqrt(1 - np.cos(alpha) * np.cos(alpha)
                    - np.cos(beta) * np.cos(beta)
                    - np.cos(gamma) * np.cos(gamma)
                    + 2 * np.cos(alpha) * np.cos(beta) * np.cos(gamma))

        rawmatrix = [[a, b * np.cos(gamma), c * np.cos(beta)],
                     [0, b * np.sin(gamma), (c * (np.cos(alpha)
                                                  - np.cos(beta) * np.cos(gamma))) / np.sin(gamma)],
                     [0, 0, c * v / np.sin(gamma)]]
        frac2cartmatrix = np.matrix(rawmatrix)

        return frac2cartmatrix

    @staticmethod
    def _frac2cart(coord, matrix):
        """
        Tranforms an array representing frational coordinates
        to an array representing cartesian coordinates.
        The transformation is defined by 'matrix'.

        :param coord: List of three floats representing the
        atom's position in fractional coordinates.
        :param matrix: 3x3 numpy matrix representing the transformation
        to cartesian coordinates.

        :return: List of three floats representing the atom's
        position in cartesian coordinates.
        """
        return np.dot(matrix, coord).flatten().tolist()[0]

    def __sub__(self, atom2):
        """
        Returns the difference vector between two atoms.

        :param atom2: Atom instance

        :return: numpy array of lengths 3 representing
        the difference vector between self and atom2.
        """
        return self.get_cart() - atom2.get_cart()

    def add_bond(self, bond):
        """
        Adds an instance of the Bond class the the atom's
        bonds dictionary.

        :param bond: Bond instance.
        """
        self.bonds[bond.get_id()] = bond

    def add_angle(self, angle):
        """
        Adds an instance of the Angle class to the atom's
        angle dictionary.

        :param angle: Angle instance.
        """
        self.angles[angle.get_id()] = angle

    def iter_bonds(self):
        """
        An iterator iterating over all bonds in the atom's
        bonds dictionary.

        :return: Bond instances.
        """
        for bond in self.bonds.values():
            yield bond

    def iter_bond_pairs(self):
        """
        An iterator iterating of all pairs of bonds in the atom's
        bonds dictionary.

        :return: List of two Bond instances.
        """
        for bond1 in self.iter_bonds():
            for bond2 in self.iter_bonds():
                if not bond1 == bond2:
                    yield bond1, bond2

    def get_atom_priority(self):
        """
        :return: string representing the atom's priority.
        """
        return self.priority

    def grow_enviroment(self):
        """
        Adds an instance of the Enviroment class to the atom and
        triggers the enviroment's grow() and build_invariom_name()
        methods.
        """
        self.enviroment = Enviroment(self)
        self.enviroment.grow()
        self.enviroment.build_invariom_name()

        # =======================================================================
        # print self.enviroment
        # if ': C7' in self.enviroment.__str__():
        # exit()
        #=======================================================================

    def does_grow(self):
        """
        :return: Boolean: True if the atom's element requires consideration
        of next next neighbors as defined by the invariom
        formalism.
        """
        if self.grow:
            return True
        return False

    def get_invariom_name(self):
        """
        :return: String representing the atom's invariom name as determined
        by the atom's Enviroment instance.
        """
        return self.enviroment.get_invariom_name()

    def get_invariom_char(self):
        """
        :return: String representing the atom's representation in an invariom name if
        the atom is not the first atom in the string and not
        a bridge head atom of a ring system.
        """
        return self.get_element().lower()

    def get_invariom_char_prime(self):
        """
        :return: String representing the atom's representation in an invariom string
        if the atom is the first atom in the string.
        """
        return self.prefix + self.get_element()

    def get_invariom_char_trunk(self):
        """
        :return: String representing the atom's representation in an invariom string
        if the atom is a bridge head of a ring system.
        """
        return ''.join(self.rings) + self.get_element().lower()

    def add_ring(self, size, ring_id):
        """
        Resets the properties of the atom instance considering
        it is part of a ring system of size 'size'.

        :param size: Integer representing the number of ring atoms.
        :param ring_id: String specifying all atoms that are part of
        the ring.
        """
        self.ring_ids.append(ring_id)
        self.rings.append(str(size))
        self.rings = sorted(self.rings, reverse=True)
        self.prefix = ''.join(self.rings) + '-'

    def update_ring_data(self):
        """
        This looks strange. Take a closer look!
        Who has the time? It works. Better not touch it...
        """
        if self.is_ring_atom():
            for bond in self.bonds.values():
                if not bond.is_ring_bond():
                    bond.set_at_bond()

    def is_ring_atom(self):
        """
        :return: Boolean: True if the atom is part of a ring system.
        """
        if len(self.rings) > 0:
            return True

    def get_rings(self):
        """
        :return: List of integers each representing the size of a ring
        the instance is a part of.
        """
        return self.rings

    def get_orientation(self):
        """
        :return: List of to numpy arrays of lengths 3 representing the atoms
        orientation vectors as computed by the corresponding Enviroment instance.
        """
        return self.enviroment.get_orientation()

    def get_bonds(self):
        return self.bonds


class Angle(object):
    """
    A class representing an angle defined by the positions
    of three atoms.
    """

    def __init__(self, atom1, atom2, atom3):
        """
        Initializes an Angle instance. atom1, atom2 and atom3
        are the atoms whose positions define the angle.

        :param atom1: Atom instance.
        :param atom2: Atom instance.
        :param atom3: Atom instance.
        """
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom3 = atom3
        self.id = None
        self.norm = None
        self.center = None
        self.scale = None
        self.normal = None
        self.hash = '{}'.format(''.join(sorted([self.atom1.get_name(), self.atom2.get_name(), self.atom3.get_name()])))
        v1x = atom2 - atom1
        self.v1 = v1x / norm(v1x)
        self.v1x = v1x
        v2x = atom3 - atom1
        self.v2 = v2x / norm(v2x)
        self.v2x = v2x
        self.avarage_len = (norm(v1x) * norm(v2x)) ** .5
        self.avarage_len1 = (norm(v1x) + norm(v2x)) / 2
        self.avarage_len = 2. / (1. / norm(v1x) + 1. / norm(v2x))

        self.cos_angle = np.dot(self.v1, self.v2)
        self.angle = np.arccos(self.cos_angle)
        self.set_id()
        self.set_center()
        self.set_normal()
        # =======================================================================
        # print self.avarage_len,self.avarage_len1,self.avarage_len2,self.id
        # =======================================================================

    def __str__(self):
        return '{} {} {}'.format(self.atom1.get_name(), self.atom2.get_name(), self.atom3.get_name())

    def set_normal(self):
        """
        Calculates the Angle instance normal vector defining the plane
        the three Atom instances are forming.
        """
        self.normal = np.cross(self.v1, self.v2)
        self.normal /= norm(self.normal)

    def get_normal(self):
        """
        :return: Numpy array of lengths three representing
        the Angle instance's orientation in space.
        """
        return self.normal

    def set_id(self):
        """
        Determines an unique ID from the names of atom1, atom2
        and atom3.
        """
        namelist = sorted([i.get_name() for i in [self.atom1, self.atom2, self.atom3]])
        self.id = '{}*{}*{}'.format(*namelist)

    def get_id(self):
        """
        :return: String representing the Angle instance's unique ID.
        """
        return self.id

    def set_center(self):
        """
        Computes the center of an ideal polyeder where
        the postions of atom1, atom2 and atom3 are on three
        of the polyeder's corners.
        """
        self.get_scale_factor()
        # =======================================================================
        # print self.scale*self.avarage_len,self.id,self.angle*180/np.pi,self.scale,self.avarage_len
        # =======================================================================
        self.norm = self.v1 + self.v2
        self.norm /= norm(self.norm)
        self.center = self.norm * self.scale * self.avarage_len + self.atom1.get_cart()
        if abs(self.angle * 180. / np.pi - 90) < 2:
            self.center = self.atom1.get_cart() + (self.v1x + self.v2x) / 2.

    def get_center(self):
        """
        :return: Numpy array of lenght 3 representing the center as
        computed by 'set_center()'.
        """
        return self.center

    def get_scale_factor(self):
        """
        Computes the distance from the postion of
        atom1 to the center of an ideal polyhedron
        based on the angle between atom1, atom2 and atom3.

        :return: None
        """
        thsin = np.sin(0.5 * self.angle)
        thsin *= thsin
        tsin = np.sin(self.angle)
        tsin *= tsin
        self.scale = thsin / tsin



class Enviroment(object):
    """
    A class representing the chemical enviroment of an atom.
    The class is also responsible for generating the invariom
    string representing the chemical enviroment.
    """

    def __init__(self, atom):
        """
        Initializes the Enviroment instance by defining
        the atom that is the 'seed' of the enviroment.

        :param atom: Atom instance representing the beginning
        of an enviroment.
        """

        self.seed = atom
        self.chains = {}
        self.chain_order = None
        self.orientation = None
        self.o_atom_1 = None
        self.o_atom_2 = None
        self.invariom_name = None
        self.priorities = None
        self.check_for_at_sorting = None
        self.check_indices = None

    def grow(self):
        """
        Determines the atoms that are required to define
        the chemical enviroment of the seed atom. the size
        of the chemical enviroment is determined by checking
        the 'does_grow()' methods of directly bound atoms
        and their Bond instances.

        For every directly bond atom the grow() method
        creates an instance of the Chain class representing
        the atom 'chain' originating from the neighbor atom.
        """
        for bond in self.seed.iter_bonds():
            self.chains[bond.get_id()] = Chain(self.seed, bond)
        for chain in self.chains.values():
            if chain.does_grow():
                for bond in chain.get_root_atom().iter_bonds():
                    partner = bond.get_partner(chain.get_root_atom())
                    if not partner == self.seed:
                        chain.append(bond)
        self.sort_chains()

    def sort_chains(self):
        """
        Sorting all created chain instances by the value of their
        priority attribute.
        """
        self.chain_order = [i.get_id() for i in sorted([chain for chain in self.chains.values()],
                                                       key=lambda thischain: thischain.get_chain_priority(),
                                                       reverse=True)]
        self.priorities = [i.get_chain_priority() for i in sorted([chain for chain in self.chains.values()],
                                                                  key=lambda thischain: thischain.get_chain_priority(),
                                                                  reverse=True)]
        for p in self.priorities:
            if self.priorities.count(p) is 2:
                c = ''.join(p)
                self.check_indices = [i for i, x in enumerate(self.priorities) if ''.join(x) == c]
                self.check_for_at_sorting = True

    def build_invariom_name(self):
        """
        Generates the invariom string representing the chemical
        enviroment of seed atom by calling the get_invariom_char...()
        methods of all significant atoms in the order defined by
        their priorities.
        """

        #self.invariom_name = '{}'.format(self.seed.get_invariom_char_prime())
        name_list = ['{}'.format(self.seed.get_invariom_char_prime())]

        for chain_id in self.chain_order:
            chain = self.chains[chain_id]

            if chain.is_ring_chain() and not self.seed.is_ring_atom():
                name_list.append(chain.build_trunk_string())
                #self.invariom_name += name_list[-1]
            else:
                name_list.append(chain.build_chain_string())
                #self.invariom_name += name_list[-1]

        if self.check_for_at_sorting:
            name_part1 = name_list[self.check_indices[0] + 1]
            name_part2 = name_list[self.check_indices[1] + 1]
            if name_part1.count('@') < name_part2.count('@'):
                name_list[self.check_indices[0]+1], name_list[self.check_indices[1]+1] = name_list[self.check_indices[1]
                                                                                                   + 1],\
                                                                                         name_list[self.check_indices[0]
                                                                                                   + 1]

        self.invariom_name = ''.join(name_list)
        if classic_names:
            self.invariom_name = truncate_neighbors(self.invariom_name)

    def get_invariom_name(self):
        """
        :return: String representing the Enviroment's invariom name.
        """
        return self.invariom_name

    def set_invariom_name(self, name):
        """
        Overwrites the determined invariom name with 'name'.

        :param name: String representing the new invariom name.
        """
        self.invariom_name = name

    def set_orientation(self):
        """
        Determines how the orientation of the Enviroment instance
        can be described by analysing the priorities of all atoms
        in the enviroment.
        Subsequently, a method for computing the actual orientation
        vectors is called depending on the results of the first step.
        """
        chain_priorities = []
        unique_chains = []
        for chain_name in self.chain_order:
            chain = self.chains[chain_name]
            chain_priorities.append(''.join(chain.get_chain_priority()))
        for i, cp in enumerate(chain_priorities):
            if chain_priorities.count(cp) == 1:
                unique_chains.append(i)
        if len(unique_chains) == 0:
            self.set_high_symmerty_orientation()
        elif len(unique_chains) == 1:
            self.set_single_chain_orientation(self.chains[self.chain_order[unique_chains[0]]])
        else:
            self.o_atom_1 = self.chains[self.chain_order[unique_chains[0]]].root_atom
            self.o_atom_2 = self.chains[self.chain_order[unique_chains[1]]].root_atom
        if self.o_atom_1:  # and self.o_atom_2:
            self.set_orientation_vectors()
        else:
            self.orientation = [np.array([1, 0, 0]), np.array([0, 1, 0])]

    def set_high_symmerty_orientation(self):
        """
        Determines the orientation vectors for highly symmetric
        enviroments where all chains are equivalent.
        """
        try:
            self.o_atom_1 = self.chains[self.chain_order[0]].root_atom
            self.o_atom_2 = self.chains[self.chain_order[1]].root_atom
        except IndexError:
            pass

    def set_single_chain_orientation(self, chain):
        """
        Determines the orientation vectors for enviroments where
        only one chain exists or all but one chain are equivalent.

        :param chain: Chain instance.
        """
        self.o_atom_1 = chain.root_atom
        chain_atoms = [chain.atoms[atom[0]] for atom in chain.ordered_atoms]
        priorities = chain.branch_priorities.values()
        unique_atoms = []
        for i, priority in enumerate(priorities):
            if list(priorities).count(priority) == 1:
                unique_atoms.append(i)
        if len(unique_atoms) > 0:
            self.o_atom_2 = chain_atoms[unique_atoms[0]]
        else:
            if chain.has_grown():

                self.o_atom_2 = chain_atoms[0]
            else:

                if len(self.chains.values()) > 1:
                    for chain2 in self.chains.values():
                        if not chain2 == chain:
                            self.o_atom_2 = chain2.root_atom
                            break
                else:
                    self.o_atom_2 = None

    def set_orientation_vectors(self):
        """
        Computes normalized orientation vectors from the
        previously determined orientation definitions.
        """
        v1 = self.o_atom_1.get_cart() - self.seed.get_cart()
        v1 /= norm(v1)
        if not self.o_atom_2:
            mv = 0
            mi = 0
            for i, v in enumerate(v1):
                if abs(v) > mv:
                    mv = v
                    mi = i
            vt = np.array(v1)
            vt[mi] = mv * -1
            vt = vt + np.array([0.1, 0.1, 0.1])
            v2 = np.cross(v1, vt)
            v2 /= norm(v2)
        else:
            v2 = self.o_atom_2.get_cart() - self.seed.get_cart()
            v2 /= norm(v2)
        self.orientation = [v1, v2]

    def get_orientation(self):
        """
        :return: List of two numpy arrays of length 3 representing
         the enviroments orientation vectors.
        """
        if not self.orientation:
            self.set_orientation()
        return self.orientation

    def __str__(self):
        """
        :return: Stringrepresentation of the Enviroment instance.
        Mainly used for debugging purposes.
        """
        string = '\nEnviroment of atom: {}\n'.format(self.seed.get_name())
        for chain in self.chains.values():
            string += '{}\n'.format(str(chain))
        # self.build_invariom_name()
        string += 'Invariom Name: {}\n'.format(self.invariom_name)
        return string


class Chain(object):
    """
    A class representing a chain of neighbor atoms originating from
    an atom directly bound to an Enviroment's seed atom.
    """

    def __init__(self, seed, bond):
        """
        Initializes a Chain instance.

        :param seed: is the seed atom of
        the Enviroment instance initializingthe chain.
        :param bond: is a bond between that seed atom
        and a directly bound neighbor atom.
        """
        self.id = None
        self.invariom_name = None
        self.root = bond
        self.root_atom = self.root.get_partner(seed)
        if bond.does_grow() or seed.does_grow() or self.root_atom.does_grow():
            self.grow = True
        else:
            self.grow = False
        self.seed = seed
        self.branch = {}
        self.branch_priorities = {}
        self.ordered_atoms = []
        self.atoms = {}
        self.brackets = False

        #########################################################
        firstpriority = ''.join([self.root.get_bond_priority(),
                                 self.root.get_partner(self.seed).get_atom_priority()])
        #############################################################
        self.priority = [firstpriority, '000000']
        self.set_id()

    def append(self, bond):
        """
        Extends the chain by 'bond'.

        :param bond: Bond instance.
        """
        self.branch[bond.get_id()] = bond

    def get_root_atom(self):
        """
        :return: Atom instance representing the atom of the Chain
        that is directly bound to the seed atom.
        """
        return self.root.get_partner(self.seed)

    def set_id(self):
        """
        Determines a unique ID for the Chain instance.
        """
        self.id = self.root.get_id()

    def get_id(self):
        """
        :return: String representing the instance's the unique ID.
        """
        return self.id

    def get_chain_priority(self):
        """
        Determines the chain's priority by analysing all bonds
        and atoms that are part of the chain.

        :return: String representing the instance's priority.
        """
        priorities = []
        for bond in self.branch.values():
            self.atoms[bond.get_partner(self.root_atom).get_id()] = bond.get_partner(self.root_atom)
            secondpriority = ''.join([bond.get_bond_priority(),
                                      bond.get_partner(self.root_atom).get_atom_priority()])
            if bond.get_partner(self.root_atom).is_ring_atom() and not bond.is_at_bond():
                # Working arround the issue that being part of a ring can also be an atom property not only
                # a bond property.
                secondpriority = '{p:{f}<3}'.format(p=''.join(bond.get_partner(self.root_atom).rings), f='0') + bond.get_partner(self.root_atom).get_atom_priority()
            self.branch_priorities[bond.get_partner(self.root_atom).get_id()] = secondpriority
            priorities.append(secondpriority)


        priorities = sorted(priorities, reverse=True)
        self.priority[1] = ''.join(priorities)
        self.ordered_atoms = sorted([i for i in self.branch_priorities.items()], key=lambda pair: pair[1], reverse=True)
        if len(self.ordered_atoms) > 0 and self.grow:
            self.brackets = True

        return self.priority

    def build_chain_string(self):
        """
        Generates the invariom string representation of the
        chain instance by calling the appropriate functions
        of the Atom and Bond instances depending on their
        priorieties.
        """
        rootstring = self.root.get_invariom_char()
        if '#' in rootstring:
            rootstring = '#{}'.format(''.join(sorted(self.root_atom.get_rings(), reverse=True)))
        string = '{}{}'.format(rootstring, self.root_atom.get_invariom_char())
        if self.brackets:
            string += '['
        for atom_name, _ in self.ordered_atoms:
            for bond in self.branch.values():
                if atom_name in bond.get_id():
                    if self.atoms[atom_name].is_ring_atom() and not self.seed.is_ring_atom():
                        chain_id = [bond.get_invariom_char_noring(self.atoms[atom_name]),
                                    self.atoms[atom_name].get_invariom_char()]

                    elif (self.atoms[atom_name].is_ring_atom() and self.seed.is_ring_atom()) and (
                            not any([ring_id in self.seed.ring_ids for ring_id in self.atoms[atom_name].ring_ids])):
                        chain_id = [bond.get_invariom_char_noring(self.atoms[atom_name]),
                                    self.atoms[atom_name].get_invariom_char()]

                    else:
                        chain_id = [bond.get_invariom_char(), self.atoms[atom_name].get_invariom_char()]

                    if '#' in chain_id[0]:
                        # Working arround the issue that being part of a ring can also be an atom property not only
                        # a bond property.
                        chain_id[0] = '#{}'.format(''.join(sorted(self.atoms[atom_name].get_rings(), reverse=True)))

                    string += '{}{}'.format(*chain_id)
                    break
        # if str(self).startswith('C(17)'):
        #                     print self, string
        if self.brackets:
            string += ']'
        self.invariom_name = string

        return self.invariom_name

    def __str__(self):
        """
        String representation of the Chain instance.
        Mainly used for debugging purposes.
        """
        string = '{:4} --> '.format(self.root_atom.get_name())
        for bond in self.branch.values():
            string += '{:4} '.format(bond.get_partner(self.root_atom).get_name())
        string = '{:25}  Priority: {}'.format(string, ''.join(self.priority))
        return string

    def does_grow(self):
        """
        :return: Boolean: True if the chemical envioment of the seed
        atom needs to include next next neighbors that would
        be part of this Chain instance.
        """
        if self.grow:
            return True
        return False

    def has_grown(self):
        """
        :return: Boolean: True the Chain instance has actually grown
        and therefore consists of more than one atom.
        This method can return False even when does_grow()
        returns True in cases where next next neighbors
        would need to be considered but the corresponding
        next neighbor has no other neighbor atoms.
        """
        if len(self.atoms.keys()) > 0:
            return True
        return False

    def is_ring_chain(self):
        """
        :return: Boolean: True is the root atom of the chain is
        part of a ring system.
        """
        if self.root_atom.is_ring_atom():
            return True

    def build_trunk_string(self):
        """
        :return: String representing the invariom string representation of the
        Chain if the seed atom is not part of a ring system
        and the root atom is part of a ring system.
        """
        return '@{}'.format(self.root_atom.get_invariom_char_trunk())

    def iter_atoms(self):
        """
        Iterator for iterating over all atoms that are
        part of the chain. Starting with the atom with
        the lowest priority...

        :return: Atom instances.
        """
        for atom_name in self.ordered_atoms:
            yield self.atoms[atom_name[0]]


class CorrectionFilter(object):
    """
    A class for applying empirical corrections to
    the generated invariom names.
    """

    def __init__(self, filepointer):
        """
        Initializes the CorrectionFilter instance.

        :param filepointer:
        must be a filepointer to a 'empirical_corrections.txt' file.
        """
        self.filepointer = filepointer
        self.corrections = {}
        try:
            self.setup()
        except AttributeError:
            self.correct = self.dummy

    def setup(self):
        """
        Creates a dictionary from the 'empirical_corrections.txt'
        file.
        """
        for line in self.filepointer.readlines():
            if line.lstrip(' ').startswith('#'):
                continue
            line = line.partition(':')
            self.corrections[line[0]] = line[2]

    @staticmethod
    def dummy(_):
        """
        Dummy method.
        :param _: ...
        """
        pass

    def correct(self, enviroment):
        """
        Changes the invarioms string representing the enviroment
        of 'enviroment' based on the entries of self.corrections.

        :param enviroment: Enviroment instance.
        """
        if enviroment.get_invariom_name() in self.corrections.keys():
            oldname = enviroment.get_invariom_name()
            enviroment.set_invariom_name(self.corrections[enviroment.get_invariom_name()].rstrip('\n'))
            printer('Empircal correction applied: {} --> {}'.format(oldname, enviroment.get_invariom_name()))
            return True
        return False


def test():
    """
    Function for testing the functionality of the module.
    """
    from lauescript.laueio.shelxl_iop import ShelxlIOP

    shelx = ShelxlIOP('shelx.res')
    shelx.read()

    #===========================================================================
    # invgen=InvariomGenerator()
    #===========================================================================
    names = shelx.get_names()
    coords = [shelx.get_frac()[i] for i in names]
    cell = shelx.get_cell()
    #===========================================================================
    # invgen.populate(names, coords, 'frac',cell)
    #===========================================================================
    for i in get_invariom_names(frac=coords, cell=cell, names=names, orientations=True,
                                corrections=open('../data/empirical_corrections.txt'), dynamic=True):
        print(i)


if __name__ == '__main__':
    test()