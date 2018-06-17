__author__ = 'jens'

from lauescript.cryst.tables import electron_number


class SortAtom(object):
    @staticmethod
    def __call__(data, order):
        SortAtom.sort(data, order)

    @staticmethod
    def sort(data=None, order=None, molecule=None):
        if not order:
            order = (('name', False), ('element', True))
        if not molecule:
            atom_list = [atom for atom in data['exp'].atoms]
        else:
            atom_list = molecule.atoms
        for o in order:
            atom_list = sorted(atom_list, key=getattr(SortAtom, '_sort_{}'.format(o[0])), reverse=o[1])
        return atom_list

    @staticmethod
    def _sort_name(atom):
        string = atom.name
        return string

    @staticmethod
    def _sort_element(atom):
        string = str(electron_number[atom.get_element()])
        return string