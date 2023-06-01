from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from DB import mysqlDB

from customizedWidgets import cButton
from customizedWidgets import cLabel
from screen.MaterialShow import MaterialShow


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
            button = cButton(text=material, size_hint_y=None, size=(100, 250), background_normal=f'img/material/{material}.png')
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
            # Handle the case when the 'recipe' screen object does not exist
            print("The 'material' screen does not exist.")

        MaterialShowScreen = MaterialShow(Name)
        self.manager.add_widget(MaterialShowScreen)
        self.manager.current = 'material'