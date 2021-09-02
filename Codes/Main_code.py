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

"""
# ==================================================================================================================== #
# Importing libraries and classes
from Codes.Math.Transformation_of_vertices import *

from Codes.BlockMesh.BlockMesh import BlockMesh
from Codes.BlockMesh.Vertices import Vertices
from Codes.BlockMesh.Hexes import Hexes
from Codes.BlockMesh.Splines import Splines
from Codes.BlockMesh.Boundaries import Boundaries

from Codes.Profiles.Profile import Profile

M_HEIGHT = 10
M_WIDTH = 20
M_LENGTH = 7
M_BOUNDARY = 15

# Calculating number of airfoils and hub connections
number_of_airfoils = 0
for file in os.listdir(os.path.abspath('../Coordinates')):
    if file.startswith('airfoil'):
        number_of_airfoils += 1

# ==================================================================================================================== #
# Functions
# ==================================================================================================================== #


def blade_profile(profile, n):
    verts, splines = get_airfoil_data(n)
    z = verts[0][2]
    verts.extend(((1, 0.5, z),
                 (-1, 0.5, z),
                 (-1, -0.5, z),
                 (1, -0.5, z)))
    Vertices.set_verts(profile, verts)
    profile.set_b_splines(1, 0, splines[0])
    profile.set_b_splines(2, 1, splines[1])
    profile.set_b_splines(3, 2, splines[2])
    Splines.set_splines(profile)


def blade_hex(profile1, profile2, boundary="blade", m_z=M_LENGTH, g_x=1, g_y=1, g_z=1):
    Hexes.set_hexes(profile1, profile2, [0, 3, 7, 4], (M_HEIGHT, M_BOUNDARY, m_z), (g_x, g_y, g_z))
    Hexes.set_hexes(profile1, profile2, [1, 0, 4, 5], (M_WIDTH, M_BOUNDARY, m_z), (g_x, g_y, g_z))
    Hexes.set_hexes(profile1, profile2, [2, 1, 5, 6], (M_HEIGHT, M_BOUNDARY, m_z), (g_x, g_y, g_z))
    Hexes.set_hexes(profile1, profile2, [3, 2, 6, 7], (M_WIDTH, M_BOUNDARY, m_z), (g_x, g_y, g_z))
    Boundaries.set_boundaries(boundary, profile1, [1, 0], profile2, [0, 1])
    Boundaries.set_boundaries(boundary, profile1, [2, 1], profile2, [1, 2])
    Boundaries.set_boundaries(boundary, profile1, [3, 2], profile2, [2, 3])
    Boundaries.set_boundaries(boundary, profile1, [0, 3], profile2, [3, 0])


def copy_blade_profile(prof, ref):
    Vertices.set_verts(prof, rotate_on_angle(ref.verts, 180))
    prof.set_b_splines(1, 0, rotate_on_angle(ref.b_splines[0][2], 180))
    prof.set_b_splines(2, 1, rotate_on_angle(ref.b_splines[1][2], 180))
    prof.set_b_splines(3, 2, rotate_on_angle(ref.b_splines[2][2], 180))
    Splines.set_splines(prof)


# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #
profile_one = []

for i in range(number_of_airfoils):
    profile_one.append(Profile())
    blade_profile(profile_one[i], i)

for i in range(0, number_of_airfoils - 1):
    if i == 0:
        current_z = round(M_LENGTH * 2.25)
    elif i == number_of_airfoils - 2:
        current_z = round(M_LENGTH / 3)
    else:
        current_z = M_LENGTH
    blade_hex(profile_one[i], profile_one[i + 1], "blade_one", current_z)

profile_two = []
for i in range(number_of_airfoils):
    profile_two.append(Profile())
    copy_blade_profile(profile_two[i], profile_one[i])

for i in range(0, number_of_airfoils - 1):
    if i == 0:
        current_z = round(M_LENGTH * 2.25)
    elif i == number_of_airfoils - 2:
        current_z = round(M_LENGTH / 3)
    else:
        current_z = M_LENGTH
    blade_hex(profile_two[i], profile_two[i + 1], "blade_two", current_z)
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
