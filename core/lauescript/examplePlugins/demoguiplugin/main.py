__author__ = 'jens'

from kivy.config import Config
Config.set('graphics', 'width', '250')
Config.set('graphics', 'height', '400')
import unicodedata
from functools import partial
import kivy

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner




def run(pluginManager):
    global printer
    printer = pluginManager.get_active_printer()
    global pM
    pM = pluginManager
    printer('Starting GUI plugin.')
    APD_Toolkit().run()


class APD_Toolkit(App):
    def build(self):
        global APP
        APP = self
        self.main_window = Main_Window()
        return self.main_window


class Main_Window(BoxLayout):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.add_widget(PluginCaller())


class PluginCaller(BoxLayout):
    def __init__(self):
        self.buildPluginDict()
        # self.nameDict = {'TLS': 'T2', 'AUTO': 'A', 'Compare': 'compare'}
        super(PluginCaller, self).__init__(orientation='vertical', size_hint=(None, 1), width=250)
        label = Label(text='Call Plugin', size_hint=(1, None), height=35)
        self.pluginSelectionSpinner = PluginSelectionSpinner(self.nameDict.keys())
        self.optionsSelector = OptionSelector()
        self.add_widget(label)
        self.add_widget(self.pluginSelectionSpinner)
        self.add_widget(self.optionsSelector)
        self.add_widget(RunPluginButton())

    def getPlugin(self):
        return self.nameDict[self.pluginSelectionSpinner.text]

    def buildPluginDict(self):
        self.nameDict = {}
        for key, value in pM.plugins.items():
            try:
                self.nameDict[value.NAME] = key
            except AttributeError:
                self.nameDict[key] = key

class PluginSelectionSpinner(Spinner):
    def __init__(self, values):
        super(PluginSelectionSpinner, self).__init__(values=values, text='SelectPlugin', size_hint=(1, None), height=35)
        self.bind(text=self.updateSelection)

    def updateSelection(self, _, newText):
        plugin = pM.plugins[self.parent.nameDict[newText]]
        try:
            optionArguments = plugin.OPTION_ARGUMENTS
        except AttributeError:
            optionArguments = {}
        try:
            options = plugin.OPTIONS
        except:
            options = ()
        self.parent.optionsSelector.update(options, optionArguments)


class OptionSelector(BoxLayout):
    def __init__(self):
        super(OptionSelector, self).__init__(orientation='vertical', size_hint=(1, None), height=35)
        self.inputs = []
        self.options = []

    def update(self, options=(), optionsWithArguments=()):
        self.inputs = []
        self.options = []
        self.clear_widgets()
        requiredSlots =  len(options) + len(optionsWithArguments)
        self.height = requiredSlots * 35
        for option in options:
            optionInput = OptionInput(option)
            self.options.append(optionInput)
            self.add_widget(optionInput)
        if type(optionsWithArguments) is dict:
            for option, argument in optionsWithArguments.items():
                if type(argument) is list:
                    argument = ':'.join(argument)
                selector = OptionArgumentInput(option, argument)
                self.inputs.append(selector)
                self.add_widget(selector)

    def harvest(self):
        return [option.getName() for option in self.options if option.getValue()], {input.getOption(): input.getArgument() for input in self.inputs}


class OptionArgumentInput(BoxLayout):
    def __init__(self, option, argument):
        super(OptionArgumentInput, self).__init__(orientation='horizontal')
        self.label = OptionLabel(text=option, size_hint=(None, 1), width=85)
        self.argument = TextInput(multiline=False, text=str(argument))
        self.add_widget(self.argument)
        self.add_widget(self.label)


    def getOption(self):
        return self.label.text

    def getArgument(self):
        try:
            argument = unicodedata.normalize('NFKD', self.argument.text).encode('ascii', 'ignore')
        except TypeError:
            argument = self.argument.text
        if ':' in argument:
            argument = [argument.split(':')]
        else:
            argument = [argument]
        return argument


class OptionInput(BoxLayout):
    def __init__(self, option):
        super(OptionInput, self).__init__(orientation='horizontal')
        self.option = option
        self.label = OptionLabel(text=option, size_hint=(None, 1), width=150)
        self.value = CheckBox()
        self.add_widget(self.label)
        self.add_widget(self.value)

    def getValue(self):
        return self.value.active

    def getName(self):
        return self.option


class RunPluginButton(Button):
    def __init__(self):
        super(RunPluginButton, self).__init__(text='Run Plugin', size_hint=(1, None), height=35)
        self.bind(on_release=self.run)

    def run(self, _):
        try:
            plugin = self.parent.getPlugin()
        except KeyError:
            printer('Please select Plugin.')
            return
        optionList, moreOption = self.parent.optionsSelector.harvest()
        options = {'options': optionList}

        for key, value in moreOption.items():
            options[key] = value
        optionString = '-{} {} {}'.format(plugin, ' '.join(optionList), ' '.join(['{} {}'.format(key, ':'.join(value[0])) if type(value[0]) is list else '{} {}'.format(key, value[0]) for key, value in moreOption.items()]))
        try:
            printer('Calling plugin {} with parameters:'.format(plugin), optionString)
            pM.call(plugin, options)
        except Exception as error:
            printer('Failed to run plugin:')
            printer(error.message)

class OptionLabel(Label):
    def __init__(self, *args, **kwargs):
        super(OptionLabel, self).__init__(*args, **kwargs)
        kivy.clock.Clock.schedule_interval(partial(self.isHovered, 'my value', 'my key'), 0.5)
        self.tooltip = False
        # Window.bind(on_motion=self.on_motion)

    def isHovered(self, dt, x, y):
        if self.collide_point(Window.mouse_pos[0], Window.mouse_pos[1]):
            if not self.tooltip:
                self.tooltip = True
                self.spawnTooltip()

        else:
            self.tooltip = False
            self.clear_widgets()

    def spawnTooltip(self):
        self.tooltipLabel = Button(text='test', pos_hint=(None, None), pos=Window.mouse_pos, size_hint=(None, None), width=50, height=35, color=(.3,.8,1,1), background=(.7,.2,0,1))
        self.add_widget(self.tooltipLabel)


