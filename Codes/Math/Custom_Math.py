import math


def Sin(angle):
    return math.sin(math.radians(angle))


def ASin(sin):
    return math.degrees(math.asin(sin))


def Cos(angle):
    return math.cos(math.radians(angle))


def ACos(cos):
    return math.degrees(math.acos(cos))


def new_x(x, z, angle):
    return round(x * Cos(angle) - z * Sin(angle), 4)


def new_z(x, z, angle):
    return round(z * Cos(angle) + x * Sin(angle), 4)


def rotate_on_angle(coord, angle):
    return (new_x(coord[0], coord[2], angle),
            coord[1],
            new_z(coord[0], coord[2], angle))
