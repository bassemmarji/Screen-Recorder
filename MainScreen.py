from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from plyer import filechooser
from kivytoast import Toast
from screenRecorder import RecordClass
from screenSettings import SettingsClass
from kivy.uix.video import Video
import os
from applogger import applogger

mainscreen_kv = "./static/kv/mainscreen.kv"

class MainScreen(Screen):
    foldername      = ""
    filename        = ""
    frame_per_sec   = ""

    sr              = None
    ss              = None
    video           = None
    logger          = None
    def __init__(self, **kwargs):
        self.name = 'MainScreen'
        super(MainScreen, self).__init__()
        from kivy.app import App
        app = App.get_running_app()
        self.ids.select_folder_label.text    = app.config.get("CustSettings", "defaultFolder")
        self.ids.frame_per_sec.text          = app.config.get("CustSettings", "framePerSec")
        self.ids.file_name.text              = app.config.get("CustSettings", "defaultFileName")

        MSToolbar = self.ids.MainScreen_Toolbar
        MSToolbar.left_action_items  = [["play"              ,self.play_video]]
        MSToolbar.right_action_items = [["file-search"       ,self.file_manager_open]
                                       ,["camera"            ,self.start_recording]
                                       ,["camera-party-mode" ,self.stop_recording ]]


        self.ss = SettingsClass()
        self.ids.screen_resolution.text = str(self.ss.get_screen_resolution())

    #def build(self):
    #    return Builder.load_string(mainscreen_kv)

    def file_manager_open(self, widget):
        raw_path = filechooser.choose_dir()
        if raw_path:
            self.ids.select_folder_label.text = raw_path[0]

    def start_recording(self,widget):
        self.foldername     = self.ids.select_folder_label.text
        self.filename       = self.ids.file_name.text
        self.frame_per_sec  = self.ids.frame_per_sec.text

        if self.foldername is None or self.foldername == "":
           Toast().toast("Please select a valid folder...")

        if self.filename is None or self.filename == "":
           Toast().toast("Please select a valid filename...")

        if self.frame_per_sec is None or self.frame_per_sec == "":
           Toast().toast("Please select a valid rate of frame per seconds...")

        try:
            if not self.sr:
               self.sr = RecordClass(foldername = self.foldername
                                    ,filename = self.filename
                                    ,frame_per_sec = self.frame_per_sec)

            self.sr.start_recording()
        except Exception as e:
            print("Error: ", __name__, " Exception ", e)
            applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__, Exception = e))

    def stop_recording(self,widget):
        try:
            if self.sr:
               self.sr.stop_recording()
        except Exception as e:
            print("Error: ", __name__, " Exception ", e)
            applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__, Exception = e))

    def play_video(self,widget):
        try:
            self.foldername     = self.ids.select_folder_label.text
            self.filename       = self.ids.file_name.text

            if self.foldername is None or self.foldername == "":
                Toast().toast("Please select a valid folder...")

            if self.filename is None or self.filename == "":
                Toast().toast("Please select a valid filename...")

            self.filename = os.path.join(self.foldername, self.filename)

            if self.video:
               self.ids.videoContainer.remove_widget(self.video)
               self.video = None

            self.video = Video()
            self.video.source = self.filename
            self.video.state = 'play'
            #self.video.options = {'eos':'stop'}
            self.video.bind(eos=self.VideoDone)
            self.video.allow_stretch = True
            self.ids.videoContainer.add_widget(self.video)
        except Exception as e:
            print("Error: ", __name__, " Exception ", e)
            applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__, Exception = e))

    def VideoDone(self,value,value2):
        #print("video Done",value,value2)
        self.video.state = 'stop'
        self.video.unload()
        applogger().logger.info('{ModuleName} - {Message}'.format(ModuleName=__name__,Message="video completed successfully"))