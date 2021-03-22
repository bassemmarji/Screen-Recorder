from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from applogger import applogger

class NavigationScreen(Screen):
    Builder.load_file("./static/kv/navigationscreen.kv")

    def __init__(self):
        super(NavigationScreen, self).__init__()
        from kivy.app import App
        app = App.get_running_app()
        f_path = app.user_data_dir
        applogger().logger.info('User Data Directory:{path}' .format(path=f_path))
        #print("User Data Dir =",f_path)


