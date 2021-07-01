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
    # -7-----8----------9---------------10-
    # -------------------------------------
    # ------------------1------------------
    # -----------------------2-------------
    # -6-----0--------------------3-----11-
    # -----------------------4-------------
    # ------------------5------------------
    # -------------------------------------
    # -15----14---------13--------------12-

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

TIP_LENGTH = 120
MESH_OUTER_RADIUS = 30

BLADE_TIP_RAD = triangle_rad(HUB_LENGTH, TIP_LENGTH)
RADS = [HUB_RAD, 5.5, 8.2, 11.7, 15.6, 20.0, 24.1, 28.0, 32.4,
        36.2, 40.4, 44.5, 48.6, 52.5, 56, 59.0, 61.6, BLADE_TIP_RAD]

M_TAIL = 6
M_BACK = 8
M_FRONT = 4
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
    verts.extend([[HUB_LENGTH, 0, z],
                  [HUB_LENGTH, HUB_LENGTH, z],
                  [-HUB_LENGTH / 3, HUB_LENGTH, z],
                  [-HUB_LENGTH, HUB_LENGTH, z],
                  [-HUB_LENGTH, 0, z],
                  [-HUB_LENGTH, -HUB_LENGTH, z],
                  [-HUB_LENGTH / 3, -HUB_LENGTH, z],
                  [HUB_LENGTH, -HUB_LENGTH, z]])
    Vertices.set_verts(prof, verts)
    prof.set_b_splines(0, 7, splines[0])
    prof.set_b_splines(7, 6, splines[1])
    prof.set_b_splines(6, 5, splines[2])
    prof.set_b_splines(5, 4, splines[3])
    prof.set_b_splines(4, 3, splines[4])
    prof.set_b_splines(3, 2, splines[5])
    prof.set_b_splines(2, 1, splines[6])
    prof.set_b_splines(1, 0, splines[7])
    Splines.set_splines(prof)

def blade_hex(profile1, profile2):
    Hexes.set_hexes(profile1, profile2, [1, 0, 8, 9], [M_TAIL, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [2, 1, 9, 10], [M_BACK, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [3, 2, 10, 11], [M_FRONT, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [4, 3, 11, 12], [M_TAIL, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [5, 4, 12, 13], [M_TAIL, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [6, 5, 13, 14], [M_FRONT, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [7, 6, 14, 15], [M_BACK, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [0, 7, 15, 8], [M_TAIL, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Boundaries.set_boundaries("blade", profile1, [1, 0], profile2, [0, 1])
    Boundaries.set_boundaries("blade", profile1, [2, 1], profile2, [1, 2])
    Boundaries.set_boundaries("blade", profile1, [3, 2], profile2, [2, 3])
    Boundaries.set_boundaries("blade", profile1, [4, 3], profile2, [3, 4])
    Boundaries.set_boundaries("blade", profile1, [5, 4], profile2, [4, 5])
    Boundaries.set_boundaries("blade", profile1, [6, 5], profile2, [5, 6])
    Boundaries.set_boundaries("blade", profile1, [7, 6], profile2, [6, 7])
    Boundaries.set_boundaries("blade", profile1, [0, 7], profile2, [7, 0])

def blade_profile_tip(prof, n):
    verts, splines = get_airfoil_data(n)
    z = verts[0][2]
    verts.extend([[HUB_LENGTH, 0, z],
                  [HUB_LENGTH, HUB_LENGTH, z],
                  [-HUB_LENGTH / 3, HUB_LENGTH, z],
                  [-HUB_LENGTH, HUB_LENGTH, z],
                  [-HUB_LENGTH, 0, z],
                  [-HUB_LENGTH, -HUB_LENGTH, z],
                  [-HUB_LENGTH / 3, -HUB_LENGTH, z],
                  [HUB_LENGTH, -HUB_LENGTH, z]])
    v1 = [(verts[1][0] + verts[7][0]) / 2, (verts[1][1] + verts[7][1]) / 2, (verts[1][2] + verts[7][2]) / 2]
    v2 = [(verts[2][0] + verts[6][0]) / 2, (verts[2][1] + verts[6][1]) / 2, (verts[2][2] + verts[6][2]) / 2]
    v3 = [(verts[3][0] + verts[5][0]) / 2, (verts[3][1] + verts[5][1]) / 2, (verts[3][2] + verts[5][2]) / 2]
    v1 = [(v1[0] + v2[0])/2, (v1[1] + v2[1])/2, (v1[2] + v2[2])/2]
    v3 = [(v3[0] + v2[0])/2, (v3[1] + v2[1])/2, (v3[2] + v2[2])/2]
    verts.extend([v1, v2, v3])
    Vertices.set_verts(prof, verts)
    prof.set_b_splines(0, 7, splines[0])
    prof.set_b_splines(7, 6, splines[1])
    prof.set_b_splines(6, 5, splines[2])
    prof.set_b_splines(5, 4, splines[3])
    prof.set_b_splines(4, 3, splines[4])
    prof.set_b_splines(3, 2, splines[5])
    prof.set_b_splines(2, 1, splines[6])
    prof.set_b_splines(1, 0, splines[7])
    Splines.set_splines(prof)

def blade_hex_tip(profile1, profile2):
    Hexes.set_hexes(profile1, profile2, [1, 0, 8, 9], [M_TAIL, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [2, 1, 9, 10], [M_BACK, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [3, 2, 10, 11], [M_FRONT, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [4, 3, 11, 12], [M_TAIL, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [5, 4, 12, 13], [M_TAIL, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [6, 5, 13, 14], [M_FRONT, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [7, 6, 14, 15], [M_BACK, M_BOUNDARY, M_BETWEEN], [1, 30, 1])
    Hexes.set_hexes(profile1, profile2, [0, 7, 15, 8], [M_TAIL, M_BOUNDARY, M_BETWEEN], [1, 30, 1])

    Hexes.set_hexes(profile1, profile2, [0, 1, 16, 7], [M_TAIL, M_BOUNDARY, M_BETWEEN])
    Hexes.set_hexes(profile1, profile2, [1, 2, 16, 17], [M_TAIL, M_BOUNDARY, M_BETWEEN])
    Hexes.set_hexes(profile1, profile2, [0, 7, 15, 8], [M_TAIL, M_BOUNDARY, M_BETWEEN])
    Hexes.set_hexes(profile1, profile2, [0, 7, 15, 8], [M_TAIL, M_BOUNDARY, M_BETWEEN])
    Hexes.set_hexes(profile1, profile2, [0, 7, 15, 8], [M_TAIL, M_BOUNDARY, M_BETWEEN])
    Hexes.set_hexes(profile1, profile2, [0, 7, 15, 8], [M_TAIL, M_BOUNDARY, M_BETWEEN])

# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #
profile = []

for i in range(number_of_airfoils):
    profile.append(Profile())
    blade_profile(profile[i], i)

for i in range(number_of_airfoils - 2):
    blade_hex(profile[i], profile[i+1])
blade_hex_tip(profile[-2], profile[-1])
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

# v1 = [(verts[1][0] + verts[7][0]) / 2, (verts[1][1] + verts[7][1]) / 2, (verts[1][2] + verts[7][2]) / 2]
# v2 = [(verts[2][0] + verts[6][0]) / 2, (verts[2][1] + verts[6][1]) / 2, (verts[2][2] + verts[6][2]) / 2]
# v3 = [(verts[3][0] + verts[5][0]) / 2, (verts[3][1] + verts[5][1]) / 2, (verts[3][2] + verts[5][2]) / 2]
# v1 = [(v1[0] + v2[0])/2, (v1[1] + v2[1])/2, (v1[2] + v2[2])/2]
# v3 = [(v3[0] + v2[0])/2, (v3[1] + v2[1])/2, (v3[2] + v2[2])/2]
# verts.extend([v1, v2, v3])

# Hexes.set_hexes(profile[i], profile[i+1], [0, 1, 16, 7])
# Hexes.set_hexes(profile[i], profile[i+1], [1, 2, 17, 16])
# Hexes.set_hexes(profile[i], profile[i+1], [2, 3, 18, 17])
# Hexes.set_hexes(profile[i], profile[i+1], [3, 4, 5, 18])
# Hexes.set_hexes(profile[i], profile[i+1], [5, 6, 17, 18])
# Hexes.set_hexes(profile[i], profile[i+1], [6, 7, 16, 17])
