import kivy

kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


class Main_Menu(BoxLayout):
    def __init__(self, main_window):
        self.main_window = main_window
        super(Main_Menu, self).__init__(size_hint=(None, 1),
                                        width=220,
                                        pos_hint={'right': 1},
                                        orientation='vertical')
        self.load_button = Button(text='Load', size_hint=(1, None), height=30)
        self.load_button.bind(on_release=self.main_window.loading_dialog)
        self.add_widget(self.load_button)
        for _ in range(10):
            self.add_widget(Button(text='test', size_hint=(1, None), height=30))
        self.editor = Editor(size_hint=(1, .3))
        self.add_widget(self.editor)
        self.input = Cmdline(size_hint=(1, None), height=30, editor=self.editor)
        self.add_widget(self.input)


class Editor(TextInput):
    def __init__(self, *_, **kwargs):
        super(Editor, self).__init__(**kwargs)
        self.set_inactive()

    def set_inactive(self):
        self.active = False
        self.bkpclr = list(self.background_color)
        self.background_color = [.7, .7, .7, 1]

    def set_active(self):
        self.active = True
        self.background_color = self.bkpclr

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        key, _ = keycode
        if self.active or key in (273, 274, 275, 276):
            super(Editor, self)._keyboard_on_key_down(window, keycode, text, modifiers)
        else:
            pass


class Cmdline(TextInput):
    def __init__(self, *_, **kwargs):
        kwargs['multiline'] = False
        super(Cmdline, self).__init__(**kwargs)
        self.editor = kwargs['editor']

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        key, _ = keycode
        if key == 13:
            self.submit()
        else:
            super(Cmdline, self)._keyboard_on_key_down(window, keycode, text, modifiers)

    def submit(self):
        self.editor.text += ('\n' + self.text)
        self.text = ''

        # ===========================================================================
        # def on_focus(self,x,y):
        #     super(Editor,self).on_focus(x,y)
        #     self.set_active()
        #===========================================================================





