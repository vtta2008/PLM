"""
Created on Jan 23, 2014

@author: Jens Luebben

Module for coordinate system transformations between
reciprocal space and cartesian space.

To avoid unecessary operations, the last transformation
matrix is cached and reused if the same transformation
is requested again.
"""
from numpy import matrix, array, sqrt, cos, sin, pi, dot, transpose
from numpy.linalg import inv


def ADP_to_matrix(lst):
    """
    Returns the matrix representation of an ADP
    provided as a XD style list ('lst').
    """
    return matrix([[lst[0], lst[3], lst[4]],
                   [lst[3], lst[1], lst[5]],
                   [lst[4], lst[5], lst[2]]])


def ADP_to_XD_list(mtrx):
    """
    Returns the XD style lis representation of an ADP
    ('mtrx') in its matrix representation.
    """
    return array([mtrx[0, 0], mtrx[1, 1], mtrx[2, 2], mtrx[0, 1], mtrx[0, 2], mtrx[1, 2]])


def frac2cart(frac, cell):
    """
    Returns the cartesian representation of a numpy array
    representing a position in reciprocal space as a numpy
    array.

    'cell' must be a list of length six containing:
    a, b, c, alpha, beta, gamma
    """
    return transformator(frac, cell, 'frac2cart')


def cart2frac(cart, cell):
    """
    Returns the reciprocal representation of a numpy array
    representing a position in cartesian space as a numpy
    array.

    'cell' must be a list of length six containing:
    a, b, c, alpha, beta, gamma
    """
    return transformator(cart, cell, 'cart2frac')


def frac2cart_ADP(frac, cell):
    """
    Returns the cartesian representation of an ADP as
    a XD style list in reciprocal space.

    'cell' must be a list of length six containing:
    a, b, c, alpha, beta, gamma
    """
    return adp_transformator(frac, cell, 'frac2cart')


def cart2frac_ADP(cart, cell):
    """
    Returns the fractional representation of an ADP as
    a XD style list in cartesian space.

    'cell' must be a list of length six containing:
    a, b, c, alpha, beta, gamma
    """
    return adp_transformator(cart, cell, 'cart2frac')


class Transformator(object):
    """
    A class for cashing transformation matrices and
    applying them to 3D coordinates.
    """

    def __init__(self):
        """
        Initializes an empty transformator
        """
        self.refcell = [None]
        self.matrix = None

    def __call__(self, coord, cell, do):
        """
        Interface method:
        Returns the transformed coordinate array.

        'coord' must be a numpy array representing a
        position in 3D space.

        'cell' must be a list of length six representing
        the unit cell: a, b, c, alpha, beta, gamma

        'do' must be the string 'frac2cart' to transform
        from fractional to cartesian space. Otherwise
        the transformation for cartesian to fractional
        space is performed.
        """
        if not all([i == j for i, j in zip(cell, self.refcell)]) or not do == self.do:
            self.refcell = cell
            self.do = do
            if do == 'frac2cart':
                self.get_f2c_matrix()
            else:
                self.get_c2f_matrix()

        return self.transform(coord)

    def transform(self, coord):
        """
        Performes the actual transformation of the
        3D position 'coord'.
        """
        return array(dot(self.matrix, coord).tolist()[0])

    def get_f2c_matrix(self):
        """
        Uses the 'cell' provided to the '__call__' function
        to determine the transformation matrix from fractional
        to cartesian space.
        """
        self.cell = [float(i) for i in self.refcell]
        self.cell[3], self.cell[4], self.cell[5] = self.cell[3] / 180 * pi, self.cell[4] \
                                                   / 180 * pi, self.cell[5] / 180 * pi
        v = sqrt(1 - cos(self.cell[3]) * cos(self.cell[3]) \
                 - cos(self.cell[4]) * cos(self.cell[4]) \
                 - cos(self.cell[5]) * cos(self.cell[5]) \
                 + 2 * cos(self.cell[3]) * cos(self.cell[4]) * cos(self.cell[5]))

        self.matrix = matrix(
            [[self.cell[0], self.cell[1] * cos(self.cell[5]), self.cell[2] * cos(self.cell[4])],
             [0, self.cell[1] * sin(self.cell[5]), (self.cell[2] * (cos(self.cell[3])
                                                                    - cos(self.cell[4]) * cos(self.cell[5]))) / sin(
                 self.cell[5])],
             [0, 0, self.cell[2] * v / sin(self.cell[5])]])


    def get_c2f_matrix(self):
        """
        Uses the 'cell' provided to the '__call__' function
        to determine the transformation matrix from cartesian
        to fractional space.
        """
        self.cell = [float(i) for i in self.refcell]
        self.cell[3], self.cell[4], self.cell[5] = self.cell[3] / 180 * pi, self.cell[4] \
                                                   / 180 * pi, self.cell[5] / 180 * pi
        v = sqrt(1 - cos(self.cell[3]) * cos(self.cell[3]) \
                 - cos(self.cell[4]) * cos(self.cell[4]) \
                 - cos(self.cell[5]) * cos(self.cell[5]) \
                 + 2 * cos(self.cell[3]) * cos(self.cell[4]) * cos(self.cell[5]))
        self.matrix = matrix([[1 / self.cell[0],
                               -cos(self.cell[5]) / (self.cell[0] * sin(self.cell[5])),
                               (cos(self.cell[3]) * cos(self.cell[5]) - cos(self.cell[4]))
                               / (self.cell[0] * v * sin(self.cell[5]))],
                              [0, 1 / (self.cell[1] * sin(self.cell[5])), (cos(self.cell[4])
                                                                           * cos(self.cell[5]) - cos(self.cell[3])) / (
                               self.cell[1] * v
                               * sin(self.cell[5]))],
                              [0, 0, sin(self.cell[5]) / (self.cell[2] * v)]])


class ADP_Transformator(Transformator):
    """
    Class for cashing transformation matrices and applying them.
    This class is designed to transform ADP instead of coordinates
    and takes care of the scaling as well.
    The interface is inherited from the parent class 'Transformator'.
    """

    def transform(self, adp):
        """
        Takes care of the actual transformation of the 'adp'.
        """
        if self.do == 'frac2cart':
            return self.frac2cart(adp, self.matrix, self.cell)
        elif self.do == 'cart2frac':
            return self.cart2frac(adp, self.matrix, self.cell)

    def frac2cart(self, adp, rotmat, cell):
        """
        Transforms an ADP from fractional to cartesian coordinates.
        """
        adp = matrix([[float(adp[0]), float(adp[3]), float(adp[4])],
                      [float(adp[3]), float(adp[1]), float(adp[5])],
                      [float(adp[4]), float(adp[5]), float(adp[2])]])
        # =======================================================================
        # rotmat=inv(rotmat)
        #=======================================================================
        rotmatT = transpose(rotmat)
        Nmat = matrix([[1 / cell[0], 0, 0],
                       [0, 1 / cell[1], 0],
                       [0, 0, 1 / cell[2]]])
        #=======================================================================
        # Nmat=inv(Nmat)
        #=======================================================================
        NmatT = transpose(Nmat)

        adp = dot(Nmat, adp)
        adp = dot(adp, NmatT)

        adp = dot(rotmat, adp)
        adp = dot(adp, rotmatT)

        adp = array(adp).flatten().tolist()
        return [adp[0], adp[4], adp[8], adp[1], adp[2], adp[5]]


    def cart2frac(self, adp, rotmat, cell):
        """
        Transforms and ADP from cartesian to fractional coordinates.
        """
        adp = matrix([[float(adp[0]), float(adp[3]), float(adp[4])],
                      [float(adp[3]), float(adp[1]), float(adp[5])],
                      [float(adp[4]), float(adp[5]), float(adp[2])]])
        rotmati = matrix(rotmat)
        rotmatiT = transpose(rotmati)
        # =======================================================================
        # rotmat=inv(rotmat)
        #=======================================================================
        #=======================================================================
        # rotmati=rotmat
        # rotmatiT=transpose(rotmat)
        #=======================================================================


        Nmat = matrix([[1 / cell[0], 0, 0],
                       [0, 1 / cell[1], 0],
                       [0, 0, 1 / cell[2]]])
        Nmat = inv(Nmat)
        NmatT = transpose(Nmat)
        adp = dot(rotmati, adp)
        adp = dot(adp, rotmatiT)

        adp = dot(Nmat, adp)
        adp = dot(adp, NmatT)
        adp = array(adp).flatten().tolist()
        return [adp[0], adp[4], adp[8], adp[1], adp[2], adp[5]]


# ===============================================================================
# if __name__=='__main__':
#===============================================================================
transformator = Transformator()
adp_transformator = ADP_Transformator()

if __name__ == '__main__':
    adp = [1, 1, 1, .5, .5, .5]
    frac = [1, 1, 1]
    cell = [5.6353, 30.9870, 10.8170, 90.000, 95.232, 90.000]
    print(adp)
    #===========================================================================
    # print frac2cart_ADP(adp,cell)
    #===========================================================================
    x = frac2cart_ADP(adp, cell)

    #===========================================================================
    # print cart2frac_ADP(adp,cell)
    #===========================================================================

    #===========================================================================
    # print cart2frac(frac2cart(frac,cell),cell)
    #===========================================================================
    print(cart2frac_ADP(x, cell))
