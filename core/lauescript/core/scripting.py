"""
Created on Dec 15, 2013

@author: Jens Luebben

Module implementing the APD-Scripting language.
"""

from sys import argv

from lauescript.core import apd_printer


class apd_action():
    """
    Class for defining actions to be carried out by the
    APD-Toolkit.
    The class is used to abstract the execution of a function
    from the declaration of its arguments and to give
    the program the possibility to dynamically use
    conditional arguments that depend of the time of
    execution rather the time of declaration.
    """

    def __init__(self, module='main', arguments=None, argv=argv):
        self.module = module
        self.arguments = arguments
        self.argv = argv

    def __call__(self):
        apd_do(self.module, self.arguments, self.argv)


def apd_do(module='main', arguments=None, argv=argv):
    """
    Calls the 'APD_GUI()' function of the module specified in
    'module' with the arguments specified in 'arguments'
    and uses the options specified in 'argv' instead of
    the 'real' cmdline options.

    defaults:
        module: main.py
        arguments: No arguments
        argv: argv as passed by the cmdline interface
    """
    current_module = __import__(module)
    current_module.run()


def set_action(action):
    """
    Defines a default action that is used if no other action
    is specified.
    """


def apd_load(filename):
    """
    Loads the cif file with the name 'filename'
    and transfers the internal ADPs.
    """
    from lauescript.laueio.inout import Load
    from lauescript.types.data import DATA

    data_dict[filename] = DATA()
    Load(data_dict[filename], dabapath, printer, filename=filename)

    data_dict[filename].update(match='geom')


def apd_for(files, action):
    """
    For every file in 'files' the corresponding data
    is loaded and the action specified in 'action' is
    applied.
    """
    for filename in files:
        apd_load(filename)
        action()


def generate_sample():
    """
    Generates a sample script file in the working
    directory.
    """
    print 'The sample script file generation is not implemented yet.'


def generate_interactive():
    """
    Asks the user a series of question to generate
    a custom script file interactively.
    """
    print 'The interactive script generation is not implemented yet.'


def apd_enter(name, indent):
    """
    Imports all necessary modules and calls the appropriate
    functions.
    """

    global data_dict, printer, path, dabapath
    data_dict = {}
    printer = apd_printer(name=name, indent=indent)
    path = '/home/jens/APD-toolkit'
    dabapath = '/home/jens/APD-toolkit'
    # ===========================================================================
    # printer.first()
    #===========================================================================
    printer.headline(custom='Entering APD-Script: {}'.format(name))


def apd_exit(name):
    """
    Calls the necessary terminating functions.
    """
    printer.bottomline(custom='Exiting APD-Script: {}'.format(name))
    # ===========================================================================
    # printer.last()
    #===========================================================================


class Parser(object):
    """
    Parser for .apd script files.
    """

    def __init__(self, filename=None, indent=0, config=None):
        self.config = config
        self.commands = {'FILES': self.parse_file_list,
                         'DO': self.execute,
                         'PATH': self.set_path,
                         'MICRO': self.set_micro}
        self.actions = {'AUTO': ['autosegment', None],
                        'HIRSHFELD': ['hirshfeld', None]}
        from os import listdir

        if not filename:
            script_file_name = max([f for f in listdir('.') if f.endswith('.apd')])
        else:
            script_file_name = filename
        self.script = open(script_file_name)
        self.name = script_file_name
        self.current_file = None
        #self.current_data = None
        self.indent = indent
        self.config.printer.mute()


    def set_path(self, newpath):
        """
        Resets the current database directory.
        """
        global dabapath
        dabapath = newpath[0]

    def set_micro(self, _):
        """
        Sets the database directory to the working directory.
        """
        self.set_path(['.'])


    def execute(self, action, current_file):
        """
        Executes an action.
        """
        import imp

        printer('Executing {} using file {}'.format(action, current_file))
        data = data_dict[current_file]
        action = self.actions[action]
        current_module = imp.load_source(action[0], path + '/apd/examplePlugins/' + action[0] + '.py')
        data.set_argv(action[1])
        printer('Using cmdline options: {}'.format(data.get_argv()))
        self.config.set_data(data)
        options = ['_', '-' + current_module.KEY] + action[1].split(' ')
        self.config.parse_argv(options)
        self.config.call(current_module.KEY)


    def execute_loop(self, action_list):
        """
        Executes a series of actions defined in a loop.
        """
        for current_file in self.file_list:
            apd_load(current_file)
            for action in action_list:
                self.execute(action, current_file)

    def parse_file_list(self, strings):
        """
        Reads the specified file list from the script file.
        """
        self.file_list = strings

    def define(self, strings):
        """
        Defines a new action as defined in a line of the script file.
        """
        split_strings = [i for i in strings.split(' ') if len(i) > 0]
        actionname = split_strings[0]
        action = strings.lstrip('\t').lstrip(' ').lstrip(actionname).lstrip(' ')
        action = [i for i in action.split('\'') if len(i) > 0]
        action[0] = action[0].rstrip(' ')
        if len(action) < 2:
            action = action[0].split(' ')
        if len(action) < 2:
            action.append('')
        self.actions[actionname] = action
        printer('Define command {} as {}'.format(actionname, action))


    def __call__(self):
        """
        Parses an input script file and generates
        the corresponding python code.
        """
        script = self.script
        apd_enter(self.name, self.indent)
        lines = script.readlines()
        printer('\nScript:\n#######################################')
        for line in lines:
            printer(line.rstrip('\n'))
        printer('#######################################\n')
        skip = None
        for i, line in enumerate(lines):

            if not skip:
                if line.startswith('FOR'):
                    skip = self._parse_loop(lines[i + 1:])
                    continue
                try:
                    command = self.commands[line.rstrip('\n').split(' ')[0]]
                    command(line.rstrip('\n').split(' ')[1:])
                except:
                    self.define(line.rstrip('\n'))

            else:
                skip -= 1
        apd_exit(self.name)

    def _parse_loop(self, lines):
        """
        Parses a loop in the script file.
        """
        indent = self._get_indent(lines[0])
        skip = None
        action_list = []
        for i, line in enumerate(lines):
            if not skip:
                if line.startswith('FOR'):
                    skip = self._parse_loop(lines[i + 1:])
                    continue

                if not indent == self._get_indent(line):
                    break
                try:
                    action_list.append(line.rstrip('\n').split(' ')[1:][0])
                except:
                    self.define(line.rstrip('\n'))
            else:
                skip -= 1
        self.execute_loop(action_list)
        return i + 1

    def _get_indent(self, line):
        """
        Determines the current indentation level of the line
        to test whether a line is part of a loop.
        """
        for i, char in enumerate(line):
            if not char == '\t' and not char == ' ':
                break
        return i
