from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from DB import mysqlDB
from shelves import shelves
from customizedWidgets import cLabel, setting
from kivy.clock import Clock
import time


class MaterialShow(Screen):
    def __init__(self, materialName, **kwargs):
        super(MaterialShow, self).__init__(**kwargs)
        self.materialName = materialName
        self.name = 'material'
        layout = BoxLayout(orientation='vertical')
        centerLabel = cLabel(text=materialName+'을 꺼내는 중입니다...', pos_hint={'center_x':0.5, 'center_y':0.5}, font_size=25)
        layout.add_widget(centerLabel)
        self.add_widget(layout)
        self.rotateShelf()

    def rotateShelf(self):
        db = mysqlDB()
        position = db.getPosition(self.materialName)
        sh = shelves([position])
        sh.rotate()
        Clock.schedule_once(self.switchMain(), 0)

    def switchMain(self, *args):
        S = setting()
        mode = S.getMode()
        if mode == 'button':
            self.manager.current = 'main_screen_button'
        else:
            self.manager.current = 'main_screen_voice'