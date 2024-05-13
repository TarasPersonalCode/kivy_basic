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

BUFF_SIZE = 4096

class MyCounterApp(App):
    def build(self):
        self.data_dir = self.user_data_dir
        root_widget = self.build_root_widget()
        return root_widget

    def build_root_widget(self):
        grid = GridLayout()
        grid.cols = 1
        self.info_label = Label(text=f'enter IP:PORT in the window below\ndata_dir = {self.data_dir}')
        self.ip_input       = TextInput(multiline=False, text='146.168.100.42:16771')
        self.request_input  = TextInput(multiline=False, text='Farewell to Erin - Mandolin and Bodhrán')
        button      = Button(text="process video")
        button.bind(on_press=self.button_callback)
        grid.add_widget(self.info_label)
        grid.add_widget(self.ip_input)
        grid.add_widget(self.request_input)
        grid.add_widget(button)
        return grid 

    def button_callback(self, obj):
        self.send_request(obj)
        self.write_random_file(obj)
        self.read_file(obj)

    def send_request(self, obj):
        client = socket.socket()
        IP, PORT = self.ip_input.text.split(':')
        client.connect((str(IP), int(PORT)))
        nm = NetworkManager(client, BUFF_SIZE)
        nm.send({"query": self.request_input.text, "add_video": False, "high_quality": False})
        video_meta = nm.recv()
        self.info_label.text += '\n' + video_meta['filename']
        nm.file_receive(f'{self.data_dir}/{video_meta["filename"]}')
        nm.close()

    def write_random_file(self, obj):
        pathlib.Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        with open(f'{self.data_dir}/text.txt', 'w') as f:
            f.write('Hello world!')
        if platform == 'android':
            shared_path = SharedStorage().copy_to_shared(f'{self.data_dir}/text.txt')
            self.info_label.text += '\n' + str(shared_path)

    def read_file(self, obj):
        with open(f'{self.data_dir}/text.txt', 'r') as f:
            line = f.readline().strip()
            self.info_label.text += '\n' + line

if __name__ == "__main__":
    MyCounterApp().run()
