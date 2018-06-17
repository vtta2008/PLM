"""
Module to open a file loading dialog.
The class calling the module must implement a
.load_file() method taking one string as an
argument representing the path to the file
to load.

To start the dialog an instance of 'Load_Popup'
must be created with the pointer to the class
instance implementing the .load_file() as the
only argument.
The dialog is then opened by calling the Popup's
open() method.
"""

import kivy

kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView

filename = 'File path'


class Load_Popup(Popup):
    def __init__(self, main_window):
        self.main_window = main_window
        super(Load_Popup, self).__init__(title='Loading File',
                                         content=Loading_Layout(self),
                                         size_hint=(None, None),
                                         height=(120), width=(250),
                                         auto_dismiss=False)

    def dismiss(self):
        print filename
        # =======================================================================
        # if not filename=='File path' and filename:
        #=======================================================================
        self.main_window.load_file(filename)
        super(Load_Popup, self).dismiss()


class Loading_Layout(BoxLayout):
    def __init__(self, popup):
        self.popup = popup
        super(Loading_Layout, self).__init__(orientation='vertical')
        self.add_widget(File_Select_Line())
        self.add_widget(Button_Line())


class Button_Line(BoxLayout):
    def __init__(self):
        super(Button_Line, self).__init__(orientation='horizontal',
                                          size_hint=(1, None),
                                          height=30)
        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_release=self.cancel)
        load_button = Button(text='Load')
        load_button.bind(on_release=(self.load))
        self.add_widget(cancel_button)
        self.add_widget(load_button)

    def cancel(self, instance):
        global filename
        filename = None
        print 'canceling'
        self.parent.popup.dismiss()

    def load(self, instance):
        self.parent.popup.dismiss()


class File_Select_Line(BoxLayout):
    def __init__(self):
        super(File_Select_Line, self).__init__(orientation='horizontal',
                                               size_hint=(1, None),
                                               height=30)
        self.text_input = File_Name_Input()
        self.add_widget(self.text_input)
        self.button = Browse_Button(self.text_input)
        self.add_widget(self.button)


class File_Name_Input(TextInput):
    def __init__(self):
        super(File_Name_Input, self).__init__(size_hint=(0.75, 1),
                                              multiline=False,
                                              text='File path')
        self.bind(text=self.set_filename)

    def set_filename(self, instance, value):
        global filename
        filename = value


class Browse_Button(Button):
    def __init__(self, textinput):
        self.textinput = textinput
        super(Browse_Button, self).__init__(text='Browse',
                                            size_hint=(.25, 1))
        self.bind(on_release=self.open_browser)

    def open_browser(self, instance):
        browser = Browser_Popup(self.textinput)
        browser.open()


class Browser_Popup(Popup):
    def __init__(self, textinput):
        self.textinput = textinput
        chooser = FileChooserListView()
        chooser.bind(selection=self.select)
        super(Browser_Popup, self).__init__(title='Choosing File',
                                            content=chooser,
                                            size_hint=(None, None),
                                            height=(500), width=(350))

    def select(self, instance, path):
        self.textinput.text = str(path[0])
        self.dismiss()


