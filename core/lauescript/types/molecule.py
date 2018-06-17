"""
Created on Nov 1, 2013

@author: jens

Module containing definitions for datatypes representing molecules.
"""
from numpy import array, pi, matrix, sqrt, sin, cos, zeros, tanh
from sklearn.neighbors import NearestNeighbors
from lauescript.cryst.iterators import iter_atoms, iter_atom_pairs
from lauescript.types.atom import ATOM
# from lauescript.invstring2 import get_invariom_names
from lauescript.cryst.symmetry import SymmetryElement
from lauescript.cryst.crystgeom import proton_number
from lauescript.cryst.geom import is_bound, framework_crawler, get_framework_neighbors
from lauescript.cryst.sort import SortAtom


class MoleculeInterface(object):
    """
    Definition of an interface for Molecule data types.
    """

    def __init__(self):
        self.atom_dict = {}
        self.bonds = {}
        self.atoms = []

    def add_atom(self, atom):
        self.atom_dict[atom.get_id()] = atom
        try:
            self.atoms.append(atom)
        except AttributeError:
            pass

    def set_cell(self, value):
        self.cell = value
        self.cell_deg = value

    def get_cell(self, degree=True):
        if degree:
            return self.cell_deg
        else:
            return self.cell

    def _get_bonds(self, unique=True, hydrogen=True):
        for atom1 in self.atom_dict.values():
            for atom2 in self.atom_dict.values():
                if not atom1 == atom2:
                    if hydrogen == False and (atom1.get_element() == 'H' or atom2.get_element() == 'H'):
                        continue
                    if is_bound(atom1.get_cart(),
                                atom1.get_element(),
                                atom2.get_cart(),
                                atom2.get_element()):
                        bondatoms = [atom1.get_id(), atom2.get_id()]
                        if unique:
                            bondatoms = sorted(bondatoms)
                        bondatoms = ':'.join(bondatoms)
                        self.bonds[bondatoms] = [atom1, atom2]

    def get_bonds(self, unique=True, hydrogen=True):
        if len(self.bonds) == 0 or not unique == self.unique_bonds:
            self._get_bonds(unique=unique, hydrogen=hydrogen)
            self.unique_bonds = unique
        try:
            for bond in self.bonds.values():
                yield bond
        except:
            yield None

    # def atoms(self):
    #     for atom in self.atom_dict.values():
    #         yield atom

    def __getitem__(self, name):
        """
        Overwrites the __getitem__ method of the molecule.
        """

        return self.atom_dict[name]


class MOLECULE(MoleculeInterface):
    # class MOLECULE(object):
    """
    Class representing a molecule. The class is used mainly
    as an interface to access the methods of the atoms
    belonging to an MOLECULE instance.
    """

    def __add__(self, newatom):
        self.atoms.append(newatom)
        return self

    def __init__(self, name, cell=None):
        """
        Initializes the molecule instance.
        The 'cell' information can be added later by calling
        the appropriate method.
        """
        #=======================================================================
        # self.add_atom=self.give_atom
        #=======================================================================
        self.atoms = []
        self.dist_done= False
        self.name = name
        self.daba = False
        self.chem_mol = []
        self.keep = ['cell',
                     'daba',
                     'frac2cartmatrix',
                     'cart2fracmatrix',
                     'name',
                     'atoms',
                     'keep']
        if cell:
            self.give_cell(cell)
        else:
            self.frac2cartmatrix = None
            self.cart2fracmatrix = None

    def __str__(self):
        """
        Overwrites the string representation of the molecule.
        """
        return self.name

    def __getitem__(self, name):
        """
        Overwrites the __getitem__ method of the molecule.
        """
        for atom in self.atoms:
            if atom.name == name:
                return atom

    def get_chem_molecule(self, ID):
        """
        Returns a list of all atoms with the chemical molecule
        ID 'ID'.
        If ID is negative, all atoms are returned.
        """
        if ID >= 0:
            return self.chem_mol[ID]
        else:
            return self.atoms

    def get_all_chem_molecules(self):
        """
        Returns all chemical molecules.
        """
        return self.chem_mol


    def give_cell(self, cell):
        """
        Adds the unit cell information to the molecule instance.

        cell=[ a , b , c , alpha , beta , gamma]
        """
        self.cell = array(cell)
        self.cell_deg = array(cell)
        v = self._get_frac2cart_matrix()
        self._get_cart2frac_matrix(v)
        for atom in self.atoms:
            atom.update_coordinates(self.frac2cartmatrix, self.cart2fracmatrix)

    def coords(self, use='cart'):
        """
        Returns a list of numpy arrays representing the positions
        of all atoms of the molecule instance.
        """
        if use == 'cart':
            return [atom.cart for atom in self.atoms]
        else:
            return [atom.frac for atom in self.atoms]

    def _get_frac2cart_matrix(self):
        """
        Calculates the matrix to transform fractional coordinates to
        cartesian coordinates.
        """

        self.cell[3], self.cell[4], self.cell[5] = self.cell[3] / 180 * pi, self.cell[4] \
                                                   / 180 * pi, self.cell[5] / 180 * pi
        v = sqrt(1 - cos(self.cell[3]) * cos(self.cell[3]) \
                 - cos(self.cell[4]) * cos(self.cell[4]) \
                 - cos(self.cell[5]) * cos(self.cell[5]) \
                 + 2 * cos(self.cell[3]) * cos(self.cell[4]) * cos(self.cell[5]))

        self.frac2cartmatrix = matrix(
            [[self.cell[0], self.cell[1] * cos(self.cell[5]), self.cell[2] * cos(self.cell[4])],
             [0, self.cell[1] * sin(self.cell[5]), (self.cell[2] * (cos(self.cell[3])
                                                                    - cos(self.cell[4]) * cos(self.cell[5]))) / sin(
                 self.cell[5])],
             [0, 0, self.cell[2] * v / sin(self.cell[5])]])
        return v

    def _get_cart2frac_matrix(self, v):
        """
        Calculates the matrix to transform cartesian coordinates to
        fractional coordinates.
        """
        self.cart2fracmatrix = matrix([[1 / self.cell[0],
                                        -cos(self.cell[5]) / (self.cell[0] * sin(self.cell[5])),
                                        (cos(self.cell[3]) * cos(self.cell[5]) - cos(self.cell[4]))
                                        / (self.cell[0] * v * sin(self.cell[5]))],
                                       [0, 1 / (self.cell[1] * sin(self.cell[5])), (cos(self.cell[4])
                                                                                    * cos(self.cell[5]) - cos(
                                           self.cell[3])) / (self.cell[1] * v
                                                             * sin(self.cell[5]))],
                                       [0, 0, sin(self.cell[5]) / (self.cell[2] * v)]])


    def give_atom(self,
                  name=None,
                  element=None,
                  cart=None,
                  frac=None,
                  molecule=None,
                  model_compound=None):
        """
        Adds an atom to the molecule.
        """
        if not molecule:
            molecule = self
        if not name in [i.name for i in self.atoms]:
            self.atoms.append(ATOM(name,
                                   element,
                                   cart,
                                   frac,
                                   molecule,
                                   model_compound))

    def add_atom(self,
                 name=None,
                 element=None,
                 cart=None,
                 frac=None,
                 molecule=None,
                 model_compound=None):
        """
        Adds an atom to the molecule.
        """

        if not molecule:
            molecule = self
        if not name in [i.name for i in self.atoms]:
            self.atoms.append(ATOM(name=name,
                                   element=element,
                                   cart=frac,
                                   frac=frac,
                                   molecule=molecule,
                                   model_compound=model_compound))


    # def get_code_atom_links(self):
    #     atom_names = [atom.name for atom in self.atoms]
    #     cart = [atom.cart for atom in self.atoms]
    #     for _, orientations in get_invariom_names(atom_names,
    #                                               cart=cart,
    #                                               orientations=True,
    #                                               verbose=False,
    #                                               corrections_directory='/home/jens/APD-toolkit/apd/data/'):
    #
    #         for atom in self.atoms:
    #             atom.set_orientation(orientations[atom.name])
    #             #===================================================================
    #             # print atom, invariom_data[-1][atom.name]
    #             #===================================================================

    def identify_molecules(self):
        """
        Takes an instance of the MOLECULE class as argument and returns a
        dictionary that keys an identifying integer to every atom name
        specifying which of the atoms in the molecule form an 'independent'
        molecule in the chemical sense.
        If all atoms are part of the same molecule, all atoms get the
        integer '0'.
        """
        blacklist = set()
        #===========================================================================
        # molecules=[]
        #===========================================================================
        self.ID = 0
        for atom1 in self.atoms:
            framework = []
            for atom2 in get_framework_neighbors(atom1):
                if not atom1.get_name() in blacklist and not atom2.get_name() in blacklist:
                    framework += framework_crawler(atom1, atom2)
                    framework += framework_crawler(atom2, atom1)
                    framework = list(set(framework))
                    [blacklist.add(atom.get_name()) for atom in framework]
                    #===============================================================
                    # molecules.append(framework)
                    #===============================================================
            if framework:
                chem_mol = framework
                for atom in framework:
                    atom.set_molecule_id(self.ID)
                    for h in get_framework_neighbors(atom, useH=True):
                        if h.get_element() == 'H':
                            h.set_molecule_id(self.ID)
                            chem_mol.append(h)
                self.ID += 1
                self.chem_mol.append(chem_mol)
        for atom in self.atoms:
            if atom.molecule_id == None:
                atom.set_molecule_id(self.ID)
                self.ID += 1
        # for m in self.chem_mol:
        #     print([a.name for a in m])
        return self.ID

    def get_distances(self, force_update=False):
        """
        Computes the distance matrix.
        :arg force_update: Boolean used to force an update of the
        """
        if self.dist_done and not force_update:
            return
        # samples = self.coords()
        # neigh = NearestNeighbors(5, 0.4)
        # neigh.fit(samples)
        # result = neigh.kneighbors(samples, len(samples), return_distance=False)
        # self.distance_matrix = result
        # for atom_dist in result:
        #     self.atoms[atom_dist[0]].partner = [self.atoms[i] for i in atom_dist[1:]]
        self.dist_done = True

        # samples2 = [atom.get_frac() for atom in self.atoms]

        dist_results = []
        for atom1 in self.atoms:
            dists = []
            for i, atom2 in enumerate(self.atoms):
                d = atom1-atom2
                dists.append((d, i))
            dists = sorted(dists, key=lambda pair: pair[0])
            dists = [self.atoms[d[1]] for d in dists[1:]]
            atom1.partner = dists
            # if atom1.name == 'C(2)':
            #     print(atom1, [a for a in atom1.partner[:10]])
            #     print(atom1, [a.name for a in atom1.partner])

    def iter_atoms(self, sort=False):
        """
        Iterator iterating over all atoms of the molecule with the
        name 'exp'.
        """
        if not sort:
            for atom in self.atoms:
                yield atom
        else:
            for atom in SortAtom.sort(molecule=self):
                yield atom

    def iter_atom_pairs(self, bound=True, unique=True, sort=True):
        """
        Iterator iterating over all pairs of atoms in the molecule
        'exp'

        :param bound: Boolean specifying whether all atom pairs are
        returned or only those with chemical bonds between them.
        """
        blacklist = []
        for atom1 in self.iter_atoms(sort=sort):
            # for atom2 in self.iter_atoms(sort=sort):
            if bound:
                for atom2 in atom1.partner:
                    # if not atom1 == atom2:
                        if not bound or is_bound(atom1.cart, atom1.element, atom2.cart, atom2.element):
                            blackstring = '{}{}'.format(*sorted([atom1.name, atom2.name]))
                            if unique and not blackstring in blacklist:
                                yield atom1, atom2
                                blacklist.append(blackstring)
                            elif not unique:
                                yield atom1, atom2
                        else:
                            break
            else:
                for atom2 in self.iter_atoms(sort=sort):
                    if not atom1 == atom2:
                        yield atom1, atom2

    def expand(self, pluginManager):
        printer = pluginManager.get_active_printer()
        loader = pluginManager.get_variable('loader')
        active_id = loader.get_active_id()
        if not active_id.startswith('shelx'):
            printer.highlight('Error: Wrong input file ID: {}.'.format(active_id))
            printer('Molecule expansion currently only works with \'Shelxl\' type files.')
            printer('Note: CIFs written by \'Shelxl\' will be supported soon.')
            return
        symmetry_elements = loader.get_symmetry()
        lattice = float(loader.get_lattice())
        if lattice > 0:
            centric = True
        else:
            centric = False
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
        for atom in iter_atoms(self):
            atom.normalize()
            for symm in symms:
                newatom = symm + atom
                newatom.normalize()
                if not atom - newatom < 0.1:
                    newatoms.append(newatom)
                else:
                    atom.set_special(True)
                asymunits[str(symm)].append(newatom)
        for atom in newatoms:
            self += atom

    def smartExpand(self):
        pass


class DABA_MOLECULE(MOLECULE):
    """
    A MOLECULE subclass with special methods needed for
    molecules representing model compounds.
    """

    def __init__(self, name, cell=None, properties=None):
        """
        This subclass may need the optional argument 'properties'
        containing some information about the quantum chemical
        calculations carried out to obtain the data.
        The 'properties' value can be generated by the
        crystgeom.get_compound_properties() function.
        """
        super(DABA_MOLECULE, self).__init__(name, cell)
        self.daba = True
        self.freq = []
        self.properties = properties
        self.keep += ['properties', 'freq']

    def give_atom(self,
                  name=None,
                  element=None,
                  cart=None,
                  frac=None,
                  molecule=None,
                  model_compound=None):
        """
        Adds an atom the the molecule.
        """
        if not element:
            i = name.index('(')
            element = name[:i]

        if not molecule:
            molecule = self
        if not name in [i.name for i in self.atoms]:
            self.atoms.append(ATOM(name,
                                   element=element,
                                   cart=cart,
                                   frac=frac,
                                   molecule=molecule,
                                   model_compound=model_compound))

    def give_adp(self, adp_list, use='cart_int'):
        """
        Uses the ADP in 'adp_list' to overwrite the ATOMS.adp dictionaries
        at the key 'use'. This method is used when ADP calculation are
        done in multiprocessor mode.
        The ADP in 'adp_list' must be in the same order as the atoms in
        self.atoms.
        """
        for i in range(len(self.atoms)):
            self.atoms[i].adp[use] = adp_list[i]

    def strip_molecule(self, keep):
        """
        Strips the molecule instance of all unnecessary data
        to minimize the size of the serialized file.
        all attributes specified in the 'self.keep' list will
        be preserved.
        """
        types = [type(self.strip_molecule),
                 type(self.__class__)]

        for attr in dir(self):
            # ===================================================================
            # print attr,type(getattr(self,attr))
            #===================================================================
            if not type(getattr(self, attr)) in types:
                if any(i in attr for i in self.keep) \
                        or any(i in attr for i in keep) \
                        or attr[0:2] == '__':
                    #===========================================================
                    # print attr,type(getattr(self,attr))
                    #===========================================================
                    continue
                else:
                    #===========================================================
                    # print attr,type(getattr(self,attr))
                    #===========================================================
                    x = getattr(self, attr)
                    del x
        for atom in self.atoms:
            atom.strip_atom(self.keep)
            exit()

    def get_adp(self, Temp):
        """
        Calculates the vibrational energies for every frequency depending
        of the global variable Temp.
        """
        # #        c=29979245800 #cm/s
        ##        h=float(6.62606957E-34) #Js
        ##        kb=float(1.3806488E-23) #J/K
        #=======================================================================
        # if not hasattr(self.atoms[0],'cart_adp') and ver:
        #     print '\nCalculating ADPs for '+self.name+' (XD format)'
        # if not hasattr(self.atoms[0],'cart_adp'):
        #     log.write('\n\nCalculating ADPs for '+self.name+' (XD format)')
        #=======================================================================
        hk = 0.719385E0
        hc = 16.85773329E0
        deltalist = []
        freqmat = zeros((len(self.freq), len(self.atoms) * 3))
        freqmat2 = zeros((len(self.freq), len(self.atoms) * 3))
        for k in range(len(self.freq)):
            freq0 = self.freq[k]
            m_red = freq0[1]
            delta = (1 / (tanh(hk * freq0[0] / Temp))) * hc / freq0[0] / m_red
            deltalist.append(delta)
            atomcount = 0
            for atom in self.atoms:
                for i in range(3):
                    freqmat[k][atomcount + i] = atom.disps[str(freq0[0])][i]
                    freqmat2[k][atomcount + i] = atom.disps[str(freq0[0])][i] * deltalist[k]
                atomcount += 3

        Umat = zeros((len(self.atoms) * 3, len(self.atoms) * 3))
        for i in range(len(self.atoms) * 3):
            for j in range(len(self.atoms) * 3):
                for k in range(len(self.freq)):
                    Umat[i, j] += freqmat[k, i] * freqmat2[k, j]
        for i in range(len(self.atoms)):
            j = 3 * i
            atom = self.atoms[i]
            adp = []
            adp.append(Umat[j, j])
            adp.append(Umat[j + 1, j + 1])
            adp.append(Umat[j + 2, j + 2])
            adp.append(Umat[j, j + 1])
            adp.append(Umat[j, j + 2])
            adp.append(Umat[j + 1, j + 2])
            #===================================================================
            # if ver: print atom.name+' {:+5f} {:+5f} {:+5f} {:+5f} {:+5f} {:+5f}'\
            #             .format(adp[0],adp[1],adp[2],adp[3],adp[4],adp[5])
            #===================================================================
            atom.adp['cart_int'] = adp

    def get_criterion(self):
        """
        Determines the sorting criterion representing the molecule's 'size'.
        """
        penalty = 0
        for atom in self.atoms:
            if atom.element == 'H':
                continue
            elif atom.element == 'C':
                penalty += 1
            elif atom.element == 'O':
                penalty += 2
            elif atom.element == 'N':
                penalty += 3
            else:
                penalty += int(proton_number[atom.element])
        self.penalty = penalty
        self.criterion = '{:8} {:3} {:8} {:15.3f} {:18.12f}'.format(self.penalty,
                                                                    abs(int(self.properties[0])),
                                                                    int(self.properties[1]),
                                                                    self.properties[2],
                                                                    float(self.properties[3]) + 1000000)


















