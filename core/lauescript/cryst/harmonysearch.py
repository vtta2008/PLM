"""
Created on May 20, 2014

@author: Jens Luebben

Experimental implementation of the 'Harmony Search' global
optimization algorithm proposed by 'Zong Woo Geem,
Joong Hoon Kim and G. V. Loganathon, SIMULATION 2001, 76:60'
"""

from random import uniform, randint, shuffle
from operator import itemgetter, attrgetter

from numpy.linalg import norm
from numpy import array


class ConvergenceReached(Exception):
    pass


class PermutationError(Exception):
    pass


class RouteError(Exception):
    pass


class Harmony(object):
    """
    Class representing a Harmony. Instances are
    created by the HarmonyGenerator class and
    are managed by the Memory class.
    A Harmony contains a point in n-dimensional
    space and a 'cost' value determined by a
    'costFunction' that is used to estimate the
    function value of that point.
    """
    ID = 0
    costFunction = None

    def __init__(self, values):
        """
        Initializes a Harmony object. The list 'values'
        represents a point in n-dimensional space.
        """
        self.ID = Harmony.ID
        Harmony.ID += 1
        self.values = values
        self.cost = Harmony.costFunction(self, *values)

    def __str__(self):
        """
        Returns a string representation of the Harmony
        object.
        """
        try:
            return 'Harmony {:<5} --  Cost: {:6.3f}  |  Values: {}'.format(str(self.ID), self.cost,
                                                                           ' '.join([' {:6.3f}'.format(value)
                                                                                     for value in self.values]))
        except:
            return 'Harmony {:<5} --  Cost: {:6.3f}  |  Values: {}'.format(str(self.ID), self.cost, self.values)


    def __getitem__(self, index):
        """
        Returns the value of the i^th element in
        self.values representing the i^th coordinate.
        """
        return self.values[index]


    def get_cost(self):
        """
        Returns the estimated function value determined
        by the costFunction.
        """
        return self.cost

    def getValues(self):
        """
        Returns the values.
        """
        return self.values

    @staticmethod
    def registerCostFunction(function):
        """
        Registers the class attribute 'costFunction' that
        defines the function used for estimating function
        values by all instances.
        """
        Harmony.costFunction = function


class Memory(object):
    """
    Class representing the harmony memory. The class
    manages instances of the Harmony class and contains
    information on the current state of the algorithm.
    """

    def __init__(self, size, convergenceRate=0, dynamicPitch=0):
        """
        Initializes the Memory instance. The integer
        'size' defines the number of Harmonies kept in
        the memory. The integer 'convergenceRate' defines
        how often the next Harmony is allowed to be
        rejected before the algorithm is considered
        converged.
        The integer parameter 'dynamicPitch' defines
        after how many rejected Harmonies the pitchRange
        should be halfed.
        """
        self.size = size
        self.convergenceRate = convergenceRate
        self.dynamicPitch = dynamicPitch
        self.memory = None
        self.maximum = 0
        self.Imax = 0
        self.tries = 0
        self.pitchTries = 0
        self.generator = None
        self.accepted = False

    def populate(self, generator):
        """
        Populates the Memory instance with randomly generated
        Harmony objects.
        """
        self.generator = generator
        self.memory = [generator.createRandomHarmony() for _ in range(self.size)]
        self._introspect()

    def _introspect(self):
        """
        Determines the currently most costly Harmony object
        and sets the self.Imax and self.maximum attributes
        accordingly.
        """
        self.Imax, self.maximum = max(enumerate([harmony.get_cost()
                                                 for harmony in self.memory]),
                                      key=itemgetter(1))
        self.accepted = True

    def __str__(self):
        """
        Returns the string representation of the Memory object's
        current state.
        """
        return '\n'.join([str(harmony) for harmony in self.memory])

    def get_size(self):
        """
        Returns the maximum number of Harmonies in the Memory
        object.
        """
        return self.size

    def __getitem__(self, indices):
        """
        indices = (i,j)
        Returns the value of the variable with index 'i'
        from the Harmony 'j'.
        """
        return self.memory[indices[1]][indices[0]]

    def __add__(self, newHarmony):
        """
        Checks whether the newHarmony has a lower 'cost'
        if the current memory with the highest 'cost' and
        replaces the latter, if True. Subsequently
        self.introspect() is called and the updated object
        is returned.
        """
        if newHarmony.get_cost() < self.maximum:
            self.memory[self.Imax] = newHarmony
            self._introspect()
            self.tries = 0
            self.pitchTries = 0
        else:
            self.tries += 1
            self.pitchTries += 1
        if self.convergenceRate and self.tries > self.convergenceRate:
            raise ConvergenceReached('convergenceReached')
        if self.dynamicPitch and self.pitchTries > self.dynamicPitch:
            self.generator.updatePitchRange()
            self.pitchTries = 0
        return self

    def harvest(self):
        """
        Returns the values of the Harmony instance and the
        corresponding costFunction value.
        """
        bestHarmony = min([harmony for harmony in self.memory], key=attrgetter('cost'))
        return bestHarmony.getValues(), bestHarmony.get_cost()


class HarmonyGenerator(object):
    """
    Factory class for generating Harmony instances.
    The created Harmony object depends on the current
    state of the algorithm.
    """

    def __init__(self,
                 bounds,
                 startValues=None,
                 memoryConsideringRate=0.9,
                 pitchAdjustRate=0.1,
                 pitchRange=0.1):
        """
        Creates a HarmonyGenerator object. The mandatory
        argument 'bounds' must be a list of arbitrary length
        containing one element for every variable of the system.
        Every element must be an iterable object defining
        the lower bound for a variable in its first value and
        the upper bound in its second value.

        ...
        """
        self.bounds = bounds
        self.length = len(bounds)
        self.memoryConsideringRate = memoryConsideringRate
        self.pitchAjustRate = pitchAdjustRate
        self.pitchRange = pitchRange
        self.startValues = startValues

    def createRandomHarmony(self):
        """
        Returns a Harmony object with random values. Each
        value is within its bounds.
        """
        if not self.startValues:
            return Harmony([uniform(*bound) for bound in self.bounds])
        else:
            harmony = Harmony([uniform(*bound) for bound in self.bounds])
            self.startValues = None
            return harmony

    def createHarmony(self, memory):
        """
        Creates and returns a default Harmony instance based
        on the current state of the algorithm provided by the
        Memory instance 'memory' and the initialization
        parameters.
        """
        newValues = []
        memorySize = memory.get_size()
        for i, bound in enumerate(self.bounds):
            if uniform(0, 1) > self.memoryConsideringRate:
                newValue = uniform(*bound)
            else:
                j = randint(0, memorySize - 1)
                newValue = memory[i, j]
                if uniform(0, 1) < self.pitchAjustRate:
                    newValue += self.pitchRange * (1 - randint(0, 1) * 2)
            newValues.append(newValue)
        newValues = self._clamp(newValues)
        return Harmony(newValues)

    def _clamp(self, values):
        """
        Checks whether every value is still within its bounds
        and clamps values that are not.
        """
        return [value if (self.bounds[i][0] < value < self.bounds[i][1])
                else self._getClampValue(value, i)
                for i, value in enumerate(values)]

    def _getClampValue(self, value, index):
        """
        Determines whether the upper or the lower bound should
        be clamped to.
        """
        if value > self.bounds[index][1]:
            return self.bounds[index][1]
        else:
            return self.bounds[index][0]

    def updatePitchRange(self):
        """
        Adjusts the pitchRange attribute to improve
        convergence. The method is called by by a
        Memory instance if 'dynamicPitch' is used.
        """
        self.pitchRange *= 0.5

    def get_pitchRange(self):
        """
        Returns the current value of 'pitchRange'.
        """
        return self.pitchRange


class PathGenerator(HarmonyGenerator):
    """
    HarmonyGenerator class for solving the 'Traveling
    Salesman' problem and similar problems.
    """


    def createRandomHarmony(self):
        """
        Creates a random route by shuffling the waypoints.
        """
        route = list(self.bounds)
        shuffle(route)
        return Harmony(route)


    def createHarmony(self, memory):
        """
        Creates a new route.
        Since every waypoint must be used exactly once,
        the generation of random waypoints must be delayed
        until all waypoints from memory are considered.
        Pitch shifts are implemented by swapping the
        current waypoint with the previous waypoint. Since
        the first waypoint has no previous waypoint, no
        shifting is allowed for that point.
        To make sure points are not used more than one time
        a blacklist ist kept. If a point from memory is
        on the blacklist, a random point is chosen instead.
        """
        newValues = []
        memorySize = memory.get_size()
        blacklist = []

        for i, _ in enumerate(self.bounds):
            if uniform(0, 1) > self.memoryConsideringRate:
                newValues.append(None)
            else:
                j = randint(0, memorySize - 1)
                newValue = memory[i, j]
                if newValue in blacklist:
                    newValues.append(None)
                else:
                    newValues.append(newValue)
                    blacklist.append(newValue)
                    if uniform(0, 1) < self.pitchAjustRate:
                        if not i == 0:
                            newValues[-1], newValues[-2] = newValues[-2], newValues[-1]

        freeList = [point for point in self.bounds if not point in blacklist]
        shuffle(freeList)
        for i, value in enumerate(newValues):
            if not value:
                newValues[i] = freeList.pop()
        return Harmony(newValues)

def dummy(i):
    pass

def harmonize(bounds,
              costFunction,
              iterations,
              memorySize=5,
              startValues=None,
              memoryConsideringRate=0.9,
              pitchAdjustRate=0.1,
              pitchRange=0.1,
              convergenceRate=0,
              dynamicPitch=0,
              verbose=False,
              generator=HarmonyGenerator,
              callBack=dummy):
    """
    Interface function for the Harmony Search global
    optimization algorithm.

    Returns the optimized parameter as a list and a float
    representing the corresponding value of the costFunction.

    Parameters:

      Mandatory:
        bounds: List of tuples defining the upper and
           lower bounds for each variable. The length
           of the list defines the number of variables.
           The first tuple value must contain the lower
           bound, the second the upper bound for each
           variable.
        costFunction: Function accepting at least a
           number of parameters equal to the length of
           the 'bounds' parameter. The function is used
           to estimate a function value for each point
           in the space defined by 'bounds'.
        iterations: Maximum number of iterations before
           termination of the algorithm.

      Optional:
        memorySize: Number of Harmonies kept in the
           Harmony memory. Defaults to 5.
        startValues: List of floats used as start values
           in the harmony memory. The values are not
           checked to fit the defined bounds.
        memoryConsideringRate: Float between 0 and 1
           defining the probabillity of using a parameter
           value from the harmony memory instead of a
           random value.
        pitchAdjustRate: Float between 0 and 1 defining
           the probabillity of slightly changing the value
           of a value picked from the harmony memory.
        pitchRange: Float defining by how much a parameter
           is changed in case of a pitch adjustment. The
           Range can be added or subtracted by chance.
        convergenceRate: Integer defining the number of
           iteration steps without accepting a new harmony
           before terminating the algorithm.
        dynamicPitch: Integer defining after how many
           rejected new Harmonies the pitchRange parameter
           should be halfed. Default of '0' means no
           pitch adjustment.
        verbose: Boolean defining whether a output should
           be printed to the console.
    """
    Harmony.registerCostFunction(costFunction)
    gen = generator(bounds,
                    startValues,
                    memoryConsideringRate,
                    pitchAdjustRate,
                    pitchRange)
    memory = Memory(memorySize, convergenceRate, dynamicPitch)
    memory.populate(gen)
    converged = False
    for _ in range(iterations):
        try:
            memory += gen.createHarmony(memory)
        except ConvergenceReached:
            converged = True
            break
        callBack(_)
    if verbose:
        print 'Final Memory:'
        print memory
        print 'Current pitchRange: {}'.format(gen.get_pitchRange())
        if converged:
            print 'Terminated by convergence criterion.'
    return memory.harvest()


def routeCost(self, *args):
    return sum([norm((array(point) - array(args[i % (len(args) - 1) + 1]))) for i, point in enumerate(args)])


def harmonize_par(bounds,
                  costFunction,
                  iterations,
                  memorySize=5,
                  startValues=None,
                  memoryConsideringRate=0.9,
                  pitchAdjustRate=0.1,
                  pitchRange=0.1,
                  convergenceRate=0,
                  dynamicPitch=0,
                  verbose=False,
                  generator=HarmonyGenerator):
    import multiprocessing
    import time
    from copy import deepcopy

    start2 = time.time()

    class Worker(multiprocessing.Process):
        def __init__(self, memory, generator, message_queue, job_q, i, update_q):
            super(Worker, self).__init__()
            self.memory = memory
            self.generator = generator
            self.message_q = message_queue
            self.job_q = job_q
            self.id = i
            self.update_q = update_q

        def run(self):
            converged = False
            while True:
                if self.job_q.empty():
                    self.message_q.put(False)
                    return
                else:
                    self.job_q.get()
                try:
                    newMemory = self.update_q.get_nowait()
                    if newMemory:
                        self.memory = newMemory
                except:
                    pass

                self.memory += self.generator.createHarmony(self.memory)
                if self.memory.accepted:
                    self.memory.accepted = False
                    self.message_q.put(deepcopy(self.memory))


    Harmony.registerCostFunction(costFunction)
    gen = generator(bounds,
                    startValues,
                    memoryConsideringRate,
                    pitchAdjustRate,
                    pitchRange)
    memory = Memory(memorySize, convergenceRate, dynamicPitch)
    memory.populate(gen)
    converged = False

    job_q = multiprocessing.Queue()
    n = 4
    i = 0
    for i in range(iterations):
        job_q.put(i)
    jobs = []
    message_q = multiprocessing.Queue()
    update_qs = []
    for i in range(n):
        update_qs.append(multiprocessing.Queue())
        p = Worker(deepcopy(memory), deepcopy(gen), message_q, job_q, i, update_qs[-1])
        jobs.append(p)
        p.start()

    counter = 0

    while True:
        message = message_q.get()
        if message:
            best = message
            print best
            print
            for uq in update_qs:
                uq.put(deepcopy(message))
        else:
            counter += 1

        if counter == n:
            break

    for job in jobs:
        job.join()

    end2 = time.time()
    print best
    print 'xxx', best.harvest()


if __name__ == '__main__':
    def costFunction(self, *args):
        """
        Example for a simple costFunction that is used
        to estimate the function value of a point in
        n-dimensional space.
        """
        return sum(args)

    def costFunction2(self, *args):
        """
        Test costFunction. Keep the pitchRange low to
        asure convergence ore use the dynamicPitch option.
        """
        return sum([arg ** 2 for arg in args])

    def costFunction3(self, *args):
        x = sum([arg ** 2 for arg in args])
        x += abs(args[0] + args[1] - 1) * 100
        y = args[2] + args[3] - 3
        if y < 0:
            x += abs(y) * 10
        return x

    def costFunction4(self, *args):
        x = (args[0] - 2) ** 2 + (args[1] - 1) ** 2
        x += abs(args[0] - 2 * args[1] + 1) * 2
        y = -1 * args[0] ** 2 / 4. - args[1] ** 2 + 1
        if y < 0:
            x += abs(y) * 3
        return x

    def report(*args):
        x = (args[0] - 2) ** 2 + (args[1] - 1) ** 2
        g1 = abs(args[0] - 2 * args[1] + 1)
        g2 = -1 * args[0] ** 2 / 4. - args[1] ** 2 + 1

        print 'Restraint 1: ', g1
        print 'Restraint 2: ', g2
        print 'Function value: ', x


    # ===========================================================================
    # bounds=[(-1,1),(2,3),(15,23),(-1,1),(2,3),(15,23),(-1,1),(2,3),(15,23),(-1,1),(2,3),(15,23)]
    #===========================================================================


    #===========================================================================
    # bounds=[(0.,2.),(0.,2.)]
    # values,cost= harmonize(bounds,costFunction4,40000,convergenceRate=0,pitchRange=0.1,dynamicPitch=10000,verbose=True)
    # print values,cost
    # report(*values)
    #===========================================================================

    #===========================================================================
    # bounds=[(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
    # values,cost= harmonize(bounds,routeCost,5000,generator=PathGenerator,verbose=True,memoryConsideringRate=0.8)
    # print values,cost
    #===========================================================================


    bounds = [(0., 2.), (0., 2.)]
    harmonize_par(bounds, costFunction2, 1000, convergenceRate=0, pitchRange=0.1, dynamicPitch=10000, verbose=True)
