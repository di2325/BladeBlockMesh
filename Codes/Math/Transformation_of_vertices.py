"""
This file contains functions for various manipulations with vertices

    get_airfoil_data            returns vertices and splines from airfoil files

    create_square               returns four coordinates from z position and length of a side
"""
import os


def get_airfoil_data(airfoil_number):
    # Declaration of variables
    coord = []
    index = []
    top = []
    bot = []

    # Searching for airfoil files
    for line in open(os.path.abspath(f'../Coordinates/airfoil{airfoil_number}'), "r"):
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
    boundary_right = [most_right[0] + 0.1 *
                      (most_left[0] - most_right[0]),
                      (most_left[1] + most_right[1]) / 2,
                      (most_left[2] + most_right[2]) / 2]

    boundary_left = [most_right[0] + 0.95 *
                     (most_left[0] - most_right[0]),
                     (most_left[1] + most_right[1]) / 2,
                     (most_left[2] + most_right[2]) / 2]

    # Finding boundary points
    delta = 1000
    for line in top:
        if delta > abs(boundary_right[0] - line[0]):
            top_right = line
            delta = abs(boundary_right[0] - line[0])
    delta = 1000
    for line in bot:
        if delta > abs(boundary_right[0] - line[0]):
            bot_right = line
            delta = abs(boundary_right[0] - line[0])
    delta = 1000
    for line in top:
        if delta > abs(boundary_left[0] - line[0]):
            top_left = line
            delta = abs(boundary_left[0] - line[0])
    delta = 1000
    for line in bot:
        if delta > abs(boundary_left[0] - line[0]):
            bot_left = line
            delta = abs(boundary_left[0] - line[0])

    # Brining back most_left and most_right points
    top.append(most_left)
    bot.append(most_right)

    # Creating splines
    top_spline = []
    left_spline = []
    right_spline = []
    bot_spline = []

    # Dividing top and bot to bot_right/bot_left/top_right/top_left
    for line in bot:
        if line[0] < bot_right[0]:
            right_spline.append(line)
        elif bot_left[0] > line[0] > bot_right[0]:
            bot_spline.append(line)

    for line in top:
        if line[0] > top_left[0]:
            left_spline.append(line)

    for line in top:
        if line[0] < top_right[0]:
            right_spline.append(line)
        elif top_left[0] > line[0] > top_right[0]:
            top_spline.append(line)

    for line in bot:
        if line[0] > bot_left[0]:
            left_spline.append(line)

    # Saves vertices to verts and IDs to verts_id
    verts = [top_right, bot_right, bot_left, top_left]
    splines = [top_spline, left_spline, bot_spline, right_spline]

    return verts, splines


def create_square(length, z):
    length /= 2
    return [(-length,  length, z),
            (-length, -length, z),
            ( length, -length, z),
            ( length,  length, z)]
