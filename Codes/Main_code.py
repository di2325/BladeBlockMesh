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


def blade_hex(profile1, profile2, boundary="blade", m_z=M_LENGTH):
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


def create_solid_blade():
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
        profile = profile_two[i]
        ref = profile_one[i]
        Vertices.set_verts(profile, rotate_on_angle(ref.verts, 180))
        profile.set_b_splines(1, 0, rotate_on_angle(ref.b_splines[0][2], 180))
        profile.set_b_splines(2, 1, rotate_on_angle(ref.b_splines[1][2], 180))
        profile.set_b_splines(3, 2, rotate_on_angle(ref.b_splines[2][2], 180))
        profile.set_b_splines(4, 3, rotate_on_angle(ref.b_splines[3][2], 180))
        profile.set_b_splines(6, 5, rotate_on_angle(ref.b_splines[4][2], 180))
        profile.set_b_splines(7, 6, rotate_on_angle(ref.b_splines[5][2], 180))
        profile.set_b_splines(8, 7, rotate_on_angle(ref.b_splines[6][2], 180))
        profile.set_b_splines(9, 8, rotate_on_angle(ref.b_splines[7][2], 180))
        Splines.set_splines(profile)

    for i in range(number_of_airfoils - 2):
        if i == 0:
            current_z = round(M_LENGTH * 1.75)
        elif i == number_of_airfoils - 3:
            current_z = round(M_LENGTH / 2.25)
        else:
            current_z = M_LENGTH
        blade_hex(profile_two[i], profile_two[i + 1], "blade_two", current_z)

    Hexes.set_hexes(profile_one[0], profile_two[0], [8, 1, 0, 9], [6, 3, 4, 5], (M_BOUNDARY, M_0, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [7, 2, 1, 8], [7, 2, 3, 6], (M_BOUNDARY, M_1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [6, 3, 2, 7], [8, 1, 2, 7], (M_BOUNDARY, M_1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [5, 4, 3, 6], [9, 0, 1, 8], (M_BOUNDARY, M_0, M_LENGTH * 2))

    Boundaries.set_boundaries("blade_one_tip", profile_one[-1], [1, 8, 9, 0])
    Boundaries.set_boundaries("blade_one_tip", profile_one[-1], [2, 7, 8, 1])
    Boundaries.set_boundaries("blade_one_tip", profile_one[-1], [3, 6, 7, 2])
    Boundaries.set_boundaries("blade_one_tip", profile_one[-1], [4, 5, 6, 3])

    Boundaries.set_boundaries("blade_two_tip", profile_two[-1], [1, 8, 9, 0])
    Boundaries.set_boundaries("blade_two_tip", profile_two[-1], [2, 7, 8, 1])
    Boundaries.set_boundaries("blade_two_tip", profile_two[-1], [3, 6, 7, 2])
    Boundaries.set_boundaries("blade_two_tip", profile_two[-1], [4, 5, 6, 3])

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


def blade_hex_hollow(profile1, profile2, m_z=M_LENGTH):
    Hexes.set_hexes(profile1, profile2, [10, 19, 9, 0], None, (1, 1, m_z))
    Hexes.set_hexes(profile1, profile2, [11, 10, 0, 1], None, (M_0, 1, m_z))
    Hexes.set_hexes(profile1, profile2, [12, 11, 1, 2], None, (M_1, 1, m_z))
    Hexes.set_hexes(profile1, profile2, [13, 12, 2, 3], None, (M_1, 1, m_z))
    Hexes.set_hexes(profile1, profile2, [14, 13, 3, 4], None, (M_0, 1, m_z))
    Hexes.set_hexes(profile1, profile2, [15, 14, 4, 5], None, (1, 1, m_z))
    Hexes.set_hexes(profile1, profile2, [16, 15, 5, 6], None, (M_0, 1, m_z))
    Hexes.set_hexes(profile1, profile2, [17, 16, 6, 7], None, (M_1, 1, m_z))
    Hexes.set_hexes(profile1, profile2, [18, 17, 7, 8], None, (M_1, 1, m_z))
    Hexes.set_hexes(profile1, profile2, [19, 18, 8, 9], None, (M_0, 1, m_z))


def blade_boundaries(profile1, profile2, boundary="blade", inner=False):
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

    if not inner:
        Boundaries.set_boundaries(boundary + "_i", profile1, [11, 10], profile2, [10, 11])
        Boundaries.set_boundaries(boundary + "_i", profile1, [12, 11], profile2, [11, 12])
        Boundaries.set_boundaries(boundary + "_i", profile1, [13, 12], profile2, [12, 13])
        Boundaries.set_boundaries(boundary + "_i", profile1, [14, 13], profile2, [13, 14])
        Boundaries.set_boundaries(boundary + "_i", profile1, [15, 14], profile2, [14, 15])
        Boundaries.set_boundaries(boundary + "_i", profile1, [16, 15], profile2, [15, 16])
        Boundaries.set_boundaries(boundary + "_i", profile1, [17, 16], profile2, [16, 17])
        Boundaries.set_boundaries(boundary + "_i", profile1, [18, 17], profile2, [17, 18])
        Boundaries.set_boundaries(boundary + "_i", profile1, [19, 18], profile2, [18, 19])
        Boundaries.set_boundaries(boundary + "_i", profile1, [10, 19], profile2, [19, 10])
    else:
        Boundaries.set_boundaries(boundary + "_i", profile1, [10, 19, 18, 11])
        Boundaries.set_boundaries(boundary + "_i", profile1, [11, 18, 17, 12])
        Boundaries.set_boundaries(boundary + "_i", profile1, [12, 17, 16, 13])
        Boundaries.set_boundaries(boundary + "_i", profile1, [13, 16, 15, 14])

        Boundaries.set_boundaries(boundary + "_tip", profile2, [10, 19, 9, 0])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [11, 10, 0, 1])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [12, 11, 1, 2])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [13, 12, 2, 3])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [14, 13, 3, 4])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [15, 14, 4, 5])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [16, 15, 5, 6])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [17, 16, 6, 7])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [18, 17, 7, 8])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [19, 18, 8, 9])

        Boundaries.set_boundaries(boundary + "_tip", profile2, [11, 18, 19, 10])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [12, 17, 18, 11])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [13, 16, 17, 12])
        Boundaries.set_boundaries(boundary + "_tip", profile2, [14, 15, 16, 13])


def create_hollow_blade():
    profile_one = []
    for i in range(1, number_of_airfoils):
        profile_one.append(Profile())
        profile = profile_one[-1]
        verts, splines = get_airfoil_data(i)
        verts_i, splines_i = get_airfoil_data(i + 100)
        verts.extend(verts_i)
        splines.extend(splines_i)
        Vertices.set_verts(profile, verts)
        profile.set_b_splines(1, 0, splines[0])
        profile.set_b_splines(2, 1, splines[1])
        profile.set_b_splines(3, 2, splines[2])
        profile.set_b_splines(4, 3, splines[3])
        profile.set_b_splines(6, 5, splines[4])
        profile.set_b_splines(7, 6, splines[5])
        profile.set_b_splines(8, 7, splines[6])
        profile.set_b_splines(9, 8, splines[7])
        profile.set_b_splines(11, 10, splines[8])
        profile.set_b_splines(12, 11, splines[9])
        profile.set_b_splines(13, 12, splines[10])
        profile.set_b_splines(14, 13, splines[11])
        profile.set_b_splines(16, 15, splines[12])
        profile.set_b_splines(17, 16, splines[13])
        profile.set_b_splines(18, 17, splines[14])
        profile.set_b_splines(19, 18, splines[15])
        Splines.set_splines(profile)

    for i in range(number_of_airfoils - 2):
        if i == 0:
            current_z = round(M_LENGTH * 1.75)
        elif i == number_of_airfoils - 3:
            current_z = round(M_LENGTH / 2.25)
        else:
            current_z = M_LENGTH
        blade_hex_hollow(profile_one[i], profile_one[i + 1], current_z)
        if i != number_of_airfoils - 3:
            blade_boundaries(profile_one[i], profile_one[i + 1], "blade_one", False)
        else:
            blade_boundaries(profile_one[i], profile_one[i + 1], "blade_one", True)
    Hexes.set_hexes(profile_one[-2], profile_one[-1], [11, 18, 19, 10], None, (1, M_0, round(M_LENGTH / 2.25)))
    Hexes.set_hexes(profile_one[-2], profile_one[-1], [12, 17, 18, 11], None, (1, M_1, round(M_LENGTH / 2.25)))
    Hexes.set_hexes(profile_one[-2], profile_one[-1], [13, 16, 17, 12], None, (1, M_1, round(M_LENGTH / 2.25)))
    Hexes.set_hexes(profile_one[-2], profile_one[-1], [14, 15, 16, 13], None, (1, M_0, round(M_LENGTH / 2.25)))

    profile_two = []
    for i in range(number_of_airfoils - 1):
        profile_two.append(Profile())
        profile = profile_two[i]
        ref = profile_one[i]
        Vertices.set_verts(profile, rotate_on_angle(ref.verts, 180))
        profile.set_b_splines(1, 0, rotate_on_angle(ref.b_splines[0][2], 180))
        profile.set_b_splines(2, 1, rotate_on_angle(ref.b_splines[1][2], 180))
        profile.set_b_splines(3, 2, rotate_on_angle(ref.b_splines[2][2], 180))
        profile.set_b_splines(4, 3, rotate_on_angle(ref.b_splines[3][2], 180))
        profile.set_b_splines(6, 5, rotate_on_angle(ref.b_splines[4][2], 180))
        profile.set_b_splines(7, 6, rotate_on_angle(ref.b_splines[5][2], 180))
        profile.set_b_splines(8, 7, rotate_on_angle(ref.b_splines[6][2], 180))
        profile.set_b_splines(9, 8, rotate_on_angle(ref.b_splines[7][2], 180))
        profile.set_b_splines(11, 10, rotate_on_angle(ref.b_splines[8][2], 180))
        profile.set_b_splines(12, 11, rotate_on_angle(ref.b_splines[9][2], 180))
        profile.set_b_splines(13, 12, rotate_on_angle(ref.b_splines[10][2], 180))
        profile.set_b_splines(14, 13, rotate_on_angle(ref.b_splines[11][2], 180))
        profile.set_b_splines(16, 15, rotate_on_angle(ref.b_splines[12][2], 180))
        profile.set_b_splines(17, 16, rotate_on_angle(ref.b_splines[13][2], 180))
        profile.set_b_splines(18, 17, rotate_on_angle(ref.b_splines[14][2], 180))
        profile.set_b_splines(19, 18, rotate_on_angle(ref.b_splines[15][2], 180))
        Splines.set_splines(profile)

    for i in range(number_of_airfoils - 2):
        if i == 0:
            current_z = round(M_LENGTH * 1.75)
        elif i == number_of_airfoils - 3:
            current_z = round(M_LENGTH / 2.25)
        else:
            current_z = M_LENGTH
        if i != number_of_airfoils - 3:
            blade_boundaries(profile_two[i], profile_two[i + 1], "blade_two", False)
        else:
            blade_boundaries(profile_two[i], profile_two[i + 1], "blade_two", True)
        blade_hex_hollow(profile_two[i], profile_two[i + 1], current_z)
    Hexes.set_hexes(profile_two[-2], profile_two[-1], [11, 18, 19, 10], None, (1, M_0, round(M_LENGTH / 2.25)))
    Hexes.set_hexes(profile_two[-2], profile_two[-1], [12, 17, 18, 11], None, (1, M_1, round(M_LENGTH / 2.25)))
    Hexes.set_hexes(profile_two[-2], profile_two[-1], [13, 16, 17, 12], None, (1, M_1, round(M_LENGTH / 2.25)))
    Hexes.set_hexes(profile_two[-2], profile_two[-1], [14, 15, 16, 13], None, (1, M_0, round(M_LENGTH / 2.25)))

    Hexes.set_hexes(profile_one[0], profile_two[0], [19, 10, 0, 9], [15, 14, 4, 5], (1, 1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [10, 11, 1, 0], [14, 13, 3, 4], (M_0, 1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [11, 12, 2, 1], [13, 12, 2, 3], (M_1, 1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [12, 13, 3, 2], [12, 11, 1, 2], (M_1, 1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [13, 14, 4, 3], [11, 10, 0, 1], (M_0, 1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [14, 15, 5, 4], [10, 19, 9, 0], (1, 1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [15, 16, 6, 5], [19, 18, 8, 9], (M_0, 1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [16, 17, 7, 6], [18, 17, 7, 8], (M_1, 1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [17, 18, 8, 7], [17, 16, 6, 7], (M_1, 1, M_LENGTH * 2))
    Hexes.set_hexes(profile_one[0], profile_two[0], [18, 19, 9, 8], [16, 15, 5, 6], (M_0, 1, M_LENGTH * 2))

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

    Boundaries.set_boundaries("hub_i", profile_one[0], [10, 11], profile_two[0], [13, 14])
    Boundaries.set_boundaries("hub_i", profile_one[0], [11, 12], profile_two[0], [12, 13])
    Boundaries.set_boundaries("hub_i", profile_one[0], [12, 13], profile_two[0], [11, 12])
    Boundaries.set_boundaries("hub_i", profile_one[0], [13, 14], profile_two[0], [10, 11])
    Boundaries.set_boundaries("hub_i", profile_one[0], [14, 15], profile_two[0], [19, 10])
    Boundaries.set_boundaries("hub_i", profile_one[0], [15, 16], profile_two[0], [18, 19])
    Boundaries.set_boundaries("hub_i", profile_one[0], [16, 17], profile_two[0], [17, 18])
    Boundaries.set_boundaries("hub_i", profile_one[0], [17, 18], profile_two[0], [16, 17])
    Boundaries.set_boundaries("hub_i", profile_one[0], [18, 19], profile_two[0], [15, 16])
    Boundaries.set_boundaries("hub_i", profile_one[0], [19, 10], profile_two[0], [14, 15])

# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #


# create_solid_blade()


create_hollow_blade()

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
