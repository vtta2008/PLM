"""
Created on Mar 28, 2014

@author: jens
"""
from lauescript.cryst.transformations import frac2cart, \
    frac2cart_ADP, \
    cart2frac, \
    cart2frac_ADP
from lauescript.laueio.io import IOP
from lauescript.cryst.cif import CIF, value


class CIFIOP(IOP):
    def parse(self):
        self.names = []
        self.adp_frac = {}
        self.adp_error_frac = {}
        self.adp_cart = {}
        self.adp_error_cart = {}
        self.frac = {}
        self.cart = {}
        self.element = {}
        self.cif = CIF(self.filename)
        self.cell = self.cif.cell
        self.T = value(self.cif['_diffrn_ambient_temperature'])
        for atomname, values in self.cif.positions.items():

            self.names.append(atomname)

            self.frac[atomname] = values['frac']
            self.cart[atomname] = frac2cart(values['frac'], self.cell)
            self.element[atomname] = values['element']
            if atomname in self.cif.atoms.keys():
                self.adp_frac[atomname] = self.cif.atoms[atomname]['adp']
                self.adp_error_frac[atomname] = self.cif.atoms[atomname]['adp_error']
                self.adp_cart[atomname] = frac2cart_ADP(self.cif.atoms[atomname]['adp'], self.cell)
                try:
                    self.adp_error_cart[atomname] = frac2cart_ADP(self.cif.atoms[atomname]['adp_error'], self.cell)
                except TypeError:
                    self.adp_error_cart[atomname] = None
            else:
                self.adp_error_frac[atomname] = None
                self.adp_frac[atomname] = None
                self.adp_error_cart[atomname] = None
                self.adp_cart[atomname] = None


    def __str__(self):
        self.push()
        return str(self.cif)

    def push(self):
        new_x = []
        new_y = []
        new_z = []
        new_U = []
        new_11 = []
        new_22 = []
        new_33 = []
        new_12 = []
        new_13 = []
        new_23 = []
        for atom_name in self.cif['_atom_site_label']:
            frac = self.frac[atom_name]
            adp = self.adp_frac[atom_name]
            new_x.append('{:6.4f}'.format(frac[0]))
            new_y.append('{:6.4f}'.format(frac[1]))
            new_z.append('{:6.4f}'.format(frac[2]))
            if not adp is None:
                new_U.append('Uani')
            else:
                new_U.append('Uiso')
        self.cif['_atom_site_fract_x'] = new_x
        self.cif['_atom_site_fract_y'] = new_y
        self.cif['_atom_site_fract_z'] = new_z
        self.cif['_atom_site_adp_type'] = new_U
        for atom_name in self.cif['_atom_site_aniso_label']:
            adp = self.adp_frac[atom_name]

            new_11.append('{:6.4f}'.format(adp[0]))
            new_22.append('{:6.4f}'.format(adp[1]))
            new_33.append('{:6.4f}'.format(adp[2]))
            new_12.append('{:6.4f}'.format(adp[3]))
            new_13.append('{:6.4f}'.format(adp[4]))
            new_23.append('{:6.4f}'.format(adp[5]))
        self.cif['_atom_site_aniso_U_11'] = new_11
        self.cif['_atom_site_aniso_U_22'] = new_22
        self.cif['_atom_site_aniso_U_33'] = new_33
        self.cif['_atom_site_aniso_U_12'] = new_12
        self.cif['_atom_site_aniso_U_13'] = new_13
        self.cif['_atom_site_aniso_U_23'] = new_23

    def set_id(self):
        self.id = '{}{}'.format('CIF', IOP.instance)

    def set_cart(self, name, value):
        self.cart[name] = value
        frac = cart2frac(value, self.cell)
        self.frac[name] = frac
        # =======================================================================
        # self.cif.change_value(self,frac[0],'_atom_site_fract_x',name)
        # self.cif.change_value(self,frac[1],'_atom_site_fract_y',name)
        # self.cif.change_value(self,frac[2],'_atom_site_fract_z',name)
        #=======================================================================

    def set_adp_cart(self, name, value):
        self.adp_cart[name] = value
        frac = cart2frac_ADP(value, self.cell)
        self.adp_frac[name] = frac

        # =======================================================================
        # done=False
        # done=self.cif.change_value(self,frac[0],'_atom_site_aniso_U_11',name)
        # done=self.cif.change_value(self,frac[1],'_atom_site_aniso_U_22',name)
        # done=self.cif.change_value(self,frac[2],'_atom_site_aniso_U_33',name)
        # done=self.cif.change_value(self,frac[3],'_atom_site_aniso_U_12',name)
        # done=self.cif.change_value(self,frac[4],'_atom_site_aniso_U_13',name)
        # done=self.cif.change_value(self,frac[5],'_atom_site_aniso_U_23',name)
        # if not done:
        #     print 'ADP not found in CIF for {}.'.format(name)
        #=======================================================================


if __name__ == '__main__':
    test = CIFIOP('bats.cif')
    test.read()
    print(test.get_cart())
