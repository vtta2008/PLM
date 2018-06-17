"""
Created on 08.02.2014

@author: Jens Luebben

Module for formatting ASCII output while giving feedback
on the current execution state of the program.
"""
from __future__ import print_function
from sys import stdout



class apd_table(object):
    """
    Class representing an ASII table.
    """

    def __init__(self, columns):
        """
        Initializes the table.
        'columns' must be a list of strings representing a line
        of the table
        """
        self.columns = columns
        self.width = len(columns)
        self.head = True
        self.body = [columns]

    def add_head(self, row):
        """
        Adds a header to the table. Row must be a list of strings.
        """
        self.body.append(row)

    def append(self, row):
        """
        Adds a row the the table. Row must be a list of strings.
        """
        if self.head:
            self.body.append('%end_head%')
        self.head = False
        self.body.append(row)

    def line(self):
        """
        Adds a seperating line to the table.
        """
        self.body.append([None])

    def flush(self):
        """
        Calculate the space requirements of all cells and creates
        a list of strings (self.strings) representing the table.
        A loop calling print of every sting in self.strings would
        print to table.
        """
        self.space = [0 for _ in range(self.width)]
        for i, _ in enumerate(self.columns):
            self.space[i] = max([len(row[i]) for row in self.body if row[0] is not None])
        self.strings = ['' for _ in range(len(self.body))]
        self.maxwidth = sum(self.space) + len(self.space) * 3 + 1
        for i, row in enumerate(self.body):
            if row[0] is None:
                self.strings[i] = self.maxwidth * '-'
                continue

            if row == '%end_head%':
                self.strings[i] = (self.maxwidth - 1) * '='
            else:
                for j, element in enumerate(row):
                    self.strings[i] += '| {0:{1}} '.format(element, self.space[j])
                    if j == 0:
                        self.strings[i] = self.strings[i][1:]


class apd_printer(object):
    """
    A class for formatting the program output depending
    on the module producing that output.
    Every module should create an instance of the class thus
    allowing customization for every module independently.
    """

    def __init__(self, indent=0, name='_____', filename=None):
        """
        the 'indent' argument specifies how far the output
        should be indented. The 'name' argument is used to
        generate the 'headline' and 'bottomline' strings.
        """
        self.muted = False
        self.indent = indent
        self.name = name
        self.charlen = len(name)

        self.files = {}
        self.table_data = False
        if filename:
            import sys

            self.stdout = sys.stdout
            f = open(filename, 'w')
            sys.stdout = f
        self._reindent()

    def _reindent(self):
        """
        Resets the self.line_start and self.line_break attributes
        with a newly defined indentation level.
        """
        self.line = '  ' + 26 * '#' + self.charlen * '#' + '\n'
        self.line_start = ' {0:{2}<{1}}| '.format('', self.indent, ' ')
        self.line_break = '\n' + self.line_start

    def mute(self):
        """
        Mutes the printer.
        """
        self.muted = True

    def unmute(self):
        """
        Unmutes the printer.
        """
        self.muted = False

    def reindent(self, amount=5):
        """
        Increases the indentation level by 'amount' characters.
        """
        self.indent += amount
        self._reindent()

    def dedent(self, amount=1):
        """
        Decreases the indentation level by 'amount' characters.
        """
        self.indent -= amount
        self._reindent()

    def release(self):
        """
        Resets the output to stdout.
        """
        import sys

        try:
            sys.stdout = self.stdout
        except:
            pass

    def write(self, *args, **kwargs):
        """
        Writes to the defined output.
        See '__call__' for detailed documentation.
        """
        self.__call__(*args, **kwargs)

    def ask(self, question):
        """
        Uses 'raw_input' to ask for user input.
        The string 'question' will be indented correctly and
        placed before the input prompt.
        """
        return input(self.line_start + '{} :'.format(question))

    def __call__(self, *args, **kwargs):
        """
        Standard interface for printing data.
        Prints the correctly indented string represenation
        for every argument in a new line.

        The keyword 'use' can be used to write files to
        previously registered files. 'use' should be keyed
        to a list of strings. One for every file key.
        If the string is 'all', The args are written to the
        default output as well as to all registered files.
        """
        if self.muted:
            return
        if 'use' in kwargs:
            if not type(kwargs['use']) == type([]):
                kwargs['use'] = list(kwargs['use'])
            if 'all' in kwargs['use']:
                self(*args)
                for key in self.files.keys():
                    for value in args:
                        self._write(value, key)
                return
            for key in kwargs['use']:
                for value in args:
                    self._write(value, key)

        else:
            for value in args:
                print(self.line_start + str(value).replace('\n', self.line_break))
            if not args:
                print(self.line_start)

    def _write(self, string, filename):
        """
        Redirects the write command to the filename specified in
        'filename'.
        """
        self.files[filename].write(string + '\n')

    def table(self, strings=None, head=False, done=False):
        """
        Interface for creating ASCII tables.

        'strings' must be a list of strings representing
        a row of the table.

        'head' specifies whether the row belongs to the
        head of the table (True) or the body (False).

        If 'done' is True, the table is printed to the output.
        """
        if strings:
            strings = [str(i) for i in strings]

        if not self.table_data:
            self.table_data = apd_table(strings)
        elif strings and head:
            self.table_data.add_head(strings)
        elif strings and not head:
            self.table_data.append(strings)
        if done:
            self.table_data.flush()
            for row in self.table_data.strings:
                self(row)
            self.table_data = None

    def table_line(self):
        """
        Interface for adding a separating line to an ASCII table.
        """
        self.table_data.line()

    def first(self):
        """
        Called at the beginning by the main program so start the
        indentation line.
        """
        print('_')

    def last(self):
        """
        Called by the main program before termination to end
        the indentation line.
        Also the self.release() method is called to restore
        sys.stdout if necessary.
        """
        print('_|')
        self.release()

    def enter(self):
        """
        Increase the indentation line.
        """
        print(self.line_start[:-7] + '|')
        print(self.line_start[:-7] + '|----|')
        print(self.line_start[:-7] + '     |')

    def exit(self):
        """
        Decrease the indentation line.
        """
        print(self.line_start[:-7] + '     |')
        print(self.line_start[:-7] + '|----|')
        print(self.line_start[:-7] + '|')

    def spacer(self):
        """
        Prints a spacer to optically seperate parts of
        the output.
        """
        print(self.line_start + '        ------|------')

    def headline(self, custom=False):
        """
        Prints a correctly indented string signaling the starting
        of an module.
        """
        if custom:
            line = '  ' + (6 + len(custom)) * '#' + '\n'
            self.__call__(line + '- #  {}  #\n'.format(custom) + line)
        else:
            self.__call__(self.line + '- #  Starting module: {}.py  #\n'.format(self.name) + self.line)

    def bottomline(self, custom=False):
        """
        Prints a correctly indented string signaling the exiting
        of an module.
        """
        if custom:
            line = '  ' + (6 + len(custom)) * '#' + '\n'
            self.__call__(line + '- #  {}  #\n'.format(custom) + line)
        else:
            self.__call__('', self.line + '- #  Exiting module: {}.py   #\n'.format(self.name) + self.line)

    def noreturn(self, value):
        """
        Prints the correctly indented string passed as argument
        and adds an 'carriage return'.
        """
        print(self.line_start + str(value), end='\r')
        stdout.flush()

    def create_progressbar(self, length=None):
        """
        Creates an ASCII progressbar.

        'lenght' must be an integer representing the number of
        characters that will be reserved for the progress bar.
        """
        if not length:  # == 'auto':
            length = 24 + self.charlen
        self.progress_bar = '[' + (length - 2) * '-' + ']'
        self.noreturn(self.progress_bar)

    def update_progressbar(self, percent):
        """
        Updates a previously created progressbar.
        'percent' must be an integer representing the
        progress in percent.
        """
        length = len(self.progress_bar) - 2
        complete = int(length * (float(percent) / 100.))
        free = length - complete
        self.progress_bar = '[' + complete * '#' + free * '-' + ']'
        self.noreturn(self.progress_bar)

    def finish_progressbar(self):
        """
        Fills any remaining characters to create a completed
        progress bar.
        """
        self.update_progressbar(100)
        print

    def register_file(self, filename, keyword, mode=None):
        """
        Registers a file to which the arguments passed to __call__
        will be send.
        'keyword' specifies which key will be used by the __call__
        method to identify which possible output will be used.
        the argument 'mode' specifies the mode in which the file
        should be opened. 'mode' will default to 'w'.
        """
        if not mode:
            mode = 'w'
        try:
            self.files[keyword] = open(filename, mode)
        except IOError:
            self.files[keyword] = open(filename, 'w')

    def highlight(self, arg, char='!'):
        """
        Surrounds a string 'arg' by character of type 'char' to
        highlight the output.

        'char' must be a string of arbitrary length.
        """
        l = len(arg) // len(char) + 4
        self()
        self(char * l)
        self('{0} {1:{2}} {0}'.format(char, arg, (l - 2) * len(char) - 2))
        self(char * l)

    def logo(self):
        return """
  WWWWWWWWWW    WWWWWWWW     WWWWWWWWW
  WWWWWWWW    WWWWWWWWWWWW    WWWWWWWW
  WWWWWWWW    WWWWWWWWWWWW     WWWWWWW
  WWWWWWW  W  WWWWWWWWWWWW  W  WWWWWWW
  WWWWWWW   W   WWWWWWWW   W   WWWWWWW
  WWWWWWWW   WW   WWWW   WW   WWWWWWWW
  WWWWWWWWW    WW      WW    WWWWWWWWW
  WWWWWWWWWWW     WWWW     WWWWWWWWWWW
  WWWWWWWWWW   WW      WW   WWWWWWWWWW
  WWWWWWWW   WW   WWWW   WW   WWWWWWWW
  WWWWWWW   W   WWWWWWWW   W   WWWWWWW
  WWWWWWW  W  WWWWWWWWWWWW  W  WWWWWWW
  WWWWWWWW    WWWWWWWWWWWW     WWWWWWW
  WWWWWWWW    WWWWWWWWWWWW    WWWWWWWW
  WWWWWWWWW     WWWWWWWW     WWWWWWWWW
  WWWWWWWWWW                WWWWWWWWWW
"""

    def Logo(self):
        return """
__________________________________________________________________________________
|                                                                                |
|                                                                                |
|     WWWWWWWWWWWWWWWWWWWW                               WWWWWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWWWW            WWWWWWWWWW            WWWWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWW           WWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWW          WWWWWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWW          WWWWWWWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWW         WWWWWWWWWWWWWWWWWWWWWWWW         WWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWW         WWWWWWWWWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWW          WWWWWWWWWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWW     W     WWWWWWWWWWWWWWWWWWWWWW     W     WWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWW    W      WWWWWWWWWWWWWWWWWWWW      W     WWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWW     W       WWWWWWWWWWWWWWWW       W     WWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWW      WW        WWWWWWWWWW        WW      WWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWW       WW          WW          WW       WWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWWW       WW                  WW        WWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWWWW        W                W        WWWWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWWWWWW                              WWWWWWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWWWWWWW                             WWWWWWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWWWW                                  WWWWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWW        WWW                 WW        WWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWW      WWW          WW          WW       WWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWW     WW         WWWWWWWWW        WW      WWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWW     W        WWWWWWWWWWWWWWW       W     WWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWW     W      WWWWWWWWWWWWWWWWWWWW      W     WWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWW     W     WWWWWWWWWWWWWWWWWWWWWW           WWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWW          WWWWWWWWWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWW          WWWWWWWWWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWW         WWWWWWWWWWWWWWWWWWWWWWWW         WWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWW          WWWWWWWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWW          WWWWWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWW           WWWWWWWWWWWWWWWWW          WWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWWWW           WWWWWWWWWWW             WWWWWWWWWWWWWWWWWW    |
|     WWWWWWWWWWWWWWWWWWW                                WWWWWWWWWWWWWWWWWWWW    |
|                                                                                |
L________________________________________________________________________________|
"""
