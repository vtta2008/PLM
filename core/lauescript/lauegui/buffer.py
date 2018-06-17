# ===============================================================================
# import kivy
# kivy.require('1.0.6') # replace with your current kivy version !
#===============================================================================

from operator import attrgetter

from numpy import matrix, array, dot
from numpy.linalg import norm
from kivy.graphics import *

import lauescript.cryst.crystgeom as cg

#===============================================================================
# import argparse
# from sys import argv,exit
# from kivy.app import App
# from kivy.uix.button import Button
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.popup import Popup
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.filechooser import FileChooserListView
# from kivy.properties import StringProperty
# from kivy.event import EventDispatcher
#===============================================================================


Color_Table = {'C': (.3, .3, .3, 1),
               'H': (1, 1, 1, 1),
               'O': (1, 0, 0, 1),
               'N': (0, 0, 1, 1)}


class Factory(object):
    counter = 0

    def __init__(self, buffer):
        self.buffer = buffer

    def atom(self, coords, element, label):
        self.increment()
        if not label:
            label = element + str(self.counter)
        return Buffer_Atom(self.buffer, coords, element, label)

    def bond(self, atom1, atom2):
        self.increment()
        return None

    def label(self, atom):
        self.increment()
        return None

    def register_atom(self):
        pass

    def register_bond(self):
        pass

    def register_label(self):
        pass

    def increment(self):
        Factory.counter += 1


class Buffer(dict):
    counter = 0

    def __init__(self):
        self['atoms'] = {}
        self['bonds'] = {}
        self['labels'] = {}
        self.widget_pos = (15, 15)
        self.widget_size = (200, 200)
        self.zoom = 45
        self.centered = False
        if Buffer.counter == 0:
            self.prime = True
        else:
            self.prime = False


    def draw_background(self):
        self.widget.canvas.clear()
        with self.widget.canvas:
            Color(0.2, 0.2, 0.2)
            Rectangle(size=(self.widget.width - 250, self.widget.height - 30), pos=(15, 15))


    def register_factory(self, factory):
        self.factory = factory

    def register_widget(self, widget):
        self.widget = widget
        self.draw_background()
        self.widget.bind(size=self.set_mask)
        self.widget.bind(size=self.update)


    def set_mask(self, widget, value):
        self.widget_size = value


    def add_atom(self, coords, element, label=None):
        self['atoms'][label] = self.factory.atom(coords, element, label)

    def populate(self, data):
        pass

    def populate_cif(self, cif):
        for name, data in cif.positions.items():
            self.add_atom(data['cart'], data['element'], label=name)

        for atom1 in self['atoms'].values():
            for atom2 in self['atoms'].values():
                if not atom1 == atom2:
                    distance = norm(atom1.coords - atom2.coords)
                    if distance < cg.covalence_radius[atom1.element] + cg.covalence_radius[atom2.element] + .1:
                        bondname = self.get_bondname(atom1.label, atom2.label)
                        self['bonds'][bondname] = Buffer_Bond(self, atom1, atom2)

        self.order()
        self.update()

    def order(self):
        cmpfnc = attrgetter('z')
        sorted_list = sorted(self['atoms'].values(), key=cmpfnc, reverse=True)
        self.atom_keys = [i.label for i in sorted_list]


    def get_bondname(self, label1, label2):
        labels = [label1, label2]
        labels.sort()
        return ''.join(labels)

    def update(self, *args, **kwargs):

        if self.prime:
            self.draw_background()

        if len(self['atoms']) > 0:
            try:
                rotmat = kwargs['rotmat']
            except KeyError:
                rotmat = matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            if not self.centered:
                self.center()
                for atom in self['atoms'].values():
                    atom.update(rotmat, center=self.cent)
            else:
                for label in self.atom_keys:
                    atom = self['atoms'][label]
                    atom.update(rotmat)
            for bond in self['bonds'].values():
                bond.update()
            for label in self['labels'].values():
                label.update()
        self.order()

    def coords(self):
        return [atom.coords for atom in self['atoms'].values()]

    def center(self):
        self.cent = cg.get_geom_center(self.coords())
        self.centered = True


class Buffer_Item(object):
    def __init__(self, Buffer):
        self.position = None
        self.position = None
        self.state = True
        self.buffer = Buffer

    def set_active(self):
        self.state = True

    def set_inactive(self):
        self.state = False

    def active(self):
        return self.state

    def rotate(self, pos, rotmat):
        return array(dot(pos, rotmat)).flatten().tolist()

    def visible(self):
        if 15 + Buffer_Atom.size < self.position[0] < self.buffer.widget_size[0] - 15 + Buffer_Atom.size - 260 \
                and 15 + Buffer_Atom.size < self.position[1] < self.buffer.widget_size[1] - 15 + Buffer_Atom.size - 50:
            return True
        else:
            return False


class Buffer_Atom(Buffer_Item):
    size = 30

    def __init__(self, Buffer, coords, element, label):
        super(Buffer_Atom, self).__init__(Buffer)
        self.coords = array(coords)
        self.position = array(coords)
        self.element = element
        self.label = label
        self.color = Color_Table[self.element]
        self.z = self.coords[2]


    def set_size(self, size):
        Buffer_Atom.size = size

    def project(self):
        self.position = array(self.coords[:-1]) * self.buffer.zoom
        self.position[0] += (self.buffer.widget_size[0] - 250) / 2
        self.position[1] += (self.buffer.widget_size[1]) / 2

    def get_coords(self, project=True):
        if project:
            self.project()
            return self.position
        else:
            return self.coords

    def get_element(self):
        return self.element

    def get_label(self):
        return self.label

    def update(self, rotmat, center=None):
        if not center is None:
            self.coords -= center
        self.coords = (self.rotate(self.coords, rotmat))
        self.project()
        self.draw()
        self.z = self.coords[2]


    def draw(self):
        if self.state and self.visible():
            with self.buffer.widget.canvas:
                Color(*self.color)
                Ellipse(size=(Buffer_Atom.size, Buffer_Atom.size),
                        pos=(self.position[0] - Buffer_Atom.size / 2, self.position[1] - Buffer_Atom.size / 2))


class Buffer_Bond(Buffer_Item):
    def __init__(self, Buffer, atom1, atom2):
        super(Buffer_Bond, self).__init__(Buffer)
        self.start_atom = atom1
        self.end_atom = atom2
        self.color = (.7, .7, .7, 1)
        self.update()

    def update(self):
        self.position = [self.start_atom.get_coords(), self.end_atom.get_coords()]
        vector = self.position[0] - self.position[1]
        vector /= norm(vector)
        self.start = self.position[0] - vector * (Buffer_Atom.size / 2)
        self.end = self.position[1] + vector * (Buffer_Atom.size / 2)
        self.draw()


    def draw(self):
        if self.start_atom.state and self.end_atom and self.start_atom.visible() and self.end_atom.visible():
            if norm(self.position[0] - self.position[1]) > 25:
                with self.start_atom.buffer.widget.canvas:
                    Color(*self.color)
                    Line(points=[self.start[0],
                                 self.start[1],
                                 self.end[0],
                                 self.end[1]],
                         width=5)


class Buffer_Label(Buffer_Item):
    pass



