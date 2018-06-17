"""
Created on 11.01.2014

@author: arrah_000
"""

import kivy

kivy.require('1.2.0')
from kivy.uix.settings import Settings, SettingItem, SettingsPanel


class Settings(Settings):
    def __init__(self):
        super(Settings, self).__init__()
        self.add_kivy_panel()
        self.panels = {'test': SettingsPanel(title='test', settings=self)}
        self.items = {'test': [
            SettingItem(panel=self.panels['test'], title='test1 title', desc='Lets see if that works.', settings=self)]}
        self.panels['test2'] = (SettingsPanel(title='test2', settings=self))
        self.items['test2'] = [
            SettingItem(panel=self.panels['test2'], title='test2 title', desc='Lets see if that works.', settings=self)]
        for key, panel in self.panels.items():
            for item in self.items[key]:
                panel.add_widget(item)
            self.add_widget(panel)






