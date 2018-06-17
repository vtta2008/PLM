__author__ = 'jens'

KEY = 'thma'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt'}  # Edit this to define cmd line options for
# the plugin and their default values.
from lauescript.core import *
import numpy as np
from lauescript.cryst.match import match_point_clouds


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
    filename = pluginManager.arg('load')
    thmaADPs = {}
    thmaCoords = {}
    with open(filename, 'r') as fp:
        adpSwitch = False
        coordSwitch = False
        currentAtom = None
        for line in fp.readlines():
            if line.startswith('0 WEIGHTED R FOR ALL U\'S = 0.112; FOR DIAGONAL U\'S  ONLY, WEIGHTED R = 0.08'):
                break
            elif line.startswith('0EIGENVALUES OF THE TENSOR OF INERTIA'):
                coordSwitch = False
            elif line.startswith('0VIBRATION TENSORS IN THE CARTESIAN CRYSTAL SYSTEM'):
                adpSwitch = True
            elif line.startswith('0THESE ARE FROM SUBROUTINE INERT AND ARE RELATIVE TO THE CRYSTAL ORIGIN; AX(I,K)'):
                coordSwitch = True
            elif adpSwitch:
                currentAtom = parseADPLine(line, thmaADPs, currentAtom)
            elif coordSwitch:
                parseCoordLine(line, thmaCoords)


    printer('THMA ADPs:')
    for atomName, ADP in thmaADPs.items():
        printer('{:5} {}  at {}'.format(atomName, '{:7.4f} {:7.4f} {:7.4f} {:7.4f} {:7.4f} {:7.4f}'.format(*ADP),
                                       '{:7.4f} {:7.4f} {:7.4f}'.format(*thmaCoords[atomName])))

    data = pluginManager.get_variable('data')
    mainCoords = []
    mainNames = []
    for atom in data.iter_atoms():
        mainCoords.append(atom.get_cart())
        mainNames.append(atom.get_name())
    newCoords = []
    newNames = []
    for key, value in thmaCoords.items():
        newNames.append(key)
        newCoords.append(value)
    hitlist, _ = match(mainCoords, newCoords)
    printer('\nIdentified equivalent atoms:')
    translator = {}
    for i, name1 in enumerate(mainNames):
        printer('{:5} <-> {:5}'.format(name1, newNames[hitlist[i]]))
        translator[name1] = newNames[hitlist[i]]

    for atom in data.iter_atoms():
        atom.adp['cart_ext'] = thmaADPs[translator[atom.get_name()]]
        atom.adp['cart_sum'] = thmaADPs[translator[atom.get_name()]] + atom.adp['cart_int']


def parseADPLine(line, thmaADPs, currentAtom ):
    startChunk = line[:7]
    if startChunk != '       ':
        currentAtom = startChunk.lstrip().rstrip()
    elif 'CALCULATED' in line:
        values = [float(i) for i in line[:-1].split()[:-1] if i]
        thmaADPs[currentAtom] = values
    return currentAtom

def parseCoordLine(line, thmaCoords):
    if line[0] == ' ' and not line[1] == ' ':
        line = [i for i in line.split() if i][:4]
        thmaCoords[line[0]] = np.array([float(value) for value in line[1:]])


def match(cloud1, cloud2):
    hitlist, transformation = match_point_clouds(cloud1, cloud2, threshold=.2)
    return hitlist, transformation