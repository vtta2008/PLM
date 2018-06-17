"""
Created on Okt 1, 2013

@author: jens

Module handling the data input and output of the APD-Toolkits main functions.
The CIF-Parser class is deprecated. Instead the CIF-Parser in the crystgeom2
package should be used.
"""

import os
from sys import exit
from string import digits

import numpy as np

from lauescript.core import core
import lauescript.cryst.crystgeom as cg
import lauescript.invstring2 as invstring
from lauescript.core import core


# ===============================================================================
# from apd.lib.apdio.loader import Loader
#===============================================================================

#===============================================================================
# from apd.invstring import _get_frac2cart_matrix
#===============================================================================



value_digits = digits + '()'


def read_invarioms_workdir():
    """
    Function for reading an 'Invariome.descent' file in the working
    directory.

    Reads the Invariome.descent file and returns a list of model systems needed
    to replace all the atoms.
    It also returns a dictionary keying the atom name to the invariom name and
    the model system containing the atom.
    """
    invariomlist = []
    invdict = {}
    atomlist = []
    filepointer = open('Invariome.descent', 'r')
    for line in filepointer.readlines():
        line = line.split(' ')
        newline = [i for i in line if len(i) > 2]

        atomlist.append(newline[0])
        if newline[-1][-1] == '\n':
            newline[-1] = newline[-1][:-1]
        newline[-1] = newline[-1].replace(',', '.')
        if not newline[-1] in invariomlist:
            invariomlist.append(newline[-1])
        invdict[newline[0][:-1]] = newline[1:]
    return invariomlist, invdict, atomlist


def read_database2(data, dabapointer, invlist):  #,invdict,atomlist):
    """
    Function for reading the 'APD_DABA.txt' file.

    invlist=[names of modelcompounds]
    atomlist=Deprecated
    invdict=Deprecated
    """
    parseswitch = False
    for inv in invlist:
        data.give_daba_molecule(inv)

    for line in dabapointer.readlines():
        if any('!' + i + '\n' in line for i in invlist):
            mol = line[1:][:-1]
            parseswitch = True
        if parseswitch and '!=' in line: parseswitch = False

        if parseswitch and not '!' in line:
            if 'Nam' in line: name, invname = line.split(' ') \
                                                  [-1][:-1], line.split(' ')[-2]
            if 'Pos' in line: pos = line.split(' ')[1:]
            if 'ADP' in line:
                adp = line.split(' ')[1:]
                pos = np.array([float(i) for i in list(pos)])
                adp = np.array([float(i) for i in list(adp)])
                #---------------------------------------------------------- try:
                #-------------------- data[mol].add_atom(name=name,cart=pos)
                #------------------------------------------------------- except:
                #mol=mol.replace('.',',')
                data[mol].give_atom(name=name,
                                    cart=pos,
                                    invariom_name=invname)
                data[mol].atoms[-1].give_adp(key='cart_int', value=adp)


def read_database(data, database, invlist, readAll=False):
    reader = DatabaseReader(database, readAll=readAll)
    reader.read(data, invlist)


class DatabaseReader(object):
    def __init__(self, database, readAll=False):
        self.readAll = readAll
        self.daba = database
        self.reset()

    def reset(self):
        self.compound = None
        self.element = None
        self.invariom = []
        self.orientation = []
        self.coordinates = None
        self.ADP = None
        self.atoms = []
        self.hit = False
        self.i = 0

    def readline(self, line):
        key = line[0]
        getattr(self, '_parse_' + key)(line.rstrip('\n')[2:])

    def read(self, data, invlist):
        self.data = data
        self.reset()
        self.invlist = invlist
        for inv in invlist:
            if not inv in self.data.keys():
                data.give_daba_molecule(inv)

        for line in self.daba:
            if not line.startswith('#'):
                if line.startswith('N') or self.hit:
                    self.readline(line)
                    #=======================================================================
                    # dabapointer.close()
                    #=======================================================================
                    #=======================================================================
                    # print self.data.keys()
                    # for value in self.data.values():
                    #     print
                    #     print value
                    #     for atom in value.atoms:
                    #         print atom
                    #=======================================================================

    def _parse_N(self, line):
        self.reset()
        if any([line == inv for inv in self.invlist]) or self.readAll:
            self.compound = line
            self.hit = True
        if self.readAll:
            self.data.give_daba_molecule(line)

    def _parse_E(self, line):
        self.element = line

    def _parse_I(self, line):
        line = line.split(' ')
        self.invariom.append(line[0])
        self.orientation.append([np.array([float(i) for i in line[1:4]]), np.array([float(i) for i in line[4:]])])

    def _parse_C(self, line):
        self.coordinates = np.array([float(i) for i in line.split(' ')])

    def _parse_A(self, line):
        self.ADP = np.array([float(i) for i in line.split(' ')])
        self.flush()


    def flush(self):
        #=======================================================================
        # print
        # print self.compound
        # print self.invariom
        # print self.coordinates
        # print self.ADP
        #=======================================================================
        self.data[self.compound].give_atom(name=self.element + '(' + str(self.i) + ')',
                                           cart=self.coordinates)
        self.i += 1
        self.data[self.compound].atoms[-1].give_adp(key='cart_int', value=self.ADP)
        for i, j in enumerate(self.invariom):
            self.data[self.compound].atoms[-1].add_invariom(j, self.orientation[i])
        self.soft_reset()

    def soft_reset(self):
        self.element = None
        self.invariom = []
        self.orientation = []
        self.coordinates = None
        self.ADP = None


def read_experimental_coordinates(data):
    """
    Function for reading XD format files in the working
    directory.
    """
    expcell, exppos, names = cg.read_coordinates(sort=False)
    data['exp'].give_cell(expcell)
    for atom in names:
        data['exp'].add_atom(vars()['atom'])
        data['exp'].atoms[-1].molecule = data['exp']
        data['exp'].atoms[-1].give_frac(np.array(exppos[atom]))


def FlexLoad(data, loader, dabapath, config, filename='./', noTransfer=False, planarityThreshold=.1):
    """
    A more flexible variation of the 'Load' function.

    The actual 'loading' is handled by the 'Loader'
    class which relies on InputOutputProviders to
    access files independent of their specific file
    format.

    FlexLoad itself is only integrating the molecule
    returned by the 'Loader' in the APD-Toolkit's
    data structure and subsequently populating the
    data structure with the necessary model molecules.
    """
    printer = config.get_active_printer()
    loader.auto_setup(filename)

    iop = loader.get_IOP()
    # if iop.supportsSym:
    #     iop.grow()
    #     for a in data['exp'].atoms:
    #         print(a.get_name())
    data.register_molecule(loader.load('exp', grow=iop.supportsSym), 'exp')

    data['exp'].give_cell(loader.get_cell())
    T = config.arg('temp')
    if not T:
        T = loader.get_temperature()
    if not T:
        printer.highlight('Warning: No temperature specified. Falling back to default.')
        T = 100
    T = int(T)
    data.give_temperature(T)


    dabapa = dabapath + '/APD_DABA_{:.1f}_.txt'.format(data.temperature)
    printer('Crystal temperature: {:.1f} K'.format(data.temperature))
    try:
        dabapointer = open(dabapa)
    except IOError:
        printer('inout.py: Error: File {} not found.'.format(dabapa))
        printer('Calling database generator to generate appropriate database file.\n\n')
        import lauescript.database as db

        frequency_cutoff = config.get_frequency_cutoff()
        db.generate_database(data, frequency_cutoff, clean=False, temperatures=[data.temperature], path=dabapath,
                             newh=config.get_config_valueBool('APD', 'newH'))
        dabapointer = open(dabapa)

    database = dabapointer.readlines()
    printer()
    if noTransfer:
        read_database(data, database, invlist=[], readAll=True)
        return
    correctionsPointer = open(dabapath + '/empirical_corrections.txt')
    for invdict, orientations, compounds in invstring.get_invariom_names(names=[i.name for i in data['exp'].atoms],
                                                                         cart=[i.cart for i in data['exp'].atoms],
                                                                         cell=iop.get_cell(),
                                                                         dictionary=True,
                                                                         orientations=True,
                                                                         compounds=open(dabapath + '/APD_MAP.txt'),
                                                                         corrections=correctionsPointer,
                                                                         dynamic=True,
                                                                         output=printer,
                                                                         verbose=False,
                                                                         newH=config.get_config_valueBool('APD', 'newH'),
                                                                         planarityThreshold=planarityThreshold):


        invlist = [item for _, item in compounds.items()]
        read_database(data, database, invlist)
        kill = False
        misses = []
        for atom in data['exp'].atoms:
            invname = invdict[atom.name]
            orientation = orientations[atom.name]
            atom.add_invariom(invname, orientation)
            if invname in compounds.keys() and not atom.model_compound:
                modelname = compounds[invname]
                atom.model_compound = data[modelname]
                atom.set_active_invariom(invname)
            elif invname not in compounds.keys() and not atom.model_compound:
                misses.append((atom, invname))
                kill = True
                printer('Trying dynamic invariom name for atom {}. {} not available'.format(atom.name, invname))
    printer()
    if kill:
        for atom in misses:
            atom = atom[0]
            neighbours = cg.get_framework_neighbours(atom, useH=False)
            if len(neighbours) > 1:
                for atom2 in neighbours:
                    if not atom2.get_active_invariom():
                        message = 'Error: The following invarioms are missing in the database:\n'
                        message += '\n'.join(['{:<6} <-> {:>}'.format(miss[0].name, miss[1]) for miss in misses])
                        message += '\n\n!!!Terminating program due to fatal error: MISSING INVARIOMS!!!'
                        core.apd_exit(message=message)
                atom.tolerate()
                printer('WARNING: Tolerating missing invariom for {}.'.format(atom.name))
            else:
                message = 'Error: The following invarioms are missing in the database:\n'
                message += '\n'.join(['{:<6} <-> {:>}'.format(miss[0].name, miss[1]) for miss in misses])
                message += '\n\n!!!Terminating program due to fatal error: MISSING INVARIOMS!!!'
                core.apd_exit(message=message)
        return
        message = 'Error: The following invarioms are missing in the database:\n'
        message += '\n'.join(['{:<6} <-> {:>}'.format(miss[0].name, miss[1]) for miss in misses])
        message += '\n\n!!!Terminating program due to fatal error: MISSING INVARIOMS!!!'
        core.apd_exit(message=message)


class CIF(dict):
    """
    A very simple parser for CIF files.

    Just initialize instance with the cif file's filename and access
    the atom by adressing the dictionary CIF.atoms
    Every key of the dictionary is an atom name and holds a second
    dictionary holding the keys 'element', 'frac', 'adp' and 'adp_error'.
    Each of the keys holds a numpy.array with the corresponding values.
    Note: The dictionary CIF.atoms only holds atoms with specified U_ij
    values. To access the positional data of atoms without specified
    U_ij values the dictionary CIF.positions with the keywords
    'frac' and 'element' can be used.

    Every other value of the cif file can be accessed by adressing
    the CIF instance with the name of the value. If the value is part
    of a loop, a list of strings is returned. Otherwise a single string
    is returned.
    A list of all parsed values can be accessed by calling the build-in
    method CIF.keys() which returns a list of all parsed cif keywords.
    """

    def __init__(self, filename):
        """
        Just initialize the class by specifying the filename.
        Everything else will be handled automatically.
        """
        self.filename = 'apd.cif'
        self.tables = []
        self.data = ''
        super(CIF, self).__init__()
        self.readpointer = open(filename, 'r')
        self.content = self.readpointer.readlines()
        self.read_content()
        try:
            self.parse()
            self.convert()
        except:
            print('inout.py: Error: Could not parse CIF.')


    #===========================================================================
    # def convert(self):
    #     '''
    #     Transforms the fractional coordinates in cartesian
    #     coordinates.
    #     '''
    #     transmatrix=invstring._get_frac2cart_matrix(self.cell)
    #     for value in self.positions.values():
    #         value['cart']=cg.frac2cart(value['frac'],transmatrix)
    #===========================================================================


    def parse(self):
        """
        Evaluates the data read by self.read_content() and creates
        the dictionarys self.atoms and self positions for making
        the positional and vibrational data of the molecules
        easily accessable.
        """
        a = value(self['_cell_length_a'])
        b = value(self['_cell_length_b'])
        c = value(self['_cell_length_c'])
        alpha = value(self['_cell_angle_alpha'])
        beta = value(self['_cell_angle_beta'])
        gamma = value(self['_cell_angle_gamma'])
        self.cell = (a, b, c, alpha, beta, gamma)

        atomdict = {}
        fullatomdict = {}

        for i in range(len(self['_atom_site_label'])):
            name = self['_atom_site_label'][i]
            if 'DUM' in name:
                continue
            atomdict[self['_atom_site_label'][i]] = {'frac': \
                                                         np.array([value(self['_atom_site_fract_x'][i]),
                                                                   value(self['_atom_site_fract_y'][i]),
                                                                   value(self['_atom_site_fract_z'][i])]),
                                                     'Uiso': value(self['_atom_site_U_iso_or_equiv'][i])}
            try:
                atomdict[self['_atom_site_label'][i]] \
                    ['element'] = str(self['_atom_site_type_symbol'][i])
            except:
                atomdict[self['_atom_site_label'][i]] \
                    ['element'] = cg.xd_element(self['_atom_site_label'][i])

        for i in range(len(self['_atom_site_aniso_label'])):
            name = self['_atom_site_aniso_label'][i]
            if 'DUM' in name:
                continue
            fullatomdict[name] = {'frac': atomdict[name]['frac'],
                                  'adp': np.array([value(self['_atom_site_aniso_U_11'][i]),
                                                   value(self['_atom_site_aniso_U_22'][i]),
                                                   value(self['_atom_site_aniso_U_33'][i]),
                                                   value(self['_atom_site_aniso_U_12'][i]),
                                                   value(self['_atom_site_aniso_U_13'][i]),
                                                   value(self['_atom_site_aniso_U_23'][i])]),
                                  'adp_error': np.array([error(self['_atom_site_aniso_U_11'][i]),
                                                         error(self['_atom_site_aniso_U_22'][i]),
                                                         error(self['_atom_site_aniso_U_33'][i]),
                                                         error(self['_atom_site_aniso_U_12'][i]),
                                                         error(self['_atom_site_aniso_U_13'][i]),
                                                         error(self['_atom_site_aniso_U_23'][i])])}

            try:
                fullatomdict[name]['element'] = str(self['_atom_site_type_symbol'][i])

            except:
                fullatomdict[name]['element'] = \
                    cg.xd_element(name)

        self.atoms = fullatomdict
        self.positions = atomdict


    def read_content(self):
        """
        Searches the cif file for all keywords starting with
        '_' and creates a dictionary entry with the same name
        holding the value of that keyword.
        """
        self.read_tables()
        linecontent = ''
        for line in self.content:
            linecontent += line.replace('\n', ' ')
        wordcontent = [i for i in linecontent.split(' ') if len(i) > 0]
        read = False
        for i in range(len(wordcontent)):
            word = wordcontent[i]
            if word.startswith('data_'):
                self.data = word[5:]
            if '_' in word[0] and not word in self.keys():
                read = word
            elif read:
                self[read] = word
                read = False


    def read_tables(self):
        """
        Searches the cif file for loops and creates
        dictionary entries for each column of every
        table.
        """
        stringcontent = ''
        for line in self.content:
            stringcontent += line
        wordcontent = [i for i in stringcontent.replace('\n', ' ').split(' ') if len(i) > 0]
        tableswitch = False
        bodyswitch = False

        columns = []
        body = ''

        for word in wordcontent:
            if tableswitch:
                if '_' in word.lstrip(' ')[0] and not bodyswitch:
                    colname = word.rstrip('\r')
                    self[colname] = []
                    columns.append(colname)
                elif bodyswitch and '_' in word.lstrip(' ')[0] or 'loop_' in word or word.lstrip(' ').startswith("#"):
                    tableswitch = False
                    self._parse_table_body(columns, body)
                    if 'loop_' in word:
                        tableswitch = True
                        body = ''
                        columns = []
                        bodyswitch = False
                elif not ';' in word:
                    body += ' ' + word
                    bodyswitch = True

            elif 'loop_' in word:

                body = ''
                columns = []
                tableswitch = True
                bodyswitch = False

        if tableswitch:
            self._parse_table_body(columns, body)


    def _parse_table_body(self, columns, body):
        """
        Parses the body of a loop in the cif file by
        assigning the read values to the columns specified
        in 'columns'.
        """
        #=======================================================================
        # print columns
        #=======================================================================
        body = body.replace('\n', ' ').replace('\r', '')  #.split('\'')
        linelen = len(columns)
        self.tables.append(columns)
        body = body.split(' ')
        cleanbody = []
        join = False
        joined = ''
        for element in body:
            if not len(element) == 0:
                if '\'' in element and join:
                    joined += ' ' + element[:-1]
                    cleanbody.append(joined)
                    join = False
                elif '\'' in element and not join:
                    join = True
                    joined = element[1:]
                elif join:
                    joined += ' ' + element
                elif not join:
                    cleanbody.append(element)
        content = [[columns[i]] for i in range(linelen)]
        for i in range(len(cleanbody) / linelen):
            line = cleanbody[linelen * i:linelen * (i + 1)]
            for j in range(linelen):
                content[j].append(line[j])
        for line in content:
            self[line[0]] = line[1:]

    def make_table(self, columns):
        """
        Returns an ASCII representation of a CIF loop.
        """
        string = ['loop_\n']
        length = max([len(i) for i in columns])
        widths = [0] * len(columns)
        types = [True] * len(columns)
        for i in range(length - 1):
            i += 1
            for j, col in enumerate(columns):
                try:
                    _ = value(col[i])
                    _ = error(col[i])
                except:
                    types[j] = False
                if not len(col[i]) > 1:
                    types[j] = False
                try:
                    if len(col[i]) > widths[j]:
                        widths[j] = len(col[i])
                except:
                    pass
        for i in range(length):
            for j, col in enumerate(columns):
                try:
                    if types[j] and not col[i].endswith(')'):
                        col[i] += '   '
                    string.append('{0:>{1}}'.format(col[i], widths[j]))
                except:
                    string.append('{:10}'.format('.'))
                if i == 0:
                    string.append('\n')
            if not i == 0:
                string.append('\n')
        string.append('\n')
        string = ' '.join(string)
        return string

    def construct_file(self, omit=None):
        """
        Generates an ASCII representation of the CIF file.
        """
        self.file = 'data_{}\n'.format(self.data)
        self.columns = []
        if not omit:
            omit = []
        keys = sorted([i for i in self.keys() if not i in omit])
        for key in keys:
            if key[0] == '_':
                value = self[key]
                if not type(value) == type([]):
                    self.file += '{:40s}     {} \n'.format(key, value)

        for table in self.tables:
            columns = []
            for column in table:
                columns.append([column] + self[column])
            self.file += self.make_table(columns)

        redo = True
        while redo:
            redo = self._limit_lines()


    def _limit_lines(self):
        """
        Checks if all lines are 78 or less characters long.
        If a line is longer, a function inserting a linebreak
        is called and the method returns True.
        If no line is too long the method returns False.
        """
        new_file = ''
        redo = False
        for line in self.file.split('\n'):
            if len(line) > 78:
                redo = True
                line = self._break_line(line)
            new_file += '\n' + line
        self.file = new_file
        return redo


    def write(self, filename=None):
        """
        Writes to content of the CIF instance to a file.
        """
        self.construct_file()
        if not filename:
            filename = self.filename
        writepointer = open(filename, 'w')
        self.filename = filename
        for line in self.file:
            writepointer.write(line)
        writepointer.close()


    def _break_line(self, line):
        """
        Tries to break the line at the first ' ' character after
        character number 60. If there is no such character after
        position 60, the first ' ' character after position
        10 is replaced by a '\n' character.
        """
        try:
            breakpoint = line[60:].index(' ') + 60
            return line[:breakpoint] + '\n' + line[breakpoint:]
        except:
            breakpoint = line[10:].index(' ') + 10
            return line[:breakpoint] + '\n' + line[breakpoint:]


    def complete(self, CIFfile):
        """
        Searches the CIF instance 'CIFfile' for information that
        is missing in the current instance.
        If missing information is found. The data is added to
        the current instance.
        """
        for key in CIFfile.keys():
            if not key in self.keys() or self[key] == '?':
                self[key] = CIFfile[key]

    def change_value(self, new_value, column, row_keys, search_columns=None):
        """
        Changes a specific value in a CIF-Loop. The 'new_value' argument
        specifies the what value should be set instead of the original
        value. If 'new_value' is 'no_esd', the original value is stripped
        off it's estimated standard deviation.
        The 'column' option specifies which loop column the value is located
        in.
        'row_keys' specifies the key values that are used to determine
        the appropriate row the value belongs to. eg: two atom labels for
        a specific bond length.
        The optional 'search_columns' keyword is used to specify how many
        columns are searched for the 'row_keys'. eg: If all angles are
        supposed to be changed that are defined by the positions of two
        atoms, the correct option would be (0:3). This would indicate
        that the first three columns of the loop containing the the the
        column 'geom_angle' are searched for the 'row_keys'.
        If instead the columns 2 to 4 should be searched, the argument
        must be (1:4).
        'search_columns' defaults to (0:len(row_keys)).

        """
        if not search_columns:
            search_columns = (0, len(row_keys))
        for table in self.tables:
            if column in table:
                for i in range(len(self[column])):
                    checks = []

                    for c in table[search_columns[0]:search_columns[1]]:
                        checks.append(self[c][i])
                    if all([any([key == check for check in checks]) for key in row_keys]):
                        if new_value == 'no_esd':

                            self[column][i] = '{:>.4f} '.format(value(str(self[column][i])))
                        else:
                            self[column][i] = new_value
                        break
                break

    def remove_row(self, column, index):
        for table in self.tables:
            if column in table:
                for col in table:
                    del self[col][index]
                break


    def remove_table(self, column):
        for i, table in enumerate(self.tables):
            if column in table:
                for col in table:
                    del self[col]
                del self.tables[i]


def value(string):
    """
    Needs a string of the format '1.234(5)' as argument and
    returns the float '1.234'. If the string is of the format
    '1.234' the same string is returned. If the string has a
    different format, the function returns 'None'.
    """
    if not '(' in string:
        return float(string)
    for i in range(len(string)):
        if string[i] == '(':
            break
    try:
        return float(string[:i])
    except:
        return None


def error(string):
    """
    Needs a string of the format '1.234(5)' as argument and
    returns the error of the value as the float '0.005'.
    If the string has a different format, the function
    returns 'None'.
    """
    newstring = ''
    for i in range(len(string)):
        if string[i] == '(':
            break
        elif string[i] == '.':
            newstring += '.'
        else:
            newstring += '0'
    errorstring = string[i + 1:-1]
    newstring = newstring[:-len(errorstring)]
    try:
        return float(newstring + string[i + 1:-1])
    except:
        return None




