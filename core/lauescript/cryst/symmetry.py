"""
Created on Jun 19, 2014

@author: jens
"""
from copy import deepcopy, copy
from numpy import array, matrix, dot
from lauescript.cryst.transformations import ADP_to_matrix, ADP_to_XD_list, frac2cart, frac2cart_ADP, cart2frac, cart2frac_ADP
from lauescript.types.adp import ADPDataError


class SymmetryElement(object):
    """
    Class representing a symmetry operation.
    """
    symm_ID = 1


    def __init__(self, symms, centric=False):
        """
        Constructor
        """
        self.symms = symms
        self.ID = SymmetryElement.symm_ID
        SymmetryElement.symm_ID += 1
        lines = []
        trans = []
        for symm in self.symms:
            line, t = self._parse_line(symm)
            lines.append(line)
            trans.append(t)
        self.matrix = matrix(lines).transpose()
        self.trans = array(trans)
        if centric:
            self.matrix *= -1
            self.trans *= -1

    def __str__(self):
        string = '''|{aa:2} {ab:2} {ac:2}|   |{v:2}|
|{ba:2} {bb:2} {bc:2}| + |{vv:2}|
|{ca:2} {cb:2} {cc:2}|   |{vvv:2}|'''.format(aa=self.matrix[0, 0],
                                             ab=self.matrix[0, 1],
                                             ac=self.matrix[0, 2],
                                             ba=self.matrix[1, 0],
                                             bb=self.matrix[1, 1],
                                             bc=self.matrix[1, 2],
                                             ca=self.matrix[2, 0],
                                             cb=self.matrix[2, 1],
                                             cc=self.matrix[2, 2],
                                             v=self.trans[0],
                                             vv=self.trans[1],
                                             vvv=self.trans[2])
        return string

    def _parse_line(self, symm):
        symm = symm.lower().replace(' ', '')
        chars = ['x', 'y', 'z']
        line = []
        for char in chars:
            element, symm = self._partition(symm, char)
            line.append(element)
        if symm:
            trans = self._float(symm)
        else:
            trans = 0
        return line, trans

    def _float(self, string):
        try:
            return float(string)
        except ValueError:
            if '/' in string:
                string = string.replace('/', './') + '.'
                return eval('{}'.format(string))

    def _partition(self, symm, char):
        parts = symm.partition(char)
        if parts[1]:
            if parts[0]:
                sign = parts[0][-1]
            else:
                sign = '+'
            if sign is '-':
                return -1, ''.join((parts[0][:-1], parts[2]))
            else:
                return 1, ''.join((parts[0], parts[2])).replace('+', '')
        else:
            return 0, symm

    def __add__(self, atom):
        new_atom = copy(atom)
        oldfrac = new_atom.get_frac()
        newfrac = dot(oldfrac, self.matrix) + self.trans
        newfrac = array(*newfrac[0,].tolist())
        new_atom.set_frac(newfrac.flatten().tolist())
        newcart = frac2cart(newfrac, atom.molecule.get_cell())
        new_atom.cart = newcart
        new_atom.set_name(new_atom.get_name() + '_' + str(self.ID))
        try:
            old_adp = ADP_to_matrix(new_atom.adp['cart_meas'])
            new_adp = dot(self.matrix.transpose(), old_adp)
            new_adp = dot(new_adp, self.matrix)
            new_adp = ADP_to_XD_list(new_adp)
            new_atom.adp['cart_meas'] = new_adp
            new_adp_frac = frac2cart_ADP(new_adp, atom.molecule.get_cell())
            new_atom.adp['frac_meas'] = new_adp_frac
        except ADPDataError:
            pass
        return new_atom

    def apply2cart(self, position, cell):
        positionFrac = cart2frac(position, cell)

        newfrac = dot(positionFrac, self.matrix) + self.trans
        newfrac = array(*newfrac[0,].tolist())
        newcart = frac2cart(newfrac, cell)
        return newcart


    def apply2cart_ADP(self, adp, cell):
        adpFrac = cart2frac_ADP(adp, cell)

        old_adp = ADP_to_matrix(adpFrac)
        new_adp = dot(self.matrix.transpose(), old_adp)
        new_adp = dot(new_adp, self.matrix)
        new_adp = ADP_to_XD_list(new_adp)
        new_adp_frac = frac2cart_ADP(new_adp, cell)
        return new_adp_frac


