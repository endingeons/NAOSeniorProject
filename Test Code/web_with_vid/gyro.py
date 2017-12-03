from naoqi import ALProxy
import almath

def moveHead(arg, ip):
    print(arg)
    argRad = int(arg) * 3.14 / 180
    moProx = ALProxy("ALMotion", ip, 9559)
    moProx.setStiffnesses("Head", 1.0)
    if abs(int(arg)) < 60:
        moProx.angleInterpolation("HeadYaw", argRad, 1, True)
