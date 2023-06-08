from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager

from code.screens import *

class MyApp(App):
    def build(self):
        self.title = 'Smart Kitchen System'
        # Config.set('graphics', 'fullscreen', 'auto')

        # set window size
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '480')

        screen_manager = ScreenManager()
        mainScreenButton = MainScreenButton(name='main_screen_button')
        mainScreenVoice = MainScreenVoice(name='main_screen_voice')
        recipeScreen = RecipeScreen(name='recipe_screen')
        materialScreen = MaterialScreen(name='material_screen')
        tmpScreen = RecipeScreen(name='recipe')
        tmpScreen2 = RecipeScreen(name='material')

        screen_manager.add_widget(mainScreenButton)
        screen_manager.add_widget(mainScreenVoice)
        screen_manager.add_widget(recipeScreen)
        screen_manager.add_widget(materialScreen)
        screen_manager.add_widget(tmpScreen)
        screen_manager.add_widget(tmpScreen2)

        S = setting()
        mode = S.getMode()

        if mode == 'button':
            screen_manager.current = 'main_screen_button'
        else:
            screen_manager.current = 'main_screen_voice'

        return screen_manager


if __name__ == '__main__':
    MyApp().run()
