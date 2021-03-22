from PIL import ImageGrab
from applogger import applogger

class SettingsClass:

      def get_screen_resolution(self):
          try:
             resolution = ImageGrab.grab().size
             print("Resolution = ",resolution)
          except Exception as e:
             print("Error: ", __name__, " Exception ", e)
             applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__, Exception = e))
          return resolution
