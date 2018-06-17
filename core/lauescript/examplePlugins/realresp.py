'''
Created on 04.06.2014

@author: Jens Luebben & Claudia Orben

This is a a plugin for the APD-Toolkit. based on 
a Template from 08.02.2014.

The plugin assigns resp-charges to all atoms of a 
molecule according to their atom number.
In order to do this it needs a file called 
charge.log containing all atom numbers in the first column
something in the second column and the charge in the third.
An according xd.rresp.inp file is written, in which
the monopole populations are set according to the 
charges.

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
KEY = 'realresp'
OPTION_ARGUMENTS = ['']


def run(conf):
    global config
    config = conf
    printer = config.setup()
    printer('\nThe real resp plugin has been successfully' \
            ' started.\nNow, resp-charges are assigned according to their atom number.' \
            '\nIn order to do this a file called charge.log \ncontaining all  atom numbers with' \
            'the correcponding resp charges is needed.\n')

    printer('\nAsking config for value of option \'load\': {}'.format(config.arg('load')))
    printer('Asking config for value of option \'x\': {}'.format(config.arg('x')))

    filename = 'xd.rresp'
    loader = config.get_variable('loader')
    writer = loader.get_write_copy(filename)

    global multidict
    multidict = {}
    global electron_number
    from lauescript.cryst.tables import electron_number

    ###--------reading charge.log into dictionary chargedict ---------------#
    global chargedict
    chargedict = {}
    f = open('charge.log', 'r')
    for line in f.readlines():
        line = line[
               :-1].split()  #unter teile die linie durch whitespace und lese bis ausschliesslich des letzten zeichens d.h.ohne linebreak
        chargedict[line[0]] = float(line[2])
    f.close()
    ###----------------------

    resp = 0.0
    monopole_pop = 0.0
    data = config.get_variable()

    ### -------------------------------------
    ### -------------------------------------
    ###  Setting monopole populations
    print '\natom elec val_elec invariom resp_charge monop_pop\n'
    i = 0
    numb = 0 #fuer Atomnummer im label
    zero_list = [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
                 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]
    data = config.get_variable()
    for atom in data['exp'].atoms:
        i = i + 1
        numbstr = atom.name

        #print numbstr[(numbstr.rfind("(")+1):numbstr.rfind(")")]
        numb = numbstr[(numbstr.rfind("(") + 1):numbstr.rfind(")")]
        #numbs.join([x for x in numbstr  if numbstr.isdigit()])
        #numb=int(numbs)
        resp = chargedict[numb]
        el_num = int(electron_number[atom.element])
        if el_num < 3:
            val_num = el_num % 8
        else:
            val_num = (el_num - 2) % 8
        monopole_pop = val_num - resp

        print atom.name, electron_number[atom.element], val_num, numb, resp, monopole_pop
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
        '\n File xd.rresp.inp was written, in which the monopole populations are set according to the real resp charges :).\n')
    ###----------------------------------- 	

    ### -----------------------------------
    ###
    ### Writing the charges into a pqr file
    ###
    ### -----------------------------------

    #from apd.lib.io.pdb_iop import PDBIOP
    #global data
    #pdbiop = PDBIOP('test.test')   
    #pdbiop.setup(new=True)
    #pdb_data = config.get_data()

    #pdbiop.set(['cart', 'serial_numbers', 'name_prefixes', 'occupancies',
    #            'adp_cart', 'residue_numbers', 'vdw_radii', 'point_charges'],
    #           provide_pdb, new=True)  
    #print pdbiop.export('PQR')
    #    
    #text_file = open("resp.pqr", "w")
    #text_file.write("%s" % pdbiop.export('PQR'))
    #text_file.close()
    #printer('\n resp.pqr has been written, with the assigned resp charges and vdw radii according to  J Phys Chem, 2009, p. 5806-5812.\n')

###-----------

def provide():
    data = config.get_variable()
    for atom in data['exp'].atoms:
        #print atom.name,multidict[atom.name]
        yield atom.name, multidict[atom.name]

#def provide_pdb():  
#    for i, atom in enumerate(data.iter_atoms()):
#          yield [atom.get_name(), atom.get_cart(), i, atom.get_element(), 1, atom.adp['cart_meas'], 1, None, chargedict[atom.invariom_name]]
### ---------------------------------------------------------------------------------  hier drueber wird die resp ladung als punkt ladung gesetzt !!!! lezter eintrag in der eckigen klammer!


