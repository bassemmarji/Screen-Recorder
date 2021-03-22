"""
 StartupScreen:
 =============
 This is just a flash screen before displaying the main dashboard
"""

from kivy.uix.screenmanager import Screen

from kivy.app import App
from kivy.lang import Builder

class StartupScreen(Screen):
    """This screen acts as a buffer before displaying the dashbord"""

    Builder.load_file("./static/kv/startupscreen.kv")

    def __init__(self):
        super(StartupScreen, self).__init__()


    def on_enter(self, *args):
        from kivy.clock import Clock

        Clock.schedule_once(lambda dt: self.load_navigation(), 2)

    @staticmethod
    def load_navigation():
        from navigation import NavigationScreen

        """Set the app theme settings"""
        from kivymd.theming import ThemeManager

        app = App.get_running_app()
        app.theme_cls = ThemeManager()
        app.theme_cls.primary_palette = "Teal"
        app.theme_cls.accent_palette = "Amber"
        app.theme_cls.theme_style = "Light"


        from screens import Screens

        app.screens = Screens()
        app.screens.app = app

        app.screens.primary_widget = NavigationScreen()
        app.root.add_widget(app.screens.primary_widget)
        app.root.current = "NavigationScreen"


