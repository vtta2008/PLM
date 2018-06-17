"""
Created on Feb 18, 2014

@author: Jens Luebben

Module for simple geometry operations.
"""
import numpy as np

from lauescript.cryst.tables import covalence_radius, electro_negativity
from lauescript.cryst.match import get_transform
from lauescript.cryst.crystgeom import get_adp_as_matrix


# def bond_error(cart1, cart2, err1, err2):
#     """
#     Calculates and returns the error of a bond lengths based on the
#     error of the coordinates.
#
#     WARNING: Not properly tested.
#     """
#     cart1 = np.array(cart1)
#     cart2 = np.array(cart2)
#     norm = np.linalg.norm(cart1 - cart2)
#     return sum([(((0.5 * (2 * cart1[i] - 2 * (cart2[i] + 1)) / norm) ** 2) * err1[i]) * 2 for i in range(3)])


def is_bound(pos1, el1, pos2, el2):
    """
    Uses the covalence radii to test whether two atoms are bound
    based on their cartesian coordinates and thei element symbol.
    """
    threshold = 0.1
    if el1 == 'H' or el2 == 'H':
        threshold = 0.2
    if np.linalg.norm(np.array(pos1) - np.array(pos2)) < covalence_radius[el1] + covalence_radius[el2] + threshold:
        return True
    return False

def is_bound2(d, el1, el2):
    threshold = 0.1
    if el1 == 'H' or el2 == 'H':
        threshold = 0.2
    return d < covalence_radius[el1] + covalence_radius[el2] + threshold



# ===============================================================================
# cart1=[1.1,1.2,0]
# cart2=[-1.1,1.2,0]
# err1=[0.01,0.01,0.02]
# err2=[0.01,0.01,0.02]
# print bond_error(cart1,cart2,err1,err2)
#===============================================================================


def framework_crawler(atom, direction, rigid_group_old=None):
    """
    Function to identify atoms belonging to a rigid group defined by
    a bond axis.
    Arguments:
        atom:            the name of the first atom of the rigid group.
        direction:       the name of the second atom of the rigid group.
        rigid_group_old: used by the function itself for recursive calls.

    Returns a list of atom names belonging to the rigid group.
    """
    if not rigid_group_old:
        rigid_group = [atom, direction]
    else:
        rigid_group = rigid_group_old
    for atom in get_framework_neighbors(direction):
        if not atom in rigid_group and not atom.element == 'H':
            rigid_group.append(atom)
            framework_crawler(rigid_group[0], atom, rigid_group)
    if not rigid_group_old:
        #=======================================================================
        # print '    Determined rigid group:', [i.name for i in rigid_group]
        #=======================================================================
        return rigid_group

def xi(element1, element2, distance):
    """
    Calculates the bond distinguishing parameter Xi.
    """
    return (float(covalence_radius[element1]) + float(covalence_radius[element2]) -
            (0.08 * float(abs(electro_negativity[element1] - electro_negativity[element2]))) - distance)


def get_framework_neighbors(atom, useH=True):
    """
    Needs a ATOM.atom instance as argument.
    Returns the names of the framework atoms bound to that atom.
    """
    neighborlist = []
    for atom2 in atom.partner[:5]:
        if atom-atom2 <= float(covalence_radius[atom.element]) + float(
                covalence_radius[atom2.element]) + .1:
            if not 'H' == atom2.element or useH:
                neighborlist.append(atom2)
    return neighborlist


def get_center_of_mass(molecule, use='cart'):
    return np.mean(molecule.coords(use))
#===============================================================================
# def identify_molecules(molecule):
#     '''
#     Takes an instance of the MOLECULE class as argument and returns a
#     dictionary that keys an identifying integer to every atom name
#     specifying which of the atoms in the molecule form an 'independent'
#     molecule in the chemical sense.
#     If all atoms are part of the same molecule, all atoms get the
#     integer '0'.
#     '''
#     blacklist=set()
#     #===========================================================================
#     # molecules=[]
#     #===========================================================================
#     ID=0
#     for atom1 in molecule.atoms:
#         framework=[]
#         for atom2 in get_framework_neighbors(atom1):
#             if not atom1.get_name() in blacklist and not atom2.get_name() in blacklist:
#                 framework+=framework_crawler(atom1,atom2)
#                 framework+=framework_crawler(atom2,atom1)
#                 framework = list(set(framework))
#                 [blacklist.add(atom.get_name()) for atom in framework]
#                 #===============================================================
#                 # molecules.append(framework)
#                 #===============================================================
#         if framework:
#             for atom in framework:
#                 atom.set_molecule_id(ID)
#             ID+=1
#===============================================================================


def rotate_point_about_axis(point, angle, axisDirection, axisOrigin=(0, 0, 0)):
    """
    Rotates a point about an axis by a given angle.
    :param point: list type containing three floats representing a point in cartesian space. (x, y ,z)
    :param angle: float representing the angle the point is about to be rotated in degree.
    :param axisDirection: list type containing three floats representing the direction of the vector
    the point is rotated about. (x, y, z)
    :param axisOrigin: list type containing three floats representing a point on the axis the point is
    rotated about. (x, y, z)
    :return: numpy.array representing the rotated point. (x, y, z)
    """
    from numpy import sin, cos, pi
    t = angle * (pi/180)
    x, y, z = point[0], point[1], point[2]
    a, b, c = axisOrigin[0], axisOrigin[1], axisOrigin[2]
    axisDirection /= np.linalg.norm(axisDirection)
    u, v, w = axisDirection[0], axisDirection[1], axisDirection[2]
    xx = (a*(v**2+w**2)-u*(b*v+c*w-u*x-v*y-w*z)) * (1-cos(t)) + x*cos(t) + (-1*c*v+b*w-w*y+v*z) * sin(t)
    yy = (b*(u**2+w**2)-v*(a*u+c*w-u*x-v*y-w*z)) * (1-cos(t)) + y*cos(t) + ( 1*c*u-a*w+w*x-u*z) * sin(t)
    zz = (c*(u**2+v**2)-w*(a*u+b*v-u*x-v*y-w*z)) * (1-cos(t)) + z*cos(t) + (-1*b*u+a*v-v*x+u*y) * sin(t)
    return np.array((xx, yy, zz))


def rotate_ADP_about_axis(ADP, angle, axisDirection):
    """
    Rotates an ADP about an axis by a given angle.
    :param ADP: list type containing six floats representing an ADP in XD format. (U11, U22, U33, U12, U13, U23)
    :param angle: float representing the angle the point is about to be rotated in degree.
    :param axisDirection: list type containing three floats representing the direction of the vector
    the point is rotated about. (x, y, z)
    :return: tuple containing six floats representing the rotated ADP.
    """
    adp = get_adp_as_matrix(ADP)
    u, v = np.linalg.eig(adp)
    startPoints = [v[:, i].flatten().tolist()[0] for i in range(3)]
    endPoints = [rotate_point_about_axis(point, angle, axisDirection, (0, 0, 0)) for point in startPoints]
    rotMat = get_transform(startPoints, endPoints, matrix=True).transpose()
    newadp = np.dot(rotMat.transpose(), np.dot(adp, rotMat))
    return newadp[0, 0], newadp[1, 1], newadp[2, 2], newadp[0, 1], newadp[0, 2], newadp[1, 2]



def sparseDistance(atom1, atom2, radius=25, noAtoms = False):
    """
    Computes the euclidean distance of atom1 and atom2.
    If the manhatten distance in one dimension is larger than 'radius'**.5 the
    distance is not computed and 'None' is returned instead.
    This is significantly faster when computing large number of distances
    where only short contacts are relevant e.g. determination of chemical environments.
    :param atom1:
    :param atom2:
    :return: float
    """
    if not noAtoms:
        cart1 = atom1.get_cart()
        cart2 = atom2.get_cart()
    else:
        cart1 = atom1
        cart2 = atom2
    D = 0
    for i in range(3):
        d = (cart1[i] - cart2[i])**2
        if d > radius:
            return None
        D += d
    return np.sqrt(D)

class ArgumentError(Exception):
    """
    Illegal combination of optional arguments.
    """
    pass

class SpaceTree(object):
    """
    Class for managing efficient closest neighbour computation.

    The algorithm uses space partitioning to assign points in a
    dataset to evenly spread grid points. After assignment each
    Grid point holds a list of references to all data points to
    which the grid point is closest.
    To find which data points are close to a given test point,
    the corresponding grid point for the test point needs to be
    found. All data points referenced by that grid point and all
    neighbouring grid points must be close to the test point.

    Usage:
    Instanciate a SpaceTree: sT = SpaceTree(...)
    Fit data points to tree: sT.fitPoints(points)
        (Use sT.fitAtoms(atoms) to fit atoms instead of just points.)
    Find closest points: closePoints = sT.getClosePoints(testPoint)
        (If sT.fitAtoms(atoms) was used, atoms are returned instead of points.)
    """
    def __init__(self, size=(10., 10., 10.), depth=None, neighbourRadius=None):
        """
        :param size: List type with at least three elements defining the size of the
        search space.
        :param depths: Int type defining how many levels of grid points are created.
        depth=1 means: 2^0 points per dimension are created.
        depths=2 means: a second level of 2^1 points per dimension are created.
        depths=3 means: a third level of 2^2 points per dimension are created.
        Defaults to 'None'. Default only legal if 'NeighbourRadius' is not 'None'.
        :param neighbourRadius: Float type defining how large the search radius around
        each test point should be. The appropriate value of 'depth' is then created
        based on this value.
        Defaults to 'None'. Default only legal if 'depth' is not 'None'.
        """
        if depth is None and neighbourRadius is None:
            raise ArgumentError
        if not depth:
            depth = self._estimateDepth(size, neighbourRadius)
        self.size = size
        self.depth = depth
        self.maxIndex = 2**(depth-1)
        self.grid = Grid(depth)
        self.dataPoints = None
        self.dataSignatures = None
        self.tree = {}
        self.spacings = None
        self._buildGridPoints()

    def _estimateDepth(self, size, neighbourRadius):
        """
        Estimates the required value for 'depth' if the desired
        neighbourradius is given.
        :param size: List type defining the size of the search space.
        :param neighbourRadius: Float type defining the desired search radius.
        """
        neighbourRadius *= 1.5
        for i in range(100):
            j = 2**i
            spacings = [c/j for c in size]
            maxSpace = max(spacings)
            if maxSpace < neighbourRadius:
                return i+1

    def _buildGridPoints(self):
        """
        Creates the required grid points for each level.
        :return: None
        """
        self.spacings = []
        for level in range(self.depth):
            levelSpacings = []
            refLevel = level + 1
            level = 2**level
            axisData = []
            for axis in self.size:
                spacing = axis / (level+1)
                levelSpacings.append(spacing)
                axisData.append([gridValue*spacing for gridValue in range(1, level+1)])
            pointList = [((i, j, k), np.array([axisData[0][i], axisData[1][j], axisData[2][k]]))
                         for i in range(level)
                         for j in range(level)
                         for k in range(level)]
            self.grid[refLevel] = {point[0]: point[1] for point in pointList}
            self.spacings.append(levelSpacings)

    def fitPoints(self, points, atoms=None):
        """
        Fits a set of data points to the grid points for fast lookup of close
        neighbours of test points.
        :param points: List of lists type. The inner lists must define a point in the search space.
        Periodic space is assumed.
        :param atoms: List of atoms type. Don't use this directly. Use 'fitAtoms' instead.
        :return: None
        """
        self.dataPoints = points
        self.dataSignatures = []
        if atoms:
            iterList = zip(points, atoms)
        else:
            iterList = [(p, None) for p in points]
        for point, atom in iterList:
            testPoint = [c if c > 0 else self.size[i]-c for i, c in enumerate(point)]
            testPoint = [c if c < self.size[i] else c % self.size[i] for i, c in enumerate(testPoint)]
            signature = self.grid.getSignature2(testPoint, self.spacings)
            self.dataSignatures.append(signature)
            if not atoms:
                try:
                    self.tree[tuple(signature)].append(point)
                except KeyError:
                    self.tree[tuple(signature)] = [point]
            else:
                try:
                    self.tree[tuple(signature)].append(atom)
                except KeyError:
                    self.tree[tuple(signature)] = [atom]

    def fitAtoms(self, atoms):
        """
        Equivalent to 'fitPoints' but stores references to
        atoms for each grid point instead of references to
        points.
        :param atoms: List of Atoms type defining the atoms that
        are supposed to be fitted to the grid points.
        :return: None
        """
        points = [atom.get_frac() for atom in atoms]
        self.fitPoints(points, atoms)


    def getClosePoints(self, point, depth=None):
        """
        Determines the corresponding grid point of the test point and
        returns a list of of points that were referenced by that grid
        point via a 'fitPoints' execution. If 'fitAtoms' was used
        instead of 'fitPoints', a list of Atom references is returned.
        :param point: List type of length three defining a point in the search space
        whose closest neighbours are searched.
        :param depth: Int type defining a which level the search should be searched.
        NOT USED.
        :return: List of points if 'fitPoints' was used.
        List of Atoms if 'fitAtoms' was used.
        """
        if not depth:
            depth = self.depth

        point = [c if c > 0 else self.size[i]-c for i, c in enumerate(point)]
        point = [c if c < self.size[i] else c % self.size[i] for i, c in enumerate(point)]
        # testSignature = self.grid.getSignature(point, self.spacings)
        testSignature = self.grid.getSignature2(point, self.spacings)
        # print testSignature, point
        # print testSignature
        # return self.tree[tuple(testSignature)]

        neighbors = []
        for neighborSignature in self.grid.getNeighborNodes(testSignature):
            neighborSignature = [s if s>=0 else self.maxIndex for s in neighborSignature]
            # neighborSignature = testSignature[:-1] + [neighborSignature]
            try:
                neighbors += self.tree[tuple(neighborSignature)]
            except KeyError:
                pass
        return neighbors


class Grid(dict):
    """
    Class used by the SpaceTree class for convience.
    """
    def __init__(self, levels):
        self.levels = levels

    def getSignature(self, testPoint, spacings):
        """
        Computes the signature of a point in the search space.
        A signature is a tuple of three integers that uniquely
        defines a grid point.
        :param testPoint: List type containing three float types
        defining a point in the search space.
        :param spacings: List type containing one float for each
        level of grid points. Each float represents the spacing
        between two grid points for one level of points.
        :return: Tuple type of length three defining the grid
        point the test point belongs to.
        """
        signatureChunks = []
        nextLevelPoints = [(0, 0, 0)]
        for level in range(1, self.levels+1):
            radius = max(spacings[level-1])**2 + .5
            if radius < 9:
                # if radius < 4.5:
                #     break
                radius = 9
            try:
                nextLevelPoints = self.getSubdivisionNodes(bestSignature)
            except UnboundLocalError:
                pass
            bestDist = 9999999999
            bestSignature = (9999999999, 9999999999, 9999999999)
            for signature in nextLevelPoints:
                gridPoint = self[level][signature]
                dist = sparseDistance(gridPoint, testPoint, radius=radius**2+1, noAtoms=True)
                if dist != None and dist < bestDist:
                    bestDist = dist
                    bestSignature = signature
            signatureChunks.append(bestSignature)
        return signatureChunks[-1]

    def getSignature2(self, testPoint, spacings):
        numberOfGridPoints = 2**(self.levels-1)
        fracSpacing = 1./numberOfGridPoints
        return tuple([int(round(dimension/fracSpacing-.5)) for dimension in testPoint])
        # for dimension in testPoint:
        #     point = round(dimension/fracSpacing)
        #     print point, dimension

    def getSubdivisionNodes(self, signature):
        """
        Given a signature for a lower level 'i' of grid points is known
        this method determines a list of possible grid points for
        the next grid level 'i+1'.
        :param signature: Tuple type of length three defining a signature
        at grid level 'i'
        :return:List type of Tuples of length three defining possible
        signatures for grid level 'i+1'.
        """
        x, y, z = signature[0], signature[1], signature[2]
        return [(2*x+1, 2*y, 2*z), (2*x, 2*y, 2*z),
                (2*x+1, 2*y+1, 2*z), (2*x, 2*y, 2*z+1),
                (2*x+1, 2*y+1, 2*z+1), (2*x, 2*y+1, 2*z),
                (2*x+1, 2*y, 2*z+1), (2*x, 2*y+1, 2*z+1)]

    def getNeighborNodes(self, signature):
        """
        Returns all neighboring grid point signatures.
        :param signature: Tuple type of length three defining which
        grid points neighbours are required.
        :return: List type of tuples of length three defining the signatures
        of all neighbouring grid points.
        """
        x, y, z = signature[0], signature[1], signature[2]
        return [(x+1, y+1, z+1), (x+1, y, z+1), (x+1, y-1, z+1),
                (x, y+1, z+1), (x, y, z+1), (x, y-1, z+1),
                (x-1, y+1, z+1), (x-1, y, z+1), (x-1, y-1, z+1),
                (x+1, y+1, z-1), (x+1, y, z-1), (x+1, y-1, z-1),
                (x, y+1, z-1), (x, y, z-1), (x, y-1, z-1),
                (x-1, y+1, z-1), (x-1, y, z-1), (x-1, y-1, z-1),
                (x+1, y+1, z), (x+1, y, z), (x+1, y-1, z),
                (x, y+1, z), (x, y, z), (x, y-1, z),
                (x-1, y+1, z), (x-1, y, z), (x-1, y-1, z)]




'''
st = SpaceTree(size=(1000,1000,1000), depth=5)
import random
# data = [np.array([1,1,1]),
#         np.array([1,1,0]),
#         np.array([5,7,8]),]
data = []
for i in range(10):
    # i *= 0.1
    data.append(np.array([i,i,i]))


data = [np.array([random.randrange(0, 1000), random.randrange(0, 1000), random.randrange(0, 1000)]) for _ in range(10000)]
import datetime
startFit = datetime.datetime.now()
st.fitPoints(data)
doneFit = datetime.datetime.now()
print 'Time for fit:', doneFit - startFit
# print 'Close points:', st.getClosePoints(np.array([5.1, 6.5, 8]))
# print 'Close points:', st.getClosePoints(np.array([1, 1, 1]))
# print 'Close points:', st.getClosePoints(np.array([2, 1, 1]))
# print 'Close points:', st.getClosePoints(np.array([1, 1, 10]))
for point in data:
    i = 0
    for point2 in st.getClosePoints(point):
        i+=1
        sparseDistance(point, point2, noAtoms=True)
        pass
    # print i
doneSearch = datetime.datetime.now()

print 'Time for search:', doneSearch - doneFit
# print st.grid[5][(7,7,7)]
# for point in data:
#     d = sparseDistance(point, np.array([4.7,4.7,4.7]), radius=9, noAtoms=True)
#     if d:
#         print point, d
'''






