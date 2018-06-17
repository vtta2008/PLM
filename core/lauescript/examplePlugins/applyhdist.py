__author__ = 'claudia'

'''
Created on 25.11.2014

@author: Claudia Wandtke

This is a a plugin for the APD-Toolkit, based on
different other plugins (example_database_iterator).

The plugin reads a file called hdistDABA.txt, located
in the database directory. It contains the covalent hydrogen
bond distances according to invarioms.
These distances are transfere to the molecule of interest
and the hydrogen atoms set to the new distance along the
original bond direction.

'''

from lauescript.laueio.xd_iop import XDIOP
from lauescript.cryst.transformations import cart2frac

KEY = 'applyhdist'
OPTION_ARGUMENTS = ['write']


def run(pluginManager):
    global config, data2
    config = pluginManager
    printer = config.setup()
    write = config.arg("write")

    printer('\nAsking config for value of option \'load\': {}'.format(config.arg('load')))
    printer('Asking config for value of option \'write\': {}'.format(config.arg('write')))


    ###--------reading chargeDABA.txt into dictionary chargedict ---------------#
    global hdistdict
    hdistdict = {}
    path_string = pluginManager.get_databasepath()
    f = open(path_string + '/hdistDABA.txt', 'r')
    for line in f.readlines():
        line = line[:-1].split()
        hdistdict[line[0]] = float(line[1])
    f.close()
    ###----------------------
    printer('hdistDABA.txt found and loaded')

    data2 = config.get_variable()

    #for molecule in data2['exp'].molecules:


    for atom in data2['exp'].atoms:
        if atom.element == 'H':
            dist = hdistdict[atom.invariom_name]
            direction_vec= (atom.cart-atom.partner[0].cart)
            print 'Reset bond length of ', atom, 'from', ((direction_vec[0]**2+direction_vec[1]**2+direction_vec[2]**2)**(-0.5)), 'to', dist
            #print 'old bond length', ((direction_vec[0]**2+direction_vec[1]**2+direction_vec[2]**2)**(-0.5))
            norm_direction_vec=[0.0, 0.0, 0.0]
            norm_direction_vec[0]= direction_vec[0]*((direction_vec[0]**2+direction_vec[1]**2+direction_vec[2]**2)**(-0.5))
            norm_direction_vec[1]= direction_vec[1]*((direction_vec[0]**2+direction_vec[1]**2+direction_vec[2]**2)**(-0.5))
            norm_direction_vec[2]= direction_vec[2]*((direction_vec[0]**2+direction_vec[1]**2+direction_vec[2]**2)**(-0.5))
            new_dist_vec=[0.0, 0.0, 0.0]
            new_dist_vec[0]=norm_direction_vec[0] * dist
            new_dist_vec[1]=norm_direction_vec[1] * dist
            new_dist_vec[2]=norm_direction_vec[2] * dist
            atom.cart[0]=atom.partner[0].cart[0]+new_dist_vec[0]
            atom.cart[1]=atom.partner[0].cart[1]+new_dist_vec[1]
            atom.cart[2]=atom.partner[0].cart[2]+new_dist_vec[2]
            atom.set_cart(atom.cart)


    if write == "xd":

        xdiop=config.get_variable('loader').get_write_copy('new_h_xd')
        #xdiop = XDIOP('test.test')   # wuerede neues leeres XD file erzeugen anstelle der vorigen zeile
        xdiop.set(['cart'], provide)   # man gibt das was man weiss und bekommt die datei im richtigen format
        xdiop.write()



def provide():
    """
    Iterator iterating over all atoms yielding the attributes specified above.
    :return:
    """
    for i, atom in enumerate(data2.iter_atoms()):
        #yield [atom.set_frac( atom.cart2frac(data2['exp'].cart2fracmatrix)  )]
        yield [atom.name, atom.cart] # man gibt das was man weiss und bekommt die datei im richtigen format














