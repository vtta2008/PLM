from __future__ import print_function
"""
Created on Nov 1, 2013

@author: jens

This module contains definitions for the data classes representing the
data structure of the APD-Toolkit. These classes serve as containers
for molecules and atoms and provide the interface for manipulating
most of their properties.
"""

import operator
from lauescript.types.molecule import MOLECULE, DABA_MOLECULE
from lauescript.cryst.match import match_point_clouds, get_transform
from lauescript.cryst.geom import is_bound
from lauescript.cryst.sort import SortAtom
from lauescript.core.core import apd_exit
from sys import platform


class DATA(dict):
    """
    This class provides a convinient interface for all data handled
    by the APD-Toolkit
    """
    def __init__(self, temperature=None, daba=True, *args, **kwargs):
        """
        The DATA class should be initialized without any arguments.
        """
        super(DATA, self).__init__(*args, **kwargs)
        self.daba = daba
        self.temperature = temperature
        self.argv = None
        self.config = None

    def set_argv(self, string):
        """
        Sets the currently used cmd line argument string.
        This way the 'active' arguments can be changed at
        runtime.
        :param string: String representing a cmd line input.
        :return: None
        """
        try:
            self.argv = string.split(' ')
        except AttributeError:
            if string:
                self.argv = string
            else:
                self.argv = []

    def get_argv(self):
        """
        :return: A list of strings representing a cmd line input.
        """
        return self.argv

    def register_config(self, config):
        """
        Registers a configuration file.
        :param config: A python module.
        :return: None
        """
        self.config = config

    def give_temperature(self, value):
        """
        Sets the current temperature.
        :param value: Float representing the measurement temperature.
        :return: None
        """
        self.temperature = value

    def give_molecule(self, name, cell=None):
        """
        Adds a molecule representing not a model compound to the DATA
        instance.

        :param name: String representing the molecule name.
        :param cell: List with six floats: [a, b, c, alpha, beta, gamma]
        """
        self[name] = MOLECULE(name=name, cell=cell)

    def register_molecule(self, molecule, name):
        """
        Registers an existing MOLECULE instance.

        :param molecule: MOLECULE instance.
        :param name: String representing the instance's name.
        :return: None
        """
        self[name] = molecule

    def add_molecule(self, name, cell=None):
        """
        Adds a molecule representing not a model compound to the DATA
        instance.

        DEPRECATED
        :param name: String representing the molecule name.
        :param cell: List with six floats: [a, b, c, alpha, beta, gamma]
        """
        print('DATA.add_molecule is deprecated. Please use DATA.give_molecule')
        self[name] = MOLECULE(name=name, cell=cell)

    def give_daba_molecule(self, name, cell=None, properties=None):
        """
        Adds a molecule representing a model compound the DATA instance.

        :param name: String representing the molecule's name
        :param cell: List of six floats representing the unit cell.
        :param properties: List representing the quantum chemically
        determined properties of the molecule.
        """
        self[name] = DABA_MOLECULE(name, cell=cell, properties=properties)

    def update(self, match='inv', *args, **kwargs):
        """
        Main interface function for transfering ADP from model
        compounds the the 'exp' molecule.

        All necessary funtions and methods will be called by
        this method.

        :param match: String specifying how relative orientations
        should be determined. 'inv' uses the invstring2 module to
        determine orientations. 'geom' uses iterative shape
        recognition.
        :param args: ...
        :param kwargs: ...
        """
        if match == 'inv':
            self._link()
        self._get_atoms()
        self._get_distances()
        self._find_molecules()

        if match == 'inv':
            # self._get_code_atom_links()
            self._get_prochirality()
            # ===================================================================
            # self._get_orientations()
            #===================================================================
            self._transfer_adp()
        elif match == 'geom':
            self._match_molecules()
        elif match == 'trust':
            self._trust_molecules()
        else:
            apd_exit(1, 'Unknown ADP transfer method. Use inv/geom/trust.')
        self._update_H_ADP()

    def _find_molecules(self):
        self.number_of_molecules = self['exp'].identify_molecules()

    def _match_molecules(self):
        cloud1 = self['exp'].coords()
        cloud2 = self['micro'].coords()
        hitlist, transformation = match_point_clouds(cloud1, cloud2, threshold=.2)
        for i, atom in enumerate(self['exp'].atoms):
            # print atom.element, self['micro'].atoms[hitlist[i]].element,hitlist[i],self['micro'].atoms[hitlist[i]].name
            atom.transfer_matched_ADP(self['micro'].atoms[hitlist[i]], transformation)

    def _trust_molecules(self):
        cloud1 = self['exp'].coords()[:3]
        cloud2 = self['micro'].coords()[:3]
        transformation = get_transform(cloud1, cloud2, matrix=True)
        for i, atom in enumerate(self['exp'].atoms):
            atom.transfer_matched_ADP(self['micro'].atoms[i], transformation)

    def _update_H_ADP(self):
        """
        Constrains the ADP values for all atoms in the 'exp'
        molecule depending on the values of the APD of the
        bonding partner.
        """
        # return
        for atom in self.invarioms:
            if (not 'cart_meas' in atom.adp.keys() or len(atom.adp['cart_meas']) == 1) and atom.molecule.name == 'exp':
                atom.update_H_ADP()

    # def _get_code_atom_links(self):
    #     """
    #     Sets the code_atom_link dictionary for every atom and
    #     creates for every atom in self.invarioms a molecule
    #     fragment containing the atoms specified in the invariom
    #     string.
    #     """
    #     return
    #     for molecule in self.values():
    #         if not molecule.name == 'exp':
    #             molecule.get_code_atom_links()

    def _get_prochirality(self):
        """
        Determines wether an atom is prochiral and determines the
        atom's side if necessary.
        """
        for atom in self.invarioms:
            atom.get_prochirality()
            atom.invariom.get_prochirality()

    def _transfer_adp(self):
        """
        Transfers the ADP from the modelcompounds to the 'exp' molecule.
        """
        toleratedAtoms = []
        for atom in self['exp'].atoms:
            tolerated = atom.transfer_adp()
            if tolerated:
                toleratedAtoms.append(tolerated)
        for atom in toleratedAtoms:
            atom.averageADP()

    def _get_orientations(self):
        """
        Determines the orientation vectors of all atoms in self.invarioms.
        """
        for atom in self.invarioms:
            atom.get_orientation()

    def _link(self):
        """
        Links all atoms in 'exp' to their invarioms.
        """
        for exp_atom in self['exp'].atoms:
            if exp_atom.isTolerated():
                continue
            for model_atom in self[exp_atom.model_compound.name].atoms:
                inv = exp_atom.get_active_invariom()
                if inv in model_atom.invarioms.keys():
                    exp_atom.set_invariom_atom(model_atom)
                    model_atom.set_invariom_atom(exp_atom)
                    exp_atom.set_active_invariom(inv)
                    model_atom.set_active_invariom(inv)
                    break

    def _get_distances(self):
        """
        Calculates all intramolecular distances for all molecules
        and sortes the distances by length.
        """
        for molecule in self.values():
            molecule.get_distances()

        # for atom in self.atoms:
        #     atom.get_distances()



    def _get_atoms(self):
        """
        Generates the attributes self.atoms and self.invarioms
        containing lists of all atoms in all molecules and
        a list of all atoms that are part of the 'exp' molecules
        and their invarioms respectively.
        """
        atoms = []
        invarioms = []

        for molecule in self.values():
            atoms += [atom for atom in molecule.atoms]
            invarioms += [atom for atom in molecule.atoms if atom.invariom_name is not None]
        self.atoms = atoms
        self.invarioms = invarioms

    def iter_atoms(self, sort=False, key='exp'):
        """
        Iterator iterating over all atoms of the molecule with the
        name 'exp'.
        """
        if not sort:
            for atom in self[key].atoms:
                yield atom
        else:
            for atom in SortAtom.sort(self, molecule=self[key]):
                yield atom


    def iter_atom_pairs(self, bound=True, unique=True, sort=True):
        """
        Iterator iterating over all pairs of atoms in the molecule
        'exp'

        :param bound: Boolean specifying whether all atom pairs are
        returned or only those with chemical bonds between them.
        """
        blacklist = []
        for atom1 in self.iter_atoms(sort=sort):
            for atom2 in self.iter_atoms(sort=sort):
                if not atom1 == atom2:
                    if not bound or is_bound(atom1.cart, atom1.element, atom2.cart, atom2.element):
                        blackstring = '{}{}'.format(*sorted([atom1.name, atom2.name]))
                        if unique and not blackstring in blacklist:
                            yield atom1, atom2
                            blacklist.append(blackstring)
                        elif not unique:
                            yield atom1, atom2


class GENERATOR(DATA):
    """
    A class for generating the 'APD_DABA.txt' and 'APD_MAP.txt'
    files.
    The class is subclassed from the DATA class has some
    additional methods needed for the database generation.

    The main interface function '.update()' is overwritten
    to generate the database files instead of transfering
    ADP.
    """

    def __init__(self, Temperature, save, keep=None):
        """
        Every database file is valid for a given temperature
        used for the ADP calculation.
        """
        super(GENERATOR, self).__init__()
        self.Temp = Temperature
        self.save = save
        if not keep:
            keep = []
        keep += ['cart', 'adp[\'cart_int\']', 'map', 'keep']
        self.keep = keep
        self.printer = None
        self.errorlog = None

    def set_temperature(self, temperature):
        """
        Sets the temperature used for ADP calculation.
        :param temperature: Float representing a temperature in Kelvin.
        :return: none
        """
        self.Temp = temperature

    def update(self, errorlog, printer, path=None, parallel=True, *args, **kwargs):
        """
        Calls all the necessary functions and methods
        to create the 'APD_DABA.txt' and 'APD_MAP.txt' files
        in the working directory.

        :param errorlog: Filepointer of a file opened in 'w' mode that
        is used for logging error messages.
        :param printer: Instance of the APD_Printer class used for printing
        output.
        :param path: String representing the path to the database directory.
        :param parallel: Boolean specifying whether the multiprocessing
        module will be used to calculate ADPs on multiple CPUs. This boolean
        will be forced to be False on windows platforms.
        :param args: ...
        :param kwargs: ...
        """
        if 'win' in platform:
            parallel = False

        self.printer = printer
        self.errorlog = errorlog
        self._get_invariom_list()
        self._get_criteria()
        self._sort_compounds()
        self._map_invarioms()
        self._get_distances()
        for Temp in self.Temp:
            if parallel:
                self._update_adp_calculation_parallel(Temp)
            else:
                self._update_adp_calculation(Temp)
            self._update_database_file(Temp, path)
        self._update_database_map(path)
        if self.save:
            self.serialize()

    def serialize(self):
        """
        Uses the cPickle module to serialize the GENERATOR
        instance.
        """
        self.printer('\n    ...Serializing database content...\n')
        self.release()

        # self.strip()
        try:
            import cPickle
        except ImportError:
            import pickle as cPickle

        f = open('database.pkl', 'wb')
        cPickle.dump(self, f, protocol=0)

    def strip(self):
        """
        Strips the GENERATOR instance of all unnecessary data
        to minimize the size of the serialized file.
        all attributes specified in the 'self.keep' list will
        be preserved.
        """
        types = [type(self.strip),
                 type(self.values),
                 type(self.__ne__),
                 type(self.__class__)]

        for attr in dir(self):
            if not type(getattr(self, attr)) in types:
                if any(i in attr for i in self.keep) or attr[0:2] == '__':
                    continue
                else:
                    x = getattr(self, attr)
                    del x
        for molecule in self.values():
            molecule.strip_molecule(self.keep)
            exit()

    def _get_invariom_list(self):
        """
        Generates a unique list of all invariom names in all
        model compounds.
        """
        self.invariom_list = []
        for molecule in self.values():
            for atom in molecule.atoms:
                for invariom in atom.invarioms:
                    if not invariom in self.invariom_list:
                        self.invariom_list.append(invariom)

    def _map_invarioms(self):
        """
        Maps the invariom names to the 'smallest' model compound
        containing that invariom.
        """
        self.map = {}
        for invariom in self.invariom_list:
            kill = False
            for molecule in self.sorted_molecules:
                for atom in molecule.atoms:
                    if invariom in atom.invarioms:
                        self.map[invariom] = molecule.name
                        kill = True
                        break
                if kill:
                    break

    def release(self):
        """
        Closes the error log filepointer and removes the reference.
        This step is necessary for pickling the GENERATOR instance.
        """
        self.errorlog.close()
        del self.errorlog
        del self.printer

    def _sort_compounds(self):
        """
        Creates a sorted list of all molecules. The sorting criterion
        is the molecule.criterion attribute defining the 'size' of
        an modelcompound.
        """
        self.sorted_molecules = sorted(self.values(), key=operator.attrgetter('criterion'))

    def _get_criteria(self):
        """
        Calls the necessary methods for calculating the 'size' of every
        molecule.
        """
        for molecule in self.values():
            molecule.get_criterion()

    def _update_adp_calculation(self, Temp):
        """
        Recalculates the ADP from theoretical data.
        """
        from sys import stdout

        self.printer('\n  ...calculating ADPs...\n')

        import time

        start = time.time()

        daba_counter = 0.
        max_counter = float(len(self.keys()))
        for molecule in self.keys():
            daba_counter += 1.

            pstate = daba_counter / max_counter
            pstate = int(58 * pstate)
            bar = '[' + pstate * '#' + (58 - pstate) * '-' + ']'
            print('      |  {}'.format(bar), end='\r')
            stdout.flush()

            try:
                self[molecule].get_adp(Temp)

            except KeyError:
                self.errorlog.write('Error: No ADP calculated by atom.get_adp() for {}.'.format(molecule))
        end = time.time()
        self.printer('\n\n  Time used for ADP calculation: {:5.3f} sec on {} CPUs'.format(end - start, 1))

    def _update_adp_calculation_parallel(self, Temp):
        """
        Multi CPU implementation of the ADP calculation.

        For some mysterious reason this code does not work
        on Windows machines. Don't ask me why. The traceback
        looks like ancient chinese to me.
        """
        import multiprocessing

        import time

        start2 = time.time()

        class Worker(multiprocessing.Process):
            """
            Worker class used for calculating ADPs.
            """
            def __init__(self, data_pointer, Tempe, message_queue, job_queue, ID):
                super(Worker, self).__init__()
                self.data_pointer = data_pointer
                self.Temp = Tempe
                self.counter = 0
                self.message_q = message_queue
                self.job_q = job_queue
                self.id = ID

            def run(self):
                """
                Starting the ADP calculation.
                """
                while True:
                    if self.job_q.empty():
                        self.message_q.put(False)
                        return
                    try:
                        smolecule = self.job_q.get()
                        self.data_pointer[smolecule].get_adp(self.Temp)
                    except IndexError:
                        self.message_q.put((smolecule, None))
                    try:
                        self.message_q.put((smolecule, [j.adp['cart_int'] for j in self.data_pointer[smolecule].atoms]))
                    except KeyError:
                        # =======================================================
                        # self.message_q.put((molecule,[0 for i in self.data_pointer[molecule].atoms]))
                        #=======================================================
                        pass

        job_q = multiprocessing.Queue()
        n = 4
        # i = 0
        molecules = self.keys()
        max_len = len(molecules)
        for molecule in molecules:
            job_q.put(molecule)
        jobs = []
        message_q = multiprocessing.Queue()
        for i in range(n):
            p = Worker(self, Temp, message_q, job_q, i)
            jobs.append(p)
            p.start()

        counter = 0
        state = 0

        self.printer('\n  ...calculating ADPs at {:.1f} K...\n'.format(Temp))
        while True:
            message = message_q.get()
            if message:
                state += 1
                pstate = float(state) / max_len
                pstate = int(58 * pstate)
                bar = '[' + pstate * '#' + (58 - pstate) * '-' + ']'
                self.printer.noreturn('  {}'.format(bar))
                if message[1] is not None:
                    self[message[0]].give_adp(message[1])
                else:
                    self.errorlog.write('Error: No ADP calculated by atom.get_adp() for {}.'.format(message[0]))
            else:
                counter += 1

            if counter == n:
                print
                break

        for job in jobs:
            job.join()

        end2 = time.time()
        self.printer('\n  Time used for ADP calculation: {:5.3f} sec on {} CPUs'.format(end2 - start2, n))
        return

    def _update_database_file(self, Temp, path):
        """
        Writes the 'APD_DABA.txt' file.
        """
        from datetime import datetime

        if path:
            filename = path + '/APD_DABA_{:.1f}_.txt'.format(Temp)
        else:
            filename = 'APD_DABA_{:.1f}_.txt'.format(Temp)
        self.printer('\n  ...Writing database file: {}...\n'.format(filename))
        filepointer = open(filename, 'w')

        filepointer.write('# Database file for the APD-Toolkit\n# Generated: {}\n'.format(datetime.now()))
        for mname, molecule in self.items():
            if len(mname) > 1:
                filepointer.write('N {}\n'.format(mname))
                for atom in molecule.atoms:
                    filepointer.write('E {}\n'.format(atom.element))

                    for invariom_name, orientation in atom.invarioms.items():
                        filepointer.write('I {} '.format(invariom_name))
                        filepointer.write('{:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}\n'.format(
                            *(orientation[0].tolist() + orientation[1].tolist())))
                    filepointer.write('C {:.3f} {:.3f} {:.3f}\n'.format(*atom.cart))
                    try:
                        filepointer.write('A {:.2e} {:.2e} {:.2e} {:.2e} {:.2e} {:.2e}\n'.format(*atom.adp['cart_int']))
                    except KeyError:
                        filepointer.write('A {:.2e} {:.2e} {:.2e} {:.2e} {:.2e} {:.2e}\n'.format(0, 0, 0, 0, 0, 0))
        filepointer.close()

    def _update_database_map(self, path):
        """
        Writes the 'APD_MAP.txt' file.
        """
        if path:
            filename = path + '/APD_MAP.txt'
        else:
            filename = 'APD_MAP.txt'
        filepointer = open(filename, 'w')
        for invariom, molecule in self.map.items():
            filepointer.write(invariom + ':' + molecule + '\n')
        filepointer.close()
