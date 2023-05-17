from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functools import partial
from customizedWidgets import setting, cButton
import configparser

from kivy.uix.switch import Switch

from customizedWidgets import cLabel


class MainScreenButton(Screen):

    def __init__(self, **kwargs):
        super(MainScreenButton, self).__init__(**kwargs)

        layout = FloatLayout()
        bLayout = BoxLayout(orientation='horizontal', size_hint=(0.75, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            spacing=30)

        rButton = cButton(text='요리')
        mButton = cButton(text='재료')
        sButton = Button(text='Settings', pos_hint={'center_x':0.9, 'center_y':0.9}, size_hint=(0.1,0.1))
        nameLabel = cLabel(text='Smart Kitchen System', pos_hint={'center_x':0.5, 'center_y':0.9})
        footLabel = cLabel(text='Made by 최금자', pos_hint={'center_x':0.5, 'center_y':0.1})

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

    def settingPopUp(self, *args):
        S = setting()
        mode = S.getMode()
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
            S = setting()
            S.setMode(mode)
            if switch.active:
                self.manager.current = 'main_screen_voice'
            else:
                self.manager.current = 'main_screen_button'