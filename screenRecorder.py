import pyautogui
import cv2
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
import os
from PIL import ImageGrab
from applogger import applogger

class RecordClass:
    #Specify Resolution / Get it From OS Settings / SCREEN_SIZE
    #You need to get the correct SCREEN_SIZE from your operating system.
    #You can use pyautogui.size() function to get the size of the primary monitor
    resolution       = None
    foldername       = None
    filename         = None
    framepersec      = None
    sched            = None
    out              = None
    windowName       = None

    def __init__(self,**kwargs):
        try:
            self.resolution  = ImageGrab.grab().size
            self.foldername  = kwargs.get('foldername')
            self.filename    = kwargs.get('filename')
            self.framepersec = int(kwargs.get('frame_per_sec'))

            self.filename = os.path.join(self.foldername,self.filename)
            if os.path.exists(self.filename):
                os.remove(self.filename)

            self.windowName  = "Screen Recorder"
            #print("File Name = "    ,self.filename)
            #print("Frame Per Sec = ",self.framepersec)

            self.sched = BackgroundScheduler()
            #Define the video codec
            self.codec = cv2.VideoWriter_fourcc(*"XVID")
            #Create the video write object
            self.out = cv2.VideoWriter(self.filename, self.codec, self.framepersec, self.resolution)
            #Create an Empty Window
            cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
            #Resize this window
            cv2.resizeWindow(self.windowName, 480, 270)


            #self.sched.add_job(self.record, 'interval', seconds=5)
            #self.sched.start()
        except Exception as e:
            print("Error: ", __name__, " Exception ", e)
            applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__, Exception = e))

    def stop_recording(self):
        try:
             self.out.release()
             cv2.destroyAllWindows()
             self.sched.shutdown()
        except Exception as e:
             print("Error: ", __name__, " Exception ", e)
             applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__, Exception = e))



    def record(self):
            try:
                #while continue_capture == 1:
                #make a screenshot
                img = pyautogui.screenshot()
                #convert these pixels to a proper numpy array to work with OpenCV
                frame = np.array(img)
                #convert colors from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #write the frame
                self.out.write(frame)
                #show the frame
                cv2.imshow(self.windowName, frame)
                #if cv2.waitKey(1) == ord("q"):
                #      break
                #make sure everything is closed when exited
                #cv2.destroyAllWindows()
                #out.release()
            except Exception as e:
                print("Error: ", __name__, " Exception ", e)
                applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__, Exception = e))

    def start_recording(self):
            try:
                #print(1)
                self.sched.add_job(self.record,'interval',seconds=0.5)
                #print(2)
                self.sched.start()
            except Exception as e:
                print("Error: ", __name__, " Exception ", e)
                applogger().logger.error('{ModuleName} - Error = {Exception}'.format(ModuleName=__name__, Exception = e))
