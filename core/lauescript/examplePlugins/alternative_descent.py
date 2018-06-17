"""
Created on Jul 24, 2014

@author: claudia
This Plugin is meant for the printing of alternatives invairomnames
to files called apd.descent
apd.descent2 and apd.descent3
all of them include the invarioms of all atoms and only
in the case of an alternative invariom name this alternative one is written to the second file
and only if a third invariom name is possible apd.descent is differnt from apd.descent.

Primary usage is for every modelcopound in roder to be able to average the charges
with a weight of 3/3 if an invariom is very well defined and 2/3 if it is close to a
bond order limit so that it can also  be taken into account for the different invariom name by a weight of 1/3..

"""

KEY = 'descent2'
OPTION_ARGUMENTS = {'file': 'apd.descent2'}


def run(config):
    printer = config.setup()
    filename = config.arg('file')
    file2_pointer = open('apd.descent3', 'w')
    file1_pointer = open('apd.descent', 'w')
    file_pointer = open(filename, 'w')

    printer('Writing apd.descent, apd.descent2 and apd.descent3')

    for atom in config.get_variable().iter_atoms(sort=True):
        #print atom.name, atom.invarioms.keys()

        inv_name=atom.invariom_name

        file1_pointer.write('{}: {} from: {}\n'.format(atom.name,
                                                      atom.invarioms.keys()[0],
                                                      atom.model_compound.name))

        if 2 < len(atom.invarioms.keys()):

            #print atom.invarioms.keys()[2]
            ainv_name=atom.invarioms.keys()[2]
            #print atom.invariom_name

        file2_pointer.write('{}: {} from: {}\n'.format(atom.name,
                                                      inv_name,
                                                      atom.model_compound.name))

        if 1 < len(atom.invarioms.keys()):
            #print atom.invarioms.keys()[1]
            inv_name=atom.invarioms.keys()[1]
            #print atom.invariom_name


        file_pointer.write('{}: {} from: {}\n'.format(atom.name,
                                                      inv_name,
                                                      atom.model_compound.name))

