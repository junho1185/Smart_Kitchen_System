import configparser

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton

font_name = 'NanumGothicBold.ttf'

class cLabel(Label):
    def __init__(self, **kwargs):
        super(cLabel, self).__init__(**kwargs)
        self.font_name = font_name

class cButton(Button):

    def __init__(self, **kwargs):
        super(cButton, self).__init__(**kwargs)
        self.font_name = font_name

class cToggleButton(ToggleButton):

    def __init__(self, **kwargs):
        super(cToggleButton, self).__init__(**kwargs)
        self.font_name = font_name

class setting:
    def getMode(self):
        config = configparser.ConfigParser()
        config.read('code/data/settings.ini')
        mode = config.get('Control', 'mode')
        return mode
    def setMode(self, mode, *args):
        with open('code/data/settings.ini', 'w') as configfile:
            config = configparser.ConfigParser()
            config['Control'] = {'mode':mode}
            config.write(configfile)
