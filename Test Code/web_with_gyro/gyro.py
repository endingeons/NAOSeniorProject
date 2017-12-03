from naoqi import ALProxy

def moveHead(argZ, argY, ip):
    print("Y: ")
    print(argY)
    print("Z: ")
    print(argZ)
    argYRad = int(argY) * 3.14 / 180
    argZRad = int(argZ) * 3.14 / 180
    moProx = ALProxy("ALMotion", ip, 9559)
    moProx.setStiffnesses("Head", 1.0)
    names = ["HeadPitch", "HeadYaw"]
    angles = [argYRad, argZRad]
    times = [.5, .5]
    if (abs(int(argY)) < 25) and (abs(int(argZ)) < 90):
        moProx.angleInterpolation(names, angles, times, True)
    moProx.setStiffnesses("Head", 0.0)
