from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functools import partial
import configparser

from kivy.uix.switch import Switch


class MainScreenButton(Screen):

    def __init__(self, **kwargs):
        super(MainScreenButton, self).__init__(**kwargs)

        layout = FloatLayout()
        bLayout = BoxLayout(orientation='horizontal', size_hint=(0.75, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            spacing=30)

        rButton = Button(text='Recipe')
        mButton = Button(text='Material')
        sButton = Button(text='Settings', pos_hint={'center_x':0.9, 'center_y':0.9}, size_hint=(0.1,0.1))
        nameLabel = Label(text='Smart Kitchen System', pos_hint={'center_x':0.5, 'center_y':0.9})
        footLabel = Label(text='Made by 최금자', font_name='AppleGothic.ttf', pos_hint={'center_x':0.5, 'center_y':0.1})

        rButton.bind(on_press=self.switchToRecipe)
        mButton.bind(on_press=self.switchToMaterial)
        sButton.bind(on_press=self.settingPopUp)

        layout.add_widget(nameLabel)
        layout.add_widget(sButton)
        bLayout.add_widget(rButton)
        bLayout.add_widget(mButton)
        layout.add_widget(bLayout)
        layout.add_widget(footLabel)

        self.add_widget(layout)

    def switchToRecipe(self, *args):
        self.manager.current = 'recipe_screen'

    def switchToMaterial(self, *args):
        self.manager.current = 'material_screen'

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

    def settingPopUp(self, *args):
        mode = self.getMode()
        popup_content = FloatLayout()
        modeSwitch = Switch(pos_hint = {'center_x':0.5, 'center_y':0.5})

        if mode == 'button':
            modeSwitch.active = False
        else:
            modeSwitch.active = True

        popup_content.add_widget(modeSwitch)

        popup = Popup(title='Setting', content=popup_content, size_hint=(0.5, 0.5))
        callDismiss = partial(self.popupDismiss, mode, modeSwitch)
        popup.bind(on_dismiss=callDismiss)
        popup.open()

    def popupDismiss(self, mode, switch, *args):
        m = True if mode == 'voice' else False
        mode = 'voice' if switch.active else 'button'
        if m != switch.active:
            self.setMode(mode)
            if switch.active:
                self.manager.current = 'main_screen_voice'
            else:
                self.manager.current = 'main_screen_button'