"""
Created on Feb 19, 2014

@author: Jens Luebben

Module for parsing a CIF and providing and interface for
accessing and editing the file.
"""
import numpy as np
import lauescript.cryst.crystgeom as cg
import lauescript.cryst.transformations as transformations


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
        self.order = []
        self.filename = filename
        self.tables = []
        self.data = ''
        super(CIF, self).__init__()
        self.read()
        self.read_content()
        # =======================================================================
        # try:
        #=======================================================================
        self.parse()
        self.convert()
        #=======================================================================
        # except Exception as x:
        #     print 'Error: Could not parse CIF.\n{}'.format(x)
        #=======================================================================
        self.postprocess()


    def read(self):
        self.readpointer = open(self.filename, 'r')

        self.words = []
        for line in self.readpointer.readlines():
            if not line.lstrip(' ')[0] == '#':
                self.words += [i for i in line.rstrip('\r\n').split(' ') if len(i) > 0]
        self.preprocess()

    def preprocess(self):
        """
        Searches the content for multi word and multi line
        values and joins them to a single string.
        """
        new_words = []
        longword = ''
        long_switch = False
        multiword = ''
        multi_switch = False
        multi_counter = 0
        for word in self.words:
            if word[-1] == '\'' and long_switch:
                long_switch = False
                longword += word
                new_words.append(longword)
                longword = ''
            elif long_switch:
                longword += word + ' '
            elif word[0] == '\'':
                longword += word + ' '
                long_switch = True
                if word[-1] == '\'':
                    new_words.append(word)
                    longword = ''
                    long_switch = False

            elif word == ';' and multi_switch:
                multi_switch = False
                multiword += '\n' + word
                new_words.append(multiword)
                multiword = ''
            elif multi_switch:
                if multi_counter == 6:
                    multiword += '\n'
                    multi_counter = 0
                multiword += word + ' '
                multi_counter += 1
            elif word[0] == ';' and not multi_switch:
                multiword += '\n' + word + '\n'
                multi_switch = True
                multi_counter = 0

            else:
                new_words.append(word)
        self.words = new_words

    def postprocess(self):
        """
        Checks if multiline values contain only a '?' character.
        If that is the case the multiline value is replaced by
        by a single line '?' character.
        """
        for key, value in self.items():
            if key[0] == '_' and type(value) == type(''):
                if value.lstrip(' ;\n').rstrip(' ;\n') == '?':
                    self[key] = '?'
        for key, value in self.items():
            if type(value) == type(''):
                if ' ' in value and not ';' in value and not '\'' in value:
                    self[key] = '\'' + value + '\''
            else:
                for i, entry in enumerate(value):
                    if ' ' in entry:
                        value[i] = '\'' + entry + '\''

    def convert(self):
        """
        Transforms the fractional coordinates in cartesian
        coordinates.
        """
        #transmatrix = invstring._get_frac2cart_matrix(self.cell)
        for value in self.positions.values():
            #value['cart'] = cg.frac2cart(value['frac'], transmatrix)
            value['cart'] = transformations.frac2cart(value['frac'],self.cell)

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
                                                                   value(self['_atom_site_fract_z'][i])])}

            try:
                atomdict[self['_atom_site_label'][i]]['Uiso'] = value(self['_atom_site_U_iso_or_equiv'][i])
            except:
                atomdict[self['_atom_site_label'][i]]['Uiso'] = ''
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
        wordcontent = self.words
        read = False
        for i in range(len(wordcontent)):
            word = wordcontent[i]
            if word.startswith('data_'):
                self.data = word[5:]
            if '_' in word[0] and not word in self.keys():
                read = word
            elif read:
                self.order.append(read)
                self[read] = word
                read = False


    def read_tables(self):
        """
        Searches the cif file for loops and creates
        dictionary entries for each column of every
        table.
        """
        wordcontent = self.words
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
        body = body.replace('\n', ' ').replace('\r', '')  # .split('\'')
        linelen = len(columns)
        self.tables.append(columns)
        body = body.split(' ')
        cleanbody = []
        join = False
        joined = ''
        for element in body:
            if not len(element) == 0:
                if element.startswith('\'') and element.endswith('\''):
                    element = element[1:-1]
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
        for i in range(int(len(cleanbody) / linelen)):
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
                try:
                    if not len(col[i]) > 1:
                        types[j] = False
                except:
                    types[j] = False
                try:
                    if len(col[i]) > widths[j]:
                        widths[j] = len(col[i])
                except:
                    pass
        for i, width in enumerate(widths):
            if width > 15:
                widths[i] = 5
        for i in range(length):
            for j, col in enumerate(columns):
                try:
                    if types[j] and not col[i].endswith(')'):
                        col[i] += '   '
                    if col[i].startswith('_'):
                        string.append('{0:>}'.format(col[i]))
                    else:
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
        # =======================================================================
        # keys=self.order
        #=======================================================================
        try:
            i = keys.index('_shelx_res_checksum')
            j = keys.index('_shelx_res_file')
            if i < j:
                keys[i], keys[j] = keys[j], keys[i]

            i = keys.index('_shelx_hkl_checksum')
            j = keys.index('_shelx_hkl_file')
            if i < j:
                keys[i], keys[j] = keys[j], keys[i]
        except:
            pass
        for key in keys:
            if key[0] == '_':
                value = self[key]
                if not type(value) == type([]):
                    self.file += '{:40s}     {} \n'.format(key, value)

        for table in self.tables:
            columns = []
            for column in table:
                plus = self[column]
                if not type(plus) == type([]):
                    plus = [plus]
                columns.append([column] + plus)
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
            if len(line) > 79:
                redo = True
                line = self._break_line(line)
            new_file += '\n' + line  # .lstrip(' ')
        self.file = new_file.lstrip('\n')
        return redo


    def __str__(self):
        self.construct_file()
        return self.file


    def write(self, filename=None):
        """
        Writes to content of the CIF instance to a file.
        """
        self.construct_file()
        if not filename:
            filename = 'apd.cif'
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
        line = line.rstrip(' ')
        try:
            breakpoint = line[60:].index(' ') + 60
            line.lstrip(' ')
            if line.endswith('\''):
                line = line.replace('\'', '\n;')
            return line[:breakpoint].lstrip(' ') + '\n' + line[breakpoint:].lstrip(' ')
        except:
            try:
                breakpoint = line[10:].index(' ') + 10
                line.lstrip(' ')
                if line.endswith('\''):
                    line = line.replace('\'', '\n;')
                return line[:breakpoint].lstrip(' ') + '\n' + line[breakpoint:].lstrip(' ')
            except:
                return line


    def complete(self, CIFfile, omit):
        """
        Searches the CIF instance 'CIFfile' for information that
        is missing in the current instance.
        If missing information is found. The data is added to
        the current instance.
        """
        new = []
        for key in CIFfile.keys():
            if not key in self.keys() or self[key] == '?':
                if not key in omit and not CIFfile[key] == '?':
                    self[key] = CIFfile[key]
                    new.append(key)
        new_tables = []
        for table in CIFfile.tables:
            if not self.has_table(table) and not any(v in table for v in omit):
                self.tables.append(table)
                new_tables.append(table)

            for value in table:
                try:
                    new.remove(value)
                except:
                    pass
        return [new, new_tables]

    def has_table(self, table):
        """
        Returns True if the CIF contains the loop defined by
        'table'. To be evaluated as True one table in the CIF
        must contain at least two thirdth of the same columns
        as 'table'.
        """
        for table1 in self.tables:
            check = len(table1)
            checkref = int(check)
            for value in table:
                if value in table1:
                    check -= 1
            if abs(check - checkref) > checkref - checkref / 3:
                return True
        return False


    def change_value(self, new_value, column, row_keys, search_columns=None):
        """
        Changes a specific value in a CIF-Loop. The 'new_value' argument
        specifies the what value should be set instead of the original
        value. If 'new_value' is 'no_esd', the original value is stripped
        off it's estimated standard deviation.
        The 'column' option specifies which loop column the value is located
        in.
        'row_keys' specifies the key values that are used to determine
        the appropriate row the value belongs to. e.g.: two atom labels for
        a specific bond length.
        The optional 'search_columns' keyword is used to specify how many
        columns are searched for the 'row_keys'. e.g.: If all angles are
        supposed to be changed that are defined by the positions of two
        atoms, the correct option would be (0:3). This would indicate
        that the first three columns of the loop containing the
        column 'geom_angle' are searched for the 'row_keys'.
        If instead the columns 2 to 4 should be searched, the argument
        must be (1:4).
        'search_columns' defaults to (0:len(row_keys)).

        """
        done = False
        if not search_columns:
            search_columns = (0, len(row_keys))
        for table in self.tables:
            if column in table:
                for i in range(len(self[column])):
                    checks = []

                    for c in table[search_columns[0]:search_columns[1]]:
                        checks.append(self[c][i])
                    if all([any([key == check for check in checks]) for key in row_keys]):
                        done = True
                        if new_value == 'no_esd':

                            self[column][i] = '{:>.4f} '.format(value(str(self[column][i])))
                        else:
                            self[column][i] = new_value
                        break
                break
        if done:
            return True


    def remove_row(self, column, index):
        """
        Removes a the row with the index 'index' from the
        table containing the column 'column'.
        """
        for table in self.tables:
            if column in table:
                for col in table:
                    del self[col][index]
                break


    def remove_table(self, column):
        """
        Removes the table containing the column 'column' from
        the CIF.
        """
        for i, table in enumerate(self.tables):
            if column in table:
                for col in table:
                    del self[col]
                del self.tables[i]

    def add_value(self, key, value):
        """
        Adds a record to the CIF.

        'key' mus be a string starting with a '_' character.
        'value' can be any string.
        """
        self[key] = value

    def add_table(self, columns):
        """
        Adds a loop to the CIF instance. The 'columns'
        argument must be a list containing one list for
        every column. Every column list must contain the
        column name as its first value and the corresponding
        data as subsequent values.
        """
        table = []
        for column in columns:
            table.append(column[0])
            self[column[0]] = column[1:]
        self.tables.append(table)


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
