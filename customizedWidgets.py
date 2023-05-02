from kivy.uix.button import Button
from kivy.uix.label import Label

class cLabel(Label):
    def __init__(self, **kwargs):
        super(cLabel, self).__init__(**kwargs)
        self.font_name = 'malgun.ttf'