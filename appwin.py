from kivy.app import App
from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from startupscreen import StartupScreen

class APPWin(App):
    """This is the Main Window Application class"""

    title = "Screen Recorder"
    date = None
    screens = ObjectProperty()
    item_selection = DictProperty()

    def __init__(self, **kwargs):
        super(APPWin, self).__init__(**kwargs)

    def build(self):
        from kivy.utils import platform

        if platform == "android":
            pass
            # from android import loadingscreen
            #loadingscreen.hide_loading_screen()

        self.use_kivy_settings = False
        Window.bind(on_keyboard=self.key_input)
        sm = ScreenManager()
        return sm

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True  # override the default behaviour
        else:  # the key now does nothing
            return False

    def build_config(self, config):
        """Set default settings for the application
            Mode       : Whether Dark or Light mode
        """
        config.setdefaults(
            "CustSettings",
            {"Mode": "Light"},
        )

    def on_start(self):
        """On Application start show the startup screen"""
        ss = StartupScreen()
        self.root.add_widget(ss)
        self.root.current = "StartupScreen"


