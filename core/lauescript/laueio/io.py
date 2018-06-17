"""
Created on Mar 18, 2014

@author: Arrahed

Base class for Input Output Providers.
"""

from copy import deepcopy


class IOP(object):
    """
    Base class for Input Output Providers.
    """
    instance = 0

    def __init__(self, filename):
        self.filename = filename
        self.supportsSym = False
        self.T = None
        self.set_id()
        self.symmetry = []
        IOP.instance += 1

    def set_id(self):
        self.id = '{}{}'.format('none', IOP.instance)

    def get_id(self):
        return self.id

    def read(self):
        """
        Interface function for reading file contents.
        :return: None
        """
        self.content = open(self.filename, 'r').readlines()
        self.parse()

    def write(self):
        """
        Interface function for writing file representations.
        :return: None
        """
        try:
            self.content.close()
        except:
            pass
        writer = open(self.filename, 'w')
        writer.write(str(self))

    def parse(self):
        """
        Virtual method. Override this method when implementing an IOP.
        :return: None
        """
        pass

    def _rebuild_file(self):
        """
        Virtual method. Override this method when implementing an IOP.
        :return: None
        """
        pass

    def get_temperature(self):
        """
        :return: float representing the data collection temperature.
        """
        return self.T

    def get_cart(self):
        return self.cart

    def get_frac(self):
        return self.frac

    def get_names(self):
        return self.names

    def get_adps_cart(self):
        return self.adp_cart

    def get_adps_frac(self):
        return self.adp_frac

    def get_cell(self):
        return self.cell

    def get_symmetry(self):
        print('Symmetry is not available in all file types.')
        print('Override this method in IOPs that support symmetry.')

    def clone(self, filename):
        """
        Creates a deep copy of the IOP instance.
        :param filename: string representing the filename of the file ascociated with the new IOP.
        :return: IOP instance.
        """
        clone = deepcopy(self)
        clone.filename = filename
        clone.set_id()
        return clone

    def set_afix(self, *values):
        pass

    def provide(self, key_string):
        """
        Generator.
        Recommended method for accessing data from the IOP.
        The 'key_string' argument defines which attributes
        of each atom are required.
        Each list the generator returns starts with the name
        of the atom as its first element. Every subsequent
        element is defined by 'key_string'.
        e.g.: for 'key_string'=['frac','cart','adp'] the
        every list contains the elements [name,frac,cart,adp].

        Allowed keys are:
            frac
            cart
            adp_frac
            adp_cart
            adp_error_frac
            adp_error_cart
            (All attributes of child classes that are a
            dictionary containing a set of keys that
            includes the names of all atoms.)
        """
        for name in self.names:
            atom = [name]
            for key in key_string:
                attr = getattr(self, key)
                atom.append(attr[name])
            yield atom

    def set(self, keys, provider, new=False):
        """
        Interface for changing values in the file representations.
        'Keys' is a list of attribute names like 'cart', 'adp_cart'.
        provider must be an iterator object that yields a list
        of parameters for every iteration. The first element of
        each list must allways be an atom name. The subsequent
        elements must be the elements specified by keys.

        For every element a 'set_<<attributename>>' method must be
        implemented. This method is called for every element with the
        atom name and
        the value of the corresponding list entry as arguments.
        """
        for atom in provider():
            name = atom[0]
            if new:
                self.create_atom(name)
            for i, key in enumerate(keys):
                attr = getattr(self, 'set_' + key)
                attr(name, atom[i + 1])
        if new:
            self._rebuild_file()

    def export(self, exportformat, **kwargs):
        """
        Interface method for exporting to different file formats.
        The implementing IOP must implement a method with the name
        'export_{exportformat}'
        :param exportformat:
        :return: None
        """
        attr = getattr(self, 'export_' + exportformat)
        return attr(**kwargs)

    def __str__(self):
        return 'To make use of the \'write\' method please override ' \
               'the \'__str__\' method of the corresponding \'IOP\' subclass.'






