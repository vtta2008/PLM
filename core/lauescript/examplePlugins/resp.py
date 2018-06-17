__author__ = 'claudia'
'''
Created on 04.06.2014

@author: Jens Luebben & Claudia Orben

This is a a plugin for the APD-Toolkit. based on 
a Template from 08.02.2014.

The plugin assigns resp-charges to all atoms of a 
molecule according to their invariom name.
In order to do this it needs a file called 
chargeDABA.txt containing all invariomnames with
the correcponding resp charges.
An according xd.resp.inp file is written, in which
the monopole populations are set according to the 
resp charges.

To be recognized as a plugin by the plugin manager
the module must implement the global 'KEY' variable.
The value of the variable defines how the plugin will
be addressed by the cmdline. In this case the module
will be executed if '-resp' is given as a cmdline
argument.
The global variable OPTION_ARGUMENTS is optional.
Not used in this case.

A plugin must also implement a 'run()'function taking
one argument. The plugin manager passes itself when
calling the run() function. Before anything else
the run() function should call the 'config.setup()'
function which returns:
    - printer: An instance of the apd_printer class.
      The instance is created with the correct
      indentation level. The plugin manager also
      calls the 'enter(), headline(), bottomline()
      and exit()' methods.
'''
KEY = 'resp'
#OPTION_ARGUMENTS = ['neutral']
OPTION_ARGUMENTS = {'neutral':'a', 'charge':0}


def run(conf):
    global config
    config = conf
    printer = config.setup()
    printer('\nThe resp_plugin has been successfully' \
            ' started.\nNow, resp-charges are assigned according to their invariom name.' \
            '\nIn order to do this a file called chargeDABA.txt \ncontaining all invariomnames with' \
            ' the corresponding resp charges is needed in the apd/data/ folder.\n')

    printer('\nAsking config for value of option \'load\': {}'.format(config.arg('load')))
    printer('Asking config for value of option \'x\': {}'.format(config.arg('x')))

    filename = 'xd.resp'
    loader = config.get_variable('loader')
    writer = loader.get_write_copy(filename)

    global multidict
    multidict = {}
    global electron_number
    from lauescript.cryst.tables import electron_number
    #from apd.lib.invstring2 import get_invariom_names
    import lauescript.invstring2 as invstring

    ###--------reading chargeDABA.txt into dictionary chargedict ---------------#

    global chargedict
    path_string = conf.get_databasepath()
    chargedict = {}
    f = open(path_string + '/chargeDABA.txt', 'r')
    for line in f.readlines():
        line = line[:-1].split()
        chargedict[line[0]] = float(line[1])
    f.close()
    ###----------------------
    ###--------molecule identifier ---------------#
    global molcount
    molcount=0
    global chargedicts
    chargedicts = {}
    global resp_arrays
    resp_arrays = {}
    global atomcounts
    atomcounts = {}
    data = config.get_variable()
    for atom in data['exp'].atoms:
         if atom.molecule_id > molcount:
            molcount = atom.molecule_id
            resp_arrays[atom.molecule_id]= []
    molcount=molcount+1
    printer('{} molecules were detected.',format(molcount))
    for j in range(0,molcount):
        resp_arrays[j] = []
        atomcounts[j] = 0
        chargedicts[j] = {}
    for atom in data['exp'].atoms:
            atomcounts[atom.molecule_id] = atomcounts[atom.molecule_id] + 1


    ###----------------------
    global average_corrections
    average_corrections = {}
    overallcharges = {}
    resp = 0.0
    monopole_pop = 0.0

    charged=config.arg("charged")
    import charge_lib
    for j in range(0,molcount):
        overallcharges[j]=charge_lib.check_charges(j, atomcounts, charged, printer )


    ###  Electroneutrality correction
    ###-------------collecting charges for the molecule 
    ###-------------to get a correction factor for electroneutrality

    ### ----Option a
    ###-------------via a correction averaged over the whole molecule

    neutral = config.arg("neutral")
    if not neutral or neutral == "a":
        #printer(neutral)

        data = config.get_variable()
        for atom in data['exp'].atoms:
            import charge_lib
            charge_lib.build_resp_arrays( atom, resp_arrays, chargedict)
        for key in resp_arrays:
            printer('\nMolecule number {}:'.format(key))
            printer('\nNumber of atoms read:')
            printer(atomcounts[key])
        #printer('\nCharges of the invarioms')
        #printer(resp_array)
            printer('\nCharge of molecule if uncorrected:')
            printer(sum(resp_arrays[key]))
            printer('\n Deviation from charge of {}:'.format(overallcharges[key]))
            printer(sum(resp_arrays[key])-overallcharges[key])
            average_corrections[key] = float(float((sum(resp_arrays[key])-overallcharges[key])) / float(atomcounts[key]))
            printer('\nCorrection for every atom:')
            printer(average_corrections[key])

        ###  Assigning charge
        #print '\natom elec val_elec invariom resp_charge corr_charge\n'
            #i = 0
            already_corrected_inv_list = []
            data = config.get_variable()
            for atom in data['exp'].atoms:
                if atom.molecule_id == key :
                    #i = i + 1
                    resp = chargedict[atom.invariom_name]

                    if atom.invariom_name not in already_corrected_inv_list:
                        charge = resp - average_corrections[key]
                        chargedicts[key][atom.invariom_name] = charge
                        already_corrected_inv_list.append(atom.invariom_name)
                    else:
                        charge = resp - average_corrections[key]
                        resp = charge
                    #print atom.name, atom.invariom_name, resp, charge


    ### ----Option b
    ###-------------via a correction averaged all hydrogen atoms only
    elif neutral == "b":
        printer(neutral)
        data = config.get_variable()
        Hatomcounts = {j}
        for j in range (0,molcount):
            Hatomcounts[j] = 0
        for atom in data['exp'].atoms:
            if atom.element == "H":
                Hatomcounts[atom.molecule_id] = Hatomcounts[atom.molecule_id] + 1
            import charge_lib
            charge_lib.build_resp_arrays( atom, resp_arrays, chargedict)
        for key in resp_arrays:
            printer(key)
            printer('\nNumber of H atoms read:')
            printer(Hatomcounts[key])
            printer('\nCharges of the invarioms')
            printer(resp_arrays[key])
            printer('\nCharge of molecule if uncorrected:')
            printer(sum(resp_arrays[key]))
            printer('\n Deviation from charge of {}:'.format(overallcharges[key]))
            printer(sum(resp_arrays[key])-overallcharges[key])
            average_corrections[key] = float(float((sum(resp_arrays[key])-overallcharges[key])) / float(Hatomcount))
            printer('\nCorrection for every H atom:')
            printer(average_corrections[key])

        ###  Assigning charge
        #print '\natom elec val_elec invariom resp_charge corr_charge\n'
            #i = 0
            already_corrected_inv_list = []
            data = config.get_variable()
            for atom in data['exp'].atoms:
                if atom.molecule_id == key :
                #i = i + 1
                    resp = chargedict[atom.invariom_name]
                    if atom.element == "H":
                        if atom.invariom_name not in already_corrected_inv_list:
                            charge = resp - average_corrections[key]
                            chargedicts[key][atom.invariom_name] = charge
                            already_corrected_inv_list.append(atom.invariom_name)
                        else:
                            charge = resp- average_corrections[key]
                            resp = charge
                    else:
                        charge = resp
                        chargedicts[key][atom.invariom_name] = charge
                    #print atom.name, atom.invariom_name, resp, charge




    ### -------------------------------------
    ### -------------------------------------
    ###  Setting monopole populations
    #print '\natom elec val_elec invariom resp_charge monop_pop\n'
    i = 0
    zero_list = [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
                 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]
    data = config.get_variable()
    for atom in data['exp'].atoms:
        i = i + 1
        resp = chargedicts[atom.molecule_id][atom.invariom_name]
        el_num = int(electron_number[atom.element])
        if el_num < 3:
            val_num = el_num % 8
        else:
            val_num = (el_num - 2) % 8
        monopole_pop = val_num - resp

        #print atom.name, electron_number[atom.element], val_num, atom.invariom_name, resp, monopole_pop
        j = 0
        for atomdata in writer.provide(['multipoles']):
            j += 1
            if j == i:
                #print atomdata[1:]
                multidict[atomdata[0]] = [monopole_pop] + zero_list
                #multidict[atomdata[0]]=[monopole_pop]+atomdata[1][1:]
        ###-----------------------------------

    ### Setting and printing the results
    attr = ['multipoles']
    writer.set(attr, provide)
    writer.write()
    printer(
        '\n File xd.resp.inp was written, in which the monopole populations are set according to the resp charges :).\n')
    ###----------------------------------- 	



###-----------

def provide():
    data = config.get_variable()
    for atom in data['exp'].atoms:
        #print atom.name,multidict[atom.name]
        yield atom.name, multidict[atom.name]


#def provide_pdb():
#    for i, atom in enumerate(data.iter_atoms()):
#        yield [atom.get_name(), atom.get_cart(), i, atom.get_element(), 1, atom.adp['cart_meas'], 1, None,
#               chargedict[atom.invariom_name]]

### ---------------------------------------------------------------------------------  hier drueber wird die resp ladung als punkt ladung gesetzt !!!! lezter eintrag in der eckigen klammer!


