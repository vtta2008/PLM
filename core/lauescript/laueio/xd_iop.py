"""
Created on Apr 1, 2014

@author: jens
"""
from numpy import array, cos, pi

from lauescript.cryst.transformations import frac2cart, \
    frac2cart_ADP, \
    cart2frac, \
    cart2frac_ADP
from lauescript.laueio.io import IOP
from lauescript.types.atom import AtomInterface
from lauescript.core.core import apd_exit
from lauescript.cryst.geom import is_bound2
from collections import OrderedDict


class KEY(dict):
    """
    Class representing the xd refinement keys for a given
    atom.
    """

    def __init__(self, name):
        super(KEY, self).__init__()
        self.name = name

    def set_U2(self, value):
        self['U2'] = value

    def __str__(self):
        string = '{:<8}{:3} {:6} {:10} {:15} {:2} {:3} {:5} {:7} {:9}\n'.format(self.name,
                                                                                self['xyz'],
                                                                                self['U2'],
                                                                                self['U3'],
                                                                                self['U4'],
                                                                                self['Mono'],
                                                                                self['Dipo'],
                                                                                self['Quato'],
                                                                                self['Okto'],
                                                                                self['Hexa'])
        return string


class XDAtom(AtomInterface):
    def __init__(self, *args, **kwargs):
        super(XDAtom, self).__init__(*args, **kwargs)
        self.cell = None
        self.adp_frac = None
        
    def set_frac(self, value):
        super(XDAtom, self).set_frac(value)

    def set_adp_cart(self, value):
        if not None is value:
            self.adp_frac = cart2frac_ADP(value, self.cell)

    def get_adp_cart(self):
        return frac2cart_ADP(self.adp_frac, self.cell)

    def set_cart(self, value):
        if not None is value:
            self.frac = cart2frac(value, self.cell)

    def get_cart(self):
        return frac2cart(self.frac, self.cell)

    def set_cell(self, value):
        self.cell = value

    def __str__(self):
        string = '{name:<8s}{icor1:>3}{icor2:>2}{nax:>5}{nay1:>4}{nay2:>4}{jtf:>2}{itbl:>3}{isfz:>3}{lmax:>2}'\
                 '{isym:>3}{ichcon:>4} {x:>9.6f} {y:>9.6f} {z:>9.6f} {o:6.4f}\n'\
            .format(name=self.get_name(),
                    icor1=self.get_custom_attribute('icor1'),
                    icor2=self.get_custom_attribute('icor2'),
                    nax=self.get_custom_attribute('nax'),
                    nay1=self.get_custom_attribute('nay1'),
                    nay2=self.get_custom_attribute('nay2'),
                    jtf=self.get_custom_attribute('max_U'),
                    itbl=self.get_custom_attribute('sfac'),
                    isfz=self.get_custom_attribute('kappa_set'),
                    lmax=self.get_custom_attribute('lmax'),
                    isym=self.get_custom_attribute('isym'),
                    ichcon=self.get_custom_attribute('ichcon'),
                    x=self.get_frac()[0], y=self.get_frac()[1],
                    z=self.get_frac()[2], o=self.get_occupancy())
        string += ' {:9.6f} {:9.6f} {:9.6f} {:9.6f} {:9.6f} {:9.6f}'.format(*self.get_adp_frac())
        for i, mult in enumerate(self.get_custom_attribute('multipoles')):
            if i % 10 == 0:
                string += '\n '
            string += '{:7.4f} '.format(mult)
        string += '\n'

        return string

    def __sub__(self, atom):
        x, y, z = self.frac
        try:
            xx, yy, zz = atom.get_frac() + 99.5
        except TypeError:
            xx, yy, zz = array(atom.get_frac()) + 99.5
        dx = (xx - x) % 1 - 0.5
        dy = (yy - y) % 1 - 0.5
        dz = (zz - z) % 1 - 0.5
        a, b, c, alpha, beta, gamma = self.get_cell()
        alpha = alpha/180*pi
        beta = beta/180*pi
        gamma = gamma/180*pi
        dd = a ** 2 * dx ** 2 + b ** 2 * dy ** 2 + c ** 2 * dz ** 2 + 2 * b * c * cos(
            alpha) * dy * dz + 2 * a * c * cos(beta) * dx * dz + 2 * a * b * cos(gamma) * dx * dy
        return dd ** .5


class XDIOP(IOP):

    def __init__(self, *args, **kwargs):
        super(XDIOP, self).__init__(*args, **kwargs)
        self.key_dict = None
        self.master_body = None
        self.cell = None
        self.current_atom_record = None
        self.master_file_name = None
        self.atoms = None
        self.body = None
        self.adp_cart = None
        self.adp_error_cart = None
        self.adp_frac = None
        self.adp_error_frac = None
        self.names = None
        self.cart = None
        self.frac = None
        self.element = None
        self.T = None
        self.multipoles = None
        self.chemcons = None
        self.supportsSym = True
        self.centric = False

    def parse(self):
        self.cell = None
        # self.master_file_name = self.filename.replace('.res', '.mas')
        self.master_file_name = self.filename[:-3] + 'mas'
        self.parse_master_file()
        self.atoms = OrderedDict()
        self.body = []
        self.current_atom_record = []
        self.names = []
        self.adp_frac = {}
        self.adp_error_frac = {}
        self.adp_cart = {}
        self.adp_error_cart = {}
        self.frac = {}
        self.cart = {}
        self.element = {}
        self.multipoles = {}
        self.T = None
        lineCounter = -1
        recLength = None
        stop = False
        for raw_line in self.content:

            line = raw_line[:-1].split()
            if not line:
                continue
            if stop:
                self.body.append(raw_line)
                continue

            isAtomStart = True if '(' in line[0] else False
            if lineCounter < 0 and isAtomStart and not recLength:
                lineCounter = 0
            elif isAtomStart and not recLength:
                recLength = lineCounter
                lineCounter -=1
            if not lineCounter < 0:
                lineCounter += 1
                if lineCounter == recLength:
                    # print' PARSE NOW'
                    # print '---------------------------', raw_line
                    self.parse_atom_record()
                    self.current_atom_record = line
                    lineCounter = 0
                    if not isAtomStart:
                        stop = True
                        self.body.append(raw_line)
                        continue
                else:
                    self.current_atom_record += line
            else:
                self.body.append(raw_line)
            continue

        for name, atom in self.atoms.items():
            self.cart[name] = atom.get_cart()
            self.frac[name] = atom.get_frac()
            self.adp_cart[name] = atom.get_adp_cart()
            self.element[name] = atom.get_element()
            self.multipoles[name] = atom.get_custom_attribute('multipoles')
            self.names.append(name)

    def parse_atom_record(self):
        rec = self.current_atom_record
        atom = XDAtom()
        atom.set_name(rec[0])
        atom.set_element(rec[0][:rec[0].index('(')])
        atom.set_custom_attribute('icor1', rec[1])
        atom.set_custom_attribute('icor2', rec[2])
        atom.set_custom_attribute('nax', rec[3])
        atom.set_custom_attribute('nay1', rec[4])
        atom.set_custom_attribute('nay2', rec[5])

        atom.set_custom_attribute('max_U', rec[6])
        atom.set_custom_attribute('sfac', rec[7])
        atom.set_custom_attribute('kappa_set', rec[8])
        atom.set_custom_attribute('lmax', rec[9])
        atom.set_custom_attribute('isym', rec[10])
        atom.set_custom_attribute('ichcon', rec[11])

        atom.set_frac(array([float(i) for i in rec[12:15]]))
        atom.set_occupancy(float(rec[15]))

        atom.set_adp_frac([float(i) for i in rec[16:22]])
        atom.set_custom_attribute('multipoles', [float(i) for i in rec[22:]])
        self.atoms[rec[0]] = atom
        atom.set_cell(self.cell)
        self.body.append(atom)

    def parse_master_file(self):
        self.key_dict = {}
        self.master_body = []
        keyswitch = False
        atomsswitch = False
        self.chemcons = {}
        try:
            filepointer = open(self.master_file_name)
        except IOError:
            apd_exit(3, '\n\nERROR: Cannot find file {}'.format(self.master_file_name))
        for line in filepointer.readlines():
            # print(line)
            if line.startswith('SYMM'):
                self.symmetry.append(
                    ' '.join([i for i in line.rstrip().split(' ') if len(i) > 0][1:]).split(','))
                continue
            if line.startswith('LATT'):
                line = [i for i in line[:-1].split() if i]
                self.centric = True if line[1].upper() == 'C' else False
                continue
            if line.lstrip(' ').startswith('!'):
                continue
            if 'END SCAT' in line:
                atomsswitch = True
            if line.startswith('DUM'):
                atomsswitch = False
            if atomsswitch:
                sline = [item for item in line[:-1].split(' ') if item]
                try:
                    self.chemcons[sline[0]] = sline[12]
                except IndexError:
                    pass
            if line.startswith('CELL') and self.cell is None:
                self.cell = list([float(i) for i in line.split(' ')[1:] if i])
            elif line.startswith('END KEY'):
                keyswitch = False
            elif line.startswith('KEY'):
                keyswitch = True
            if keyswitch:
                sline = [i.rstrip('\n') for i in line.split(' ') if i]
                if '(' in sline[0] and ')' in sline[0]:
                    key = sline[0]
                    if key in self.chemcons.keys():
                        self.key_dict[key] = self.key_dict[self.chemcons[key]]
                        self.master_body.append(key+'\n')
                        continue
                    atom_key_dict = KEY(key)
                    atom_key_dict['xyz'] = sline[1]
                    try:
                        atom_key_dict['U2'] = sline[2]
                        atom_key_dict['U3'] = sline[3]
                        atom_key_dict['U4'] = sline[4]
                    except IndexError:
                        atom_key_dict['U2'] = 0
                        atom_key_dict['U3'] = 0
                        atom_key_dict['U4'] = 0
                    try:
                        atom_key_dict['Mono'] = sline[5]
                        atom_key_dict['Dipo'] = sline[6]
                        atom_key_dict['Quato'] = sline[7]
                        atom_key_dict['Okto'] = sline[8]
                        atom_key_dict['Hexa'] = sline[9]
                    except KeyError:
                        pass
                    except IndexError:
                        atom_key_dict['Mono'] = 0
                        atom_key_dict['Dipo'] = 0
                        atom_key_dict['Quato'] = 0
                        atom_key_dict['Okto'] = 0
                        atom_key_dict['Hexa'] = 0
                    self.key_dict[key] = atom_key_dict
                    self.master_body.append(atom_key_dict)
                else:
                    self.master_body.append(line)
            else:
                self.master_body.append(line)
        filepointer.close()

    def set_U2(self, name, value):
        try:
            self.key_dict[name].set_U2(value)
        except KeyError:
            pass

    def set_adp_cart(self, name, value):
        self.atoms[name].set_adp_cart(value)
        if self.atoms[name].get_element() == 'H':
            self.set_U2(name, '000000')
            self.atoms[name].set_custom_attribute('max_U', '2')
        self.adp_cart[name] = self.atoms[name].get_adp_cart()

    def set_multipoles(self, name, value):
        self.atoms[name].set_custom_attribute('multipoles', value)
        self.multipoles[name] = self.atoms[name].get_custom_attribute('multipoles')

    def set_cart(self, name, value):
        self.atoms[name].set_cart(value)
        self.cart[name] = self.atoms[name].get_cart()

    def get_id(self):
        return 'XD'

    def get_symmetry(self):
        return self.symmetry

    def grow(self):
        from lauescript.cryst.symmetry import SymmetryElement
        symms = []
        for symm in self.symmetry:
            symmEl = SymmetryElement(symm)
            symms.append(symmEl)
        if self.centric:
            symms.append(SymmetryElement(['-X', '-Y', '-Z']))
            for symm in self.symmetry:
                symm = SymmetryElement(symm, centric=True)
                symms.append(symm)
        newatoms = []
        asymunits = {str(symm): [] for symm in symms}
        for atom in self.atoms.values():
            for symm in symms:
                newCart = symm.apply2cart(atom.get_cart(), self.get_cell())
                newName = atom.get_name() + '_{}'.format(symm.ID)
                newADP = symm.apply2cart_ADP(atom.get_adp_cart(), self.get_cell())
                newAtom = XDAtom()
                newAtom.set_name(newName)
                newAtom.set_frac(cart2frac(newCart, self.get_cell()))
                newAtom.set_adp_frac(cart2frac_ADP(newADP, self.get_cell()))
                newAtom.set_cell(self.get_cell())

                newAtom.set_element(atom.get_element())

                newAtom.set_custom_attribute('icor1',atom.get_custom_attribute('icor1'))
                newAtom.set_custom_attribute('icor2', atom.get_custom_attribute('icor2'))
                newAtom.set_custom_attribute('nax', atom.get_custom_attribute('nax'))
                newAtom.set_custom_attribute('nay1', atom.get_custom_attribute('nay1'))
                newAtom.set_custom_attribute('nay2',atom.get_custom_attribute('nay2'))

                newAtom.set_custom_attribute('max_U',atom.get_custom_attribute('max_U'))
                newAtom.set_custom_attribute('sfac', atom.get_custom_attribute('sfac'))
                newAtom.set_custom_attribute('kappa_set', atom.get_custom_attribute('kappa_set'))
                newAtom.set_custom_attribute('lmax', atom.get_custom_attribute('lmax'))
                newAtom.set_custom_attribute('isym', atom.get_custom_attribute('isym'))
                newAtom.set_custom_attribute('ichcon', atom.get_custom_attribute('ichcon'))

                newAtom.set_custom_attribute('multipoles', atom.get_custom_attribute('multipoles'))

                newAtom.set_occupancy(atom.get_occupancy())


                newatoms.append(newAtom)

        live = True
        while live:
            live = False
            addedAtoms = []
            for atom in newatoms:

                for atom2 in list(self.atoms.values()) + addedAtoms:
                    d = atom-atom2
                    if is_bound2(d, atom.get_element(), atom2.get_element()):
                        live = True
                        # print(atom.get_name(), 'is bound to', atom2.get_name())
                        addedAtoms.append(atom)
                        self.atoms[atom.get_name()] = atom
                        self.names.append(atom.get_name())
                        self.cart[atom.get_name()] = atom.get_cart()
                        self.frac[atom.get_name()] = atom.get_frac()
                        self.element[atom.get_name()] = atom.get_element()
                        self.adp_cart[atom.get_name()] = atom.get_adp_cart()
                        self.adp_frac[atom.get_name()] = atom.get_adp_frac()
                        break
            for atom in addedAtoms:
                newatoms.remove(atom)
        # for k,v in self.atoms.items():
        #     print(v)


    def __str__(self):
        self.write_master_file()
        string = ''
        for line in self.body:
            string += str(line)
        string += '\n'
        return string

    def write_master_file(self):
        filepointer = open(self.master_file_name + '2', 'w')
        for line in self.master_body:
            filepointer.write(str(line))

    def export_shelxl(self, temp = 100, waveLength=0.71073, title='XDImport',
                      disps=True, fixXYZ=False, globalU=False, scale = 1.0,
                      hklf=4):
        from lauescript.cryst.tables import atomtable
        if fixXYZ:
            fixXYZ = 10
        else:
            fixXYZ = 0
        sfacs = set([atom.get_element() for atom in self.atoms.values()])
        try:
            sfacs.remove('H')
        except KeyError:
            pass
        sfacList = sorted(list(sfacs), key=lambda sfac: atomtable[sfac]) + ['H']
        sfacs = {x: i+1 for i, x in enumerate(sfacList)}
        content = 'TITL {}\nCELL {} {}\nZERR 1 {}'.format(title, waveLength, ' '.join(['{:7.4f}'.format(x) for x in self.cell]), ' '.join(['{:7.4f}'.format(d/100.) for d in self.cell]))
        content += '\nLATT 1'
        content += '\nSFAC {}'.format(' '.join(sfacList))
        if not disps:
            for sfa in sfacList:
                content += '\nDISP ${} 0.000 0.000'.format(sfa)
        content += '\nUNIT {}'.format(' '.join([str(sfacs[x]) for x in sfacList]))
        content += '\nL.S. 10'
        content += '\nLIST 6'
        content += '\nTEMP {}'.format(temp-273)
        content += '\nPLAN 20'
        content += '\nWGHT 0.0'
        content += '\nFVAR {:.2f}'.format(scale)
        if globalU:
            content += ' {}'.format(globalU)
        atomList = sorted(self.atoms.values(), reverse=True, key= lambda atom: atom.get_name())
        for atom in atomList:
            content += '\n{:<5} {} {} 11.0'.format(atom.get_name().replace('(', '').replace(')', ''),
                                                             sfacs[atom.get_element()],
                                                             ' '.join(['{:9.5f}'.format(x+fixXYZ) for x in atom.get_frac()]))
            if not globalU:
                content += ' {}\n {}'.format(' '.join(['{:9.5f}'.format(x) for x in atom.get_adp_frac()[:2]]),
                                             ' '.join(['{:9.5f}'.format(x) for x in atom.get_adp_frac()[2:]]))
            else:
                content += ' 21.0'
        content += '\nHKLF {}\nEND'.format(hklf)
        return content


if __name__ == '__main__':
    test = XDIOP('xd.res')
    test.read()