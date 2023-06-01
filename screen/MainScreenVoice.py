import json
import threading

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from functools import partial

from DB import mysqlDB
from screen.MaterialShow import MaterialShow
from screen.RecipeStepScreen import RecipeStepScreen
from voiceRecognition import voiceRecognition
from chatGPT import ChatGPT
from customizedWidgets import setting
import configparser

from kivy.uix.switch import Switch


class MainScreenVoice(Screen):

    def __init__(self, **kwargs):
        super(MainScreenVoice, self).__init__(**kwargs)

        layout = FloatLayout()

        mic_button = Button(text='mic', pos_hint={'center_x':0.5, 'center_y':0.5}, size_hint=(0.3, 0.3))
        sButton = Button(text='Settings', pos_hint={'center_x': 0.9, 'center_y': 0.9}, size_hint=(0.1, 0.1))

        mic_button.bind(on_press=self.micFunc)
        sButton.bind(on_press=self.settingPopUp)

        layout.add_widget(mic_button)
        layout.add_widget(sButton)

        self.add_widget(layout)

    def micFunc(self, *args):
        # mThread = threading.Thread(target=self.micThread)
        # mThread.start()
        # mThread.join()
        vR = voiceRecognition()
        vR.speechToText()
        text = vR.text

        cGPT = ChatGPT(text)
        json_response = cGPT.get_response()
        json_data = json.loads(json_response)

        type = json_data['Type']
        name = json_data['Name']
        print('Type: ', type)
        print('Name: ', name)

        if type == 'Dish':
            self.switchRecipeStep(name)
        elif type == 'Ingredient':
            self.switchMaterialShow(name)



    # def micThread(self):
    #     vR = voiceRecognition()
    #     vR.speechToText()
    #     text = vR.text
    #
    #     cGPT = ChatGPT(text)
    #     json_response = cGPT.get_response()
    #     return json_response

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

    def switchRecipeStep(self, name):
        db = mysqlDB()
        foodName = name
        foodID = db.getID(foodName)
        try:
            self.manager.remove_widget(self.manager.get_screen('recipe'))
        except KeyError:
            # Handle the case when the 'recipe' screen object does not exist
            print("The 'recipe' screen does not exist.")

        recipeStepScreen = RecipeStepScreen(foodID)
        self.manager.add_widget(recipeStepScreen)
        self.manager.current = 'recipe'
        db.close()

    def switchMaterialShow(self, name):
        Name = name
        try:
            self.manager.remove_widget(self.manager.get_screen('material'))
        except KeyError:
            # Handle the case when the 'recipe' screen object does not exist
            print("The 'material' screen does not exist.")

        MaterialShowScreen = MaterialShow(Name)
        self.manager.add_widget(MaterialShowScreen)
        self.manager.current = 'material'