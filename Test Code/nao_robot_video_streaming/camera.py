import cv2
from naoqi import ALProxy
import vision_definitions
from PIL import Image
import StringIO


class VideoCamera(object):
    def __init__(self, ip, res, fps=30):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        #self.video = cv2.VideoCapture(0)

        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        IP = ip  # Replace here with your NAOqi's IP address.
        PORT = 9559
        self.camProxy = ALProxy("ALVideoDevice", IP, PORT)
        ####
        # Register a Generic Video Module

        if res == '0':
            resolution = vision_definitions.kQQVGA  # 160 * 120
        elif res == '1':
            resolution = vision_definitions.kQVGA  # 320 * 240
        elif res == '2':
            resolution = vision_definitions.kVGA  # 640 * 480
        elif res == '3':
            resolution = vision_definitions.k4VGA  # 1280 * 960
        elif res == '7':
            resolution = vision_definitions.kQQQVGA  # 80 * 60
        elif res == '8':
            resolution = vision_definitions.kQQQQVGA  # 40 * 30
        else:
            resolution = vision_definitions.kQQQVGA

        colorSpace = vision_definitions.kRGBColorSpace

        self.nameId = self.camProxy.subscribe("python_GVM", resolution, colorSpace, int(fps))

    def __del__(self):
        #self.video.release()
        self.camProxy.unsubscribe(self.nameId)
    
    def get_frame(self):
        #success, image = self.video.read()
        naoImage=self.camProxy.getImageRemote(self.nameId)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        #ret, jpeg = cv2.imencode('.jpg', image)

        # Get the image size and pixel array.
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]

        # Create a PIL Image from our pixel array.
        im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
        buf= StringIO.StringIO()
        im.save(buf, format= 'PNG')
        jpeg= buf.getvalue()
        return jpeg

        #return jpeg.tobytes()