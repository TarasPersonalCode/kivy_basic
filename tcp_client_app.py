import socket
import threading
import time

from os import urandom

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label  import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget  import Widget

from kivy.config import Config
Config.set('graphics', 'resizable', True)

IP = '146.168.100.42'
PORT = 16770

BUFF_SIZE = 16

class MyCounterApp(App):
    def build(self):
        self.data_dir = self.user_data_dir
        root_widget = self.build_root_widget()
        return root_widget

    def build_root_widget(self):
        grid = GridLayout()
        grid.cols = 1
        self.info_label = Label(text=f'enter IP:PORT in the window below\ndata_dir = {self.data_dir}')
        self.text_input  = TextInput(multiline=False)
        button      = Button(text="send random bytes")
        button.bind(on_press=self.button_callback)
        grid.add_widget(self.info_label)
        grid.add_widget(self.text_input)
        grid.add_widget(button)
        return grid 

    def button_callback(self, obj):
        self.send_random_bytestring(obj)
        self.write_random_file(obj)

    def send_random_bytestring(self, obj):
        client = socket.socket()
        IP, PORT = self.text_input.text.split(':')
        client.connect((str(IP), int(PORT)))
        byte = urandom(BUFF_SIZE)
        client.send(byte)
        client.close()

    def write_random_file(self, obj):
        with open(f'{self.data_dir}/text.txt', 'w') as f:
            f.write('Hello world!')

if __name__ == "__main__":
    MyCounterApp().run()
