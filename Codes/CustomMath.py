import math


def Sin(angle):
    return math.sin(math.radians(angle))


def ASin(sin):
    return math.degrees(math.asin(sin))


def Cos(angle):
    return math.cos(math.radians(angle))


def ACos(cos):
    return math.degrees(math.acos(cos))


def NewX(x, z, angle):
    return round(x * Cos(angle) - z * Sin(angle), 4)


def NewZ(x, z, angle):
    return round(z * Cos(angle) + x * Sin(angle), 4)


def RotateOnAngle(coord, angle):
    return (NewX(coord[0], coord[2], angle), \
            coord[1], \
            NewZ(coord[0], coord[2], angle))
