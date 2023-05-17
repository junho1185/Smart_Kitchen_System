from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class GUIApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0  # Counter variable

    def build(self):
        Window.fullscreen = 'auto'  # Set the window to open in fullscreen mode

        layout = BoxLayout(orientation='vertical', spacing=10)  # Main layout
        button = Button(text="Click Me", font_size=30, size_hint=(0.5, 0.5))  # Button to increment count
        button.bind(on_press=self.increment_counter)  # Bind button press event to increment counter

        layout.add_widget(button)

        return layout

    def increment_counter(self, instance):
        self.count += 1
        button = self.root.children[0]  # Get reference to the button
        button.text = f"Button Pressed: {self.count}"


if __name__ == '__main__':
    GUIApp().run()
