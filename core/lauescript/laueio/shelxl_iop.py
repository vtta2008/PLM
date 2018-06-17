"""
Created on Mar 18, 2014

@author: Arrahed
"""
from string import ascii_letters
import numpy as np
from lauescript.cryst.transformations import frac2cart, \
    cart2frac, \
    frac2cart_ADP, \
    cart2frac_ADP
from lauescript.laueio.io import IOP
from lauescript.cryst.tables import covalence_radius


class ShelxlAtom(object):
    def __init__(self, line, sfac_cart, cell, part, residue=0, prefix=''):
        self.get_element = self.get_sfac
        self.set_element = self.set_sfac
        self.sfac_cart = sfac_cart
        self.cart = None
        self.cell = cell
        self.residue = residue
        self.content = [line.rstrip('\n')]
        self.name = (self.content[0].split(' ')[0] + '_' + str(self.residue)) if self.residue else self.content[0].split(' ')[0]
        self.part = part
        self.adp_updated = False
        self.prefix = prefix
        self.bedeInstructions = None
        self.loneInstructions = None

    def setBedeInstructions(self, instructions):
        self.bedeInstructions = instructions

    def setLoneInstructions(self, instructions):
        self.loneInstructions = instructions

    def getBedeInstructions(self):
        return self.bedeInstructions

    def getLoneInstructions(self):
        return self.loneInstructions

    def append(self, line):
        self.content.append(line.rstrip('\n'))

    def __str__(self):
        return '{}'.format(self.content)

    def train(self, classinstance):
        self.__class__ = classinstance.__class__

    def parse(self):
        self.content = ' '.join([i.rstrip('=') for i in self.content])
        firstline = [i for i in self.content.split(' ') if len(i) > 0]
        self.sfac = firstline[1]
        self.frac = [float(i) for i in firstline[2:5]]
        self.var = firstline[5]
        self.adp_frac = firstline[6:]


    def get_sfac(self):
        return self.sfac_cart[int(self.sfac) - 1].title()

    def set_sfac(self, value):
        self.sfac = self.sfac_cart.index(value) + 1


    def get_frac(self):
        return self.frac

    def set_frac(self, value):
        self.frac = value

    def get_cart(self):
        if self.cart is None:
            self.cart = frac2cart(self.frac, self.cell)

        return self.cart

    def set_cart(self, value):
        if not value is None:
            self.cart = value
            self.frac = cart2frac(self.cart, self.cell)


    def get_id(self):
        return self.name

    def set_id(self, value):
        self.name = value

    def get_var(self):
        return self.var

    def set_var(self, value):
        self.var = value

    def get_adp_frac(self):
        if len(self.adp_frac) == 6:
            adp = [self.adp_frac[0], self.adp_frac[1], self.adp_frac[2],
                   self.adp_frac[5], self.adp_frac[4], self.adp_frac[3]]
        else:
            adp = self.adp_frac
        return adp

    def set_adp_frac(self, value):
        self.adp_frac = [self.adp_frac[0], self.adp_frac[1], self.adp_frac[2],
                         self.adp_frac[5], self.adp_frac[4], self.adp_frac[3]]

    def set_adp_cart(self, value):
        if not value is None:

            value = cart2frac_ADP(value, self.cell)
            # ===================================================================
            # if self.get_element()=='H':
            #     value=[10+i for i in value]
            #===================================================================
            self.adp_frac = [value[0], value[1], value[2],
                             value[5], value[4], value[3]]
            self.adp_updated = True
        else:
            self.adp_updated = False

    def get_adp_cart(self):
        adp = [self.adp_frac[0], self.adp_frac[1], self.adp_frac[2],
               self.adp_frac[5], self.adp_frac[4], self.adp_frac[3]]
        return frac2cart_ADP(adp, self.cell)

    def build(self):
        self.content = [self.prefix, self.name, str(self.sfac)] + \
                       [str(i) for i in self.frac] + \
                       [str(self.var)] + \
                       [str(i) for i in self.adp_frac if not i == '=']
        self.content = [self.content[0], self.content[1], self.content[2]] + ['{:2.6f}'.format(float(i)) for i in
                                                                              self.content[3:]]
        # =======================================================================
        # self.content=[i for i in self.content if len(i)>0]
        #=======================================================================
        #=======================================================================
        # print self.content
        #=======================================================================
        if len(self.content) > 9:
            self.content = '{}{} =\n      {} '.format(self.content[0], '  '.join(self.content[1:9]),
                                                      '  '.join(self.content[9:]))
        else:
            self.content = '{}{}'.format(self.content[0], ' '.join(self.content[1:]))
            #=======================================================================
            # print self.content
            #=======================================================================

    def set_afix(self, value):
        if value:
            self.prefix = str(value + '\n')


class ShelxlIOP(IOP):
    cmds = ['REM',
            'BEDE',
            'MOLE',
            'TITL',
            'CELL',
            'ZERR',
            'LATT',
            'SYMM',
            'SFAC',
            'UNIT',
            'TEMP',
            'L.S.',
            'BOND',
            'ACTA',
            'LIST',
            'FMAP',
            'PLAN',
            'WGHT',
            'FVAR',
            'SIMU',
            'RIGU',
            'SADI',
            'SAME',
            'DANG',
            'AFIX',
            'PART',
            'HKLF',
            'ABIN',
            'ANIS',
            'ANSC',
            'ANSR',
            'BASF',
            'BIND',
            'BLOC',
            'BUMP',
            'CGLS',
            'CHIV',
            'CONF',
            'CONN',
            'DAMP',
            'DEFS',
            'DELU',
            'DFIX',
            'DISP',
            'EADP',
            'EQIV',
            'EXTI',
            'EXYZ',
            'FEND',
            'FLAT',
            'FMAP',
            'FRAG',
            'FREE',
            'GRID',
            'HFIX',
            'HTAB',
            'ISOR',
            'LATT',
            'LAUE',
            'MERG',
            'MORE',
            'MPLA',
            'NCSY',
            'NEUT',
            'OMIT',
            'PLAN',
            'PRIG',
            'RESI',
            'RTAB',
            'SADI',
            'SAME',
            'SHEL',
            'SIMU',
            'SIZE',
            'SPEC',
            'STIR',
            'SUMP',
            'SWAT',
            'TWIN',
            'TWST',
            'WIGL',
            'WPDB',
            'XNPD',
            'REM',
            'Q',
            'END',
            'BEDE',
            'LONE',
    ]
    cmds = cmds + [cmd.swapcase() for cmd in cmds] + [cmd.title() for cmd in cmds]


    def __init__(self, *args, **kwargs):
        super(ShelxlIOP, self).__init__(*args, **kwargs)
        self.activeChain = 0
        self.activeResidue = (0, '')
        self.residuesOfName = {}
        self.bedeInstructions = {}
        self.loneInstructions = {}
        self.fvars = []


    def get_symmetry(self):
        return self.symmetry

    def get_lattice(self):
        return self.lattice

    def set_id(self):
        self.id = '{}{}'.format('shelxl', IOP.instance)

    def add_fvar(self, value=0.5):
        self.fvar.append(str(value))

    def _build_fvar(self):
        if self.content[self.fvar_line].startswith('FVAR'):
            self.content[self.fvar_line] = 'FVAR ' + ' '.join(self.fvar)
        else:
            for i, line in enumerate(self.content):
                if line.startswith('FVAR'):
                    self.content[i] = 'FVAR' + ' '.join(self.fvar)
                    self.fvar_line = i
                    break

    def T_value(self, value):
        return float(value.partition('(')[0]) + 273

    def parse(self):
        end = False
        new_content = []
        self.atoms = {}
        current_AFIX = ''
        part = 0
        for j, line in enumerate(self.content):
            if any([line.upper().startswith(cmd) for cmd in ShelxlIOP.cmds]):


                if line.startswith('CELL'):
                    self.cell = [i for i in line.rstrip().split(' ') if len(i) > 0][2:]
                    self.cell = [float(i) for i in self.cell]
                elif line.startswith('SFAC'):
                    sfac_cart = [i for i in line.rstrip().split(' ') if len(i) > 0][1:]
                    self.sfac_line = j
                elif line.startswith('FVAR'):
                    self.fvars += [i for i in line.rstrip().split(' ') if len(i) > 0][1:]
                    self.fvar_line = j
                elif line.startswith('TEMP'):
                    self.T = self.T_value([i for i in line.rstrip().split(' ') if len(i) > 0][-1])
                elif line.startswith('SYMM'):
                    self.symmetry.append(
                        ' '.join([i for i in line.rstrip().split(' ') if len(i) > 0][1:]).split(','))
                elif line.startswith('LATT'):
                    self.lattice = [i for i in line.rstrip().split(' ') if len(i) > 0][-1]
                elif any([line.startswith(string) for string in ['PART', 'Part', 'part']]):
                    part = line.rstrip().partition(' ')[2]
                elif line.startswith('AFIX'):
                    current_AFIX = line
                elif line.upper().startswith('RESI'):
                    words = line.rstrip().split()
                    number = words[1]
                    try:
                        name = words[2]
                    except IndexError:
                        name = ''
                    self.activeResidue = (number, name)
                    try:
                        self.residuesOfName[name].append(number)
                    except KeyError:
                        self.residuesOfName[name]= [number]
                elif line.upper().startswith('BEDE') or line.upper().startswith('LONE'):
                    self.registerBEDEInstruction(line[:-1], j)

                elif line.upper().startswith('HKLF'):
                    end = True


                new_content.append(line.rstrip())
            elif line[0] in ascii_letters and not end:
                atom = ShelxlAtom(line, sfac_cart, self.cell, part=part, prefix=current_AFIX, residue=self.activeResidue[1])
                current_AFIX = ''
                new_content.append(atom)
                self.atoms[atom.name] = atom
            elif len(line) > 1:
                try:
                    new_content[-1].append(line)
                except:
                    pass
        self.content = new_content
        self._resolveBEDELONE()
        self._parse_atoms()


    def __str__(self):
        self.build()
        string = ''
        for c in self.content:
            string += '{}\n'.format(str(c))
        return string

    def build(self):
        for atom in self.atoms.values():
            atom.build()

    def buildConnectionTable(self):
        connectionTable = {}
        for atom1 in self.atoms.values():
            for atom2 in self.atoms.values():
                key = ':'.join(sorted([atom1.get_name(), atom2.get_name()]))
                if np.linalg.norm(atom1.get_cart() - atom2.get_cart()) <= float(covalence_radius[atom1.get_element()])\
                        + float(covalence_radius[atom2.get_element()]) + .1:
                    connectionTable[key] = True
                else:
                    connectionTable[key] = False
        self.connectionTable = connectionTable

    def _parse_atoms(self):
        self.cart = {}
        self.frac = {}
        self.adp_cart = {}
        self.adp_frac = {}
        self.adp_iso_frac = {}
        self.element = {}
        self.names = []
        for name, atom in self.atoms.items():
            atom.parse()
            atom.build()
            self.cart[name] = atom.get_cart()
            self.frac[name] = atom.get_frac()
            adp = atom.get_adp_frac()
            if len(adp) == 6:
                self.adp_frac[name] = adp
                self.adp_cart[name] = frac2cart_ADP(adp, self.cell)
            else:
                self.adp_frac[name] = None
                self.adp_cart[name] = None
                self.adp_iso_frac[name] = adp
            self.names.append(name)
            self.element[name] = atom.get_element()

        # if self.bedeInstructions or self.loneInstructions:
        #     self.buildConnectionTable()

        for name, atom in self.atoms.items():
            self.findBEDEInstructions(name, atom)

    def findBEDEInstructions(self, atomName, atom):
        bedes = []
        try:
            bedes += self.bedeInstructions[atomName]
        except KeyError:
            pass
        try:
            bedes += self.bedeInstructions['$' + atom.get_element()]
        except KeyError:
            pass

        bedesByR = {}
        for bede in bedes:
            try:
                bedesByR[bede['r']].append(bede)
            except KeyError:
                bedesByR[bede['r']] = [bede]

        selectedBedes = []
        for r, bedes in bedesByR.items():
            firstPs = {bede['direction']: 99999 for bede in bedes}
            # print firstPs.keys()
            elements = [p for p in firstPs.keys() if '$' in p]
            for e in elements:
                firstPs[e] = 99999
            # firstP = 99999
            firstBEDEs = []
            for bede in bedes:
                p = bede['priority']
                direction = bede['direction']
                if not '$' in direction:
                        element = '$'+self.atoms[direction].get_element()
                else:
                    element = direction
                if not element in firstPs.keys():
                    element = direction
                if p < firstPs[direction] and p < firstPs[element]:

                    firstBEDEs.append(bede)
                    firstPs[direction] = p
            for firstBEDE in firstBEDEs:
                selectedBedes.append(firstBEDE)
        atom.setBedeInstructions(selectedBedes)

        lones = []
        try:
            lones += self.loneInstructions[atomName]
        except KeyError:
            pass
        try:
            lones += self.loneInstructions['$' + atom.get_element()]
        except KeyError:
            pass

        lonesByR = {}
        for lone in lones:
            try:
                lonesByR[lone['r']].append(lone)
            except KeyError:
                lonesByR[lone['r']] = [lone]

        selectedLones = []
        for r, lones in lonesByR.items():
            firstP = 999
            firstLONE = None
            for lone in lones:
                p = lone['priority']
                if p < firstP:
                    firstLONE = lone
                    firstP = p
            selectedLones.append(firstLONE)
        atom.setLoneInstructions(selectedLones)




    def set_cart(self, name, value):
        self.atoms[name].set_cart(value)

    def set_adp_cart(self, name, value):
        self.atoms[name].set_adp_cart(value)

    def set_afix(self, name, value):
        self.atoms[name].set_afix(value)

    def registerBEDEInstruction(self, instruction, lineNumber):
        cmd = instruction[:4].upper()
        if cmd == 'BEDE':
            self._parseBEDE(instruction, lineNumber)
        else:
            self._parseLONE(instruction, lineNumber)

    def _parseBEDE(self, instr, lineNumber):
        instr = [i for i in instr.split() if i]
        if instr[-1][0] in ascii_letters:
            instr = instr[:1] + instr[-2:] + instr[1:-2]
        instr = {
            'origin': instr[1],
            'direction': instr[2],
            'r': instr[3],
            'A': self.toFVAR(instr[4]),
            'U1': self.toFVAR(instr[5]),
            'U2': self.toFVAR(instr[6]),
            'priority': lineNumber}
        try:
            self.bedeInstructions[instr['origin']].append(instr)
        except KeyError:
            self.bedeInstructions[instr['origin']] = [instr]

    def toFVAR(self, value):
        fvalue = float(value)
        if -15 > fvalue or fvalue > 15:
            index = int(value.partition('.')[0][:-1])
            factor = value.partition('.')
            factor = factor[0][-1] + '.' + factor[2]
            FVAR = (index, float(factor))
            return FVAR
        return float(value)

    def resolveFVAR(self, FVAR):
        if not type(FVAR) == tuple:
            raise TypeError
        fvar = float(self.fvars[FVAR[0]-1])
        return fvar * FVAR[1]

    def _parseLONE(self, instr, lineNumber):
        instr = [i for i in instr.split() if i][1:]
        for i, value in enumerate(instr):
            try:
                m = int(value)
                break
            except:
                pass
        try:
            p = float(instr[i+5])
        except:
            p = None
        instr = {'origin': instr[:i],
                 'm': m,
                 'A': self.toFVAR(instr[i+1]),
                 'U1': self.toFVAR(instr[i+2]),
                 'U2': self.toFVAR(instr[i+3]),
                 'r': instr[i+4],
                 'priority': lineNumber}
        for origin in instr['origin']:
            try:
                self.loneInstructions[origin].append(instr)
            except KeyError:
                self.loneInstructions[origin] = [instr]

    def _resolveBEDELONE(self):
        for bedes in list(self.bedeInstructions.values()) + list(self.loneInstructions.values()):
            for bede in bedes:
                for key, param in bede.items():
                    try:
                        value = self.resolveFVAR(param)
                    except TypeError:
                        pass
                    else:
                        bede[key] = value




if __name__ == '__main__':
    test = ShelxlIOP('km103_red.res')
    test.read()
    # ===========================================================================
    # print test
    #===========================================================================
    for atom in test.atoms.values():
        if atom.get_element() == 'H':
            atom.set_afix('AFIX 666')
    # print test
