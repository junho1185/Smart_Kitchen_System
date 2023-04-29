from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button

from RecipeScreen import RecipeScreen
from MaterialScreen import MaterialScreen


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        rButton = Button(text='Recipe')
        mButton = Button(text='Material')
        nameLabel = Label(text='Smart Kitchen System')
        footLabel = Label(text='Made by 최금자', font_name='AppleGothic.ttf')

        rButton.bind(on_press=self.switchToRecipe)
        mButton.bind(on_press=self.switchToMaterial)

        layout.add_widget(nameLabel)
        bLayout = BoxLayout(orientation='horizontal', size_hint=(0.5, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            spacing=30)
        bLayout.add_widget(rButton)
        bLayout.add_widget(mButton)
        layout.add_widget(bLayout)
        layout.add_widget(footLabel)

        self.add_widget(layout)

    def switchToRecipe(self, *args):
        self.manager.current = 'recipe_screen'

    def switchToMaterial(self, *args):
        self.manager.current = 'material_screen'


class MyApp(App):
    def build(self):
        self.title = 'Smart Kitchen System'

        screen_manager = ScreenManager()
        mainScreen = MainScreen(name='main_screen')
        recipeScreen = RecipeScreen(name='recipe_screen')
        materialScreen = MaterialScreen(name='material_screen')

        screen_manager.add_widget(mainScreen)
        screen_manager.add_widget(recipeScreen)
        screen_manager.add_widget(materialScreen)

        return screen_manager


if __name__ == '__main__':
    MyApp().run()
