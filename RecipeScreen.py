from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton


class RecipeScreen(Screen):
    def __init__(self, **kwargs):
        super(RecipeScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=30)
        hLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.scrollContent = GridLayout(cols=3, size_hint_y=None, pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                        spacing=30, padding=30)
        self.scrollContent.bind(minimum_height=self.scrollContent.setter('height'))

        cLayout = self.content_layout()

        backButton = Button(text='Back', size_hint=(0.15, 0.7), pos_hint={'center_x':0.5, 'center_y':0.5})
        nameLabel = Label(text='Choose a Recipe!', size_hint=(0.7, 1))

        backButton.bind(on_press=self.switchMain)

        hLayout.add_widget(backButton)
        hLayout.add_widget(nameLabel)

        layout.add_widget(hLayout)
        layout.add_widget(cLayout)

        self.add_widget(layout)

    def content_layout(self):
        layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        scrollLayout = ScrollView(do_scroll_x=False)
        button_column = BoxLayout(orientation='vertical', size_hint=(0.2, 1), spacing=30)
        
        korean_button = ToggleButton(text='Korean', group='food_group', on_press=self.switchScrollContent)
        japanese_button = ToggleButton(text='Japanese', group='food_group', on_press=self.switchScrollContent)
        chinese_button = ToggleButton(text='Chinese', group='food_group', on_press=self.switchScrollContent)
        western_button = ToggleButton(text='Western', group='food_group', on_press=self.switchScrollContent)

        button_column.add_widget(korean_button)
        button_column.add_widget(japanese_button)
        button_column.add_widget(chinese_button)
        button_column.add_widget(western_button)

        scrollLayout.add_widget(self.scrollContent)

        layout.add_widget(button_column)
        layout.add_widget(scrollLayout)
        return layout

    def switchMain(self, *args):
        self.manager.current = 'main_screen'
    def switchScrollContent(self, button):
        self.scrollContent.clear_widgets()

        if button.text == 'Korean':
            for i in range(10):
                button = Button(text=f'Korean dish {i}', size_hint=(0.3, None), size=(100, 300))
                self.scrollContent.add_widget(button)
        elif button.text == 'Japanese':
            for i in range(10):
                button = Button(text=f'Japanese dish {i}', size=(100, 100))
                self.scrollContent.add_widget(button)
        elif button.text == 'Chinese':
            for i in range(10):
                button = Button(text=f'Chinese dish {i}', size=(100, 100))
                self.scrollContent.add_widget(button)
        else:
            for i in range(10):
                button = Button(text=f'Western dish {i}', size=(100, 100))
                self.scrollContent.add_widget(button)