"""
Main code:
    Generates blockMeshDict file according to imported airfoil profiles.
    Currently, can generate only NREL Phase VI wind turbine.

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
HEXES = 20
MULT = 0.5
MESH = round(10 * MULT)

for i in range(number_of_airfoils):
    profile.append(Profile())
    verts, splines = get_airfoil_data("airfoil" + str(i))
    add_0 = [(verts[1][0] + verts[5][0]) / 2,
             (verts[1][1] + verts[5][1]) / 2,
             (verts[1][2] + verts[5][2]) / 2, ]
    add_1 = [(verts[2][0] + verts[4][0]) / 2,
             (verts[2][1] + verts[4][1]) / 2,
             (verts[2][2] + verts[4][2]) / 2, ]
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
    profile[i].set_b_splines(1, 0, splines[0])
    profile[i].set_b_splines(2, 1, splines[1])
    profile[i].set_b_splines(3, 2, splines[2])
    profile[i].set_b_splines(4, 3, splines[3])
    profile[i].set_b_splines(5, 4, splines[4])
    profile[i].set_b_splines(0, 5, splines[5])
    Splines.set_splines(profile[i])

z = round(HEXES / 2)
for i in range(number_of_airfoils - 1):
    if i == number_of_airfoils - 2:
        z = round(z / 2)
    Hexes.set_hexes(profile[i], profile[i + 1], [0, 1, 6, 5], [MESH, MESH, z])
    Hexes.set_hexes(profile[i], profile[i + 1], [1, 2, 7, 6], [MESH, MESH, z])
    Hexes.set_hexes(profile[i], profile[i + 1], [2, 3, 4, 7], [MESH, MESH, z])
    Hexes.set_hexes(profile[i], profile[i + 1], [4, 5, 6, 7], [MESH, MESH, z])
    Boundaries.set_boundaries("blade_one", profile[i], [0, 1], profile[i + 1], [1, 0])
    Boundaries.set_boundaries("blade_one", profile[i], [1, 2], profile[i + 1], [2, 1])
    Boundaries.set_boundaries("blade_one", profile[i], [2, 3], profile[i + 1], [3, 2])
    Boundaries.set_boundaries("blade_one", profile[i], [3, 4], profile[i + 1], [4, 3])
    Boundaries.set_boundaries("blade_one", profile[i], [4, 5], profile[i + 1], [5, 4])
    Boundaries.set_boundaries("blade_one", profile[i], [5, 0], profile[i + 1], [0, 5])
    if i == number_of_airfoils - 2:
        Boundaries.set_boundaries("blade_one", profile[i + 1], [5, 6, 1, 0])
        Boundaries.set_boundaries("blade_one", profile[i + 1], [6, 7, 2, 1])
        Boundaries.set_boundaries("blade_one", profile[i + 1], [7, 6, 5, 4])
        Boundaries.set_boundaries("blade_one", profile[i + 1], [7, 4, 3, 2])

profile_two = []
for i in range(number_of_airfoils):
    profile_two.append(Profile())
    verts = rotate_on_angle(profile[i].verts, 180)
    Vertices.set_verts(profile_two[i], verts)
    splines = profile[i].b_splines
    profile_two[i].set_b_splines(1, 0, rotate_on_angle(splines[0][2], 180))
    profile_two[i].set_b_splines(2, 1, rotate_on_angle(splines[1][2], 180))
    profile_two[i].set_b_splines(3, 2, rotate_on_angle(splines[2][2], 180))
    profile_two[i].set_b_splines(4, 3, rotate_on_angle(splines[3][2], 180))
    profile_two[i].set_b_splines(5, 4, rotate_on_angle(splines[4][2], 180))
    profile_two[i].set_b_splines(0, 5, rotate_on_angle(splines[5][2], 180))
    Splines.set_splines(profile_two[i])

z = round(HEXES / 2)
for i in range(number_of_airfoils - 1):
    if i == number_of_airfoils - 2:
        z = round(z / 2)
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [0, 1, 6, 5], [MESH, MESH, z])
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [1, 2, 7, 6], [MESH, MESH, z])
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [2, 3, 4, 7], [MESH, MESH, z])
    Hexes.set_hexes(profile_two[i], profile_two[i + 1], [4, 5, 6, 7], [MESH, MESH, z])
    Boundaries.set_boundaries("blade_two", profile_two[i], [0, 1], profile_two[i + 1], [1, 0])
    Boundaries.set_boundaries("blade_two", profile_two[i], [1, 2], profile_two[i + 1], [2, 1])
    Boundaries.set_boundaries("blade_two", profile_two[i], [2, 3], profile_two[i + 1], [3, 2])
    Boundaries.set_boundaries("blade_two", profile_two[i], [3, 4], profile_two[i + 1], [4, 3])
    Boundaries.set_boundaries("blade_two", profile_two[i], [4, 5], profile_two[i + 1], [5, 4])
    Boundaries.set_boundaries("blade_two", profile_two[i], [5, 0], profile_two[i + 1], [0, 5])
    if i == number_of_airfoils - 2:
        Boundaries.set_boundaries("blade_two", profile_two[i + 1], [5, 6, 1, 0])
        Boundaries.set_boundaries("blade_two", profile_two[i + 1], [6, 7, 2, 1])
        Boundaries.set_boundaries("blade_two", profile_two[i + 1], [7, 6, 5, 4])
        Boundaries.set_boundaries("blade_two", profile_two[i + 1], [7, 4, 3, 2])

Hexes.set_hexes_hub(profile_two[0], profile[0], [3, 2, 7, 4], [0, 1, 6, 5], [MESH, MESH, 2 * MESH])
Hexes.set_hexes_hub(profile_two[0], profile[0], [2, 1, 6, 7], [1, 2, 7, 6], [MESH, MESH, 2 * MESH])
Hexes.set_hexes_hub(profile_two[0], profile[0], [1, 0, 5, 6], [2, 3, 4, 7], [MESH, MESH, 2 * MESH])
Hexes.set_hexes_hub(profile_two[0], profile[0], [5, 4, 7, 6], [4, 5, 6, 7], [MESH, MESH, 2 * MESH])
Boundaries.set_boundaries("hub", profile_two[0], [3, 2], profile[0], [1, 0])
Boundaries.set_boundaries("hub", profile_two[0], [2, 1], profile[0], [2, 1])
Boundaries.set_boundaries("hub", profile_two[0], [1, 0], profile[0], [3, 2])
Boundaries.set_boundaries("hub", profile_two[0], [0, 5], profile[0], [4, 3])
Boundaries.set_boundaries("hub", profile_two[0], [5, 4], profile[0], [5, 4])
Boundaries.set_boundaries("hub", profile_two[0], [4, 3], profile[0], [0, 5])

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
