import kivy

from lauescript.lauegui import buffer


kivy.require('1.0.6')  # replace with your current kivy version !

import numpy as np
import lauescript.cryst.crystgeom as cg
from kivy.uix.floatlayout import FloatLayout


class Drawer(FloatLayout):
    def __init__(self, parent_widget):
        # =======================================================================
        # super(Drawer,self).__init__(size_hint=(None,0.95),
        #                             width=200,
        #                             pos_hint={'center_y':.5},
        #                             x=15)
        #=======================================================================
        super(Drawer, self).__init__()
        self.parent_widget = parent_widget
        self.buffer = buffer.Buffer()
        self.buffer.register_widget(self)




        #=======================================================================
        # self.buffer=buffer.Buffer()
        # self.buffer.register_widget(self)
        # self.factory=buffer.Factory(self.buffer)
        # self.buffer.register_factory(self.factory)
        # self.buffer.update()
        #=======================================================================

    def register_data(self, data):

        # =======================================================================
        # self.buffer=buffer.Buffer()
        # self.buffer.register_widget(self)
        #=======================================================================
        self.factory = buffer.Factory(self.buffer)
        self.buffer.register_factory(self.factory)
        self.buffer.update()
        self.buffer.populate_cif(data)

    def on_touch_move(self, touch):

        if touch.button == 'left' and touch.x < self.size[0] * 0.75:
            self.movelist.append((touch.x, touch.y))
            try:
                self.get_rotmat(self.movelist[-1], self.movelist[-2])
            except:
                pass

    def on_touch_down(self, touch):
        self.movelist = []
        self.movelist.append((touch.x, touch.y))

    def get_rotmat(self, now, then):
        vector = np.array(now) - np.array(then)

        axis = np.array([vector[1] * -1, vector[0]]).tolist()
        axis.append(0)
        angle = np.pi * np.linalg.norm(vector) * 0.005

        rotmat = cg.get_3drotation_matrix(axis, angle)

        self.buffer.update(rotmat=rotmat)









