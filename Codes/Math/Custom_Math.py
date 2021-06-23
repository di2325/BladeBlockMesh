import math


def Sin(angle):
    return math.sin(math.radians(angle))


def ASin(sin):
    return math.degrees(math.asin(sin))


def Cos(angle):
    return math.cos(math.radians(angle))


def ACos(cos):
    return math.degrees(math.acos(cos))


def triangle_rad(a, b):
    return math.sqrt((a ** 2) + (b ** 2))


def triangle_side(c, a):
    return math.sqrt((c ** 2) - (a ** 2))
