"""
This file contains functions for various manipulations with vertices

    get_airfoil_data            returns vertices and splines from airfoil files

    create_square               returns four coordinates from z position and length of a side
"""
import os
from Codes.Math.Custom_Math import *


def get_airfoil_data(airfoil_name, b0=0.62, b1=0.30):
    # Declaration of variables
    coord = []
    index = []
    top = []
    bot = []

    # Searching for airfoil files
    for line in open(os.path.abspath(f'../Coordinates/{airfoil_name}'), "r"):
        # Assign Coordinates
        if line.startswith('v'):
            coord.append((round(float(line.split()[1]), 4),
                          round(float(line.split()[2]), 4),
                          round(-1.0 * float(line.split()[3]), 4)))
        # Assign Indices
        elif line.startswith('l'):
            index.append((int(line.split()[1]) - 1, int(line.split()[2]) - 1))

    # Finding most left and right points
    most_right = (1000, 0, 0)
    most_left = (-1000, 0, 0)
    for line in coord:
        if line[0] < most_right[0]:
            most_right = line
        if line[0] > most_left[0]:
            most_left = line

    # Keeping compiler happy
    current_point = 0
    previous_point = 0

    # Finding upper point from MostRight
    for line in index:
        if coord[line[0]] == most_right:
            if coord[line[1]][1] > most_right[1]:
                previous_point = most_right
                current_point = coord[line[1]]
                break
        if coord[line[1]] == most_right:
            if coord[line[0]][1] > most_right[1]:
                previous_point = most_right
                current_point = coord[line[0]]
                break

    # Assign coordinates to Top and Bot
    on_top = True
    while True:
        if on_top:
            top.append(current_point)
        for line in index:
            if coord[line[0]] == current_point:
                if coord[line[1]] != previous_point:
                    previous_point = current_point
                    current_point = coord[line[1]]
                    break
            if coord[line[1]] == current_point:
                if coord[line[0]] != previous_point:
                    previous_point = current_point
                    current_point = coord[line[0]]
                    break
        if current_point == most_right:
            break
        if not on_top:
            bot.append(current_point)
        elif current_point == most_left:
            on_top = False

    # Calculate Center point for the front circle
    boundary_0 = [most_right[0] + b0 *
                  (most_left[0] - most_right[0]),
                  (most_left[1] + most_right[1]) / 2,
                  (most_left[2] + most_right[2]) / 2]

    boundary_1 = [most_right[0] + b1 *
                  (most_left[0] - most_right[0]),
                  (most_left[1] + most_right[1]) / 2,
                  (most_left[2] + most_right[2]) / 2]

    top_vert_0 = 0
    bot_vert_0 = 0
    top_vert_1 = 0
    bot_vert_1 = 0

    # Finding boundary points
    delta = 1000
    for line in top:
        if delta > abs(boundary_0[0] - line[0]):
            top_vert_0 = line
            delta = abs(boundary_0[0] - line[0])
    delta = 1000
    for line in bot:
        if delta > abs(boundary_0[0] - line[0]):
            bot_vert_0 = line
            delta = abs(boundary_0[0] - line[0])
    delta = 1000
    for line in top:
        if delta > abs(boundary_1[0] - line[0]):
            top_vert_1 = line
            delta = abs(boundary_1[0] - line[0])
    delta = 1000
    for line in bot:
        if delta > abs(boundary_1[0] - line[0]):
            bot_vert_1 = line
            delta = abs(boundary_1[0] - line[0])

    # Creating splines
    spline_zero = []
    spline_one = []
    spline_two = []
    spline_three = []
    spline_four = []
    spline_five = []

    # Dividing top and bot
    for line in top:
        if line[0] < top_vert_1[0]:
            spline_two.append(line)
        elif top_vert_0[0] > line[0] > top_vert_1[0]:
            spline_one.append(line)
        elif line[0] > top_vert_0[0]:
            spline_zero.append(line)

    for line in bot:
        if line[0] < bot_vert_1[0]:
            spline_three.append(line)
        elif bot_vert_0[0] > line[0] > bot_vert_1[0]:
            spline_four.append(line)
        elif line[0] > bot_vert_0[0]:
            spline_five.append(line)

    # Saves vertices to verts and IDs to verts_id
    verts = [most_left, top_vert_0, top_vert_1, most_right, bot_vert_1, bot_vert_0]
    splines = [spline_zero, spline_one, spline_two, spline_three, spline_four, spline_five]

    return verts, splines


def create_square(length, z):
    length /= 2
    return [(-length, length, z),
            (-length, -length, z),
            (length, -length, z),
            (length, length, z)]


def new_x(x, z, angle):
    return round(x * Cos(angle) - z * Sin(angle), 4)


def new_z(x, z, angle):
    return round(z * Cos(angle) + x * Sin(angle), 4)


def rotate_on_angle(coord, angle):
    if type(coord[0]) != list and type(coord[0]) != tuple:
        return (new_x(coord[0], coord[2], angle),
                coord[1],
                new_z(coord[0], coord[2], angle))
    else:
        output = []
        for i in range(len(coord)):
            output.append((new_x(coord[i][0], coord[i][2], angle),
                           coord[i][1],
                           new_z(coord[i][0], coord[i][2], angle)))
        return output
