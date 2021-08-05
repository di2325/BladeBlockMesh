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

# Calculating number of airfoils and hub connections
number_of_airfoils = 0
for file in os.listdir(os.path.abspath('../Coordinates')):
    if file.startswith('airfoil'):
        number_of_airfoils += 1
# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #
profile = []
HEXES = 10
for i in range(number_of_airfoils):
    profile.append(Profile())
    verts_out, splines_out = get_airfoil_data("airfoil" + str(i))
    verts_in, splines_in = get_airfoil_data("inner_airfoil" + str(i), 0.65)
    verts = verts_in + verts_out
    if i >= number_of_airfoils - 2:
        add_0 = [(verts_in[1][0] + verts_in[5][0]) / 2,
                 (verts_in[1][1] + verts_in[5][1]) / 2,
                 (verts_in[1][2] + verts_in[5][2]) / 2, ]
        add_1 = [(verts_in[2][0] + verts_in[4][0]) / 2,
                 (verts_in[2][1] + verts_in[4][1]) / 2,
                 (verts_in[2][2] + verts_in[4][2]) / 2, ]
        center = [(add_0[0] + add_1[0]) / 2,
                  (add_0[1] + add_1[1]) / 2,
                  (add_0[2] + add_1[2]) / 2, ]
        add_0 = [(add_0[0] + center[0]) / 2,
                 (add_0[1] + center[1]) / 2,
                 (add_0[2] + center[2]) / 2, ]
        add_1 = [(center[0] + add_1[0]) / 2,
                 (center[1] + add_1[1]) / 2,
                 (center[2] + add_1[2]) / 2, ]
        verts.extend((add_0, add_1))
    Vertices.set_verts(profile[i], verts)
    profile[i].set_b_splines(1, 0, splines_in[0])
    profile[i].set_b_splines(2, 1, splines_in[1])
    profile[i].set_b_splines(3, 2, splines_in[2])
    profile[i].set_b_splines(4, 3, splines_in[3])
    profile[i].set_b_splines(5, 4, splines_in[4])
    profile[i].set_b_splines(0, 5, splines_in[5])
    profile[i].set_b_splines(7, 6, splines_out[0])
    profile[i].set_b_splines(8, 7, splines_out[1])
    profile[i].set_b_splines(9, 8, splines_out[2])
    profile[i].set_b_splines(10, 9, splines_out[3])
    profile[i].set_b_splines(11, 10, splines_out[4])
    profile[i].set_b_splines(6, 11, splines_out[5])
    Splines.set_splines(profile[i])

z = HEXES
for i in range(number_of_airfoils-1):
    if i == number_of_airfoils-2:
        z = 4
    Hexes.set_hexes(profile[i], profile[i + 1], [1, 0, 6, 7], [HEXES, 1, z])
    Hexes.set_hexes(profile[i], profile[i + 1], [2, 1, 7, 8], [HEXES, 1, z])
    Hexes.set_hexes(profile[i], profile[i + 1], [3, 2, 8, 9], [HEXES, 1, z])
    Hexes.set_hexes(profile[i], profile[i + 1], [4, 3, 9, 10], [HEXES, 1, z])
    Hexes.set_hexes(profile[i], profile[i + 1], [5, 4, 10, 11], [HEXES, 1, z])
    Hexes.set_hexes(profile[i], profile[i + 1], [0, 5, 11, 6], [HEXES, 1, z])
    Boundaries.set_boundaries("blade", profile[i], [6, 7], profile[i + 1], [7, 6])
    Boundaries.set_boundaries("blade", profile[i], [7, 8], profile[i + 1], [8, 7])
    Boundaries.set_boundaries("blade", profile[i], [8, 9], profile[i + 1], [9, 8])
    Boundaries.set_boundaries("blade", profile[i], [9, 10], profile[i + 1], [10, 9])
    Boundaries.set_boundaries("blade", profile[i], [10, 11], profile[i + 1], [11, 10])
    Boundaries.set_boundaries("blade", profile[i], [11, 6], profile[i + 1], [6, 11])
    if i < number_of_airfoils-2:
        Boundaries.set_boundaries("blade_internal", profile[i], [1, 0], profile[i + 1], [0, 1])
        Boundaries.set_boundaries("blade_internal", profile[i], [2, 1], profile[i + 1], [1, 2])
        Boundaries.set_boundaries("blade_internal", profile[i], [3, 2], profile[i + 1], [2, 3])
        Boundaries.set_boundaries("blade_internal", profile[i], [4, 3], profile[i + 1], [3, 4])
        Boundaries.set_boundaries("blade_internal", profile[i], [5, 4], profile[i + 1], [4, 5])
        Boundaries.set_boundaries("blade_internal", profile[i], [0, 5], profile[i + 1], [5, 0])

Hexes.set_hexes(profile[-2], profile[-1], [0, 1, 12, 5], [10, 10, z])
Hexes.set_hexes(profile[-2], profile[-1], [2, 3, 4, 13], [10, 10, z])
Hexes.set_hexes(profile[-2], profile[-1], [12, 13, 4, 5], [10, 10, z])
Hexes.set_hexes(profile[-2], profile[-1], [13, 12, 1, 2], [10, 10, z])
Boundaries.set_boundaries("blade", profile[-1], [1, 0, 6, 7])
Boundaries.set_boundaries("blade", profile[-1], [2, 1, 7, 8])
Boundaries.set_boundaries("blade", profile[-1], [3, 2, 8, 9])
Boundaries.set_boundaries("blade", profile[-1], [4, 3, 9, 10])
Boundaries.set_boundaries("blade", profile[-1], [5, 4, 10, 11])
Boundaries.set_boundaries("blade", profile[-1], [0, 5, 11, 6])
Boundaries.set_boundaries("blade", profile[-1], [0, 1, 12, 5])
Boundaries.set_boundaries("blade", profile[-1], [1, 2, 13, 12])
Boundaries.set_boundaries("blade", profile[-1], [2, 3, 4, 13])
Boundaries.set_boundaries("blade", profile[-1], [12, 13, 4, 5])
Boundaries.set_boundaries("blade_internal", profile[-2], [12, 1, 0, 5])
Boundaries.set_boundaries("blade_internal", profile[-2], [12, 13, 2, 1])
Boundaries.set_boundaries("blade_internal", profile[-2], [13, 12, 5, 4])
Boundaries.set_boundaries("blade_internal", profile[-2], [13, 4, 3, 2])

profile_two = []
for i in range(number_of_airfoils):
    profile_two.append(Profile())
    verts = rotate_on_angle(profile[i].verts, 180)
    Vertices.set_verts(profile_two[i], verts)
    splines = profile[i].b_splines
    profile_two[i].set_b_splines(1, 0,  rotate_on_angle(splines[0][2], 180))
    profile_two[i].set_b_splines(2, 1,  rotate_on_angle(splines[1][2], 180))
    profile_two[i].set_b_splines(3, 2,  rotate_on_angle(splines[2][2], 180))
    profile_two[i].set_b_splines(4, 3,  rotate_on_angle(splines[3][2], 180))
    profile_two[i].set_b_splines(5, 4,  rotate_on_angle(splines[4][2], 180))
    profile_two[i].set_b_splines(0, 5,  rotate_on_angle(splines[5][2], 180))
    profile_two[i].set_b_splines(7, 6,  rotate_on_angle(splines[6][2], 180))
    profile_two[i].set_b_splines(8, 7,  rotate_on_angle(splines[7][2], 180))
    profile_two[i].set_b_splines(9, 8,  rotate_on_angle(splines[8][2], 180))
    profile_two[i].set_b_splines(10, 9, rotate_on_angle(splines[9][2], 180))
    profile_two[i].set_b_splines(11, 10, rotate_on_angle(splines[10][2], 180))
    profile_two[i].set_b_splines(6, 11, rotate_on_angle(splines[11][2], 180))
    Splines.set_splines(profile_two[i])

z = 10
for i in range(number_of_airfoils-1):
    if i == number_of_airfoils-2:
        z = 4
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [1, 0, 6, 7], [10, 1, z])
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [2, 1, 7, 8], [10, 1, z])
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [3, 2, 8, 9], [10, 1, z])
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [4, 3, 9, 10], [10, 1, z])
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [5, 4, 10, 11], [10, 1, z])
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [0, 5, 11, 6], [10, 1, z])
    Boundaries.set_boundaries("blade", profile_two[i], [6, 7], profile_two[i + 1], [7, 6])
    Boundaries.set_boundaries("blade", profile_two[i], [7, 8], profile_two[i + 1], [8, 7])
    Boundaries.set_boundaries("blade", profile_two[i], [8, 9], profile_two[i + 1], [9, 8])
    Boundaries.set_boundaries("blade", profile_two[i], [9, 10], profile_two[i + 1], [10, 9])
    Boundaries.set_boundaries("blade", profile_two[i], [10, 11], profile_two[i + 1], [11, 10])
    Boundaries.set_boundaries("blade", profile_two[i], [11, 6], profile_two[i + 1], [6, 11])
    if i < number_of_airfoils-2:
        Boundaries.set_boundaries("blade_internal", profile_two[i], [1, 0], profile_two[i + 1], [0, 1])
        Boundaries.set_boundaries("blade_internal", profile_two[i], [2, 1], profile_two[i + 1], [1, 2])
        Boundaries.set_boundaries("blade_internal", profile_two[i], [3, 2], profile_two[i + 1], [2, 3])
        Boundaries.set_boundaries("blade_internal", profile_two[i], [4, 3], profile_two[i + 1], [3, 4])
        Boundaries.set_boundaries("blade_internal", profile_two[i], [5, 4], profile_two[i + 1], [4, 5])
        Boundaries.set_boundaries("blade_internal", profile_two[i], [0, 5], profile_two[i + 1], [5, 0])

Hexes.set_hexes(profile_two[-2], profile_two[-1], [0, 1, 12, 5], [10, 10, z])
Hexes.set_hexes(profile_two[-2], profile_two[-1], [2, 3, 4, 13], [10, 10, z])
Hexes.set_hexes(profile_two[-2], profile_two[-1], [12, 13, 4, 5], [10, 10, z])
Hexes.set_hexes(profile_two[-2], profile_two[-1], [13, 12, 1, 2], [10, 10, z])
Boundaries.set_boundaries("blade", profile_two[-1], [1, 0, 6, 7])
Boundaries.set_boundaries("blade", profile_two[-1], [2, 1, 7, 8])
Boundaries.set_boundaries("blade", profile_two[-1], [3, 2, 8, 9])
Boundaries.set_boundaries("blade", profile_two[-1], [4, 3, 9, 10])
Boundaries.set_boundaries("blade", profile_two[-1], [5, 4, 10, 11])
Boundaries.set_boundaries("blade", profile_two[-1], [0, 5, 11, 6])
Boundaries.set_boundaries("blade", profile_two[-1], [0, 1, 12, 5])
Boundaries.set_boundaries("blade", profile_two[-1], [1, 2, 13, 12])
Boundaries.set_boundaries("blade", profile_two[-1], [2, 3, 4, 13])
Boundaries.set_boundaries("blade", profile_two[-1], [12, 13, 4, 5])
Boundaries.set_boundaries("blade_internal", profile_two[-2], [12, 1, 0, 5])
Boundaries.set_boundaries("blade_internal", profile_two[-2], [12, 13, 2, 1])
Boundaries.set_boundaries("blade_internal", profile_two[-2], [13, 12, 5, 4])
Boundaries.set_boundaries("blade_internal", profile_two[-2], [13, 4, 3, 2])

Hexes.set_hexes_hub(profile_two[0], profile[0], [2, 3, 9, 8], [1, 0, 6, 7], [10, 1, 10])
Hexes.set_hexes_hub(profile_two[0], profile[0], [1, 2, 8, 7], [2, 1, 7, 8], [10, 1, 10])
Hexes.set_hexes_hub(profile_two[0], profile[0], [0, 1, 7, 6], [3, 2, 8, 9], [10, 1, 10])
Hexes.set_hexes_hub(profile_two[0], profile[0], [5, 0, 6, 11], [4, 3, 9, 10], [10, 1, 10])
Hexes.set_hexes_hub(profile_two[0], profile[0], [4, 5, 11, 10], [5, 4, 10, 11], [10, 1, 10])
Hexes.set_hexes_hub(profile_two[0], profile[0], [3, 4, 10, 9], [0, 5, 11, 6], [10, 1, 10])
Boundaries.set_boundaries("hub", profile_two[0], [9, 8], profile[0], [7, 6])
Boundaries.set_boundaries("hub", profile_two[0], [8, 7], profile[0], [8, 7])
Boundaries.set_boundaries("hub", profile_two[0], [7, 6], profile[0], [9, 8])
Boundaries.set_boundaries("hub", profile_two[0], [6, 11], profile[0], [10, 9])
Boundaries.set_boundaries("hub", profile_two[0], [11, 10], profile[0], [11, 10])
Boundaries.set_boundaries("hub", profile_two[0], [10, 9], profile[0], [6, 11])
Boundaries.set_boundaries("hub_internal", profile_two[0], [2, 3], profile[0], [0, 1])
Boundaries.set_boundaries("hub_internal", profile_two[0], [1, 2], profile[0], [1, 2])
Boundaries.set_boundaries("hub_internal", profile_two[0], [0, 1], profile[0], [2, 3])
Boundaries.set_boundaries("hub_internal", profile_two[0], [5, 0], profile[0], [3, 4])
Boundaries.set_boundaries("hub_internal", profile_two[0], [4, 5], profile[0], [4, 5])
Boundaries.set_boundaries("hub_internal", profile_two[0], [3, 4], profile[0], [5, 0])

# ==================================================================================================================== #
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Create blockMesh
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
BlockMesh.add_to_verts(Vertices.get_verts())
BlockMesh.add_to_hex(Hexes.get_hexes())
BlockMesh.add_to_edges(Splines.get_splines())
BlockMesh.add_to_boundaries(Boundaries.get_boundaries())
BlockMesh.create_blockmeshdict()
# ==================================================================================================================== #
print("Done")
# ==================================================================================================================== #
