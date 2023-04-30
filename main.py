import configparser
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from RecipeScreen import RecipeScreen
from MaterialScreen import MaterialScreen
from MainScreenButton import MainScreenButton
from MainScreenVoice import MainScreenVoice

class MyApp(App):
    def build(self):
        self.title = 'Smart Kitchen System'

        screen_manager = ScreenManager()
        mainScreenButton = MainScreenButton(name='main_screen_button')
        mainScreenVoice = MainScreenVoice(name='main_screen_voice')
        recipeScreen = RecipeScreen(name='recipe_screen')
        materialScreen = MaterialScreen(name='material_screen')

        screen_manager.add_widget(mainScreenButton)
        screen_manager.add_widget(mainScreenVoice)
        screen_manager.add_widget(recipeScreen)
        screen_manager.add_widget(materialScreen)

        mode = self.getMode()

        if mode == 'button':
            screen_manager.current = 'main_screen_button'
        else:
            screen_manager.current = 'main_screen_voice'

        return screen_manager

    def getMode(self):
        config = configparser.ConfigParser()
        config.read('user/settings.ini')
        mode = config.get('Control', 'mode')

        return mode


if __name__ == '__main__':
    MyApp().run()
