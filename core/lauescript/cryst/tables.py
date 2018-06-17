"""
Created on 21.03.2014

@author: Jens Luebben

Module containing all sorts of tables representing atom parameters.
"""

class Table(object):
    data = None

    def __getitem__(self, item):
        item = item.rstrip('-+')
        item = item.rstrip('0123456789')
        item = item.capitalize()
        try:
            return self.__class__.data[item]
        except KeyError:
            raise KeyError('Unknown Element {}.'.format(item))

class Atomtable(Table):
    data = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
                 'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
                 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22,
                 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29,
                 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36,
            'D': 1}
atomtable = Atomtable()


class ElementOfNumber(Table):
    data = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8,
                 'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15,
                 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22,
                 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29,
                 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36,
            'D': 1}
    data = dict([[str(v), k] for k, v in data.items()])

    def __getitem__(self, item):
        item = item.lstrip('0')
        item = item.rstrip('-+')
        item = item.capitalize()
        return self.data[item]

elementofnumber = ElementOfNumber()

class Atomicmass(Table):
    data = {'H': 1., 'He': 4., 'Li': 6.9, 'Be': 9., 'B': 10.8, 'C': 12., 'N': 14., 'O': 16.,
                  'F': 18, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 28, 'P': 15,
                  'S': 16, 'Cl': 35, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22,
                  'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 59, 'Ni': 28, 'Cu': 29,
                  'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Pd': 106,
            'D': 1}

    def __getitem__(self, item):
        item = item.rstrip('-+')
        item = item.capitalize()
        return super(Atomicmass, self).__getitem__(item)
atomicmass = Atomicmass()

class Vdw_radius(Table):
    data = {'H': .37, 'He': .0, 'Li': 1.23, 'Be': .90, 'B': .80, 'C': .77,
                        'N': .74, 'O': .71, 'F': .72, 'Ne': 0., 'Na': 1.54, 'Mg': 1.36,
                        'Al': 1.18, 'Si': 1.11, 'P': 1.06, 'S': 1.02, 'Cl': .99, 'Ar': 0.,
                        'K': 2.03, 'Ca': 1.74, 'Sc': 1.44, 'Ti': 1.32, 'V': 1.22,
                        'Cr': 1.18, 'Mn': 1.17, 'Fe': 1.17, 'Co': 1.16, 'Ni': 1.15,
                        'Cu': 1.17, 'Zn': 1.25, 'Ga': 1.26, 'Ge': 1.22, 'As': 1.20,
                        'Se': 1.16, 'Br': 1.14, 'Kr': 0.,
                        'Rb': 2.18,
            'D': .37}  # , 191, 162, 145, 134, 130, 127, 125, 125, 128, 134, 148, 144, 141, 140, 136, 133, 0, 235, 198, 169, 165, 165, 164, 164, 162, 185, 161, 159, 159, 157, 157, 156, 170, 156, 144, 134, 130, 128, 126, 127, 130, 134, 149, 148, 147, 146, 146, 145, 0, 0, 0, 188, 165, 161, 142, 130, 151, 182, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
    def __getitem__(self, item):
        item = item.rstrip('-+')
        item = item.capitalize()
        return super(Vdw_radius, self).__getitem__(item)

vdw_radius = Vdw_radius()


class Covalence_radius(Table):
    data = {'H': .37, 'He': .0, 'Li': 1.23, 'Be': .90, 'B': .80, 'C': .77,
                        'N': .74, 'O': .71, 'F': .72, 'Ne': 0., 'Na': 1.54, 'Mg': 1.36,
                        'Al': 1.18, 'Si': 1.11, 'P': 1.06, 'S': 1.02, 'Cl': .99, 'Ar': 0.,
                        'K': 2.03, 'Ca': 1.74, 'Sc': 1.44, 'Ti': 1.32, 'V': 1.22,
                        'Cr': 1.18, 'Mn': 1.17, 'Fe': 1.17, 'Co': 1.16, 'Ni': 1.15,
                        'Cu': 1.17, 'Zn': 1.25, 'Ga': 1.26, 'Ge': 1.22, 'As': 1.20,
                        'Se': 1.16, 'Br': 1.14, 'Kr': 0.,
                        'Rb': 2.18, 'Pd': 1.39,
            'D': .37}  # , 191, 162, 145, 134, 130, 127, 125, 125, 128, 134, 148, 144, 141, 140, 136, 133, 0, 235, 198, 169, 165, 165, 164, 164, 162, 185, 161, 159, 159, 157, 157, 156, 170, 156, 144, 134, 130, 128, 126, 127, 130, 134, 149, 148, 147, 146, 146, 145, 0, 0, 0, 188, 165, 161, 142, 130, 151, 182, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
    def __getitem__(self, item):
        item = item.rstrip('-+')
        item = item.capitalize()
        return super(Covalence_radius, self).__getitem__(item)
covalence_radius = Covalence_radius()


class Electro_negativity(Table):
    """
    Taken from Invariomtool source.
    """
    data = {'H': 2.20, 'He': 5.50, 'Li': .97, 'Be': 1.47, 'B': 2.01, 'C': 2.50,
                   'N': 3.07, 'O': 3.50, 'F': 4.40, 'Ne': 4.80, 'Na': 1.01, 'Mg': 1.23,
                   'Al': 1.47, 'Si': 1.74, 'P': 2.06, 'S': 2.44, 'Cl': 2.83, 'Ar': 3.20,
                   'K': .91, 'Ca': 1.04, 'Sc': 1.20, 'Ti': 1.32, 'V': 1.45,
                   'Cr': 1.56, 'Mn': 1.60, 'Fe': 1.64, 'Co': 1.70, 'Ni': 1.75,
                   'Cu': 1.75, 'Zn': 1.66, 'Ga': 1.82, 'Ge': 2.02, 'As': 2.20,
                   'Se': 2.48, 'Br': 2.74, 'Kr': 2.90,
                   'Rb': .89,
            'D': 2.20}  # , 99, 111, 122, 123, 130, 136, 142, 145, 130, 142, 146, 149, 172, 182, 201, 221, 240, 86, 97, 108, 108, 107, 107, 107, 107, 110, 111, 110, 110, 110, 111, 111, 106, 114, 123, 133, 140, 146, 152, 155, 142, 142, 144, 144, 155, 167 }
    def __getitem__(self, item):
        # print 'x'
        item = item.rstrip('-+')
        item = item.capitalize()
        return super(Electro_negativity, self).__getitem__(item)
electro_negativity = Electro_negativity()

class Electron_number(Table):
    data = {'H': '001', 'He': '002', 'Li': '003', 'Be': '004', 'B': '005', 'C': '006', 'N': '007', 'O': '008',
                       'F': '009', 'Ne': '010', 'Na': '011', 'Mg': '012', 'Al': '013', 'Si': '014', 'P': '015',
                       'S': '016', 'Cl': '017', 'Ar': '018', 'K': '019', 'Ca': '020', 'Sc': '021', 'Ti': '022',
                       'V': '023', 'Cr': '024', 'Mn': '025', 'Fe': '026', 'Co': '027', 'Ni': '028', 'Cu': '029',
                       'Zn': '030', 'Ga': '031', 'Ge': '032', 'As': '033', 'Se': '034', 'Br': '035', 'Kr': '036',
                       'Pd': '046',
            'D': '001'}
    def __getitem__(self, item):
        item = item.rstrip('-+')
        item = item.capitalize()
        return super(Electron_number, self).__getitem__(item)
electron_number = Electron_number()


# class Proton_number(Table):
#     data = {'H': '001', 'He': '002', 'Li': '003', 'Be': '004', 'B': '005', 'C': '006', 'N': '007', 'O': '008',
#             'F': '009', 'Ne': '010', 'Na': '011', 'Mg': '012', 'Al': '013', 'Si': '014', 'P': '015',
#             'S': '016', 'Cl': '017', 'Ar': '018', 'K': '019', 'Ca': '020', 'Sc': '021', 'Ti': '022',
#             'V': '023', 'Cr': '024', 'Mn': '025', 'Fe': '026', 'Co': '027', 'Ni': '028', 'Cu': '029',
#             'Zn': '030', 'Ga': '031', 'Ge': '032', 'As': '033', 'Se': '034', 'Br': '035', 'Kr': '036'}
proton_number = Electron_number()

halogens = ['F', 'Cl', 'Br', 'I']

# number_electron = dict([[v, k] for k, v in electron_number.items()])

# priority = {'3': '5',
#             '2': '4',
#             '1.5': '3',
#             '6': '2',
#             '5': '1',
#             '1': '0'}
