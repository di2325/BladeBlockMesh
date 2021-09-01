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
    # -----------------------------
    # -------------2---------------
    # -------1------------3--------
    # -0------------------------4--
    # -9------------------------5--
    # -------8------------6--------
    # -------------7---------------
    # -----------------------------

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

M_LENGTH = 7
M_BOUNDARY = 10

M_0 = 10
M_1 = 10

# Calculating number of airfoils and hub connections
number_of_airfoils = 0
for file in os.listdir(os.path.abspath('../Coordinates')):
    if file.startswith('airfoil'):
        number_of_airfoils += 1
number_of_airfoils = round(number_of_airfoils / 2)
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
    Hexes.set_hexes(profile1, profile2, [1, 8, 9, 0], None, (M_BOUNDARY, M_0, m_z))
    Hexes.set_hexes(profile1, profile2, [2, 7, 8, 1], None, (M_BOUNDARY, M_1, m_z))
    Hexes.set_hexes(profile1, profile2, [3, 6, 7, 2], None, (M_BOUNDARY, M_1, m_z))
    Hexes.set_hexes(profile1, profile2, [4, 5, 6, 3], None, (M_BOUNDARY, M_0, m_z))

    Boundaries.set_boundaries(boundary, profile1, [0, 1], profile2, [1, 0])
    Boundaries.set_boundaries(boundary, profile1, [1, 2], profile2, [2, 1])
    Boundaries.set_boundaries(boundary, profile1, [2, 3], profile2, [3, 2])
    Boundaries.set_boundaries(boundary, profile1, [3, 4], profile2, [4, 3])
    Boundaries.set_boundaries(boundary, profile1, [4, 5], profile2, [5, 4])
    Boundaries.set_boundaries(boundary, profile1, [5, 6], profile2, [6, 5])
    Boundaries.set_boundaries(boundary, profile1, [6, 7], profile2, [7, 6])
    Boundaries.set_boundaries(boundary, profile1, [7, 8], profile2, [8, 7])
    Boundaries.set_boundaries(boundary, profile1, [8, 9], profile2, [9, 8])
    Boundaries.set_boundaries(boundary, profile1, [9, 0], profile2, [0, 9])

def copy_blade_profile(profile, ref):
    Vertices.set_verts(profile, rotate_on_angle(ref.verts, 180))
    profile.set_b_splines(1, 0,     rotate_on_angle(ref.b_splines[0][2], 180))
    profile.set_b_splines(2, 1,     rotate_on_angle(ref.b_splines[1][2], 180))
    profile.set_b_splines(3, 2,     rotate_on_angle(ref.b_splines[2][2], 180))
    profile.set_b_splines(4, 3,     rotate_on_angle(ref.b_splines[3][2], 180))
    profile.set_b_splines(6, 5,     rotate_on_angle(ref.b_splines[4][2], 180))
    profile.set_b_splines(7, 6,     rotate_on_angle(ref.b_splines[5][2], 180))
    profile.set_b_splines(8, 7,     rotate_on_angle(ref.b_splines[6][2], 180))
    profile.set_b_splines(9, 8,    rotate_on_angle(ref.b_splines[7][2], 180))
    Splines.set_splines(profile)

# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #
profile_one = []

for i in range(1, number_of_airfoils):
    profile_one.append(Profile())
    profile = profile_one[-1]
    verts, splines = get_airfoil_data(i)
    Vertices.set_verts(profile, verts)
    profile.set_b_splines(1, 0, splines[0])
    profile.set_b_splines(2, 1, splines[1])
    profile.set_b_splines(3, 2, splines[2])
    profile.set_b_splines(4, 3, splines[3])
    profile.set_b_splines(6, 5, splines[4])
    profile.set_b_splines(7, 6, splines[5])
    profile.set_b_splines(8, 7, splines[6])
    profile.set_b_splines(9, 8, splines[7])
    Splines.set_splines(profile)

for i in range(number_of_airfoils - 2):
    if i == 0:
        current_z = round(M_LENGTH * 1.75)
    elif i == number_of_airfoils - 3:
        current_z = round(M_LENGTH / 2.25)
    else:
        current_z = M_LENGTH
    blade_hex(profile_one[i], profile_one[i + 1], "blade_one", current_z)


profile_two = []
for i in range(number_of_airfoils - 1):
    profile_two.append(Profile())
    copy_blade_profile(profile_two[i], profile_one[i])

for i in range(number_of_airfoils - 2):
    if i == 0:
        current_z = round(M_LENGTH * 1.75)
    elif i == number_of_airfoils - 3:
        current_z = round(M_LENGTH / 2.25)
    else:
        current_z = M_LENGTH
    blade_hex(profile_two[i], profile_two[i + 1], "blade_two", current_z)

Hexes.set_hexes(profile_one[0], profile_two[0], [8, 1, 0, 9], [6, 3, 4, 5], (M_BOUNDARY, M_0, M_LENGTH*2))
Hexes.set_hexes(profile_one[0], profile_two[0], [7, 2, 1, 8], [7, 2, 3, 6], (M_BOUNDARY, M_1, M_LENGTH*2))
Hexes.set_hexes(profile_one[0], profile_two[0], [6, 3, 2, 7], [8, 1, 2, 7], (M_BOUNDARY, M_1, M_LENGTH*2))
Hexes.set_hexes(profile_one[0], profile_two[0], [5, 4, 3, 6], [9, 0, 1, 8], (M_BOUNDARY, M_0, M_LENGTH*2))

Boundaries.set_boundaries("blade_tip_one", profile_one[-1], [1, 8, 9, 0])
Boundaries.set_boundaries("blade_tip_one", profile_one[-1], [2, 7, 8, 1])
Boundaries.set_boundaries("blade_tip_one", profile_one[-1], [3, 6, 7, 2])
Boundaries.set_boundaries("blade_tip_one", profile_one[-1], [4, 5, 6, 3])

Boundaries.set_boundaries("blade_tip_two", profile_two[-1], [1, 8, 9, 0])
Boundaries.set_boundaries("blade_tip_two", profile_two[-1], [2, 7, 8, 1])
Boundaries.set_boundaries("blade_tip_two", profile_two[-1], [3, 6, 7, 2])
Boundaries.set_boundaries("blade_tip_two", profile_two[-1], [4, 5, 6, 3])

Boundaries.set_boundaries("hub", profile_one[0], [1, 0], profile_two[0], [4, 3])
Boundaries.set_boundaries("hub", profile_one[0], [2, 1], profile_two[0], [3, 2])
Boundaries.set_boundaries("hub", profile_one[0], [3, 2], profile_two[0], [2, 1])
Boundaries.set_boundaries("hub", profile_one[0], [4, 3], profile_two[0], [1, 0])
Boundaries.set_boundaries("hub", profile_one[0], [5, 4], profile_two[0], [0, 9])
Boundaries.set_boundaries("hub", profile_one[0], [6, 5], profile_two[0], [9, 8])
Boundaries.set_boundaries("hub", profile_one[0], [7, 6], profile_two[0], [8, 7])
Boundaries.set_boundaries("hub", profile_one[0], [8, 7], profile_two[0], [7, 6])
Boundaries.set_boundaries("hub", profile_one[0], [9, 8], profile_two[0], [6, 5])
Boundaries.set_boundaries("hub", profile_one[0], [0, 9], profile_two[0], [5, 4])

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
