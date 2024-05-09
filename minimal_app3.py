from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label  import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget  import Widget

from kivy.config import Config
Config.set('graphics', 'resizable', True)

class CountLabel(Label):
    def __init__(self, **kwargs):
        super(CountLabel, self).__init__(**kwargs)
        self.count = 0
        self.update_text()

    def increase_count(self):
        self.count += 1
        self.update_text()

    def update_text(self):
        self.text = f'default'

class MyCounterApp(App):
    def build(self):
        grid = GridLayout()
        grid.cols = 1
        self.count_label = CountLabel()
        self.text_input  = TextInput(multiline=False)
        button      = Button(text="set label.text to input.text")
        button.bind(on_press=self.button_callback)
        grid.add_widget(self.count_label)
        grid.add_widget(self.text_input)
        grid.add_widget(button)
        return grid 

    def button_callback(self, obj):
        self.count_label.text = self.text_input.text

if __name__ == "__main__":
    MyCounterApp().run()
