from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label  import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget  import Widget

class CountLabel(Label):
    def __init__(self, **kwargs):
        super(CountLabel, self).__init__(**kwargs)
        self.count = 0
        self.update_text()

    def increase_count(self):
        self.count += 1
        self.update_text()

    def update_text(self):
        self.text = f'count: {self.count}'

class MyCounterApp(App):
    def build(self):
        parent = Widget()
        grid = GridLayout(cols=1)
        self.count_label = CountLabel()
        text_input  = TextInput(multiline=False)
        button      = Button(text="Increase count by 1")
        button.bind(on_press=self.button_callback)
        grid.add_widget(self.count_label)
        grid.add_widget(text_input)
        grid.add_widget(button)
        parent.add_widget(grid)
        return parent

    def button_callback(self, obj):
        self.count_label.increase_count()

if __name__ == "__main__":
    MyCounterApp().run()
