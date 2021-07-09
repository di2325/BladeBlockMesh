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

# Constant variables
NUMBER_OF_BLADES = 3
HUB_RAD = 4
HUB_LENGTH = 3  # Real hub length divided by 2

SHELL_LENGTH = 3
SHELL_HEIGHT = 3

TIP_LENGTH = 120
MESH_OUTER_RADIUS = 30

BLADE_TIP_RAD = triangle_rad(HUB_LENGTH, TIP_LENGTH)
RADS = [HUB_RAD, 5.5, 8.2, 11.7, 15.6, 20.0, 24.1, 28.0, 32.4,
        36.2, 40.4, 44.5, 48.6, 52.5, 56, 59.0, 61.6, BLADE_TIP_RAD]

M_TAIL = 6
M_INSIDE = 8
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
    verts.extend([[SHELL_LENGTH * 2, 0, z],
                  [SHELL_LENGTH * 2, SHELL_HEIGHT, z],
                  [SHELL_LENGTH, SHELL_HEIGHT, z],
                  [-SHELL_LENGTH / 3, SHELL_HEIGHT, z],
                  [(-4 / 3) * SHELL_LENGTH, 0, z],
                  [-SHELL_LENGTH / 3, -SHELL_HEIGHT, z],
                  [SHELL_LENGTH, -SHELL_HEIGHT, z],
                  [SHELL_LENGTH * 2, -SHELL_HEIGHT, z]])
    Vertices.set_verts(prof, verts)
    prof.set_b_splines(1, 0, splines[0])
    prof.set_b_splines(2, 1, splines[1])
    prof.set_b_splines(3, 2, splines[2])
    prof.set_b_splines(0, 3, splines[3])
    prof.set_arc_splines(8, 7, (-shell_side(SHELL_HEIGHT) - 1, shell_side(SHELL_HEIGHT), z))
    prof.set_arc_splines(8, 9, (-shell_side(SHELL_HEIGHT) - 1, -shell_side(SHELL_HEIGHT), z))
    Splines.set_splines(prof)


def blade_hex(profile1, profile2):
    Hexes.set_hexes(profile1, profile2, [0, 4, 5, 6], [M_TAIL, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, 30, 1, 1, 30, 1, 1, 1, 1])
    Hexes.set_hexes(profile1, profile2, [1, 0, 6, 7], [M_INSIDE, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [2, 1, 7, 8], [M_INSIDE, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [3, 2, 8, 9], [M_INSIDE, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [0, 3, 9, 10], [M_INSIDE, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [4, 0, 10, 11], [M_TAIL, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, 1, 30, 30, 1, 1, 1, 1, 1])
    Boundaries.set_boundaries("blade", profile1, [1, 0], profile2, [0, 1])
    Boundaries.set_boundaries("blade", profile1, [2, 1], profile2, [1, 2])
    Boundaries.set_boundaries("blade", profile1, [3, 2], profile2, [2, 3])
    Boundaries.set_boundaries("blade", profile1, [0, 3], profile2, [3, 0])

    Boundaries.set_boundaries("b1_curve", profile1, [5, 6], profile2, [6, 5])
    Boundaries.set_boundaries("b1_curve", profile1, [6, 7], profile2, [7, 6])
    Boundaries.set_boundaries("b1_curve", profile1, [7, 8], profile2, [8, 7])
    Boundaries.set_boundaries("b1_curve", profile1, [8, 9], profile2, [9, 8])
    Boundaries.set_boundaries("b1_curve", profile1, [9, 10], profile2, [10, 9])
    Boundaries.set_boundaries("b1_curve", profile1, [10, 11], profile2, [11, 10])

    Boundaries.set_boundaries("b1_mid", profile1, [4, 5], profile2, [5, 4])
    Boundaries.set_boundaries("b1_mid", profile1, [11, 4], profile2, [4, 11])


def blade_profile_tip(prof):
    z = 65
    verts = [[0.42, 0, z],
             [-1, 1.41, z],
             [-2.41, 0, z],
             [-1, -1.41, z],
             [SHELL_LENGTH * 2, 0, z],
             [SHELL_LENGTH * 2, SHELL_HEIGHT, z],
             [SHELL_LENGTH, SHELL_HEIGHT, z],
             [-SHELL_LENGTH / 3, SHELL_HEIGHT, z],
             [(-4 / 3) * SHELL_LENGTH, 0, z],
             [-SHELL_LENGTH / 3, -SHELL_HEIGHT, z],
             [SHELL_LENGTH, -SHELL_HEIGHT, z],
             [SHELL_LENGTH * 2, -SHELL_HEIGHT, z]]
    Vertices.set_verts(prof, verts)
    prof.set_arc_splines(8, 7, (-shell_side(SHELL_HEIGHT) - 1, shell_side(SHELL_HEIGHT), z))
    prof.set_arc_splines(8, 9, (-shell_side(SHELL_HEIGHT) - 1, -shell_side(SHELL_HEIGHT), z))
    Splines.set_splines(prof)


def blade_hex_tip(profile1, profile2):
    Hexes.set_hexes(profile1, profile2, [0, 4, 5, 6], [M_TAIL, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, 30, 1, 1, 1, 1, 1, 1, 1])
    Hexes.set_hexes(profile1, profile2, [1, 0, 6, 7], [M_INSIDE, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, 30, 30, 1, 1, 1, 1, 1, 1])
    Hexes.set_hexes(profile1, profile2, [2, 1, 7, 8], [M_INSIDE, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, 30, 30, 1, 1, 1, 1, 1, 1])
    Hexes.set_hexes(profile1, profile2, [3, 2, 8, 9], [M_INSIDE, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, 30, 30, 1, 1, 1, 1, 1, 1])
    Hexes.set_hexes(profile1, profile2, [0, 3, 9, 10], [M_INSIDE, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, 30, 30, 1, 1, 1, 1, 1, 1])
    Hexes.set_hexes(profile1, profile2, [4, 0, 10, 11], [M_TAIL, M_BOUNDARY, M_BETWEEN],
                    [1, 1, 1, 1, 1, 30, 1, 1, 1, 1, 1, 1])
    Hexes.set_hexes(profile1, profile2, [0, 1, 2, 3], [M_INSIDE, M_INSIDE, M_BETWEEN])
    Boundaries.set_boundaries("blade", profile1, [3, 2, 1, 0])
    Boundaries.set_boundaries("b1_curve", profile1, [5, 6], profile2, [6, 5])
    Boundaries.set_boundaries("b1_curve", profile1, [6, 7], profile2, [7, 6])
    Boundaries.set_boundaries("b1_curve", profile1, [7, 8], profile2, [8, 7])
    Boundaries.set_boundaries("b1_curve", profile1, [8, 9], profile2, [9, 8])
    Boundaries.set_boundaries("b1_curve", profile1, [9, 10], profile2, [10, 9])
    Boundaries.set_boundaries("b1_curve", profile1, [10, 11], profile2, [11, 10])

    Boundaries.set_boundaries("b1_mid", profile1, [4, 5], profile2, [5, 4])
    Boundaries.set_boundaries("b1_mid", profile1, [11, 4], profile2, [4, 11])

# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #
profile = []
i = 0

for i in range(number_of_airfoils):
    profile.append(Profile())
    blade_profile(profile[i], i)

profile.append(Profile())
blade_profile_tip(profile[-1])


for i in range(number_of_airfoils - 1):
    blade_hex(profile[i], profile[i + 1])

blade_hex_tip(profile[-2], profile[-1])
Boundaries.set_boundaries("b1_bot", profile[0], [6, 5, 4, 0])
Boundaries.set_boundaries("b1_bot", profile[0], [7, 6, 0, 1])
Boundaries.set_boundaries("b1_bot", profile[0], [8, 7, 1, 2])
Boundaries.set_boundaries("b1_bot", profile[0], [9, 8, 2, 3])
Boundaries.set_boundaries("b1_bot", profile[0], [10, 9, 3, 0])
Boundaries.set_boundaries("b1_bot", profile[0], [11, 10, 0, 4])

Boundaries.set_boundaries("b1_top", profile[-1], [0, 4, 5, 6])
Boundaries.set_boundaries("b1_top", profile[-1], [1, 0, 6, 7])
Boundaries.set_boundaries("b1_top", profile[-1], [2, 1, 7, 8])
Boundaries.set_boundaries("b1_top", profile[-1], [3, 2, 8, 9])
Boundaries.set_boundaries("b1_top", profile[-1], [0, 3, 9, 10])
Boundaries.set_boundaries("b1_top", profile[-1], [4, 0, 10, 11])
Boundaries.set_boundaries("b1_top", profile[-1], [0, 1, 2, 3])
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
