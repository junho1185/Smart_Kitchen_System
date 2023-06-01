from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from customizedWidgets import cLabel, cButton, setting
from DB import mysqlDB
from shelves import shelves
from kivy.clock import Clock

class RecipeStepScreen(Screen):
    def __init__(self, foodID, **kwargs):

        super(RecipeStepScreen, self).__init__(**kwargs)
        self.name = 'recipe'
        self.mydb = mysqlDB()

        self.foodName = self.mydb.getFoodName(foodID)
        self.material_list = self.mydb.getMaterials()
        self.currentStep = 0

        layout = BoxLayout(orientation='vertical')
        footer_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        self.recipeNameLabel = cLabel(text=self.foodName, size_hint=(1, 0.2), font_size=35, pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.recipeContentLabel = cLabel(size_hint=(1, 0.7), font_size = 30)
        self.stepLabel = cLabel(size_hint=(0.3, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=25, text_size=(None, None))
        self.prevButton = cButton(text='이전', size_hint=(0.2, 0.8), pos_hint={'center_x': 0.1, 'center_y': 0.5})
        self.nextButton = cButton(text='다음', size_hint=(0.2, 0.8), pos_hint={'center_x': 0.9, 'center_y': 0.5})

        self.recipe = self.mydb.getRecipe(foodID)
        self.contentUpdate()

        self.prevButton.bind(on_press=self.prevStep)
        self.nextButton.bind(on_press=self.nextStep)

        footer_layout.add_widget(self.prevButton)
        footer_layout.add_widget(self.stepLabel)
        footer_layout.add_widget(self.nextButton)

        layout.add_widget(self.recipeNameLabel)
        layout.add_widget(self.recipeContentLabel)
        layout.add_widget(footer_layout)

        self.add_widget(layout)

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

    def contentUpdate(self):
        recipeText = self.recipe[self.currentStep]
        self.recipeContentLabel.text = recipeText
        self.stepLabel.text = f'{len(self.recipe)} 단계 중 {self.currentStep + 1} 단계'

        mList = []
        # code to rotate the shelf
        # get materials in the recipe that are in the shelf
        for material in self.material_list:
            if material in recipeText:
                mList.append(material)

        location_list = []
        # convert material names to their positions
        for material in mList:
            location_list.append(self.mydb.getPosition(material))

        sh = shelves(location_list)
        Clock.schedule_once(sh.rotate, 3)