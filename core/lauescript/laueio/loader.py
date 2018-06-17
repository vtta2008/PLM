"""
Created on Mar 31, 2014

@author: jens
"""
import glob
import os

from lauescript.core import apd_printer
from lauescript.laueio.shelxl_iop import ShelxlIOP
from lauescript.laueio.cif_iop import CIFIOP
from lauescript.laueio.xd_iop import XDIOP
from lauescript.laueio.pdb_iop import PDBIOP
from lauescript.types.molecule import MOLECULE
from lauescript.core.core import apd_exit

class DummyPrinter(object):
    def __call__(self, *args):
        string = ' '.join (args)
        print(string)


class Loader(object):
    """
    A class for creating and managing IOPs. All Loader instances
    share their created IOPs via the Loader.IOPs attribute.
    """
    IOPs = {}
    filetypes = ('.res',
                 '.cif',
                 '.mas',
                 '.pdb')
    suffix = {'shelxl': '.ins',
              'CIF': '.cif',
              'XD': '.inp',
              'PDB': '.pdb'}
    hints = {'shelx': ['titl ', 'cell ', 'zerr ', 'latt ', 'symm ', 'sfac ', 'unit ', 'temp ', 'l.s.', 'plan '],
             'xd': ['xdparfile', 'limits', 'usage'],
             'cif': ['data_', 'CIF', 'loop_', '_audit_generation_method', '_journal'],
             'pdb': ['CRYST1', 'SCALE1', 'SCALE2', 'SCALE3', 'ATOM  ', 'HETATM', 'ANISOU', 'REMARK']}
    read_files = []

    def __init__(self, printer=None):
        self.printer = printer
        if not printer:
            self.printer = DummyPrinter()
        self.IOP = None

    @staticmethod
    def get_read_files():
        """
        :return: A list of all filenames used.
        """
        return Loader.read_files

    def register_IOP(self, IOP):
        """
        Adds an IOP to the Loader.IOPs attribute and
        makes it active.
        """
        self.IOP = IOP
        try:
            Loader.IOPs[IOP.get_id()] = IOP
        except AttributeError:
            apd_exit(1, '\nError: No valid file found.\nTerminating APD-Toolkit.',
                     report=False)


    def get_active_id(self):
        """
        Returns the ID of the currently active IOP.
        """
        return self.IOP.get_id()

    def auto_setup(self, path=None):
        """
        Automatically sets up an IOP depending on the files
        present in the directory 'path'. The newest file with
        known file extension is determined and a corresponding
        IOP is registered and set active.
        """
        selected_filename = None
        if not path or path == './':
            path = './'
            for filename in sorted(glob.iglob(path + '*'), key=os.path.getctime, reverse=True):
                if any([filename.endswith(filetype) for filetype in Loader.filetypes]):
                    selected_filename = filename
                    break
        else:
            selected_filename = path
        if not selected_filename:
            self.no_file_exit()
        self.printer('Using file \'{}\' for coordinates and ADPs.'.format(selected_filename))
        self.register_IOP(self._determine_correct_IOP(selected_filename))

    def load(self, name, grow=False):
        """
        Creates and returns a molecule object.
        """
        Loader.read_files.append(self.IOP.filename)
        try:
            self.IOP.read()
        except IOError as a:
            # self.printer('Error: No valid file named {} found'.format(self.IOP.filename))
            apd_exit(1, '\nError: No valid file named {} found.\nTerminating APD-Toolkit.'.format(self.IOP.filename))
        if grow:
            self.IOP.grow()
        molecule = MOLECULE(name, cell=self.IOP.get_cell())
        for atom in self.IOP.provide(['cart', 'frac', 'adp_cart', 'element']):
            if not atom[4].startswith('W'):
                molecule.add_atom(name=atom[0],
                                  cart=atom[1],
                                  frac=atom[2],
                                  molecule=molecule,
                                  element=atom[4])
                molecule[atom[0]].give_adp(key='cart_meas', value=atom[3])
        molecule.get_distances()
        return molecule

    def get_cell(self):
        """
        Returns the cell parameters of the currently active IOP.
        """
        return self.IOP.get_cell()

    def get_temperature(self):
        """
        Returns the Temperature of the currently active IOP.
        """
        T = self.IOP.get_temperature()
        return T

    def switch_IOP(self, ID, newest=False):
        """
        Makes the IOP corresponding to 'ID' active.
        If 'newest' is True, the IOP created last with an
        ID that starts with 'ID' is set active.
        """
        if not newest:
            key = ID
        else:
            key = max([key for key in Loader.IOPs.keys() if key.startswith(ID)])
        self.IOP = Loader.IOPs[key]


    def for_IOP_of_type(self, ID):
        """
        Generator for iterating over all registered IOPs of
        a type defined by 'ID'. Legal IDs are 'shelx', 'cif'
        etc.
        """
        for key in [key for key in Loader.IOPs.keys() if key.startswith(ID)]:
            yield Loader.IOPs[key]

    def create(self, filename):
        self.register_IOP(self._determine_correct_IOP(filename))

    def _taste_file(self, filename):
        """
        Reads the first few line of the file corresponding to 'filename' in
        order to determine its file format. This makes the selection of
        the correct IOP independent of the name of the file thereby allowing
        shelx style files named 'xd.res' to be correctly identified as
        shelx style .res files.
        :param filename: String representing the path to the file to 'taste'.
        :return:
        """
        for headsize in [10, 100, 500]:
            try:
                with open(filename) as fp:
                    head = fp.readlines(headsize)
            except IOError:
                apd_exit(1, '\n\nERROR: Cannot find file >>>{}<<<'.format(filename))
            for tasteMehod in [method for method in dir(self) if method.startswith('_tastes_like_')]:
                taste = getattr(self, tasteMehod)(head)
                if taste:
                    return taste(filename)
        self.printer("File content not familiar. Relying of file name for file format.\n")
        return False

    def _tastes_like_shelx(self, filehead):
        """
        Checks whether the start of a file has a shelx flavor.
        :param filehead: list of the first few lines of a file.
        :return: returns the ShelxlIOP class if the file head has shelx flavor. False if not.
        """
        hints = Loader.hints['shelx']
        hits = sum([1 if line[:5].lower() in hints else 0 for line in filehead])
        if hits > 2:
            self.printer("Shelxl format identified.")
            return ShelxlIOP
        return False

    def _tastes_like_XD(self, filehead):
        """
        Checks whether the start of a file has a XD flavor.
        :param filehead: list of the first few lines of a file.
        :return: returns the XDIOP class if the file head has XD flavor. False if not.
        """
        hints = Loader.hints['xd']
        hits = sum([1 if line.split()[0].lower() in hints else 0 for line in filehead if len(line.split())])
        if hits > 1:
            self.printer("XD format identified.")
            return XDIOP
        return False

    def _tastes_like_CIF(self, filehead):
        hints = Loader.hints['cif']
        filehead = ''.join(filehead).lower()
        hits = sum([1 if hint in filehead else 0 for hint in hints])
        if hits > 1:
            self.printer("CIF format identified.")
            return CIFIOP
        return False

    def _tastes_like_PDB(self, filehead):
        hints = Loader.hints['pdb']
        hits = sum([1 if line[:6] in hints else 0 for line in filehead])
        if hits > 1:
            self.printer("PDB format identified.")
            return PDBIOP
        return False


    def _determine_correct_IOP(self, filename):
        """
        Returns an IOP for the given filetype.
        """
        iop = self._taste_file(filename)
        if iop:
            return iop
        if filename is 'xd.mas':
            filename = 'xd.res'
        if any([string in filename for string in ['xd.res', 'xd.inp']]):
            return XDIOP(filename)
        elif any([filename.endswith(string) for string in ['.ins', '.res']]):
            return ShelxlIOP(filename)
        elif filename.endswith('.cif'):
            return CIFIOP(filename)
        elif filename.endswith('.pdb'):
            return PDBIOP(filename)

    def no_file_exit(self):
        """
        Exits the APD-Toolkit.
        """
        message = 'ERROR: No suitable file found in working directory.'
        apd_exit(1, message=message)

    def get_symmetry(self):
        return self.IOP.get_symmetry()

    def get_lattice(self):
        return self.IOP.get_lattice()

    def write(self):
        self.IOP.write()

    def get_IOP(self):
        return self.IOP

    def get_write_copy(self, filename):
        filename += Loader.suffix[self.get_active_id().rstrip('1234567890')]
        return self.IOP.clone(filename)


if __name__ == '__main__':

    printer = apd_printer()
    test = Loader(printer)
    test.auto_setup()
    test.load('test')
