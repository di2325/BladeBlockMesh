import math


def Sin(angle):
    return math.sin(math.radians(angle))


def ASin(sin):
    return math.degrees(math.asin(sin))


def Cos(angle):
    return math.cos(math.radians(angle))


def ACos(cos):
    return math.degrees(math.acos(cos))


def square_rad(c):
    return c / math.sqrt(2)


def triangle_rad(a, b):
    return math.sqrt((a ** 2) + (b ** 2))


def triangle_side(c, a):
    return math.sqrt((c ** 2) - (a ** 2))


def shell_side(rad):
    return rad * Cos(45)
