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
        grid = GridLayout()
        grid.cols = 1
        self.info_label = Label(text='enter IP:PORT in the window below')
        self.text_input  = TextInput(multiline=False)
        button      = Button(text="send random bytes")
        button.bind(on_press=self.button_callback)
        grid.add_widget(self.info_label)
        grid.add_widget(self.text_input)
        grid.add_widget(button)
        return grid 

    def button_callback(self, obj):
        client = socket.socket()
        IP, PORT = self.text_input.text.split(':')
        client.connect((str(IP), int(PORT)))
        byte = urandom(BUFF_SIZE)
        client.send(byte)
        client.close()
    
if __name__ == "__main__":
    MyCounterApp().run()
