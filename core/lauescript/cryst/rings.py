import numpy as np

from lauescript.cryst.geom import is_bound2
import lauescript


def find_planar_rings(atoms, cell, bonds=None, planarityThreshold=.1 ):
    a = [atom.get_name() for atom in atoms]
    e = [atom.get_element() for atom in atoms]
    c = [atom.get_cart() for atom in atoms]
    return findRings(a, e, c, cell, planarityThreshold)

def findRings(atoms, elements, coordinates, cell, planarityThreshold):
    ringData = {}
    rawData = set()
    Node.reset()
    nodes = [Node(name) for name in atoms]
    for i, items in enumerate(zip(atoms, elements, coordinates)):
        atomName1, element1, pos1 = items
        frac1 = lauescript.cryst.transformations.cart2frac(pos1, cell)
        for j, items2 in enumerate(zip(atoms, elements, coordinates)):
            atomName2, element2, pos2 = items2
            if atomName1 == atomName2:
                continue

            frac2 = lauescript.cryst.transformations.cart2frac(pos2, cell)
            dist = lauescript.invstring2.Bond.dist(frac1, frac2, cell)

            if is_bound2(dist, element1, element2):
                nodes[i].connect(atomName2)
    # print()
    for node in nodes:
        # print(node.name)
        node.findRing(5)
        Node.finalize()
        rings = Node.getRings()
        rings = are_planar(atoms, coordinates, rings, planarityThreshold)
        rawData.update(['#'.join(sorted([n.name for n in ring])) for ring in rings])
        r5 = len(rings)
        Node.reset()

        node.findRing(6)
        Node.finalize()
        rings = Node.getRings()
        # for ring in rings:
        #     print('xxxxxxxxx',[x.name for x in ring])
        # print(['#'.join(sorted([n.name for n in ring])) for ring in rings])
        rings = are_planar(atoms, coordinates, rings, planarityThreshold)
        # print('planar')
        # for ring in rings:
        #     print('yyyyyyyy',[x.name for x in ring])
        rawData.update(['#'.join(sorted([n.name for n in ring])) for ring in rings])
        # for r in rings:
        #     rawData.append(r.split('#'))
        r6 = len(rings)
        Node.reset()

        node.findRing(7)
        Node.finalize()
        rings = Node.getRings()
        rings = are_planar(atoms, coordinates, rings, planarityThreshold)
        rawData.update(['#'.join(sorted([n.name for n in ring])) for ring in rings])
        r7 = len(rings)
        Node.reset()

        node.findRing(8)
        Node.finalize()
        rings = Node.getRings()
        rings = are_planar(atoms, coordinates, rings, planarityThreshold)
        rawData.update(['#'.join(sorted([n.name for n in ring])) for ring in rings])
        r8 = len(rings)

        ringData[node.name] = '{}{}{}{}'.format('8' * r8,
                                                '7' * r7,
                                                '6' * r6,
                                                '5' * r5)
    # for d in rawData:
    #     print(d)
    rawData = [datum.split('#') for datum in rawData]
    return rawData


def are_planar(atoms, coordinates, all_rings, planarityThreshold=.2):
    atom_dict = {atom: cart for atom, cart in zip(atoms, coordinates)}
    planar_rings = []
    for ring in all_rings:
        l = len(ring)
        planarity = 0
        for i, atom_name0 in enumerate(ring):
            atom_name1 = ring[(i+1) % l]
            atom_name2 = ring[(i+2) % l]
            atom_name3 = ring[(i+3) % l]
            atom0 = atom_dict[atom_name0.name]
            atom1 = atom_dict[atom_name1.name]
            atom2 = atom_dict[atom_name2.name]
            atom3 = atom_dict[atom_name3.name]
            v = abs(np.dot((atom0 - atom3), np.cross((atom1 - atom3), (atom2 - atom3)))) / 6.
            planarity += v
        if planarity / l < planarityThreshold:
            planar_rings.append(ring)
    return planar_rings


class Node(object):
    map = {}
    id = 0

    @staticmethod
    def reset():
        Node.map = {}
        Node.id = 0

    def __init__(self, name):
        self.name = name
        self.id = Node.id
        Node.id += 1
        Node.map[name] = self
        self.connections = set()

    def __lt__(self, other):
        return self.name < other.name

    def connect(self, name):
        self.connections.add(Node.map[name])
        Node.map[name]._connect(self.name)

    def _connect(self, name):
        self.connections.add(Node.map[name])

    @staticmethod
    def _registerRing( ring):
        _ring = sorted(ring, key=lambda x: x.name)
        key = ','.join([str(i.name) for i in _ring])
        Node.rings[key] = ring[:-1]

    @staticmethod
    def getRings():
        return Node.rings.values()

    def findRing(self, size=6, recursive=False, blackList=None, last=None):
        if not recursive:
            Node.rings = {}
            Node.root = self
            Node.blackList = []
            Node.stack = [self]
            blackList = []
        for nextNode in self.connections:
            if nextNode in blackList or nextNode == last:
                continue
            # if not self == Node.root:
            #     Node.blackList.append(self)
            Node.stack.append(nextNode)
            # print(self, nextNode, '     ', [str(i) for i in Node.stack])
            if len(Node.stack)>=size+1:
                if Node.stack[0] == Node.stack[-1]:
                    if not any(Node.stack.count(i)>2 for i in Node.stack):
                        # Node.rings.append(Node.stack[:])
                        self._registerRing(Node.stack[:])
                    # print('ding')
                    Node.stack.pop()
                else:
                    # print('back')
                    Node.stack.pop()
                    # print('xxxxxxxxxx', [str(i) for i in Node.stack])
                continue
            if not self == Node.root:
                blackList.append(self)
            nextNode.findRing(size=size, recursive=True, blackList=blackList, last=self)
            if not self == Node.root:
                blackList.pop()
            Node.stack.pop()
            # Node.blackList.pop()

    @staticmethod
    def finalize():
        for key, ring in Node.rings.items():
            l = len(ring)
            for i, node1, in enumerate(ring):
                prev = (i-1+l)%l
                next = (i+1+l)%l
                for j, node2 in enumerate(ring):
                    if j == prev or j == next or j == i:
                        continue
                    if node2 in node1.connections:
                        del Node.rings[key]
                        return Node.finalize()




    def __str__(self):
        return str(self.name)


if __name__ == '__main__':
    nodes = [Node(name=i) for i in range(15)]
    nodes[0].connect(13)
    nodes[1].connect(2)
    nodes[2].connect(4)
    nodes[3].connect(4)
    nodes[4].connect(5)
    nodes[5].connect(6)
    nodes[6].connect(7)
    nodes[7].connect(8)
    nodes[8].connect(9)
    nodes[9].connect(10)
    nodes[9].connect(11)
    nodes[10].connect(12)
    nodes[10].connect(13)
    nodes[11].connect(12)
    nodes[11].connect(5)
    nodes[13].connect(14)
    nodes[0].connect(8)

    x = nodes[5].findRing(6)
    Node.finalize()
    for ring in Node.getRings():
        print([str(i) for i in ring])






























# __author__ = 'jens'
#
# from networkx import cycle_basis, Graph
# from numpy import dot, cross
# from lauescript.cryst.geom import is_bound
# from lauescript.cryst.iterators import iter_atom_pairs
#
#
# def find_rings(atoms, bonds=None):
#     graph = Graph()
#     class DummyMolecule(object):
#         pass
#     mol = DummyMolecule()
#     mol.atoms = atoms
#     if bonds is None:
#         for atom1, atom2 in iter_atom_pairs():
#             graph.add_edge(atom1.name, atom2.name)
#     else:
#         blacklist = []
#         for b in bonds:
#             for atom2i in b[1:10]:
#                 string = ' : '.join(sorted([atoms[b[0]].name, atoms[atom2i].name]))
#                 if not string in blacklist:
#                     if is_bound(atoms[b[0]].cart, atoms[b[0]].element, atoms[atom2i].cart, atoms[atom2i].element):
#                         graph.add_edge(atoms[b[0]].name, atoms[atom2i].name)
#                     blacklist.append(string)
#     ring_list = cycle_basis(graph)
#     return ring_list
#
#
# def find_planar_rings(atoms, bonds=None, planarityThreshold=.1):
#     all_rings = find_rings(atoms, bonds=bonds)
#     return are_planar(atoms, all_rings, planarityThreshold)
#
#
# def are_planar(atoms, all_rings, planarityThreshold=.1):
#     atom_dict = {atom.get_name(): atom for atom in atoms}
#     planar_rings = []
#     for ring in all_rings:
#         l = len(ring)
#         planarity = 0
#         for i, atom_name0 in enumerate(ring):
#             atom_name1 = ring[(i+1) % l]
#             atom_name2 = ring[(i+2) % l]
#             atom_name3 = ring[(i+3) % l]
#             atom0 = atom_dict[atom_name0]
#             atom1 = atom_dict[atom_name1]
#             atom2 = atom_dict[atom_name2]
#             atom3 = atom_dict[atom_name3]
#             v = abs(dot((atom0.cart - atom3.cart), cross((atom1.cart - atom3.cart), (atom2.cart - atom3.cart)))) / 6.
#             planarity += v
#         if planarity / l < planarityThreshold:
#             planar_rings.append(ring)
#     return planar_rings
#
#
