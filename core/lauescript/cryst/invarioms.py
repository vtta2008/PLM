__author__ = 'jens'


class Topology(object):
    def __init__(self, molecule):
        self.molecule = molecule

        for atom in self.molecule.atoms:
            ring = self.findRings(atom)

    def classifyAminoAcids(self):
        pass

    def findRings(self, start, maxSize=8, members=None):
        if not maxSize:
            return None
        if start in members:
            return members
        if not members:
            members = [start]
        for neighbour in start.neighbours:
            self.findRings(neighbour, maxSize-1, members+[start])