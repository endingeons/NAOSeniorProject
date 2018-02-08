from naoqi import ALProxy
import almath

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
    times = [.5, .5]

    # normal case
    if (abs(int(argY)) < 25) and (abs(int(argZ)) < 90):
        angles = [argYRad, argZRad]
        moProx.angleInterpolation(names, angles, times, True)

    # if y is outside of bounds
    elif (abs(int(argY)) > 25) and (abs(int(argZ)) < 90):
        if int(argY) < 0:
            angles = [-25 * 3.14 / 180, argZRad]
        elif int(argY) > 0:
            angles = [25 * 3.14 / 180, argZRad]
        moProx.angleInterpolation(names, angles, times, True)

    # if z is outside of bounds
    elif (abs(int(argY)) < 25) and (abs(int(argZ)) > 90):
        if int(argZ) < 0:
            angles = [argY, -90 * 3.14 / 180]
        elif int(argZ) > 0:
            angles = [argY, 90 * 3.14 / 180]
        moProx.angleInterpolation(names, angles, times, True)

    # if both are outside of bounds
    elif (abs(int(argY)) > 25) and (abs(int(argZ)) > 90):
        if int(argY) < 0 and int(argZ) < 0:
            angles = [-25 * 3.14 / 180, -90 * 3.14 / 180]
        elif int(argY) < 0 and int(argZ) > 0:
            angles = [-25 * 3.14 / 180, 90 * 3.14 / 180]
        elif int(argY) > 0 and int(argZ) < 0:
            angles = [25 * 3.14 / 180, -90 * 3.14 / 180]
        elif int(argY) > 0 and int(argZ) > 0:
            angles = [25 * 3.14 / 180, 90 * 3.14 / 180]
        moProx.angleInterpolation(names, angles, times, True)

    moProx.setStiffnesses("Head", 0.0)
