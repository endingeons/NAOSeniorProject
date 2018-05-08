import cv2
from naoqi import ALProxy
import vision_definitions
from PIL import Image
import StringIO


class VideoCamera(object):
    def __init__(self, ip, res, fps):

        IP = str(ip)  # Replace here with your NAOqi's IP address.
        PORT = 9559
        res = str(res)
        self.camProxy = ALProxy("ALVideoDevice", IP, PORT)  # establishes a proxy to naos camera

        # choose appropriate resolution
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
            resolution = vision_definitions.kQQVGA

        colorSpace = vision_definitions.kRGBColorSpace

        # subscribe to naos camera
        self.nameId = self.camProxy.subscribe("python_GVM", resolution, colorSpace, int(fps))

    def __del__(self):
        self.camProxy.unsubscribe(self.nameId)
    
    def get_frame(self):
        naoImage = self.camProxy.getImageRemote(self.nameId)

        # Get the image size and pixel array.
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]

        # Create a PIL Image from our pixel array.
        im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
        buf = StringIO.StringIO()
        im.save(buf, format='PNG')
        jpeg = buf.getvalue()
        return jpeg
