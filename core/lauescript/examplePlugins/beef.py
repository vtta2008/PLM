"""
Test implementation of the BEEF.
The current implementation determines the ratio (f) of all ADPs that
has to be multplied with the corresponding atom's mass to mimimize
the average of the hirshfeld test values. f is determined via an
implementation of the Harmony Search algorithm.
Subsequently, the difference ADPs for all bonds are determined
and their eigenvalues are multiplied with the cosine of the
corresponding eigenvectors to the normalized bond vector. The
three values determined by this procedure are summed and represent
the BEEF of that bond.
"""
__author__ = 'jens'

KEY = 'BEEF'
OPTION_ARGUMENTS = {'load': 'no input specified'}
NAME = 'BEEF'

from lauescript.cryst.tables import atomicmass
from lauescript.cryst.transformations import ADP_to_matrix
from lauescript.cryst.crystgeom import get_framework_neighbours
from numpy.linalg import norm, eig
from scipy.optimize import nnls
from numpy import dot, mean, std
from lauescript.laueio.loader import Loader
from lauescript.types.data import DATA
from operator import itemgetter


# use = 'cart_sum'
use = 'cart_meas'


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
    data = pluginManager.get_variable()
    if not data:
        loader = Loader(printer)
        loader.create(pluginManager.arg('load'))
        data = DATA()
        data['exp'] = loader.load('exp')
    #     T = loader.get_temperature()
    # else:
    #     T = pluginManager.get_variable('T')
    # obj = ObjectiveObject(data)
    # printer('Searching for optimal rigid bond description...')
    # f, best_solution = harmonize([(0, 10)], obj, 1000, startValues=[5, 0], pitchRange=0.01, dynamicPitch=200)
    # hresult, esd = obj(None, f[0], 'report')
    # printer('U_int/U_all * m ratio of f={:4.2f} yields best hirshfeld solution of {:5.3f} +- {:5.3f}.\n'.
    #         format(f[0], hresult, esd))
    # f = float('{:4.2f}'.format(f[0]))
    a, b = build_ls_matrix(data)
    solution = nnls(a, b)
    f = solution[0][0]
    if f > 1:
        printer('f out of bounds ({:4.2f}).'.format(f))
        printer('Starting linear search for reasonable solution:')
        f = find_f(data)[1]
        printer('U_int/U_all * m ratio of f={:4.2f} yields best hirshfeld solution.\n'.format(f))
    else:
        printer('U_int/U_all * m ratio of f={:4.2f} yields best hirshfeld solution.\n'.format(f))
    pluginManager.register_variable(f, 'f')
    analyser = Analyser(printer, pluginManager.get_variable('f'))
    for atom1, atom2 in data.iter_atom_pairs():
        if not any([atom.adp['flag'] == 'riding' for atom in (atom1, atom2)]) or pluginManager.arg('f'):
            # if atom1.element == 'H' or atom2.element == 'H':
            #     continue
            analyser(atom1, atom2)
    printer()
    printer('Average:             {:6.4f}\n                  +- {:6.4f}'.format(*analyser.harvest()))
    if pluginManager.arg('+'):
        printer('\n\nReporting element specific mean square displacements in bond direction.\n')
        for element, values in details(data).items():
            printer('{:>3}: {:5.3f}'.format(element, mean(values)))
    if pluginManager.arg('write'):
        options = {'full': True, 'use': 'beef'}
        pluginManager.call('W', options)

def details(data):
    report = {}
    for atom1, atom2 in data.iter_atom_pairs(bound=True):
        if any(atom.adp['flag'] == 'riding' for atom in (atom1, atom2)):
            continue

        v_bond = atom1.get_cart() - atom2.get_cart()
        v_bond /= norm(v_bond)
        adp1 = atom1.adp['cart_meas']
        adp2 = atom2.adp['cart_meas']
        A = norm(dot(ADP_to_matrix(adp1), v_bond))
        B = norm(dot(ADP_to_matrix(adp2), v_bond))
        if not atom1.get_element() in report.keys():
            report[atom1.get_element()] = [A]
        else:
            report[atom1.get_element()].append(A)
        if not atom2.get_element() in report.keys():
            report[atom2.get_element()] = [B]
        else:
            report[atom2.get_element()].append(B)
    return report






def build_ls_matrix(data):
    """
    Builds the least squares matrix 'a' and vector 'b'.
    'a' is a matrix with one column containing only the number
    one.
    'b' contains the value f' for each bond which is defined as

       f' = (m_a * m_b * (B - A)) / (A*m_a*m_b - A*m_b - B*m_a*m_b + B*m_a)

    where A/B are the size of the ADP of atom A/B in the direction of the bond
    between atom A and atom B and m_a/b is the mass of the respective atom.

    :param data: Reference to a DATA instance
    :return: (a, b) as defined above.
    """
    ls_matrix = []
    ls_vector = []
    for atom1, atom2 in data.iter_atom_pairs(bound=True):
        if any(atom.adp['flag'] == 'riding' for atom in (atom1, atom2)):
            continue
        ls_matrix.append([1])
        v_bond = atom1.get_cart() - atom2.get_cart()
        v_bond /= norm(v_bond)
        adp1 = atom1.adp['cart_meas']
        adp2 = atom2.adp['cart_meas']
        A = norm(dot(ADP_to_matrix(adp1), v_bond))
        B = norm(dot(ADP_to_matrix(adp2), v_bond))
        ma = atomicmass[atom1.element]
        mb = atomicmass[atom2.element]

        v_line = abs((ma*mb * (B - A)) / (A*ma*mb - A*mb - B*ma*mb + B*ma))
        ls_vector.append(v_line)

    return ls_matrix, ls_vector


class ObjectiveObject(object):
    """
    Callable Object passed to the Harmony Search algorithm.
    Python is awesome, sometimes.
    """
    def __init__(self, data):
        self.data = data
        # self.min = 1

    def __call__(self, *args):
        value = []
        f = args[1]
        # if f < self.min:
        #     print f
        #     self.min= f
        for atom1 in self.data.iter_atoms():
            if atom1.adp['flag'] == 'riding':
                continue
            for atom2 in get_framework_neighbours(atom1, useH=True):
                if atom2.adp['flag'] == 'riding':
                    continue
                v = atom1.get_cart() - atom2.get_cart()
                v /= norm(v)
                m1 = atomicmass[atom1.get_element()]
                m2 = atomicmass[atom2.get_element()]
                adp1 = atom1.adp[use] * (1-f/m1) + atom1.adp[use] * f
                adp2 = atom2.adp[use] * (1-f/m2) + atom2.adp[use] * f
                h1 = norm(dot(ADP_to_matrix(adp1), v))
                h2 = norm(dot(ADP_to_matrix(adp2), v))
                value.append(abs(h1 - h2))
        if 'report' in args:
            # print f
            return mean(value), std(value)

        return mean(value) + 100 * std(value)


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
        f = self.f
        cmass1 = atomicmass[atom1.element]
        cmass2 = atomicmass[atom2.element]
        adp1 = atom1.adp[use] * (1-f/cmass1) + atom1.adp[use] * f
        adp2 = atom2.adp[use] * (1-f/cmass2) + atom2.adp[use] * f
        dadp = ADP_to_matrix(adp1 - adp2)
        evalues, evectors = eig(dadp)

        bvector = atom1.get_cart() - atom2.get_cart()
        bvector /= norm(bvector)
        result = Result(bvector, evalues, evectors)
        self.printer(' {:6} -- {:>6}:{}'.format(atom1, atom2, result.report()))
        self.results.append(result.get_value())
        atom1.adp['beef'] = adp1
        atom2.adp['beef'] = adp2

    def harvest(self):
        """
        Interface method for accessing the computed data
        :return: Average BEEF and its standard deviation.
        """
        return mean(self.results), std(self.results)


class Result(object):
    """
    Class for computing the actual BEEF from bond vector atom masses
    eigenvalues and eigenvectors.
    """
    def __init__(self, bondvector, evalues, evectors):
        self.results = []
        self.value = None
        for i in range(3):
            vector = evectors[:, i]
            evalue = evalues[i]
            cangle = abs(dot(bondvector, vector).flatten().tolist()[0][0])
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

    def report(self):
        """
        Prints the BEEF.
        :return: None
        """
        return '   {:6.4f}'.format(self.value)

    def get_value(self):
        """
        Interface method for accessing the results.
        :return: Float representing the BEEF.
        """
        return self.value


def find_f(data):
    pairs = build_list(data)
    l = []
    for f in range(1, 300, 2):
        f = float(f)/300.
        c = check_f(pairs, f)
        l.append((c, f))
    solution = min(l, key=itemgetter(0))
    # print 'Optimal Hirshfeld solution for f={:4.2f}.'.format(solution[1])
    return solution


def build_list(data):
    atom_pairs = []
    for atom1, atom2 in data.iter_atom_pairs(bound=True):
        if any(atom.adp['flag'] == 'riding' for atom in (atom1, atom2)):
            continue
        atom_pairs.append((atom1,atom2))
    return atom_pairs


def check_f(pairs, f):
    fs = []
    for atom1, atom2 in pairs:
        v_bond = atom1.get_cart() - atom2.get_cart()
        v_bond /= norm(v_bond)
        adp1 = atom1.adp['cart_meas']
        adp2 = atom2.adp['cart_meas']
        m1 = atomicmass[atom1.element]
        m2 = atomicmass[atom2.element]
        adp1 = adp1 * (1-f/m1) + adp1 * f
        adp2 = adp2 * (1-f/m2) + adp2 * f
        # A = norm(dot(ADP_to_matrix(adp1), v_bond))
        # B = norm(dot(ADP_to_matrix(adp2), v_bond))
        h1 = norm(dot(ADP_to_matrix(adp1), v_bond))
        h2 = norm(dot(ADP_to_matrix(adp2), v_bond))
        fs.append(abs(h1 - h2))


        # fs.append(abs((ma*mb * (B - A)) / (A*ma*mb - A*mb - B*ma*mb + B*ma)) - f)
    return mean(fs)