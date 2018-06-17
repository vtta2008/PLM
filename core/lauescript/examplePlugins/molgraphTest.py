__author__ = 'jens'

KEY = 'molgraph'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt'}  # Edit this to define cmd line options for
# the plugin and their default values.

import lauescript.cryst.molgraph as mg


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
    data = pluginManager.get_variable('data')



    graphs = []
    for graphandname in mg.Graph.molecule2Graphs(data['exp']):
        graphs.append(graphandname)
    hits = {}
    besttries = {}
    for graph1, inv in mg.GraphStorage.readDatabase('graphs2inv.dat', rebuild=False):
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

    printer('\n\nHits:')
    for atom in data.iter_atoms(sort=True):
        printer('{:6s} -->  {:40s} -->  {:4.2f}'.format(atom.get_name(),
                                                        hits[atom.get_name()],
                                                        besttries[atom.get_name()]))
    printer('\nValidating matched invarioms:')
    for graph, name in graphs:
        valid = graph.validate(hits[name], name[0])
        if not valid:
            printer('Warning: Potentially bad fit: {:6s} -> {}'.format(name, hits[name]))




