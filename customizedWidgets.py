import configparser

from kivy.uix.button import Button
from kivy.uix.label import Label

class cLabel(Label):
    def __init__(self, **kwargs):
        super(cLabel, self).__init__(**kwargs)
        self.font_name = 'NanumGothicBold.ttf'

class setting:
    def getMode(self):
        config = configparser.ConfigParser()
        config.read('user/settings.ini')
        mode = config.get('Control', 'mode')
        return mode
    def setMode(self, mode, *args):
        with open('user/settings.ini', 'w') as configfile:
            config = configparser.ConfigParser()
            config['Control'] = {'mode':mode}
            config.write(configfile)
