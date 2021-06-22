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
"""
# ==================================================================================================================== #
# Importing libraries and classes
from Codes.Math.VerticesManipulation import *

from Codes.BlockMesh.BlockMesh import BlockMesh
from Codes.BlockMesh.Vertices import Vertices
from Codes.BlockMesh.Hexes import Hexes
from Codes.BlockMesh.Splines import Splines
from Codes.BlockMesh.Boundaries import Boundaries

from Codes.Profiles.Arifoil import Airfoil
from Codes.Profiles.Hollow import Hollow

# Constant variables
NUMBER_OF_BLADES = 3
HUB_RAD = 4
HUB_LENGTH = 6

# Calculating number of airfoils and hub connections
number_of_airfoils = 0
for file in os.listdir(os.path.abspath('../Coordinates')):
    if file.startswith('airfoil'):
        number_of_airfoils += 1
# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #
# Airfoil structure:
# 7----------4
# --3------0--
# --2------1--
# 6-----------5

profiles = []
for i in range(number_of_airfoils-1):
    profiles.append(Airfoil())
    verts, splines = get_airfoil_data(i)
    z = (verts[0][2] + verts[1][2] + verts[2][2] + verts[3][2]) / 4
    verts.extend(create_square(HUB_LENGTH, z))
    Vertices.set_verts(profiles[i], verts)
    profiles[i].set_b_splines(0, 3, splines[0])
    profiles[i].set_b_splines(3, 2, splines[1])
    profiles[i].set_b_splines(2, 1, splines[2])
    profiles[i].set_b_splines(1, 0, splines[3])
    Splines.set_splines(profiles[i])

profiles.append(Airfoil())
verts = create_square(1, 65)
verts.extend(create_square(HUB_LENGTH, 65))
Vertices.set_verts(profiles[-1], verts)

for i in range(number_of_airfoils-2):
    Hexes.set_hexes(profiles[i], profiles[i+1], [0, 3, 7, 4], [15, 10, 10])
    Hexes.set_hexes(profiles[i], profiles[i+1], [3, 2, 6, 7], [10, 10, 10])
    Hexes.set_hexes(profiles[i], profiles[i+1], [2, 1, 5, 6], [15, 10, 10])
    Hexes.set_hexes(profiles[i], profiles[i+1], [1, 0, 4, 5], [10, 10, 10])

    Boundaries.set_boundaries("blade", profiles[i], [0, 3], profiles[i+1], [3, 0])
    Boundaries.set_boundaries("blade", profiles[i], [3, 2], profiles[i+1], [2, 3])
    Boundaries.set_boundaries("blade", profiles[i], [2, 1], profiles[i+1], [1, 2])
    Boundaries.set_boundaries("blade", profiles[i], [1, 0], profiles[i+1], [0, 1])

    Boundaries.set_boundaries("inlet", profiles[i], [4, 5], profiles[i + 1], [5, 4])
    Boundaries.set_boundaries("outlet", profiles[i], [6, 7], profiles[i + 1], [7, 6])
    Boundaries.set_boundaries("wall", profiles[i], [7, 4], profiles[i + 1], [4, 7])
    Boundaries.set_boundaries("wall", profiles[i], [5, 6], profiles[i + 1], [6, 5])

Hexes.set_hexes(profiles[-2], profiles[-1], [0, 3, 7, 4], [15, 10, 10])
Hexes.set_hexes(profiles[-2], profiles[-1], [3, 2, 6, 7], [10, 10, 10])
Hexes.set_hexes(profiles[-2], profiles[-1], [2, 1, 5, 6], [15, 10, 10])
Hexes.set_hexes(profiles[-2], profiles[-1], [1, 0, 4, 5], [10, 10, 10])
Hexes.set_hexes(profiles[-2], profiles[-1], [0, 1, 2, 3], [10, 15, 10])
Boundaries.set_boundaries("blade", profiles[-2], [3, 2, 1, 0])

Boundaries.set_boundaries("inlet", profiles[-2], [4, 5], profiles[-1], [5, 4])
Boundaries.set_boundaries("outlet", profiles[-2], [6, 7], profiles[-1], [7, 6])
Boundaries.set_boundaries("wall", profiles[-2], [7, 4], profiles[-1], [4, 7])
Boundaries.set_boundaries("wall", profiles[-2], [5, 6], profiles[-1], [6, 5])

Boundaries.set_boundaries("wall", profiles[0], [0, 4, 7, 3])
Boundaries.set_boundaries("wall", profiles[0], [3, 7, 6, 2])
Boundaries.set_boundaries("wall", profiles[0], [2, 6, 5, 1])
Boundaries.set_boundaries("wall", profiles[0], [1, 5, 4, 0])

Boundaries.set_boundaries("wall", profiles[-1], [3, 7, 4, 0])
Boundaries.set_boundaries("wall", profiles[-1], [2, 6, 7, 3])
Boundaries.set_boundaries("wall", profiles[-1], [1, 5, 6, 2])
Boundaries.set_boundaries("wall", profiles[-1], [0, 4, 5, 1])
Boundaries.set_boundaries("wall", profiles[-1], [0, 1, 2, 3])

# Export everything to the blockMesh
BlockMesh.add_to_verts(Vertices.get_verts())
BlockMesh.add_to_hex(Hexes.get_hexes())
BlockMesh.add_to_edges(Splines.get_splines())
BlockMesh.add_to_boundaries(Boundaries.get_boundaries())
BlockMesh.create_blockmeshdict()

# ==================================================================================================================== #
print("Done")
# ==================================================================================================================== #
