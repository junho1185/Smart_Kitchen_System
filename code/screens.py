import json

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.clock import Clock

from functools import partial

from code.customizedWidgets import *
from code.chatGPT import ChatGPT
from code.DB import mysqlDB
from code.shelves import shelves
from code.voiceRecognition import voiceRecognition

class MainScreenButton(Screen):

    def __init__(self, **kwargs):
        super(MainScreenButton, self).__init__(**kwargs)

        layout = FloatLayout()
        bLayout = BoxLayout(orientation='horizontal', size_hint=(0.75, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            spacing=30)

        rButton = cButton(text='요리', font_size=80)
        mButton = cButton(text='재료', font_size=80)
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

        popup = Popup(title='Voice Control Mode', content=popup_content, size_hint=(0.5, 0.5))
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

class MainScreenVoice(Screen):

    def __init__(self, **kwargs):
        super(MainScreenVoice, self).__init__(**kwargs)

        self.cGPT = ChatGPT()

        layout = FloatLayout()

        nameLabel = cLabel(text='Smart Kitchen System', pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.mic_button = cButton(text='mic', pos_hint={'center_x':0.5, 'center_y':0.5}, size_hint=(0.3, 0.3))
        self.statusLabel = cLabel(text='버튼을 누르고 원하시는 재료/레시피를 말씀하세요.', pos_hint={'center_x':0.5, 'center_y':0.75})
        sButton = Button(text='Settings', pos_hint={'center_x': 0.9, 'center_y': 0.9}, size_hint=(0.1, 0.1))

        self.mic_button.bind(on_press=self.micOnClick)
        sButton.bind(on_press=self.settingPopUp)

        layout.add_widget(nameLabel)
        layout.add_widget(self.statusLabel)
        layout.add_widget(self.mic_button)
        layout.add_widget(sButton)

        self.add_widget(layout)

    def micOnClick(self, *args):
        self.mic_button.text = '말씀하세요...'
        self.mic_button.disabled = True
        Clock.schedule_once(self.micFunc, 0.01)

    def micFunc(self, *args):

        vR = voiceRecognition()
        vR.speechToText()
        text = vR.text
        json_response = self.cGPT.get_response(text)
        json_data = json.loads(json_response)

        type = json_data['Type']
        name = json_data['Name']
        print('Type: ', type)
        print('Name: ', name)

        if type == 'Dish':
            self.switchRecipeStep(name)
            self.statusLabel.text = '버튼을 누르고 원하시는 재료/레시피를 말씀하세요.'
        elif type == 'Ingredient':
            self.switchMaterialShow(name)
            self.statusLabel.text = '버튼을 누르고 원하시는 재료/레시피를 말씀하세요.'
        else:
            self.statusLabel.text = "다시 말씀해주세요."

        self.mic_button.text = 'mic'
        self.mic_button.disabled = False

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

        popup = Popup(title='Voice Control Mode', content=popup_content, size_hint=(0.5, 0.5))
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
        if foodID is None:  # Recipe does not exist in the database
            print("Recipe does not exist, creating one from ChatGPT...")

            recipe_json = self.cGPT.get_recipe(name)
            recipe_json = json.loads(recipe_json)
            recipe_text = recipe_json['Recipe'].strip()
            recipe_region = int(recipe_json['Region'])
            db.putRecipe(foodName, recipe_region, recipe_text)

            foodID = db.getID(foodName)


        try:
            self.manager.remove_widget(self.manager.get_screen('recipe'))
        except KeyError:
            # Handle the case when the 'recipe' code object does not exist
            print("The 'recipe' code does not exist.")

        recipeStepScreen = RecipeStepScreen(foodID)
        self.manager.add_widget(recipeStepScreen)
        self.manager.current = 'recipe'
        db.close()

    def switchMaterialShow(self, name):
        Name = name
        try:
            self.manager.remove_widget(self.manager.get_screen('material'))
        except KeyError:
            # Handle the case when the 'recipe' code object does not exist
            print("The 'material' code does not exist.")

        MaterialShowScreen = MaterialShow(Name)
        self.manager.add_widget(MaterialShowScreen)
        self.manager.current = 'material'

class MaterialScreen(Screen):
    def __init__(self, **kwargs):
        super(MaterialScreen, self).__init__(**kwargs)
        self.mydb = mysqlDB()
        self.materials = self.mydb.getMaterials()

        self.scrollContent = GridLayout(cols=4, size_hint_y=None, pos_hint={'center_x':0.5, 'center_y':0.5},
                                        padding=30, spacing=30)
        self.scrollContent.bind(minimum_height=self.scrollContent.setter('height'))

        layout = BoxLayout(orientation='vertical', padding=30)
        hLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        cLayout = self.content_layout()
        backButton = Button(text='Back', size_hint=(0.15, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        nameLabel = cLabel(text='재료를 선택하세요!!', size_hint=(0.7, 1))

        backButton.bind(on_press=self.switchMain)

        hLayout.add_widget(backButton)
        hLayout.add_widget(nameLabel)

        layout.add_widget(hLayout)
        layout.add_widget(cLayout)

        self.add_widget(layout)

    def switchMain(self, *args):
        self.manager.current='main_screen_button'

    def content_layout(self):
        layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        scrollLayout = ScrollView(do_scroll_x=False)

        # section to add materials!
        for material in self.materials:
            button = cButton(text=material, size_hint_y=None, size=(100, 250), background_normal=f'code/img/material/{material}.png')
            button.bind(on_press=self.switchMaterialShow)
            self.scrollContent.add_widget(button)

        scrollLayout.add_widget(self.scrollContent)
        layout.add_widget(scrollLayout)

        return layout
    def switchMaterialShow(self, button):
        Name = button.text
        try:
            self.manager.remove_widget(self.manager.get_screen('material'))
        except KeyError:
            # Handle the case when the 'recipe' code object does not exist
            print("The 'material' code does not exist.")

        MaterialShowScreen = MaterialShow(Name)
        self.manager.add_widget(MaterialShowScreen)
        self.manager.current = 'material'

class MaterialShow(Screen):
    def __init__(self, materialName, **kwargs):
        super(MaterialShow, self).__init__(**kwargs)
        self.materialName = materialName
        self.name = 'material'
        layout = BoxLayout(orientation='vertical')
        centerLabel = cLabel(text=materialName+'을 꺼내는 중입니다...', pos_hint={'center_x':0.5, 'center_y':0.5}, font_size=25)
        layout.add_widget(centerLabel)
        self.add_widget(layout)

        Clock.schedule_once(self.rotateShelf, 1)

    def rotateShelf(self, *args):
        db = mysqlDB()
        position = db.getPosition(self.materialName)
        sh = shelves([position])
        sh.rot_thread.start()
        sh.rot_thread.join()
        self.switchMain()

    def switchMain(self, *args):
        S = setting()
        mode = S.getMode()
        if mode == 'button':
            self.manager.current = 'main_screen_button'
        else:
            self.manager.current = 'main_screen_voice'

class RecipeScreen(Screen):
    def __init__(self, **kwargs):
        super(RecipeScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=30)
        hLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.scrollContent = GridLayout(cols=3, size_hint_y=None, pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        spacing=30, padding=30)
        self.scrollContent.bind(minimum_height=self.scrollContent.setter('height'))
        self.scrollLayout = ScrollView(do_scroll_x=False)

        cLayout = self.content_layout()

        backButton = Button(text='Back', size_hint=(0.15, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        nameLabel = cLabel(text='Choose a Recipe!', size_hint=(0.7, 1))

        backButton.bind(on_press=self.switchMain)

        hLayout.add_widget(backButton)
        hLayout.add_widget(nameLabel)

        layout.add_widget(hLayout)
        layout.add_widget(cLayout)

        self.add_widget(layout)

    def content_layout(self):
        layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        button_column = BoxLayout(orientation='vertical', size_hint=(0.2, 1), spacing=30)

        korean_button = cToggleButton(text='한식', font_size=35, group='food_group', on_press=self.switchScrollContent)
        japanese_button = cToggleButton(text='일식', font_size=35, group='food_group', on_press=self.switchScrollContent)
        chinese_button = cToggleButton(text='중식', font_size=35, group='food_group', on_press=self.switchScrollContent)
        western_button = cToggleButton(text='양식', font_size=35, group='food_group', on_press=self.switchScrollContent)

        button_column.add_widget(korean_button)
        button_column.add_widget(japanese_button)
        button_column.add_widget(chinese_button)
        button_column.add_widget(western_button)

        self.scrollLayout.add_widget(self.scrollContent)

        layout.add_widget(button_column)
        layout.add_widget(self.scrollLayout)
        return layout

    def switchMain(self, *args):
        S = setting()
        mode = S.getMode()

        if mode == 'button':
            self.manager.current = 'main_screen_button'
        else:
            self.manager.current = 'main_screen_voice'

    def switchScrollContent(self, button):
        self.scrollContent.clear_widgets()
        self.scrollLayout.scroll_y = 1

        image_height = 150

        db = mysqlDB()

        if button.text == '한식':
            foodNames = db.getFoodNames(1)
            for foodName in foodNames:
                button = cButton(text=foodName, size_hint_y=None, size=(100, image_height),
                                 background_normal=f'code/img/Korean/{foodName}.png')
                button.bind(on_press=self.switchRecipeStep)
                self.scrollContent.add_widget(button)
        elif button.text == '일식':
            foodNames = db.getFoodNames(2)
            for foodName in foodNames:
                button = cButton(text=foodName, size_hint_y=None, size=(100, image_height),
                                 background_normal=f'code/img/Japanese/{foodName}.png')
                button.bind(on_press=self.switchRecipeStep)
                self.scrollContent.add_widget(button)
        elif button.text == '중식':
            foodNames = db.getFoodNames(3)
            for foodName in foodNames:
                button = cButton(text=foodName, size_hint_y=None, size=(100, image_height),
                                 background_normal=f'code/img/Chinese/{foodName}.png')
                button.bind(on_press=self.switchRecipeStep)
                self.scrollContent.add_widget(button)
        else:
            foodNames = db.getFoodNames(4)
            for foodName in foodNames:
                button = cButton(text=foodName, size_hint_y=None, size=(100, image_height),
                                 background_normal=f'code/img/Western/{foodName}.png')
                button.bind(on_press=self.switchRecipeStep)
                self.scrollContent.add_widget(button)

        db.close()

    def switchRecipeStep(self, button):
        db = mysqlDB()
        foodName = button.text
        foodID = db.getID(foodName)
        try:
            self.manager.remove_widget(self.manager.get_screen('recipe'))
        except KeyError:
            # Handle the case when the 'recipe' code object does not exist
            print("The 'recipe' code does not exist.")

        recipeStepScreen = RecipeStepScreen(foodID)
        self.manager.add_widget(recipeStepScreen)
        self.manager.current = 'recipe'
        db.close()

class RecipeStepScreen(Screen):
    def __init__(self, foodID, **kwargs):

        super(RecipeStepScreen, self).__init__(**kwargs)
        self.name = 'recipe'
        self.mydb = mysqlDB()

        self.foodName = self.mydb.getFoodName(foodID)
        self.material_list = self.mydb.getMaterials()
        self.location_list = []
        self.currentStep = 0

        layout = BoxLayout(orientation='vertical')
        footer_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        self.recipeNameLabel = cLabel(text=self.foodName, size_hint=(1, 0.2), font_size=35, pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.recipeContentLabel = cLabel(size_hint=(1, 0.7), font_size = 30)
        self.stepLabel = cLabel(size_hint=(0.3, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=25, text_size=(None, None))
        self.prevButton = cButton(text='이전', size_hint=(0.2, 0.8), pos_hint={'center_x': 0.1, 'center_y': 0.5})
        self.nextButton = cButton(text='다음', size_hint=(0.2, 0.8), pos_hint={'center_x': 0.9, 'center_y': 0.5})

        self.recipe = self.mydb.getRecipe(foodID)

        self.prevButton.bind(on_press=self.prevStep)
        self.nextButton.bind(on_press=self.nextStep)

        footer_layout.add_widget(self.prevButton)
        footer_layout.add_widget(self.stepLabel)
        footer_layout.add_widget(self.nextButton)

        layout.add_widget(self.recipeNameLabel)
        layout.add_widget(self.recipeContentLabel)
        layout.add_widget(footer_layout)

        self.add_widget(layout)

        self.contentUpdate()

    def prevStep(self, *args):
        if self.currentStep == 0:
            return
        self.currentStep -= 1
        self.contentUpdate()

    def nextStep(self, *args):
        if self.currentStep == len(self.recipe) - 1:
            S = setting()
            mode = S.getMode()
            if mode == 'button':
                self.manager.current = 'main_screen_button'
            else:
                self.manager.current = 'main_screen_voice'
            return
        self.currentStep += 1
        self.contentUpdate()

    def contentUpdate(self, *args):
        recipeText = self.recipe[self.currentStep]
        self.recipeContentLabel.text = recipeText
        self.stepLabel.text = f'{len(self.recipe)} 단계 중 {self.currentStep + 1} 단계'

        mList = []
        # code to rotate the shelf
        # get materials in the recipe that are in the shelf
        for material in self.material_list:
            if material in recipeText:
                mList.append(material)

        self.location_list = []
        # convert material names to their positions
        for material in mList:
            self.location_list.append(self.mydb.getPosition(material))

        if len(self.location_list) > 0:
            self.nextButton.disabled = True
            Clock.schedule_once(self.rotateShelf, 1)
    def rotateShelf(self, *args):
        sh = shelves(self.location_list)
        sh.rot_thread.start()
        sh.rot_thread.join()
        self.nextButton.disabled = False
