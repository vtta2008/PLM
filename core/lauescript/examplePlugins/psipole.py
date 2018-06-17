"""
Created on Mar 19, 2014

@author: Jens Luebben

Experimental module implementing a PSeudo dIpole refinement
model with Shelxl.

WORK IN PROGRESS!
"""
KEY = 'Psi'
OPTION_ARGUMENTS = {'load': None}

from copy import deepcopy

from lauescript.laueio.shelxl_iop import ShelxlIOP
from lauescript.laueio.shelxl_iop import ShelxlAtom
from lauescript.types.molecule import MoleculeInterface


class ShelxlMolecule(MoleculeInterface):
    """
    Class representing a molecule. Consists of atoms
    read from an shelx.res file.
    """

    def test(self):
        sample = PsipoleAtom()
        for atom in self.atoms():
            atom.train(sample)
            atom.set_sfacs()
        self.set_psipoles()

        # ===============================================================================

    #         for bond in self.get_bonds(unique=False):
    #
    #             if any([i.get_id()=='O1D' for i in bond]) and any([i.get_id()=='C4E' for i in bond]):
    #                 print bond[0].get_id(),bond[1].get_id()
    #===============================================================================


    def set_psipoles(self):
        """
        Sets the appropriate pseudo atoms along all bond axis.
        """
        fvar_len = len(self.iop.fvar)
        for i, bond in enumerate(self.get_bonds(unique=False, hydrogen=False)):
            i += fvar_len
            vec = (bond[1].get_cart() - bond[0].get_cart()) / 2
            pluspos = bond[0].get_cart() + vec
            minuspos = bond[0].get_cart() - vec
            plusatom = deepcopy(bond[0])
            plusatom.set_cart(pluspos)
            plusatom.set_sfac('Psi+')
            plusatom.set_id('P{:<3d}'.format(i))
            plusatom.set_var('{}1.00000'.format(i))
            plusatom.make_isot()
            minusatom = deepcopy(bond[0])
            minusatom.set_cart(minuspos)
            minusatom.set_sfac('Psi-')
            minusatom.set_id('M{:<3d}'.format(i))
            minusatom.set_var('{}1.00000'.format(i))
            minusatom.make_isot()

            self.add_fvar(0.5)

            #===================================================================
            # print
            # print bond[0].get_id()
            # print plusatom.get_sfac(),plusatom.get_frac(),plusatom.get_id(),plusatom.get_var()
            # print minusatom.get_sfac(),minusatom.get_frac(),minusatom.get_id(),minusatom.get_var()
            #===================================================================
            self.add_atom(plusatom, bond[0])
            self.add_atom(minusatom, bond[0])

            #===================================================================
            # print pluspos,minuspos
            #===================================================================
        self.build()
        print self.iop
        self.write()


    def write(self):
        """
        Writes a shelxl.ins file based on the current content.
        """
        fp = open('../lib/apdio/test.res', 'w')
        s = self.iop.__str__()
        fp.write(s)

    def add_atom(self, atom, parentatom=None):
        """
        Adds an atom to the molecule.
        """
        super(ShelxlMolecule, self).add_atom(atom)
        if parentatom:
            self.iop.add_atom(atom, parentatom)

    def build(self):
        """
        Generates the string representation of the current molecule content.
        """
        for atom in self.atoms():
            atom.build()
            atom.partition()

    def register_IOP(self, iop):
        """
        Registers an Input Output Provider.
        """
        self.iop = iop

    def add_fvar(self, value=0.5):
        """
        Adds a Shelxl style free variable to the molecule representation.
        """
        self.iop.add_fvar(value)


class PsipoleAtom(ShelxlAtom):
    """
    Class representing a pseudo atom that is used to emulate dipoles.
    """
    part = 4

    def __init__(self):
        """
        Initializes the atom.
        """
        pass

    def tester(self):
        """
        For testing purposes.
        """
        print 'x'

    def set_sfacs(self):
        """
        Sets the occupation factor of the atom.
        """
        self.sfac_cart += ['Psi+', 'Psi-']

    def make_isot(self):
        """
        Makes the displacement paramters isotropic.
        """
        self.adp = [str((float(self.adp[0]) + float(self.adp[1]) + float(self.adp[2])) / 3)]

    def partition(self):
        """
        Places the atom in its own part.
        """
        if self.get_sfac() == 'Psi+':
            self.content = 'part {}\n'.format(PsipoleAtom.part) + self.content + '\npart 0'
            PsipoleAtom.part += 1
        if self.get_sfac() == 'Psi-':
            self.content = 'part {}\n'.format(PsipoleAtom.part) + self.content + '\npart 0'
            PsipoleAtom.part += 1


def run(configurator):
    """
    Called by the plugin manager.
    """
    global config, printer, molecule
    # ===========================================================================
    # config=configurator
    # printer=config.setup()
    # filename=config.arg('load')
    #===========================================================================
    filename = '../lib/apdio/merg.res'

    molecule = ShelxlMolecule()

    iop = ShelxlIOP(filename)
    molecule.register_IOP(iop)
    provider_switch = None
    parameter = {'cell': _cell_parser, 'atom': _atom_parser}
    for atom in iop.provide():
        if atom in parameter.keys():
            provider_switch = atom
            continue
        elif type(atom) == type(''):
            continue
        parameter[provider_switch](atom)
    molecule.test()


def _cell_parser(value):
    """
    Sets the global variable 'cell'
    """
    global cell
    cell = value


def _atom_parser(atom):
    """
    Adds 'atom' to the global variable 'molecule'.
    """
    molecule.add_atom(atom)


if __name__ == '__main__':
    run(None)