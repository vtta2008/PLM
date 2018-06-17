"""
Created on Mar 25, 2014

@author: jens

Module implementing support for PDB formated files.
"""

from operator import attrgetter

from numpy import array

from lauescript.types.atom import AtomInterface
from lauescript.types.molecule import MoleculeInterface
from lauescript.laueio.io import IOP
import lauescript.cryst.tables as tables
from lauescript.cryst.transformations import cart2frac


class PDBAtom(AtomInterface):
    """
    Implements the 'AtomInterface for the
    'PDBIOP'.
    """

    def __init__(self, *args, **kwargs):
        super(PDBAtom, self).__init__(*args, **kwargs)
        self.vdw_radius = None
        self.name_prefix = None
        self.point_charge = None
        self.adp_cart = None
        self.serial_number = None
        self.residue_number = None
        self.type = None

    def __str__(self):
        string = 'ATOM  {:>5} {:<4}{:1}{:3}  {:4}    {} {:>5.3f}{:6.2f}\n'\
            .format(self.serial_number,
                    self.get_name_prefix(),
                    ' ',
                    self.get_residue(),
                    self.get_residue_number(),

                    '{:8.3f}{:8.3f}{:8.3f}'.format(*self.get_cart()),
                    self.get_occupancy(),
                    self.get_b_factor())
        try:
            string2 = 'ANISOU' + string[6:26]+'{}\n'.format('{:>7.0f}{:>7.0f}{:>7.0f}'
                                                            .format(*[i * 10000 for i in self.get_adp_cart()]))
        except TypeError:
            string2 = ''
        return string + string2

    def get_b_factor(self):
        """
        Returns the b factor suitable for PDB files.
        :return: Float representing the atom's b factor.
        """
        try:
            return sum(self.get_adp_cart()[:3])/3
        except ValueError:
            return float(self.get_adp_cart())
        except TypeError:
            return float(self.get_adp_cart())
        except IndexError:
            return float(self.get_adp_cart())

    def as_PQR(self):
        """
        Returns the string representation of the atom
        in PQR file format.
        """
        string = str(self)[:55] + '{:7.4f} {:6.4f}\n'.format(self.get_point_charge(),
                                                             self.get_vdw_radius())
        return string

    def get_element(self):
        """
        :return: String representing the atom's element.
        """
        if not self.element:
            self.generate_element()
        return self.element

    def generate_element(self):
        """
        Sets the instance's element attribute if not already
        set by interpreting the name_prefix attriute.
        """
        element = self.name_prefix[:2]
        if len(element) > 1:
            element = element[0] + element[1].lower()
        try:
            _ = tables.atomtable[element]
        except KeyError:
            element = element[0]
        self.element = element

    def set_vdw_radius(self, value):
        """
        Sets the instance's van der Vaals radius attribute.
        :param value: value of vdw radius.
        """
        self.vdw_radius = value

    def get_vdw_radius(self):
        """
        :return: instance's van der Vaales radius attribute.
        """
        if self.vdw_radius:
            return self.vdw_radius
        else:
            if not self.get_element():
                self.generate_element()
            self.vdw_radius = tables.vdw_radius[self.get_element()]
        return self.vdw_radius

    def set_point_charge(self, value):
        """
        Sets the instance's point charge attribute.
        :param value: value of the point charge.
        """
        self.point_charge = value

    def get_point_charge(self):
        """
        :return: Point charge value.
        """
        try:
            return self.point_charge
        except AttributeError:
            print('pdb_iop.py ERROR: No point charge available for atom:\n {}'.format(str(self)[:-1]))
            print('Setting value to zero.')
            return 0

    def set_adp_cart(self, adp):
        """
        Sets the instance's ADP parameter in cartesian
        coordinates.
        :param adp: numerical value of the displacement
        parameters.
        """
        self.adp_cart = adp

    def set_serial_number(self, value):
        """
        Sets the instance's serial number attribute.
        :param value: integer representing the instance's
        serial number.
        """
        self.serial_number = value

    def get_serial_number(self):
        """
        :return: integer value of the serial number attribute.
        """
        return self.serial_number

    def set_residue_number(self, value):
        """
        Sets the instance's residue number attribute.
        :param value: integer value of the residue number.
        """
        self.residue_number = value

    def get_residue_number(self):
        """
        :return: integer representing the residue number.
        """
        return self.residue_number

    def set_type(self, value):
        """
        Sets the instance's type attribute.
        :param value: string representing the atom type.
        """
        self.type = value

    def get_type(self):
        """
        :return: string representing the atom type.
        """
        return self.type

    def set_name_prefix(self, value):
        """
        Sets the instance's name prefix attribute.
        :param value: string representing the atom's name prefix
        """
        self.name_prefix = value

    def get_name_prefix(self):
        """
        :return: string representing the atom's name prefix.
        """
        return self.name_prefix

    def set_cart(self, value, nofrac=True):
        super(PDBAtom, self).set_cart(value)
        if not nofrac:
            self.set_frac(cart2frac(value, self.molecule.get_cell()))



class PDBMolecule(MoleculeInterface):
    """
    Implementing the 'MoleculeInterface' for the
    'PDBIOP'.
    """
    pass


class PDBIOP(IOP):
    """
    Class for providing data input output using
    the PDB file format.
    """
    
    def __init__(self, *args, **kwargs):
        super(PDBIOP, self).__init__(*args, **kwargs)
        self.force_complete_rebuild = False
        self.names = None
        self.serial_numbers = None
        self.residue_numbers = None
        self.residues = None
        self.types = None
        self.cart = None
        self.adp_cart = None
        self.elements = None
        self.molecule = None
        self.file_content = None
        self.point_charges = None
        self.vdw_radii = None
        self.name_prefixes = None
        self.occupancies = None

    def setup(self, new=False):
        """
        Sets up a newly created IOP instance.
        :param new: Must be 'True' if the an empty
        IOP is created. e.g. No file is parsed.
        :return: None
        """
        if new:
            self.force_complete_rebuild = True
        else:
            self.force_complete_rebuild = False
        self.names = []
        self.serial_numbers = {}
        self.residue_numbers = {}
        self.residues = {}
        self.types = {}
        self.cart = {}
        self.frac = {}
        self.adp_cart = {}
        self.elements = {}
        self.element = self.elements
        self.molecule = PDBMolecule()
        self.file_content = []
        self.point_charges = {}
        self.vdw_radii = {}
        self.name_prefixes = {}
        self.occupancies = {}

    def parse(self):
        """
        Parse file content.
        :return: None
        """
        self.setup()
        for line in self.content:
            self.file_content.append(self._parse_record(line))

    def _parse_record(self, line):
        """
        Identifies the value of the first column of a PDB file
        and tries to find a method that is designed to parse
        that line. If such a method is found, the line specific
        parsing method is called.
        """
        try:
            record_name = str(line[:6]).rstrip().lstrip()
            line_parser = getattr(self, '_parse_' + record_name)
        except AttributeError:
            return line
        return line_parser(line)

    def _parse_ATOM(self, line):
        """
        Parses an ATOM record.
        """
        newatom = PDBAtom()
        newatom.set_molecule(self.molecule)
        serial_number, name_prefix, residue_name, chain_id, residue_number = self._parse_common_line_start(line)

        cart = array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
        occupancy = float(line[54:60])
        b_factor = float(line[60:66])
        element = line[76:78].lstrip().rstrip()
        if not element:
            element = name_prefix[0]
            try:
                if name_prefix[1].islower():
                    element += name_prefix[1]
            except IndexError:
                pass
        name = '{}_{}_{}_{}_{}'.format(name_prefix, serial_number, residue_name, chain_id, residue_number)
        newatom.set_name(name)
        newatom.set_occupancy(occupancy)
        newatom.set_adp_cart(b_factor)
        newatom.set_cart(cart, False)
        newatom.set_name_prefix(name_prefix)
        newatom.set_serial_number(serial_number)
        newatom.set_residue_number(residue_number)
        newatom.set_residue(residue_name)
        self.names.append(newatom.get_name())
        self.cart[name] = cart
        self.frac[name] = newatom.get_frac()
        self.adp_cart[name] = b_factor
        self.name_prefixes[name] = name_prefix
        self.elements[name] = element
        self.occupancies[name] = occupancy
        self.serial_numbers[name] = serial_number
        self.residue_numbers[name] = residue_number
        self.residues[name] = residue_name
        #self.types[name] = name_prefix
        self.molecule.add_atom(newatom)
        return self.molecule[newatom.get_name()]

    def _parse_HETATM(self, line):
        """
        Parses a HETATM record.
        """
        return self._parse_ATOM(line)

    def _parse_ANISOU(self, line):
        """
        Parses an ANISOU record.
        """
        serial_number, name_prefix, residue_name, chain_id, residue_sequence = self._parse_common_line_start(line)
        name = '{}_{}_{}_{}_{}'.format(name_prefix, serial_number, residue_name, chain_id, residue_sequence)
        u11 = float(line[28:35]) * 10 ** -4
        u22 = float(line[35:42]) * 10 ** -4
        u33 = float(line[42:49]) * 10 ** -4
        u12 = float(line[49:56]) * 10 ** -4
        u13 = float(line[56:63]) * 10 ** -4
        u23 = float(line[63:70]) * 10 ** -4
        adp = array([u11, u22, u33, u12, u13, u23])
        self.molecule[name].set_adp_cart(adp)
        # print self.molecule[name]
        return ''

    @staticmethod
    def _parse_common_line_start(line):
        """
        Parses the first columns of atom related records that
        are equal for several records and returns the
        parsed values.
        """
        serial_number = int(line[6:11])
        name_prefix = line[12:17].rstrip().lstrip()
        residue_name = line[17:20].rstrip().lstrip()
        chain_id = line[21]
        residue_sequence = int(line[22:26])
        return serial_number, name_prefix, residue_name, chain_id, residue_sequence

    def _parse_CRYST1(self, line):
        """
        Parses the CRYST1 record.
        """
        a = float(line[6:15])
        b = float(line[15:24])
        c = float(line[24:33])
        alpha = float(line[33:40])
        beta = float(line[40:47])
        gamma = float(line[47:54])
        self.molecule.set_cell((a, b, c, alpha, beta, gamma))
        self.cell = self.molecule.get_cell()
        return line

    def __str__(self):
        string = ''
        for line in self.file_content:
            string += str(line)
        return string

    def complete_rebuild(self):
        """
        Rebuilds the file representation based on the available
        data from scratch.
        :return: None
        """
        self.file_content = []
        atoms = sorted(self.molecule.atoms, key=attrgetter('serial_number'))

        for thisatom in atoms:
            self.file_content.append(thisatom)

    def export_PQR(self):
        """
        Creates a data representation in PQR file format.
        :return: String representing the file.
        """
        if self.force_complete_rebuild:
            self.complete_rebuild()
        string = 'REMARK   1 PQR file generated by the APD-Toolkit (Testversion)\n'
        refatom = PDBAtom()
        for line in self.file_content:
            if type(line) == type(refatom):
                string += line.as_PQR()
            else:
                string += str(line)
        return string

    def set_point_charges(self, atomname, value):
        """
        Setter method for setting the attribute point charge.
        :param atomname: string representing the atom name that is to be updated.
        :param value: float representing the updated value.
        :return: None
        """
        self.point_charges[atomname] = value
        self.molecule[atomname].set_point_charge(value)

    def set_vdw_radii(self, atomname, value):
        """
        Setter method for setting the attribute van der Vaals radius.
        :param atomname: string representing the atom name that is to be updated.
        :param value: float representing the updated value.
        :return: None
        """
        self.vdw_radii[atomname] = value
        self.molecule[atomname].set_vdw_radius(value)

    def set_cart(self, atomname, value):
        """
        Setter method for setting the attribute cartesian coordinates.
        :param atomname: string representing the atom name that is to be updated.
        :param value: float representing the updated value.
        :return: None
        """
        self.cart[atomname] = value
        self.molecule[atomname].set_cart(value)

    def set_serial_numbers(self, atomname, value):
        """
        Setter method for setting the attribute serial number.
        :param atomname: string representing the atom name that is to be updated.
        :param value: float representing the updated value.
        :return: None
        """
        self.serial_numbers[atomname] = value
        self.molecule[atomname].set_serial_number(value)

    def set_name_prefixes(self, atomname, value):
        """
        Setter method for setting the attribute name prefix.
        :param atomname: string representing the atom name that is to be updated.
        :param value: float representing the updated value.
        :return: None
        """
        self.name_prefixes[atomname] = value
        self.molecule[atomname].set_name_prefix(value)

    def set_residue_numbers(self, atomname, value):
        """
        Setter method for setting the attribute residue number.
        :param atomname: string representing the atom name that is to be updated.
        :param value: float representing the updated value.
        :return: None
        """
        self.residue_numbers[atomname] = value
        self.molecule[atomname].set_residue_number(value)

    def set_residues(self, atomname, value):
        """
        Setter method for setting the attribute residue.
        :param atomname: string representing the atom name that is to be updated.
        :param value: String representing the updated value.
        :return: None
        """
        self.residues[atomname] = value
        self.molecule[atomname].set_residue(value)

    def set_occupancies(self, atomname, value):
        """
        Setter method for setting the attribute occupancy.
        :param atomname: string representing the atom name that is to be updated.
        :param value: float representing the updated value.
        :return: None
        """
        self.occupancies[atomname] = value
        self.molecule[atomname].set_occupancy(value)

    def set_adp_cart(self, atomname, value):
        """
        Setter method for setting the attribute adp_cart.
        :param atomname: string representing the atom name that is to be updated.
        :param value: float representing the updated value.
        :return: None
        """
        self.adp_cart[atomname] = value
        self.molecule[atomname].set_adp_cart(value)

    def create_atom(self, name):
        """
        Creates a new atom instance and adds it to the file data.
        :param name: string representing the name of the created atom
        :return: None
        """
        newatom = PDBAtom(name)
        self.molecule.add_atom(newatom)
        newatom.set_molecule(self.molecule)

    def _rebuild_file(self):
        """
        Updates the file representation of the data. Recent changes
        are considered.
        :return: None
        """
        refatom = type(PDBAtom())
        for i, line in enumerate(self.file_content):
            if type(line) == refatom:
                self.file_content[i] = self.molecule[line.get_name()]


if __name__ == '__main__':
    test = PDBIOP('kcross_set0001.pdb')
    test.read()
    exit()
    #test.write_PQR()

    #Test code for exporting to PQR format:
    atomnames = []
    carts = {}
    serial_numbers = {}
    name_prefixes = {}
    res_numbers = {}
    occupancies = {}
    adp_cart = {}
    for atom in test.provide(['cart', 'serial_numbers', 'name_prefixes', 'residue_numbers', 'occupancies', 'adp_cart']):
        atomnames.append(atom[0])
        carts[atom[0]] = atom[1]
        serial_numbers[atom[0]] = atom[2]
        name_prefixes[atom[0]] = atom[3]
        res_numbers[atom[0]] = atom[4]
        occupancies[atom[0]] = atom[5]
        adp_cart[atom[0]] = atom[6]
    test = PDBIOP('test')
    test.setup(new=True)

    def provide():
        """
        Function for updating file content. The method is passed to the
        IOP's 'set' method.
        :return: Yields a set of parameters for every atom.
        """
        x = 0
        for atomname in atomnames:
            x += 1
            yield [atomname,
                   x,
                   carts[atomname],
                   serial_numbers[atomname],
                   name_prefixes[atomname],
                   res_numbers[atomname],
                   occupancies[atomname],
                   adp_cart[atomname]]

    test.set(['point_charges', 'cart', 'serial_numbers', 'name_prefixes', 'residue_numbers', 'occupancies',
              'adp_cart'], provide, True)

    print(test.export('PQR'))
