from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from customizedWidgets import cButton, cLabel, cToggleButton
from screen.RecipeStepScreen import RecipeStepScreen
from DB import mysqlDB


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

        korean_button = cToggleButton(text='한식', font_size=45, group='food_group', on_press=self.switchScrollContent)
        japanese_button = cToggleButton(text='일식', font_size=45, group='food_group', on_press=self.switchScrollContent)
        chinese_button = cToggleButton(text='중식', font_size=45, group='food_group', on_press=self.switchScrollContent)
        western_button = cToggleButton(text='양식', font_size=45, group='food_group', on_press=self.switchScrollContent)

        button_column.add_widget(korean_button)
        button_column.add_widget(japanese_button)
        button_column.add_widget(chinese_button)
        button_column.add_widget(western_button)

        self.scrollLayout.add_widget(self.scrollContent)

        layout.add_widget(button_column)
        layout.add_widget(self.scrollLayout)
        return layout

    def switchMain(self, *args):
        self.manager.current = 'main_screen_button'

    def switchScrollContent(self, button):
        self.scrollContent.clear_widgets()
        self.scrollLayout.scroll_y = 1

        image_height = 300

        db = mysqlDB()

        if button.text == '한식':
            foodNames = db.getFoodNames(1)
            for foodName in foodNames:
                button = cButton(text=foodName, size_hint_y=None, size=(100, image_height),
                                 background_normal=f'img/Korean/{foodName}.png')
                button.bind(on_press=self.switchRecipeStep)
                self.scrollContent.add_widget(button)
        elif button.text == '일식':
            foodNames = db.getFoodNames(2)
            for foodName in foodNames:
                button = cButton(text=foodName, size_hint_y=None, size=(100, image_height),
                                 background_normal=f'img/Japanese/{foodName}.png')
                button.bind(on_press=self.switchRecipeStep)
                self.scrollContent.add_widget(button)
        elif button.text == '중식':
            foodNames = db.getFoodNames(3)
            for foodName in foodNames:
                button = cButton(text=foodName, size_hint_y=None, size=(100, image_height),
                                 background_normal=f'img/Chinese/{foodName}.png')
                button.bind(on_press=self.switchRecipeStep)
                self.scrollContent.add_widget(button)
        else:
            foodNames = db.getFoodNames(4)
            for foodName in foodNames:
                button = cButton(text=foodName, size_hint_y=None, size=(100, image_height),
                                 background_normal=f'img/Western/{foodName}.png')
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
            # Handle the case when the 'recipe' screen object does not exist
            print("The 'recipe' screen does not exist.")

        recipeStepScreen = RecipeStepScreen(foodID)
        self.manager.add_widget(recipeStepScreen)
        self.manager.current = 'recipe'
