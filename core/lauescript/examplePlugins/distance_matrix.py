__author__ = 'jens'


from sklearn.neighbors import NearestNeighbors
from numpy import array
import random
from datetime import datetime

KEY = 'dist'  # Edit this to control which cmd line keyword starts the plugin.
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
    samples = rand_coord()
    # samples = pluginManager.get_variable('data')['exp'].coords()
    neigh = NearestNeighbors(5, 0.4)
    printer('Starting sklearn: {}'.format(datetime.now()))
    neigh.fit(samples)
    result = neigh.kneighbors(samples, 5, return_distance=True)
    printer('Sklearn finished.\nStarting brute force: {}'.format(datetime.now()))
    for a in samples:
        for b in samples:
            d = a - b
    printer('Brute force finished: {}'.format(datetime.now()))


def rand_coord(size=100000):
    return [array([random.randrange(0,2000,step = 1)*0.1,
             random.randrange(0,2000,step = 1)*0.1,
             random.randrange(0,2000,step = 1)*0.1]) for _ in range(size)]