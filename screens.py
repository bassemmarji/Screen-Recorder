from kivy.factory import Factory
from kivy.lang import Builder
import os

class Screens(object):
    primary_widget = None
    app = ""
    current_screen = 'None'

    data = {
        'MainScreen':
            {'kv_content': "",
             'Factory': 'Factory.MainScreen(app=self.app)',
             'name_screen': 'MainScreen',
             'object': None}
    }

    def show_screen(self, name_screen, **kwargs):

        #print("name_screen",name_screen)

        if self.current_screen == name_screen:
            return
        if not self.data[name_screen]['object']:
            if name_screen == 'MainScreen':
                from MainScreen import mainscreen_kv, MainScreen
                self.data[name_screen]['kv_content'] = mainscreen_kv

            if os.path.isfile(mainscreen_kv):
                Builder.load_file(self.data[name_screen]['kv_content'])
            else:
                Builder.load_string(self.data[name_screen]['kv_content'])

            self.data[name_screen]['object'] = eval(self.data[name_screen]['Factory'])
            self.primary_widget.ids.scrn_mgr.add_widget(self.data[name_screen]['object'])

        self.primary_widget.ids.scrn_mgr.current = self.data[name_screen]['name_screen']
        self.current_screen = name_screen




