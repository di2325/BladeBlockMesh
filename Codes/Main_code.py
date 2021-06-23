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
    # 7----------4
    # --3------0--
    # --2------1--
    # 6-----------5
"""
# ==================================================================================================================== #
# Importing libraries and classes
from Codes.Math.Transformation_of_vertices import *
from Codes.Math.Custom_Math import triangle_side
from Codes.Math.Custom_Math import triangle_rad

from Codes.BlockMesh.BlockMesh import BlockMesh
from Codes.BlockMesh.Vertices import Vertices
from Codes.BlockMesh.Hexes import Hexes
from Codes.BlockMesh.Splines import Splines
from Codes.BlockMesh.Boundaries import Boundaries

from Codes.Profiles.Profile import Profile

# Constant variables
NUMBER_OF_BLADES = 3
HUB_RAD = 4
HUB_LENGTH = 6
TIP_LENGTH = 65
BLADE_TIP_RAD = triangle_rad(HUB_LENGTH / 2, TIP_LENGTH)
RADS = [HUB_RAD, 5.5, 8.2, 11.7, 15.6, 20.0, 24.1, 28.0, 32.4,
        36.2, 40.4, 44.5, 48.6, 52.5, 56, 59.0, 61.6, BLADE_TIP_RAD]

# Calculating number of airfoils and hub connections
number_of_airfoils = 0
for file in os.listdir(os.path.abspath('../Coordinates')):
    if file.startswith('airfoil'):
        number_of_airfoils += 1
# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Main blade
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

# Create first profile class (near the hub)
profiles = [Profile()]
# Extract coordinates and splines
verts, splines = get_airfoil_data(0)
# Calculate z position of a profile
z = triangle_side(HUB_RAD, HUB_LENGTH / 2)
# Calculate coordinates of a square shell and add them to the rest of coordinates
verts.extend(create_square(HUB_LENGTH, z))
# Add vertices to the global and local lists
Vertices.set_verts(profiles[0], verts)
# Create splines in the local lists
profiles[0].set_b_splines(0, 3, splines[0])
profiles[0].set_b_splines(3, 2, splines[1])
profiles[0].set_b_splines(2, 1, splines[2])
profiles[0].set_b_splines(1, 0, splines[3])
profiles[0].set_arc_splines(4, 7, [RADS[0], HUB_LENGTH / 2, 0])
profiles[0].set_arc_splines(5, 6, [RADS[0], -HUB_LENGTH / 2, 0])
# Send splines to the global list
Splines.set_splines(profiles[0])

# Create the rest of the profiles
for i in range(1, number_of_airfoils - 1):
    profiles.append(Profile())
    verts, splines = get_airfoil_data(i)
    z = (verts[0][2] + verts[1][2] + verts[2][2] + verts[3][2]) / 4
    verts.extend(create_square(HUB_LENGTH, z))
    Vertices.set_verts(profiles[i], verts)
    profiles[i].set_b_splines(0, 3, splines[0])
    profiles[i].set_b_splines(3, 2, splines[1])
    profiles[i].set_b_splines(2, 1, splines[2])
    profiles[i].set_b_splines(1, 0, splines[3])
    Splines.set_splines(profiles[i])

# Create blade tip profile at length of 65
profiles.append(Profile())
verts = create_square(1, TIP_LENGTH)
verts.extend(create_square(HUB_LENGTH, TIP_LENGTH))
Vertices.set_verts(profiles[-1], verts)
profiles[-1].set_arc_splines(4, 7, [RADS[-1], HUB_LENGTH / 2, 0])
profiles[-1].set_arc_splines(5, 6, [RADS[-1], -HUB_LENGTH / 2, 0])
Splines.set_splines(profiles[-1])

for i in range(number_of_airfoils - 2):
    # Create hexes and store them at the global list
    Hexes.set_hexes(profiles[i], profiles[i + 1], [0, 3, 7, 4], [15, 10, 10])
    Hexes.set_hexes(profiles[i], profiles[i + 1], [3, 2, 6, 7], [10, 10, 10])
    Hexes.set_hexes(profiles[i], profiles[i + 1], [2, 1, 5, 6], [15, 10, 10])
    Hexes.set_hexes(profiles[i], profiles[i + 1], [1, 0, 4, 5], [10, 10, 10])
    # Create boundaries and store them at the global list
    Boundaries.set_boundaries("blade", profiles[i], [0, 3], profiles[i + 1], [3, 0])
    Boundaries.set_boundaries("blade", profiles[i], [3, 2], profiles[i + 1], [2, 3])
    Boundaries.set_boundaries("blade", profiles[i], [2, 1], profiles[i + 1], [1, 2])
    Boundaries.set_boundaries("blade", profiles[i], [1, 0], profiles[i + 1], [0, 1])

# Creating tip hexes and boundaries
Hexes.set_hexes(profiles[-2], profiles[-1], [0, 3, 7, 4], [15, 10, 10])
Hexes.set_hexes(profiles[-2], profiles[-1], [3, 2, 6, 7], [10, 10, 10])
Hexes.set_hexes(profiles[-2], profiles[-1], [2, 1, 5, 6], [15, 10, 10])
Hexes.set_hexes(profiles[-2], profiles[-1], [1, 0, 4, 5], [10, 10, 10])
Hexes.set_hexes(profiles[-2], profiles[-1], [0, 1, 2, 3], [10, 15, 10])
Boundaries.set_boundaries("blade", profiles[-2], [3, 2, 1, 0])
Boundaries.set_boundaries("hub", profiles[0], [0, 4, 7, 3])
Boundaries.set_boundaries("hub", profiles[0], [3, 7, 6, 2])
Boundaries.set_boundaries("hub", profiles[0], [2, 6, 5, 1])
Boundaries.set_boundaries("hub", profiles[0], [1, 5, 4, 0])

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Left blade
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

# Create initial variables and hub profile
profiles_left = [Profile()]
angle = -120
# Copy vertices
reference = profiles[0]
verts = rotate_on_angle(reference.verts, angle)
Vertices.set_verts(profiles_left[0], verts)
# Copy splines
b_splines = []
for spline in reference.b_splines:
    b_splines.append(rotate_on_angle(spline[2], angle))
arc_splines = []
for spline in reference.arc_splines:
    arc_splines.append(rotate_on_angle(spline[2], angle))
profiles_left[0].set_b_splines(0, 3, b_splines[0])
profiles_left[0].set_b_splines(3, 2, b_splines[1])
profiles_left[0].set_b_splines(2, 1, b_splines[2])
profiles_left[0].set_b_splines(1, 0, b_splines[3])
profiles_left[0].set_arc_splines(7, 4, [RADS[0], HUB_LENGTH / 2, 0])
profiles_left[0].set_arc_splines(6, 5, [RADS[0], -HUB_LENGTH / 2, 0])
Splines.set_splines(profiles_left[0])

# Create the rest of profiles
for i in range(1, number_of_airfoils - 1):
    profiles_left.append(Profile())
    reference = profiles[i]
    verts = rotate_on_angle(reference.verts, angle)
    Vertices.set_verts(profiles_left[i], verts)
    b_splines = []
    for spline in reference.b_splines:
        b_splines.append(rotate_on_angle(spline[2], angle))
    profiles_left[i].set_b_splines(0, 3, b_splines[0])
    profiles_left[i].set_b_splines(3, 2, b_splines[1])
    profiles_left[i].set_b_splines(2, 1, b_splines[2])
    profiles_left[i].set_b_splines(1, 0, b_splines[3])
    Splines.set_splines(profiles_left[i])

# Tip profile
profiles_left.append(Profile())
reference = profiles[-1]
verts = rotate_on_angle(reference.verts, angle)
Vertices.set_verts(profiles_left[-1], verts)
profiles_left[-1].set_arc_splines(7, 4, [RADS[-1], HUB_LENGTH / 2, 0])
profiles_left[-1].set_arc_splines(6, 5, [RADS[-1], -HUB_LENGTH / 2, 0])
Splines.set_splines(profiles_left[-1])

for i in range(number_of_airfoils - 2):
    # Create hexes and store them at the global list
    Hexes.set_hexes(profiles_left[i], profiles_left[i + 1], [0, 3, 7, 4], [15, 10, 10])
    Hexes.set_hexes(profiles_left[i], profiles_left[i + 1], [3, 2, 6, 7], [10, 10, 10])
    Hexes.set_hexes(profiles_left[i], profiles_left[i + 1], [2, 1, 5, 6], [15, 10, 10])
    Hexes.set_hexes(profiles_left[i], profiles_left[i + 1], [1, 0, 4, 5], [10, 10, 10])
    # Create boundaries and store them at the global list
    Boundaries.set_boundaries("blade", profiles_left[i], [0, 3], profiles_left[i + 1], [3, 0])
    Boundaries.set_boundaries("blade", profiles_left[i], [3, 2], profiles_left[i + 1], [2, 3])
    Boundaries.set_boundaries("blade", profiles_left[i], [2, 1], profiles_left[i + 1], [1, 2])
    Boundaries.set_boundaries("blade", profiles_left[i], [1, 0], profiles_left[i + 1], [0, 1])

# Creating tip hexes and boundaries
Hexes.set_hexes(profiles_left[-2], profiles_left[-1], [0, 3, 7, 4], [15, 10, 10])
Hexes.set_hexes(profiles_left[-2], profiles_left[-1], [3, 2, 6, 7], [10, 10, 10])
Hexes.set_hexes(profiles_left[-2], profiles_left[-1], [2, 1, 5, 6], [15, 10, 10])
Hexes.set_hexes(profiles_left[-2], profiles_left[-1], [1, 0, 4, 5], [10, 10, 10])
Hexes.set_hexes(profiles_left[-2], profiles_left[-1], [0, 1, 2, 3], [10, 15, 10])
Boundaries.set_boundaries("blade", profiles_left[-2], [3, 2, 1, 0])
Boundaries.set_boundaries("hub", profiles_left[0], [0, 4, 7, 3])
Boundaries.set_boundaries("hub", profiles_left[0], [3, 7, 6, 2])
Boundaries.set_boundaries("hub", profiles_left[0], [2, 6, 5, 1])
Boundaries.set_boundaries("hub", profiles_left[0], [1, 5, 4, 0])

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Right blade
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

# Create initial variables and hub profile
profiles_right = [Profile()]
angle = 120
# Copy vertices
reference = profiles[0]
verts = rotate_on_angle(reference.verts, angle)
Vertices.set_verts(profiles_right[0], verts)
# Copy splines
b_splines = []
for spline in reference.b_splines:
    b_splines.append(rotate_on_angle(spline[2], angle))
arc_splines = []
for spline in reference.arc_splines:
    arc_splines.append(rotate_on_angle(spline[2], angle))
profiles_right[0].set_b_splines(0, 3, b_splines[0])
profiles_right[0].set_b_splines(3, 2, b_splines[1])
profiles_right[0].set_b_splines(2, 1, b_splines[2])
profiles_right[0].set_b_splines(1, 0, b_splines[3])
profiles_right[0].set_arc_splines(4, 7, [0, HUB_LENGTH / 2, RADS[0]])
profiles_right[0].set_arc_splines(5, 6, [0, -HUB_LENGTH / 2, RADS[0]])
Splines.set_splines(profiles_right[0])

# Create the rest of profiles
for i in range(1, number_of_airfoils - 1):
    profiles_right.append(Profile())
    reference = profiles[i]
    verts = rotate_on_angle(reference.verts, angle)
    Vertices.set_verts(profiles_right[i], verts)
    b_splines = []
    for spline in reference.b_splines:
        b_splines.append(rotate_on_angle(spline[2], angle))
    profiles_right[i].set_b_splines(0, 3, b_splines[0])
    profiles_right[i].set_b_splines(3, 2, b_splines[1])
    profiles_right[i].set_b_splines(2, 1, b_splines[2])
    profiles_right[i].set_b_splines(1, 0, b_splines[3])
    Splines.set_splines(profiles_right[i])

# Tip profile
profiles_right.append(Profile())
reference = profiles[-1]
verts = rotate_on_angle(reference.verts, angle)
Vertices.set_verts(profiles_right[-1], verts)
profiles_right[-1].set_arc_splines(4, 7, [0, HUB_LENGTH / 2, RADS[-1]])
profiles_right[-1].set_arc_splines(5, 6, [0, -HUB_LENGTH / 2, RADS[-1]])
Splines.set_splines(profiles_right[-1])

for i in range(number_of_airfoils - 2):
    # Create hexes and store them at the global list
    Hexes.set_hexes(profiles_right[i], profiles_right[i + 1], [0, 3, 7, 4], [15, 10, 10])
    Hexes.set_hexes(profiles_right[i], profiles_right[i + 1], [3, 2, 6, 7], [10, 10, 10])
    Hexes.set_hexes(profiles_right[i], profiles_right[i + 1], [2, 1, 5, 6], [15, 10, 10])
    Hexes.set_hexes(profiles_right[i], profiles_right[i + 1], [1, 0, 4, 5], [10, 10, 10])
    # Create boundaries and store them at the global list
    Boundaries.set_boundaries("blade", profiles_right[i], [0, 3], profiles_right[i + 1], [3, 0])
    Boundaries.set_boundaries("blade", profiles_right[i], [3, 2], profiles_right[i + 1], [2, 3])
    Boundaries.set_boundaries("blade", profiles_right[i], [2, 1], profiles_right[i + 1], [1, 2])
    Boundaries.set_boundaries("blade", profiles_right[i], [1, 0], profiles_right[i + 1], [0, 1])

# Creating tip hexes and boundaries
Hexes.set_hexes(profiles_right[-2], profiles_right[-1], [0, 3, 7, 4], [15, 10, 10])
Hexes.set_hexes(profiles_right[-2], profiles_right[-1], [3, 2, 6, 7], [10, 10, 10])
Hexes.set_hexes(profiles_right[-2], profiles_right[-1], [2, 1, 5, 6], [15, 10, 10])
Hexes.set_hexes(profiles_right[-2], profiles_right[-1], [1, 0, 4, 5], [10, 10, 10])
Hexes.set_hexes(profiles_right[-2], profiles_right[-1], [0, 1, 2, 3], [10, 15, 10])
Boundaries.set_boundaries("blade", profiles_right[-2], [3, 2, 1, 0])
Boundaries.set_boundaries("hub", profiles_right[0], [0, 4, 7, 3])
Boundaries.set_boundaries("hub", profiles_right[0], [3, 7, 6, 2])
Boundaries.set_boundaries("hub", profiles_right[0], [2, 6, 5, 1])
Boundaries.set_boundaries("hub", profiles_right[0], [1, 5, 4, 0])

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Create right fillers
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

fillers_right = []
for i in range(number_of_airfoils):
    fillers_right.append(Profile())
    fillers_right[i].verts_id = [profiles_right[i].verts_id[7], profiles_right[i].verts_id[6],
                                 profiles[i].verts_id[5], profiles[i].verts_id[4]]
    fillers_right[i].set_arc_splines(0, 3, [0, HUB_LENGTH / 2, RADS[i]])
    fillers_right[i].set_arc_splines(1, 2, [0, -HUB_LENGTH / 2, RADS[i]])
    Splines.set_splines(fillers_right[i])

Boundaries.set_boundaries("hub", fillers_right[0], [3, 2, 1, 0])

for i in range(number_of_airfoils - 1):
    Hexes.set_hexes(fillers_right[i], fillers_right[i + 1], [0, 1, 2, 3], [10, 20, 10])

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Create left fillers
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

fillers_left = []
for i in range(number_of_airfoils):
    fillers_left.append(Profile())
    fillers_left[i].verts_id = [profiles[i].verts_id[7], profiles[i].verts_id[6],
                                profiles_left[i].verts_id[5], profiles_left[i].verts_id[4]]
    fillers_left[i].set_arc_splines(3, 0, [0, HUB_LENGTH / 2, RADS[i]])
    fillers_left[i].set_arc_splines(2, 1, [0, -HUB_LENGTH / 2, RADS[i]])
    Splines.set_splines(fillers_left[i])

Boundaries.set_boundaries("hub", fillers_left[0], [3, 2, 1, 0])

for i in range(number_of_airfoils - 1):
    Hexes.set_hexes(fillers_left[i], fillers_left[i + 1], [0, 1, 2, 3], [10, 20, 10])

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
# Create bot fillers
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

fillers_bot = []
for i in range(number_of_airfoils):
    fillers_bot.append(Profile())
    fillers_bot[i].verts_id = [profiles_left[i].verts_id[7], profiles_left[i].verts_id[6],
                               profiles_right[i].verts_id[5], profiles_right[i].verts_id[4]]
    fillers_bot[i].set_arc_splines(3, 0, [RADS[i], HUB_LENGTH / 2, 0])
    fillers_bot[i].set_arc_splines(2, 1, [RADS[i], -HUB_LENGTH / 2, 0])
    Splines.set_splines(fillers_bot[i])

Boundaries.set_boundaries("hub", fillers_bot[0], [3, 2, 1, 0])

for i in range(number_of_airfoils - 1):
    Hexes.set_hexes(fillers_bot[i], fillers_bot[i + 1], [0, 1, 2, 3], [10, 20, 10])

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
