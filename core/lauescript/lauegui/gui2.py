import kivy

from lauescript.core import apd_printer
from lauescript.lauegui import drawer, loading, menu


kivy.require('1.0.6')  # replace with your current kivy version !

import argparse
import lauescript.laueio.inout as inout
import lauescript.types.data as data
# ===============================================================================
# import apd.lib.crystgeom as crystgeom
#===============================================================================
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class Config(object):
    """
    Class for handling all shared information.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='GUI for the APD-Toolkit.')
        self.parser.add_argument('load', nargs='?')
        self.dabapath = '.'
        self.printer = apd_printer()

    def __call__(self):
        self.args = self.parser.parse_args()
        print self.args.load


class Main_Window(FloatLayout):
    """
    Main widget of the program.
    """

    def __init__(self):
        super(Main_Window, self).__init__()
        self.reload_menu()
        self.reload_drawer()
        #=======================================================================
        # self.loading_dialog()
        #=======================================================================

        #=======================================================================
        # self.show_settings()
        #=======================================================================

    def reload_drawer(self):
        self.drawer = drawer.Drawer(self)
        self.add_widget(self.drawer)

    def reload_menu(self):
        self.main_menu = menu.Main_Menu(self)
        self.add_widget(self.main_menu)

    def loading_dialog(self, args):
        """
        Opens a file loading dialog including a
        file browser.
        """
        loading_popup = loading.Load_Popup(self)
        loading_popup.open()

    def load_file(self, filename):
        """
        Tries to open the file corresponding to
        'filename' as returned by the file loading
        dialog.
        """
        failed = False
        try:
            self.filepointer = open(filename, 'r')
            self.filepointer.close()

        except:
            self.raise_loading_error(filename)
            failed = True
        if not failed:
            if '.cif' in filename:
                self.cif = inout.CIF(filename)
                print 'cif loaded.'
                self.drawer.register_data(self.cif)
                try:
                    pass
                    #===========================================================
                    # self.cif=inout.CIF(filename)
                    # print 'cif loaded.'
                    # self.drawer.register_data(self.cif)
                    #===========================================================
                except:
                    self.raise_loading_error(filename)
            else:
                try:
                    inout.Load(data, config.dabapath, config.printer, filename)
                except:
                    self.raise_loading_error(filename)

    def show_settings(self):
        from lauescript.lauegui.settings import Settings

        settings = Settings()
        self.add_widget(settings)

    def raise_loading_error(self, filename):
        """
        Opens a Popup giving feedback on a failed
        file loading attempt.
        """
        errormsg = Label(text='Failed to load file: \'{}\''.format(filename))
        failed_popup = Popup(title='Error',
                             content=errormsg,
                             size_hint=(None, None),
                             height=120, width=350)
        failed_popup.open()


class APD_Toolkit(App):
    def build(self):
        global APP
        APP = self
        self.main_window = Main_Window()
        return self.main_window


def run():
    global config, data
    data = data.DATA()
    config = Config()
    config()
    APD_Toolkit().run()
