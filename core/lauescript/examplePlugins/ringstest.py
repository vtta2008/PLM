__author__ = 'jens'

from networkx import cycle_basis, Graph
from numpy import dot, cross

from lauescript.cryst.geom import is_bound


KEY = 'ring'

def find_rings(atoms):
    graph = Graph()
    for i, atom1 in enumerate(atoms):
        for atom2 in atoms[i+1:]:
            if is_bound(atom1.cart, atom1.element, atom2.cart, atom2.element):
                graph.add_edge(atom1.name, atom2.name)
    ring_list = cycle_basis(graph)
    return ring_list


def find_planar_rings(atoms):
    all_rings = find_rings(atoms)
    return are_planar(atoms, all_rings)


def are_planar(atoms, all_rings):
    atom_dict = {atom.name: atom for atom in atoms}
    planar_rings = []
    for ring in all_rings:
        l = len(ring)
        planarity = 0
        for i, atom_name0 in enumerate(ring):
            atom_name1 = ring[(i+1) % l]
            atom_name2 = ring[(i+2) % l]
            atom_name3 = ring[(i+3) % l]
            atom0 = atom_dict[atom_name0]
            atom1 = atom_dict[atom_name1]
            atom2 = atom_dict[atom_name2]
            atom3 = atom_dict[atom_name3]
            v = abs(dot((atom0.cart - atom3.cart), cross((atom1.cart - atom3.cart), (atom2.cart - atom3.cart)))) / 6.
            planarity += v
        if planarity / l < .1:
            planar_rings.append(ring)
    return planar_rings


def run(config):
    printer = config.setup()
    data = config.get_variable()
    printer(find_rings([atom for atom in data.iter_atoms()]))
    printer(find_planar_rings([atom for atom in data.iter_atoms()]))