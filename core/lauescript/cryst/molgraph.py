__author__ = 'jens'

from lauescript.cryst.geom import xi
from numpy.linalg import norm
from lauescript.cryst import rings
from numpy import mean, cos, e
import hashlib


def getInvariomNames(molecule, printer=None, databasePath=None, findSet=None):
    if not printer:
        from lauescript.core.apd_printer import apd_printer
        printer = apd_printer()
    graphs = []
    for graphandname in Graph.molecule2Graphs(molecule):
        if findSet:
            if not graphandname[1] in findSet:
                continue
        graphs.append(graphandname)
    hits = {}
    besttries = {}
    for graph1, inv in GraphStorage.readDatabase('graphs2inv.dat', rebuild=False):
        for i, graph2andatomname in enumerate(graphs):
            graph2 = graph2andatomname[0]
            atomname = graph2andatomname[1]
            diff = graph2.fastDiff(graph1)
            try:
                if besttries[atomname] > diff:
                    besttries[atomname] = diff
                    hits[atomname] = inv
            except KeyError:
                besttries[atomname] = diff
                hits[atomname] = inv
    for graph, name in graphs:
        valid = graph.validate(hits[name], name[0])
        if not valid:
            printer('Warning: Potentially bad fit: {:6s} -> {}'.format(name, hits[name]))
    return hits


class Graph(object):
    maxRed = 4
    maxGreen = 2
    maxBlue = 2
    maxAlpha = 1
    maxDouble = 0.13
    maxDoubleWidth = 0.05
    validationThresholds = {'lenient': 2,
                            'balanced': 1,
                            'strict': 0}

    def __init__(self):
        self.vertices = []
        self.edges = []

    def validate(self, invariomName, element, mode='strict'):
        """
        Validates an invariom name against the graph instance.
        :param invariomName: String representation of an invariom.
        :param element: String representing the atom's element.
        :param mode: String representing the validation mode. Allowed are 'lenient/balanced/strict'.
        Defaults to 'balanced'
        :return: Boolen. True means valid. False means invalid.
        """
        # element = self.coreVertex.getElement()
        # print
        # print invariomName
        invariomName = invariomName.split('&')[-1]
        if element == 'H':
            invariomName = 'H1' + invariomName.lower()
        # print invariomName
        killchars = '123456789#@&~-'
        workName = invariomName
        for char in killchars:
            workName = workName.replace(char, '')
        if not workName.startswith(element):
            return False
        firsts, seconds, complexity = Graph.segmentInvariomName(invariomName)
        penalty = 0
        flipchars = '3456789'
        for vertex in self.vertices:
            element = vertex.getElement().lower()
            if element[0] in flipchars:
                element = element.upper()
            if vertex.getRgba().blue == 1:
                if not element in firsts:
                    # print 'NOOOOOOOOOOOOOOOO0000000000000000000ooooooooooooooo................            Splash!'
                    # print invariomName, element
                    return False
                else:
                    firsts = firsts.replace(element, '', 1)
            if vertex.getRgba().blue == 2:
                if not element in seconds:
                    if element[0] in '3456789' and '@' in firsts:
                        continue
                    else:
                        penalty += vertex.getRgba().alpha
                else:
                    seconds = seconds.replace(element, '', 1)
        if penalty > Graph.validationThresholds[mode]+complexity:
            return False

        return True

    @staticmethod
    def segmentInvariomName(invariomName):
        starts = []
        ends = []
        seconds = []
        flips = []
        flipchars = '3456789'
        for i, char in enumerate(invariomName):
            if char == '[':
                starts.append(i)
            elif char == ']':
                ends.append(i)
            if char in flipchars:
                flips.append(i+1)
        charlist = []
        for i, char in enumerate(invariomName):
            if i in flips:
                char = char.upper()
            charlist.append(char)
        invariomName = ''.join(charlist)

        for start, end in reversed(zip(starts, ends)):
            seconds.append(invariomName[start+1:end])
            invariomName = invariomName[:start] + invariomName[end+1:]

        firsts = invariomName
        killchars = '123456789#@&~-'
        for char in killchars:
            firsts = firsts.replace(char, '')
        complexity = (len(firsts) - len(seconds) - 1)
        if len(firsts) == 2:
            complexity *= 1.5
        return invariomName, ''.join(seconds), complexity








    def addVertex(self, vertex):
        self.vertices.append(vertex)

    def addEdge(self, edge):
        self.edges.append(edge)
        # for vertex in edge.getVertices():
        #     self.vertices.append(vertex)

    def _contentString(self):
        string = ''
        for vertex in self.vertices:
            string += str(vertex) + '/'
        string += '*'
        for edge in self.edges:
            string += str(edge) + '/'
        return string

    def __str__(self):
        return self._contentString()

    def __hash__(self):
        h = hashlib.md5()
        h.update(self._contentString())
        return h.digest()

    def fullHash(self):
        return self.__hash__()

    def shortHash(self):
        h = hashlib.md5()
        h.update(self.shortString())
        return h.digest()

    def getEdges(self):
        return self.edges

    def shortString(self):
        return '\n{},{}'.format(','.join([vertex.shortString() for vertex in self.vertices]),
                                ','.join([edge.shortString() for edge in self.edges]))

    def getEdgesOf_str(self, vertex):
        return set([edge.shortString() for edge in self.edges if vertex in edge.getVertices()])

    def getEdges_str(self):
        return set([edge.shortString() for edge in self.edges])

    def getLength(self):
        vertLength = sum([vertex.getLength() for vertex in self.vertices])
        edgeLength = sum([edge.getLength() for edge in self.edges])
        vertLength = sum([vertex.getLength() for vertex in self.vertices])
        return (vertLength, edgeLength)

    def diffLength(self, other):
        selfLength = self.getLength()
        otherLength = other.getLength()
        return self._diffLength(selfLength, otherLength)

    def _diffLength(self, length1, length2):
        diff1 = abs(length1[0] - length2[0])
        # diff2 = abs(length1[1] - length2[1])
        return diff1# + diff2

    def getVertices(self):
        return self.vertices

    def fastDiff(self, graph2):
        """
        Does a fast difference computation based on the serialized representation of two graphs.
        The first pass comparison can be done without rebuilding the Graph instance. Only if the first pass
        succeeds, the Graph is rebuild and the detailed difference is computed.
        :param graph2:
        :return: Float representing the difference of the graphs.
        """

        coreHash2, len2 = graph2.split('::')[:2]
        if not self.coreHash() == int(coreHash2):
            return 99999
        diff = self._diffLength(self.getLength(), [float(x) for x in len2.split(',')])
        # if diff > 1:
        #     return 999
        g = Graph()
        g.rebuild(graph2)
        return self._secondPass(g) + diff**2

    def _firstPass(self, other):
        if type(other) is not Graph:
            raise TypeError('Object must be of type \'Graph\'')
        if not self.coreHash() == other.coreHash():
            return False
        if self.diffLength(other) > 0.5:
            return False

        return True

    def _setupBlacklist(self, graph):
        blacklist = {}
        for vertex in graph.getVertices():
            try:
                blacklist[str(vertex)] += 1
            except KeyError:
                blacklist[str(vertex)] = 1
        return blacklist

    def _secondPass(self, other):
        other_vertices = other.getVertices()
        distances = []
        blacklist = self._setupBlacklist(other)
        for vertex_self in self.vertices:
            bestHit = 999
            bestVert = None
            for vertex_other in other_vertices:
                if blacklist[str(vertex_other)]:
                    if not self.getEdgesOf_str(vertex_self) == other.getEdgesOf_str(vertex_other):
                        if vertex_self.rgba.alpha > .3 and vertex_self.rgba.blue == 2:
                            continue
                    # dis = vertex_self
                    dis = vertex_self - vertex_other
                    if dis > 8 and vertex_self.rgba.alpha < 1:
                        dis = 20 * vertex_self.rgba.alpha**2
                        vertex_other = None
                    if dis < bestHit:
                        bestHit = dis
                        bestVert = vertex_other
            if bestVert:
                blacklist[str(bestVert)] -= 1
            distances.append(bestHit)
        return sum(distances)/len(distances)

    def __sub__(self, other):
        """
        Computes the difference of two Graph instances.
        In a first pass both graphs are screened to have similar attributes.
        Only if the first pass shows sufficient similarity the more costly difference computation is carried out.
        If the first pass fails to show similarity a value of '9999' is returned.
        For application in the context of invariom partitioning differences below '0.05' can be expected for
        chemically equivalent invarioms.
        :param other: Graph instance.
        :return: Float representing the difference of both graphs
        """

        passed = self._firstPass(other)
        if not passed:
            return 999.
        return self._secondPass(other)

    @staticmethod
    def molecule2Graphs(molecule):
        """
        Iterator that yields one Graph instance for each atom
        in the molecule
        :param molecule: Molecule instance
        :return: Obne tuple for each Atom in Molecule containing a Graph instance representing the atom and the
         corresponding atom.get_name value.
        """
        decorations = Graph.decorate(molecule)
        for atom in molecule.iter_atoms():
            graph = Graph()
            graph.invariom2Graph(atom, decorations)
            yield graph, atom.get_name()

    @staticmethod
    def decorate(molecule):
        """
        Decorates atoms with additional topological attributes such as
        being part of cyclic systems.
        :param molecule: Molecule instance.
        :return: Dictionary linking decorated element identifier to the atom names.
        """
        Graph.ringList = rings.find_planar_rings(molecule.atoms)
        decorations = {atom.get_name(): atom.get_element() for atom in molecule.atoms}
        for ring in Graph.ringList:
            ringlength = str(len(ring))
            for atomName in ring:
                decorations[atomName] = ringlength + decorations[atomName]
        return decorations

    @staticmethod
    def shareRing(atom1, atom2):
        if any([atom1.get_name() in ring and atom2.get_name() in ring for ring in Graph.ringList]):
            return True
        return False

    def invariom2Graph(self, atom, decorations=None):
        """
        Sets up the graph instance to represent the chemical environment of an atom. The parameterization is designed to
        be compatible with invariom partitioning.
        :param atom: Atom instance
        :param decorations: Optional dictionary generated by Graph.decorate. If available decorations are used as vertex
        elements instead of the atom.get_element return value.
        :return: None
        """
        if not decorations:
            getter = Graph.getElement
        else:
            getter = Graph.getDecoration
        blacklist = []
        name0 = atom.get_name()
        vertex0 = Vertex(getter(atom, decorations))
        vertex0.setColor(self.getColorCenter(atom))
        blacklist.append(name0)
        self.addVertex(vertex0)
        self.setCore(vertex0)
        for atom1 in atom.iter_bound_atoms():
            name1 = atom1.get_name()
            blacklist.append(name1)
            vertex1 = Vertex(getter(atom1, decorations))
            vertex1.setColor(self.getColor(atom1, atom))
            self.addVertex(vertex1)
            self.addEdge(Edge((vertex0, vertex1)))
            if getter(atom, decorations) == 'H':
                self.setCore(vertex1)
            for atom2 in atom1.iter_bound_atoms():
                name2 = atom2.get_name()
                if name2 in blacklist:
                    continue
                vertex2 = Vertex(getter(atom2, decorations))
                ringAlpha = Graph.shareRing(atom, atom1)
                # print ringAlpha, atom, atom1, atom2
                vertex2.setColor(self.getColorNext(atom2, atom1, atom, ringAlpha))
                self.addVertex(vertex2)
                self.addEdge(Edge((vertex1, vertex2)))

    @staticmethod
    def getElement(atom, _):
        return atom.get_element()

    @staticmethod
    def getDecoration(atom, decoration):
        return decoration[atom.get_name()]

    def setCore(self, vertex):
        """
        Sets the core vertex. The core vertex is used to generate the corehash which is used to differentiate between
        the rigid core of an invariom graph and its fuzzy boundaries.
        :param vertex: Vertex instance. Vertex must be part of the Graph instance.
        :return: None
        """
        self.coreVertex = vertex

    def coreHash(self):
        """
        Recomputes the core hash.
        :return: Hash encoding the rigid graph core.
        """
        return hash(''.join(sorted(self.getEdgesOf_str(self.coreVertex))))

    def getColor(self, neighbor, center):
        """
        Generates a Color instance for atoms that are directly bound to the invariom represented by the core.
        :param neighbor: Vertex instance that is bound to the vertex representing the invariom.
        :param center: Vertex instance representing the invariom.
        :return:
        """
        red = norm(neighbor.cart - center.cart) / Graph.maxRed
        green = mean([norm(neighbor.cart - secondAtom.cart) for secondAtom in neighbor.iter_bound_atoms()]) / Graph.maxGreen
        blue = 1
        alpha = 1
        return Color((red, green, blue, alpha))

    def getColorNext(self, nextneighbor, neighbor, center, ringAlpha=None):
        distance = norm(nextneighbor.cart - center.cart)
        red = distance/Graph.maxRed
        green = distance/Graph.maxGreen
        blue = 2
        if ringAlpha:
            alpha = 1
        else:
            centerdistance = norm(neighbor.cart - center.cart)
            thisXi = xi(element1=neighbor.get_element(), element2=center.get_element(), distance=centerdistance)
            alpha = e**(-(thisXi-Graph.maxDouble)**2/(2*Graph.maxDoubleWidth**2))
        return Color((red, green, blue, alpha))

    def getColorCenter(self, atom):
        red = 0
        green = mean([norm(atom.cart - secondAtom.cart) for secondAtom in atom.iter_bound_atoms()]) / Graph.maxGreen
        blue = 0
        alpha = 1
        return Color((red, green, blue, alpha))

    def __repr__(self):
        """
        Generates a string that is supposed to be used in conjunction with the Graph.rebuild method.
        If passed to Graph.rebuild, the string is used to reconstruct the Graph instance.
        This procedure is usefull for serializing large numbers of Graph instances eficiently.
        Not all information in the returned string is actually necessary for reconstruction purposes.
        The string starts with the coreHash and the Graphlength values that are used for the first pass
        screening when computing Graph differences. This way the costly reconstruction can be omitted if the
        first pass comparison already failed.
        :return: String representing the Graph instance for reconstruction purposes
        """
        return '{}::{:7.5f},{:7.5f}::{coreID}::{full}'.format(self.coreHash(),
                                                              *self.getLength(),
                                                              coreID=str(self.coreVertex),
                                                              full=str(self))

    def rebuild(self, string):
        """
        Rebuilds a Graph instance based on the provided string. The string should have been generated by the
        Graph.__repr__ method.
        :param string: String representing the serialized Graph instance.
        :return: None
        """
        vertices = {}
        coreString = string.split('::')[-2]
        vertString, edgeString = string.split('::')[-1].split('*')
        vertList = vertString.split('/')[:-1]
        edgeList = edgeString.split('/')[:-1]
        for vertexString in vertList:
            element, colorString = vertexString.split(':')
            color = Color([float(c) for c in colorString[1:-1].split(',')])
            v = Vertex(element)
            v.setColor(color)
            if str(v) == coreString:
                coreVertex = v
            vertices[vertexString] = v
            self.addVertex(v)
        for edgeString in edgeList:
            vertexString1, vertexString2 = edgeString[1:-1].split('&')
            edge = Edge((vertices[vertexString1], vertices[vertexString2]))
            self.addEdge(edge)
        self.setCore(coreVertex)


class Color(tuple):
    def __init__(self, color):
        super(Color, self).__init__(color)
        self.red = color[0]
        self.green = color[1]
        self.blue = color[2]
        self.alpha = color[3]

class Vertex(object):
    def __init__(self, element=0, rgba=(1.,1.,1.,1.)):
        self.element = element
        self.rgba = rgba

    def getElement(self):
        return self.element

    def getRgba(self):
        return self.rgba

    def shortString(self):
        return str(self.element)

    def setColor(self, color):
        self.rgba = color

    def __str__(self):
        return '{}:({:4.2f},{:4.2f},{:4.2f},{:4.2f})'.format(self.element, *self.rgba)

    def __sub__(self, other):
        s = 0
        if not self.rgba.blue == other.getRgba().blue:
            return 999
        if not self.element == other.getElement() and not self.rgba.blue == 2:
            return 598
        if not self.element == other.getElement():
            s += abs(50 * (self.rgba[-1] - other.getRgba()[-1])) + .1 + (self.rgba[-1] + other.getRgba()[-1])**4
        else:
            s = abs(self.rgba.alpha - other.getRgba().alpha) * 10
        s += (sum([abs(other.getRgba()[i]-r)*10 for i, r in enumerate(self.rgba[:-2])]))
        return s

    def __hash__(self):
        return hash(str(self))

    def getLength(self):
        l = 1
        if self.rgba.blue == 1:
            l = self.rgba.alpha
            l += sum(self.rgba[:-1])
        return l






class Edge(object):
    def __init__(self, vertices):
        self.vertices = vertices

    def getVertices(self):
        return self.vertices

    def shortString(self):
        return '({:s}:{:s})'.format(*[vertex.shortString() for vertex in self.vertices])

    def __str__(self):
        return '({:s}&{:s})'.format(*self.vertices)

    def __hash__(self):
        return hash(str(self))

    def getLength(self):
        return min([vertex.getLength() for vertex in self.vertices])


class GraphStorage(object):
    @staticmethod
    def serialize(line, filepointer):
        line += '\n'
        filepointer.write(line)

    @staticmethod
    def writeDatabase(graphs, filename, linkTo=None, separator='='):
        """
        Interface for storing serialized Graphs in a database. It is possible to link the graphs to corresponding
        strings via the 'linkTo' argument. Data is stored in the format '<repr(graph)><separator><link>'.
        The first line of the database file always contains the separator. This way it is always known how
        to extract the data.
        :param graphs: List of Graph instances
        :param filename: String defining the filename the data is stored in.
        :param linkTo: Dictionary linking arbitrary content to the graphs. Must contain one entry for each graph.
        :param separator: String used as a separator to link graphs and content.
        :return: None
        """
        filepointer = open(filename, 'w')
        filepointer.write(separator + '\n')
        for graph in graphs:
            line = repr(graph)
            if linkTo:
                line += separator + linkTo[str(graph)]
            GraphStorage.serialize(line, filepointer)
        filepointer.close()

    @staticmethod
    def readDatabase(filename, rebuild=False):
        """
        Methods for retrieving graphs from database containing serialized graphs.
        :param filename: String representing the database file name.
        :param rebuild: Boolean specifying whether the graph should be returned in its serialized form or as an instance of
        the Graph class.
        :return: Yields one list containing the graph representation (rebuild or not) and if available, the linked
        content, for each database entry.
        """
        with open(filename, 'r') as filepointer:
            separator = filepointer.readline()[:-1]
            for line in filepointer.readlines():
                line = line[:-1].split(separator)
                if rebuild:
                    g = Graph()
                    g.rebuild(line[0])
                    line[0]=g
                yield line



def test():
    g = Graph()
    v1 = Vertex('C')
    v2 = Vertex('X', (.5, .5, .5, .5))
    v3 = Vertex('O')
    v4 = Vertex('N')
    e1 = Edge((v1, v2))
    e2 = Edge((v2, v3))
    e3 = Edge((v2, v4))
    g.addEdge(e1)
    g.addEdge(e2)
    g.addEdge(e3)

    gg = Graph()
    vv1 = Vertex('C')
    vv2 = Vertex('X', (.4, .4, .4, .4))
    vv3 = Vertex('O')
    vv4 = Vertex('N')
    ee1 = Edge((vv1, vv2))
    ee2 = Edge((vv2, vv3))
    ee3 = Edge((vv2, vv4))
    gg.addEdge(ee1)
    gg.addEdge(ee2)
    gg.addEdge(ee3)

    print(g)
    print(gg)
    print(g-gg)


if __name__ == '__main__':
    test()