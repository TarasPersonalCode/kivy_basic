import json
import os
import pathlib
import random
import socket
import threading
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label  import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget  import Widget
from kivy.utils import platform

from network_.manager import NetworkManager
from network_.file_receiver import NetworkFileReceiver

if platform == 'android':
    from androidstorage4kivy import SharedStorage
    from android import api_version
    from android import mActivity, autoclass
    

from kivy.config import Config
Config.set('graphics', 'resizable', True)

with open('./network_/config.json', 'r') as f:
    cfg = json.load(f)
IP        = cfg['IP']
PORT      = cfg['PORT']
BUFF_SIZE = cfg['BUFF_SIZE']

class SharingApp(App):
    def build(self):
        root_widget = self.build_root_widget()
        # self.start_service()
        self.button_locked = False
        print(f"[***] {self.user_data_dir=}")
        return root_widget

    def start_service(self):
        if platform == "android":
            SERVICE_NAME = u"org.test.panzavantazhenko.ServiceMyservice" 
            service = autoclass(SERVICE_NAME)
            mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            service.start(mActivity, '')

    def build_root_widget(self):
        grid = GridLayout()
        grid.cols = 1
        # initialize widgets
        self.info_label     = Label(text=f'enter IP:PORT in the window below')
        self.ip_input       = TextInput(multiline=False, text=f'{IP}:{PORT}')
        self.request_input  = TextInput(multiline=False, text='Farewell to Erin - Mandolin and Bodhrán')
        
        self.toggles = GridLayout()
        self.toggles.cols = 2
        self.quality_toggle = ToggleButton(text="Toggle for higher quality", group='quality')
        self.video_toggle   = ToggleButton(text="Toggle to add video",       group='video')
        self.toggles.add_widget(self.quality_toggle)
        self.toggles.add_widget(self.video_toggle)
        button              = Button(text="Request")
        # button bind
        button.bind( on_press=self.button_callback)
        # add widgets
        grid.add_widget(self.info_label)
        grid.add_widget(self.ip_input)
        grid.add_widget(self.request_input)
        grid.add_widget(self.toggles)
        grid.add_widget(button)
        return grid 

    def button_callback(self, obj):
        if not self.button_locked:
            self.button_locked = True
            self.info_label.text = 'Request sent, waiting on server...'
            self.send_request(obj)
            self.receive_file_meta(obj)
            self.receive_file(obj)
        else:
            self.info_label.text = "Button locked, please wait"

    def send_request(self, obj):
        client = socket.socket()
        IP, PORT = self.ip_input.text.split(':')
        client.connect((str(IP), int(PORT)))
        self.nm = NetworkManager(client, BUFF_SIZE)
        self.nm.send({"query": self.request_input.text, 
                      "add_video": self.video_toggle.state == "down", 
                      "high_quality": self.quality_toggle.state == "down"})

    def receive_file_meta(self, obj):
        file_meta = self.nm.recv()
        self.filename = file_meta["filename"]
        self.filesize = file_meta["filesize"]
        self.private_filepath = f'{self.user_data_dir}/{self.filename}'

    def receive_file(self, obj):
        nfr = NetworkFileReceiver(self.nm, self.private_filepath, 10)
        Clock.schedule_interval(lambda dt: nfr.receive_batch(), 0.03)
        Clock.schedule_interval(lambda dt: self.update_progress(), 0.2)
        Clock.schedule_interval(lambda dt: self.move_file_to_shared(), 0.2)
        Clock.schedule_interval(lambda dt: self.unlock_button(), 0.2)

    def update_progress(self):
        cursize = os.path.getsize(self.private_filepath)
        self.info_label.text = f"Progress: {round(cursize / self.filesize, 2)}"
        if cursize == self.filesize:
            return False

    def move_file_to_shared(self):
        self.checkpoint_frac = 0.1
        self.checkpoint_count = 0
        cursize = os.path.getsize(self.private_filepath)
        curfrac = cursize / self.filesize
        if int(curfrac / self.checkpoint_frac) > self.checkpoint_count:
            self.checkpoint_count = int(curfrac / self.checkpoint_frac)
            if platform == 'android':
                Environment = autoclass('android.os.Environment')
                shared_path = SharedStorage().copy_to_shared(self.private_filepath,
                                                             collection=Environment.DIRECTORY_DOWNLOADS)

        if cursize == self.filesize:
            self.info_label.text = 'Done'
            return False

    def unlock_button(self):
        cursize = os.path.getsize(self.private_filepath)
        if cursize == self.filesize:
            self.button_locked = False
            return False

if __name__ == "__main__":
    SharingApp().run()
