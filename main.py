import configparser
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
from RecipeScreen import RecipeScreen
from MaterialScreen import MaterialScreen
from MainScreenButton import MainScreenButton
from MainScreenVoice import MainScreenVoice
from customizedWidgets import setting

class MyApp(App):
    def build(self):
        self.title = 'Smart Kitchen System'
        Config.set('graphics', 'fullscreen', 'auto')

        screen_manager = ScreenManager()
        mainScreenButton = MainScreenButton(name='main_screen_button')
        mainScreenVoice = MainScreenVoice(name='main_screen_voice')
        recipeScreen = RecipeScreen(name='recipe_screen')
        materialScreen = MaterialScreen(name='material_screen')

        screen_manager.add_widget(mainScreenButton)
        screen_manager.add_widget(mainScreenVoice)
        screen_manager.add_widget(recipeScreen)
        screen_manager.add_widget(materialScreen)

        S = setting()
        mode = S.getMode()

        if mode == 'button':
            screen_manager.current = 'main_screen_button'
        else:
            screen_manager.current = 'main_screen_voice'

        return screen_manager


if __name__ == '__main__':
    MyApp().run()
