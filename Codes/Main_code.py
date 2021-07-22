"""
Main code:
    Generates blockMeshDict file according to imported airfoil profiles.
    Currently, can generate only NREL 5MW wind turbine.

    Project structure:
        BladeBlockMesh              - root folder
        \_ Codes                        - contains all scripts
        \   \_ BlockMesh                    - classes, which create blockMeshDict
        \   \_ Math                         - classes for custom math methods realisation
        \   \_ Profiles                     - classes, for profile creations
        \_ Coordinates                  - contains coordinates of all airfoils
        \_ Output                       - here you will find new blockMeshDict file

    Workflow:
        * Import required libraries and classes
        * Search for airfoils
        * Initiate variables
        * Create profiles
        * Create and store hexes, boundaries, and splines using profiles
        * Create blockMeshDict file

    # Airfoil structure:
    # -5-----6----------7------------------
    # -------------------------------------
    # ------------------1------------------
    # -------------------------------------
    # -4-----0--------------------2-----8--
    # -------------------------------------
    # ------------------3------------------
    # -------------------------------------
    # -11----10---------9------------------

    # Filler structure:
    # 3-----0
    # 2-----1

    # Back and Front structure:
    # 0-----1
    # 3-----2
"""
# ==================================================================================================================== #
# Importing libraries and classes
from Codes.Math.Transformation_of_vertices import *
from Codes.Math.Custom_Math import triangle_side
from Codes.Math.Custom_Math import triangle_rad
from Codes.Math.Custom_Math import square_rad

from Codes.BlockMesh.BlockMesh import BlockMesh
from Codes.BlockMesh.Vertices import Vertices
from Codes.BlockMesh.Hexes import Hexes
from Codes.BlockMesh.Splines import Splines
from Codes.BlockMesh.Boundaries import Boundaries

from Codes.Profiles.Profile import Profile

S_LENGTH = 2
S_START_L = 1
S_TAIL = 0.16
S_MID_L = 0.50

S_HEIGHT = 1
S_START_H = 0.5
S_MID_H = 0.6

M_TOP_CELLS = 30
M_TAIL = round(M_TOP_CELLS * S_TAIL)
M_INSIDE = round(M_TOP_CELLS * S_MID_L)
M_MID = M_TOP_CELLS - M_TAIL - M_INSIDE
M_BOUNDARY = 15
M_BETWEEN = 10

GRADING = 30

# Calculating number of airfoils and hub connections
number_of_airfoils = 0
for file in os.listdir(os.path.abspath('../Coordinates')):
    if file.startswith('airfoil'):
        number_of_airfoils += 1

# ==================================================================================================================== #
# Functions
# ==================================================================================================================== #


def blade_profile(prof, n):
    verts, splines = get_airfoil_data(n)
    z = verts[0][2]
    verts.extend([[S_START_L, S_START_H - (S_HEIGHT / 2), z],
                  [S_START_L, S_START_H, z],
                  [S_START_L - (S_TAIL * S_LENGTH), S_START_H, z],
                  [S_START_L - (S_TAIL * S_LENGTH) - (S_MID_L * S_LENGTH), S_START_H, z],
                  [S_START_L - S_LENGTH, S_START_H, z],
                  [S_START_L - S_LENGTH, S_START_H - (S_HEIGHT * S_MID_H), z],
                  [S_START_L - S_LENGTH, S_START_H - S_HEIGHT, z],
                  [S_START_L - (S_TAIL * S_LENGTH) - (S_MID_L * S_LENGTH), S_START_H - S_HEIGHT, z],
                  [S_START_L - (S_TAIL * S_LENGTH), S_START_H - S_HEIGHT, z],
                  [S_START_L, S_START_H - S_HEIGHT, z]])
    Vertices.set_verts(prof, verts)
    prof.set_b_splines(1, 0, splines[0])
    prof.set_b_splines(2, 1, splines[1])
    prof.set_b_splines(3, 2, splines[2])
    prof.set_b_splines(4, 3, splines[3])
    prof.set_b_splines(5, 4, splines[4])
    prof.set_b_splines(0, 5, splines[5])
    Splines.set_splines(prof)


def blade_hex(profile1, profile2, name="blade", dir="_one"):
    Hexes.set_hexes(profile1, profile2, [0, 6, 7, 8], [M_TAIL, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, GRADING, 1, 1, GRADING, 1, 1, 1, 1])
    Hexes.set_hexes(profile1, profile2, [1, 0, 8, 9], [M_INSIDE, M_BOUNDARY, M_BETWEEN], [1, GRADING, 1])
    Hexes.set_hexes(profile1, profile2, [2, 1, 9, 10], [M_MID, M_BOUNDARY, M_BETWEEN], [1, GRADING, 1])
    Hexes.set_hexes(profile1, profile2, [3, 2, 10, 11], [M_INSIDE, M_BOUNDARY, M_BETWEEN], [1, GRADING, 1])
    Hexes.set_hexes(profile1, profile2, [4, 3, 11, 12], [M_INSIDE, M_BOUNDARY, M_BETWEEN], [1, GRADING, 1])
    Hexes.set_hexes(profile1, profile2, [5, 4, 12, 13], [M_MID, M_BOUNDARY, M_BETWEEN], [1, GRADING, 1])
    Hexes.set_hexes(profile1, profile2, [0, 5, 13, 14], [M_INSIDE, M_BOUNDARY, M_BETWEEN], [1, GRADING, 1])
    Hexes.set_hexes(profile1, profile2, [6, 0, 14, 15], [M_TAIL, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, 1, GRADING, GRADING, 1, 1, 1, 1, 1])
    Boundaries.set_boundaries(name, profile1, [1, 0], profile2, [0, 1])
    Boundaries.set_boundaries(name, profile1, [2, 1], profile2, [1, 2])
    Boundaries.set_boundaries(name, profile1, [3, 2], profile2, [2, 3])
    Boundaries.set_boundaries(name, profile1, [4, 3], profile2, [3, 4])
    Boundaries.set_boundaries(name, profile1, [5, 4], profile2, [4, 5])
    Boundaries.set_boundaries(name, profile1, [0, 5], profile2, [5, 0])

    Boundaries.set_boundaries("merge_in0" + dir, profile1, [6, 7], profile2, [7, 6])
    Boundaries.set_boundaries("merge_in1" + dir, profile1, [7, 8], profile2, [8, 7])
    Boundaries.set_boundaries("merge_in1" + dir, profile1, [8, 9], profile2, [9, 8])
    Boundaries.set_boundaries("merge_in1" + dir, profile1, [9, 10], profile2, [10, 9])
    Boundaries.set_boundaries("merge_in2" + dir, profile1, [10, 11], profile2, [11, 10])
    Boundaries.set_boundaries("merge_in2" + dir, profile1, [11, 12], profile2, [12, 11])
    Boundaries.set_boundaries("merge_in3" + dir, profile1, [12, 13], profile2, [13, 12])
    Boundaries.set_boundaries("merge_in3" + dir, profile1, [13, 14], profile2, [14, 13])
    Boundaries.set_boundaries("merge_in3" + dir, profile1, [14, 15], profile2, [15, 14])
    Boundaries.set_boundaries("merge_in0" + dir, profile1, [15, 6], profile2, [6, 15])

def copy_blade_profile(prof, ref):
    Vertices.set_verts(prof, rotate_on_angle(ref.verts, 180))
    prof.set_b_splines(1, 0, rotate_on_angle(ref.b_splines[0][2], 180))
    prof.set_b_splines(2, 1, rotate_on_angle(ref.b_splines[1][2], 180))
    prof.set_b_splines(3, 2, rotate_on_angle(ref.b_splines[2][2], 180))
    prof.set_b_splines(4, 3, rotate_on_angle(ref.b_splines[3][2], 180))
    prof.set_b_splines(5, 4, rotate_on_angle(ref.b_splines[4][2], 180))
    prof.set_b_splines(0, 5, rotate_on_angle(ref.b_splines[5][2], 180))
    Splines.set_splines(prof)
# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #
profile = []
for i in range(number_of_airfoils):
    profile.append(Profile())
    blade_profile(profile[i], i)

for i in range(number_of_airfoils - 1):
    blade_hex(profile[i], profile[i+1])

# profile_copy = []
# for i in range(number_of_airfoils):
#     profile_copy.append(Profile())
#     copy_blade_profile(profile_copy[i], profile[i])
#
# for i in range(number_of_airfoils - 1):
#     blade_hex(profile_copy[i], profile_copy[i+1], "blade", "_two")

Boundaries.set_boundaries("bottom_one", profile[0], [8, 7, 6, 0])
Boundaries.set_boundaries("bottom_one", profile[0], [9, 8, 0, 1])
Boundaries.set_boundaries("bottom_one", profile[0], [10, 9, 1, 2])
Boundaries.set_boundaries("bottom_one", profile[0], [11, 10, 2, 3])
Boundaries.set_boundaries("bottom_one", profile[0], [12, 11, 3, 4])
Boundaries.set_boundaries("bottom_one", profile[0], [13, 12, 4, 5])
Boundaries.set_boundaries("bottom_one", profile[0], [14, 13, 5, 0])
Boundaries.set_boundaries("bottom_one", profile[0], [15, 14, 0, 6])


# Boundaries.set_boundaries("bottom_two", profile_copy[0], [8, 7, 6, 0])
# Boundaries.set_boundaries("bottom_two", profile_copy[0], [9, 8, 0, 1])
# Boundaries.set_boundaries("bottom_two", profile_copy[0], [10, 9, 1, 2])
# Boundaries.set_boundaries("bottom_two", profile_copy[0], [11, 10, 2, 3])
# Boundaries.set_boundaries("bottom_two", profile_copy[0], [12, 11, 3, 4])
# Boundaries.set_boundaries("bottom_two", profile_copy[0], [13, 12, 4, 5])
# Boundaries.set_boundaries("bottom_two", profile_copy[0], [14, 13, 5, 0])
# Boundaries.set_boundaries("bottom_two", profile_copy[0], [15, 14, 0, 6])

Boundaries.set_boundaries("top_one", profile[-1], [0, 6, 7, 8])
Boundaries.set_boundaries("top_one", profile[-1], [1, 0, 8, 9])
Boundaries.set_boundaries("top_one", profile[-1], [2, 1, 9, 10])
Boundaries.set_boundaries("top_one", profile[-1], [3, 2, 10, 11])
Boundaries.set_boundaries("top_one", profile[-1], [4, 3, 11, 12])
Boundaries.set_boundaries("top_one", profile[-1], [5, 4, 12, 13])
Boundaries.set_boundaries("top_one", profile[-1], [0, 5, 13, 14])
Boundaries.set_boundaries("top_one", profile[-1], [6, 0, 14, 15])

# Boundaries.set_boundaries("top_two", profile_copy[-1], [0, 6, 7, 8])
# Boundaries.set_boundaries("top_two", profile_copy[-1], [1, 0, 8, 9])
# Boundaries.set_boundaries("top_two", profile_copy[-1], [2, 1, 9, 10])
# Boundaries.set_boundaries("top_two", profile_copy[-1], [3, 2, 10, 11])
# Boundaries.set_boundaries("top_two", profile_copy[-1], [4, 3, 11, 12])
# Boundaries.set_boundaries("top_two", profile_copy[-1], [5, 4, 12, 13])
# Boundaries.set_boundaries("top_two", profile_copy[-1], [0, 5, 13, 14])
# Boundaries.set_boundaries("top_two", profile_copy[-1], [6, 0, 14, 15])
# ==================================================================================================================== #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Create blockMesh
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

# Export everything to the blockMesh
BlockMesh.add_to_verts(Vertices.get_verts())
BlockMesh.add_to_hex(Hexes.get_hexes())
BlockMesh.add_to_edges(Splines.get_splines())
BlockMesh.add_to_boundaries(Boundaries.get_boundaries())
BlockMesh.create_blockmeshdict()

# ==================================================================================================================== #
print("Done")
# ==================================================================================================================== #
# def blade_profile_tip(prof):
#     z = 65
#     verts = [[0.42, 0, z],
#              [-1, 1.41, z],
#              [-2.41, 0, z],
#              [-1, -1.41, z],
#              [SHELL_LENGTH * 2, 0, z],
#              [SHELL_LENGTH * 2, SHELL_HEIGHT, z],
#              [SHELL_LENGTH, SHELL_HEIGHT, z],
#              [-SHELL_LENGTH / 3, SHELL_HEIGHT, z],
#              [(-4 / 3) * SHELL_LENGTH, 0, z],
#              [-SHELL_LENGTH / 3, -SHELL_HEIGHT, z],
#              [SHELL_LENGTH, -SHELL_HEIGHT, z],
#              [SHELL_LENGTH * 2, -SHELL_HEIGHT, z]]
#     Vertices.set_verts(prof, verts)
#     prof.set_arc_splines(8, 7, (-shell_side(SHELL_HEIGHT) - 1, shell_side(SHELL_HEIGHT), z))
#     prof.set_arc_splines(8, 9, (-shell_side(SHELL_HEIGHT) - 1, -shell_side(SHELL_HEIGHT), z))
#     Splines.set_splines(prof)
#
#
# def blade_hex_tip(profile1, profile2):
#     Hexes.set_hexes(profile1, profile2, [0, 4, 5, 6], [M_TAIL, M_BOUNDARY, M_BETWEEN],
#                     [1, 1, 1, 1, 30, 1, 1, 1, 1, 1, 1, 1])
#     Hexes.set_hexes(profile1, profile2, [1, 0, 6, 7], [M_INSIDE, M_BOUNDARY, M_BETWEEN],
#                     [1, 1, 1, 1, 30, 30, 1, 1, 1, 1, 1, 1])
#     Hexes.set_hexes(profile1, profile2, [2, 1, 7, 8], [M_INSIDE, M_BOUNDARY, M_BETWEEN],
#                     [1, 1, 1, 1, 30, 30, 1, 1, 1, 1, 1, 1])
#     Hexes.set_hexes(profile1, profile2, [3, 2, 8, 9], [M_INSIDE, M_BOUNDARY, M_BETWEEN],
#                     [1, 1, 1, 1, 30, 30, 1, 1, 1, 1, 1, 1])
#     Hexes.set_hexes(profile1, profile2, [0, 3, 9, 10], [M_INSIDE, M_BOUNDARY, M_BETWEEN],
#                     [1, 1, 1, 1, 30, 30, 1, 1, 1, 1, 1, 1])
#     Hexes.set_hexes(profile1, profile2, [4, 0, 10, 11], [M_TAIL, M_BOUNDARY, M_BETWEEN],
#                     [1, 1, 1, 1, 1, 30, 1, 1, 1, 1, 1, 1])
#     Hexes.set_hexes(profile1, profile2, [0, 1, 2, 3], [M_INSIDE, M_INSIDE, M_BETWEEN])
#     Boundaries.set_boundaries("blade", profile1, [3, 2, 1, 0])
#     Boundaries.set_boundaries("b1_curve", profile1, [5, 6], profile2, [6, 5])
#     Boundaries.set_boundaries("b1_curve", profile1, [6, 7], profile2, [7, 6])
#     Boundaries.set_boundaries("b1_curve", profile1, [7, 8], profile2, [8, 7])
#     Boundaries.set_boundaries("b1_curve", profile1, [8, 9], profile2, [9, 8])
#     Boundaries.set_boundaries("b1_curve", profile1, [9, 10], profile2, [10, 9])
#     Boundaries.set_boundaries("b1_curve", profile1, [10, 11], profile2, [11, 10])
#
#     Boundaries.set_boundaries("b1_mid", profile1, [4, 5], profile2, [5, 4])
#     Boundaries.set_boundaries("b1_mid", profile1, [11, 4], profile2, [4, 11])