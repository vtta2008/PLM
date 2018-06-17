__author__ = 'claudia'

'''
Created on 25.11.2014

@author: Claudia Wandtke

This is a a plugin for the APD-Toolkit, based on
different other plugins (example_database_iterator).

The plugin reads a file calles H_MAP.txt, which is
an extraction of APD.MAP of only the Hydrogen invarioms.
If a molecule in the database appears in this file, the
hydrogen invarioms from those invarioms that are supplied
by the model compoound are looked at.

The covalent bond distances are calculated and stored for each
invariom in a file called hdistDABA.txt.
multiple atoms in the modelcompound defining one invariom are
averaged.

'''


from lauescript.cryst.iterators import database, atoms_of_element
from numpy import mean

KEY = 'gethdist'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt'}  # Edit this to define cmd line options for
# the plugin and their default values.


def run(pluginManager):
    """
    This is the entry point for the plugin manag
    The plugin manager will pass a reference to itself
    to the function.
    Use the APD_Printer instance returned by
    pluginManager.setup() instead of the 'print'
    statement to generate autoformated cmd line output.
    :param pluginManager: Reference to the plugin manager
    instance.
    """
    printer = pluginManager.setup()
    ###--------reading chargeDABA.txt into dictionary chargedict ---------------#
    printer('Reading list of molecules which are model compounds for hydrogen invarioms')
    global hmodelsdict
    global hdistdict
    hmodelsdict = {}
    hdistdict = {}
    path_string = pluginManager.get_databasepath()
    f = open(path_string + '/H_MAP.txt', 'r')
    for line in f.readlines():
        line = line[:-1].split(":")
        hmodelsdict[line[0]] = line[1]
    f.close()
    ###----------------------
    #printer('\nmodelcompound of H@6c:',hmodelsdict["H@6c"])
    #print 'h invariom model compounds in dict as list'
    #print hmodelsdict.values()

    ###----------------------
    printer('Reading database file...')
    count = 0
    altcount = 0
    dist = 0.0
    #print "\nhydrogen.invarioms.keys()[0] bond hydrogen.name name2 name3 \n"
    for molecule in database(pluginManager):
        if molecule.name in list(hmodelsdict.values()):
            #printer(molecule)
            count=count+1
            h_atoms = atoms_of_element(molecule, 'H')
            for hydrogen in h_atoms:
                if molecule.name== hmodelsdict[hydrogen.invarioms.keys()[0]]:
                    bond = hydrogen - hydrogen.partner[0]
                    name2=' '
                    name3=' '
                    if 1 < len(hydrogen.invarioms.keys()):
                        if hydrogen.invarioms.keys()[1] not in hmodelsdict:
                            altcount= altcount+1
                            name2= hydrogen.invarioms.keys()[1]
                            print "alternative invariom name NOT covered jet!!!", hydrogen.invarioms.keys()[1]
                        #else:
                            #print "alternative name already covered", hydrogen.invarioms.keys()[1]
                    if 2 < len(hydrogen.invarioms.keys()):
                        if hydrogen.invarioms.keys()[2] not in hmodelsdict:
                            altcount= altcount+1
                            name3= hydrogen.invarioms.keys()[2]
                        #else:
                           # print "2nd alternative name already covered", hydrogen.invarioms.keys()[2]
                    #print hydrogen.invarioms.keys()[0], bond, hydrogen.name, name2, name3

                    if hydrogen.invarioms.keys()[0] not in hdistdict:
                        hdistdict[hydrogen.invarioms.keys()[0]]   = bond
                        #print "not jet present, but just added:", hydrogen.invarioms.keys()[0], hdistdict[hydrogen.invarioms.keys()[0]]
                    else:
                        #print "invariom already present, need to average"
                        #print bond, hdistdict[hydrogen.invarioms.keys()[0]], hydrogen.invarioms.keys()[0]
                        average_bond = mean([bond, hdistdict[hydrogen.invarioms.keys()[0]]])
                        hdistdict[hydrogen.invarioms.keys()[0]] = average_bond

                #### For those cases in which invariom comes from an atom whose 1st alternative invariom name it is

                elif 1 < len(hydrogen.invarioms.keys()):
                    if molecule.name== hmodelsdict[hydrogen.invarioms.keys()[1]]:
                        print "the alternative invariom name appears in the hmodelsdict thereby in H_MAP.txt", hydrogen.invarioms.keys()[1]
                        bond = hydrogen - hydrogen.partner[0]
                        name2=' '
                        name3=' '
                        if 1 < len(hydrogen.invarioms.keys()):
                            if hydrogen.invarioms.keys()[1] not in hmodelsdict:
                                altcount= altcount+1
                                name2= hydrogen.invarioms.keys()[1]
                                print "alternative invariom name NOT covered jet!!!", hydrogen.invarioms.keys()[1]
                            #else:
                                #print "alternative name already covered", hydrogen.invarioms.keys()[1]
                        if 2 < len(hydrogen.invarioms.keys()):
                            if hydrogen.invarioms.keys()[2] not in hmodelsdict:
                                altcount= altcount+1
                                name3= hydrogen.invarioms.keys()[2]
                            #else:
                               # print "2nd alternative name already covered", hydrogen.invarioms.keys()[2]
                        #print hydrogen.invarioms.keys()[0], bond, hydrogen.name, name2, name3

                        if hydrogen.invarioms.keys()[1] not in hdistdict:
                            hdistdict[hydrogen.invarioms.keys()[1]]   = bond
                            #print "not jet present, but just added:", hydrogen.invarioms.keys()[0], hdistdict[hydrogen.invarioms.keys()[0]]
                        else:
                            print "invariom already present, need to average"
                            print bond, hdistdict[hydrogen.invarioms.keys()[1]], hydrogen.invarioms.keys()[1]
                            average_bond = mean([bond, hdistdict[hydrogen.invarioms.keys()[1]]])
                            hdistdict[hydrogen.invarioms.keys()[1]] = average_bond



                elif 2 < len(hydrogen.invarioms.keys()):
                    if molecule.name== hmodelsdict[hydrogen.invarioms.keys()[2]]:
                        print "the 2nd alternative invariom name appears in the hmodelsdict thereby in H_MAP.txt", hydrogen.invarioms.keys()[2]
                #else:
                    #print 'other reason to kick oth this hydrogen atom with invariom:', hydrogen.invarioms.keys()[0]


        #else:
        #    printer ('Entry in H_MAP.txt not looked at', molecule.name  )

    length = 0
    length = len (list( hmodelsdict.values() ))
    printer('The length of the hmodelsdict', length)

    printer('Number of molecules supplying hydrogen invarioms', count)
    printer('Number of alternative H invarioms to be considered (should be zero)', altcount)

    h_invariom_count = 0
    dabafile = open(path_string + '/hdistDABA.txt', 'w')
    for i in range(len(hdistdict)):
        h_invariom_count = h_invariom_count +1
        temp=list(hdistdict.popitem())
        dabafile.writelines(temp[0] + '  ' + str(temp[1]) +'\n')
    printer('Number of hydrogen invarioms written to hdistDABA.txt', h_invariom_count)

