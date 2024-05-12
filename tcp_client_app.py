import pathlib
import socket
import threading
import time

from os import urandom

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label  import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget  import Widget
from kivy.utils import platform

from network_.manager import NetworkManager

if platform == 'android':
    from androidstorage4kivy import SharedStorage
    from android import api_version
    from android import mActivity, autoclass

from kivy.config import Config
Config.set('graphics', 'resizable', True)

IP = '146.168.100.42'
PORT = 16770

BUFF_SIZE = 16

class MyCounterApp(App):
    def build(self):
        Logger.info("lalala amznsdf3")
        # Logger.info("lalala amznsdf3 api_version: " + str(api_version))
        # Logger.info("lalala amznsdf3 application_dir: " + str(mActivity.getApplicationContext().getApplicationInfo().dataDir))
        Logger.debug("lalala amznsdf4")
        self.data_dir = self.user_data_dir
        root_widget = self.build_root_widget()
        return root_widget

    def build_root_widget(self):
        grid = GridLayout()
        grid.cols = 1
        self.info_label = Label(text=f'enter IP:PORT in the window below\ndata_dir = {self.data_dir}')
        self.text_input  = TextInput(multiline=False, text='146.168.100.42:16771')
        button      = Button(text="send random bytes")
        button.bind(on_press=self.button_callback)
        grid.add_widget(self.info_label)
        grid.add_widget(self.text_input)
        grid.add_widget(button)
        return grid 

    def button_callback(self, obj):
        Logger.info( "kivyyvik: button_push1")
        Logger.debug("kivyyvik: button_push2")
        self.send_random_bytestring(obj)
        self.write_random_file(obj)
        self.read_file(obj)

    def send_random_bytestring(self, obj):
        client = socket.socket()
        IP, PORT = self.text_input.text.split(':')
        client.connect((str(IP), int(PORT)))
        nm = NetworkManager(client, BUFF_SIZE)
        nm.send(("lalalo;", {'my': 'face', 1: 2}))
        # nm.send("lalalo;")
        nm.close()

    def write_random_file(self, obj):
        pathlib.Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        with open(f'{self.data_dir}/text.txt', 'w') as f:
            f.write('Hello world!')
        if platform == 'android':
            shared_path = SharedStorage().copy_to_shared(f'{self.data_dir}/text.txt')
            self.info_label.text += '\n' + str(shared_path)
            Logger.info( "kivyyvik_shared_storage1 " + str(shared_path))
            Logger.info( "kivyyvik_shared_storage2 " + str(shared_path.getPath()))

    def read_file(self, obj):
        with open(f'{self.data_dir}/text.txt', 'r') as f:
            line = f.readline().strip()
            self.info_label.text += '\n' + line

if __name__ == "__main__":
    MyCounterApp().run()
