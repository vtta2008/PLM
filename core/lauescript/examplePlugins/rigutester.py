"""
Module for analysing the ADPs of a refined or otherwise
estimated structure. The procedure is based on the enhanced
rigid bond restraints (RIGU) by G. M. Sheldrick and tests
the assumption that the relative displacement of two
neighboring atoms should more pronounced perpendicular
to the connecting bond vector while being essentially
zero parallel to the bond vector. Two account for structures
containing atoms with strongly varying masses a mass
dependent weighting factor is introduced.
A bond enhanced evaluation factor (BEEF) is calculated for each bond as
follows:

        |U11 U12 U13|
ADP_i = |U12 U22 U23|
        |U13 U23 U33|

w_i = m_I^.5

w = w_1 / w_2

ADP_D = ADP_1 - ADP_2

e = eigenvalues of ADP_D

v = eigenvectors of ADP_D

v_bond = bond vector

v_1 = eigenvector most parallel to v_bond

e_1 = eigenvalue associated with v_1

cos_2, cos_3 = cosine of eigenvectors 2 and three to v_bond

e_2, e_3 = eigenvalues associated with cos_2 and cos_3

BEEF = (e_1 + cos_2 * e_2 + cos_3 * e_3) * w

A structure model should have a BEEF of about 0.02 to 0.05.
"""
__author__ = 'jens'

from numpy.linalg import eig, norm
from numpy import dot, mean, std

from lauescript.cryst.transformations import ADP_to_matrix
from lauescript.cryst.tables import atomicmass


KEY = 'rigu'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt'}  # Edit this to define cmd line options for
# the plugin and their default values.


def run(pluginManager):
    """
    This is the entry point for the plugin manager.
    The plugin manager will pass a reference to itself
    to the function.
    Use the APD_Printer instance returned by
    pluginManager.setup() instead of the 'print'
    statement to generate autoformated cmd line output.
    :param pluginManager: Reference to the plugin manager
    instance.
    """
    printer = pluginManager.setup()
    printer('Performing advanced rigid bond analysis.')
    data = pluginManager.get_variable()
    analyser = Analyser(printer, pluginManager.get_variable('f'))
    for atom1, atom2 in data.iter_atom_pairs():
        analyser(atom1, atom2)
    printer()
    printer('Average: {:6.4f} +- {:6.4f}'.format(*analyser.harvest()))


class Analyser(object):
    """
    Class for computing and collecting BEEF for
    a given pair of atoms.
    """
    def __init__(self, printer, f):
        self.printer = printer
        self.results = []
        self.f = f

    def __call__(self, atom1, atom2):
        """
        Computes and stores the BEEF of two atoms.
        :param atom1: ATOM instance.
        :param atom2: ATOM instance.
        :return: None
        """
        self._analyse(atom1, atom2)

    def _analyse(self, atom1, atom2):
        # print
        # print
        f = 0.05
        f = 0.5
        f = self.f
        cmass1 = atomicmass[atom1.element]#**.5
        cmass2 = atomicmass[atom2.element]#**.5
        dmass = sorted([cmass1, cmass2])
        # dmass = dmass[1] / dmass[0]
        dmass = 1
        # x1 = Uiso(atom1.adp['cart_int']) / Uiso(atom1.adp['cart_sum'])
        # x2 = Uiso(atom2.adp['cart_int']) / Uiso(atom2.adp['cart_sum'])
        # xx = sorted((x1, x2))
        # print xx[1]/xx[0]
        adp1 = atom1.adp['cart_sum'] * (1-f/cmass1) + atom1.adp['cart_sum'] * f
        adp2 = atom2.adp['cart_sum'] * (1-f/cmass2) + atom2.adp['cart_sum'] * f

        # adp1 = array(atom1.adp['cart_int']) * cmass1 + atom1.adp['cart_ext']
        # adp2 = array(atom2.adp['cart_int']) * cmass2 + atom2.adp['cart_ext']
        dadp = ADP_to_matrix(adp1 - adp2)
        evalues, evectors = eig(dadp)
        # print evalues

        bvector = atom1.get_cart() - atom2.get_cart()
        bvector /= norm(bvector)
        self.printer()
        self.printer(' {:4} -- {:>4}'.format(atom1, atom2))
        result = Result(bvector, dmass, evalues, evectors)
        result.report(self.printer)
        self.results.append(result.get_value())

    def harvest(self):
        """
        Interface method for accessing the computed data
        :return: Average BEEF and its standard deviation.
        """
        return mean(self.results), std(self.results)

    def report(self):
        """
        Method for printing an overview to the cmd line.
        :return:
        """
        print(self.results)


class Result(object):
    """
    Class for computing the actual BEEF from bond vector atom masses
    eigenvalues and eigenvectors.
    """
    def __init__(self, bondvector, relativemass, evalues, evectors):
        self.results = []
        self.value = None
        for i in range(3):
            vector = evectors[:, i]
            evalue = evalues[i]
            cangle = abs(dot(bondvector, vector).flatten().tolist()[0][0])
            # diff = abs(evalue / relativemass)
            diff = abs(evalue)
            result = (diff, cangle)
            self.results.append(result)
        self.results = sorted(self.results, key=lambda x: x[1], reverse=True)
        self.analyse()

    def analyse(self):
        """
        Computes the BEEF.
        :return: None
        """
        # first = self.results[0][1] * self.results[0][0]**.5
        second = mean([i[1] * i[0] for i in self.results])
        self.value = second

    def report(self, printer):
        """
        Prints the BEEF.
        :param printer: APD_Printer instance used for printing.
        :return: None
        """
        printer('   {:7.5f}'.format(self.value))

    def get_value(self):
        """
        Interface method for accessing the results.
        :return: Float representing the BEEF.
        """
        return self.value