"""
Main code:
    Generates blockMeshDict file according to imported airfoil profiles.
    Currently, can generate only NREL 5MW wind turbine.

    Project structure:
        BladeBlockMesh              - root folder
        \_ Codes                        - contains all scripts
        \   \_ BlockMesh                    - classes, which create blockMeshDict
        \   \_ Math                         - classes for custom math methods realisation
        \   \_ Three_dimensional            - classes, which store 3D properties
        \   \_ Two_dimensional              - classes, which store 2D properties
        \_ Coordinates                  - contains coordinates of all airfoils
        \_ Output                       - new blockMeshDict file would be save there

    Workflow:
        * Import required libraries and classes
        * Search for airfoils
        * Initiate variables
        * Create all 2D classes
        * Create all 3D classes
        * Collect all data, required for creation of blockMeshDict
        * Create blockMeshDict file
"""
# ==================================================================================================================== #
# Importing libraries and classes
import os
from Codes.BlockMesh.BlockMesh import BlockMesh
from Codes.Two_dimensional.Vertices import Vertices
from Codes.Two_dimensional.Arifoil import Airfoil
from Codes.Two_dimensional.Hollow import Hollow
from Codes.Two_dimensional.Boundaries import Boundaries
from Codes.Three_dimensional.Hex import Hex

# Constant variables
NUMBER_OF_BLADES = 3
HUB_RAD = 4
HUB_LENGTH = 6

# Calculating number of airfoils and hub connections
number_of_airfoils = 0
for file in os.listdir(os.path.abspath('../Coordinates')):
    if file.startswith('airfoil'):
        number_of_airfoils += 1

# Preparing lists for class initialisation
profiles = [0] * number_of_airfoils
blocks = [0] * (number_of_airfoils - 1)

verts = []
hexes = []
edges = []
# ==================================================================================================================== #
# Main Code
# ==================================================================================================================== #

# Generating 2D and 3D classes
for i in range(number_of_airfoils - 1):
    profiles[i] = Airfoil(i)
i += 1
profiles[i] = Hollow(i)

for i in range(number_of_airfoils - 2):
    # Create hex
    blocks[i] = Hex(profiles[i], profiles[i + 1])
    # Assign blade boundaries
    Boundaries.assign_boundaries("blade", profiles[i], [[0, 3], [3, 2], [2, 1], [1, 0]],
                                 profiles[i + 1], [[3, 0], [2, 3], [1, 2], [0, 1]])

# Create tip hex
i += 1
blocks[i] = Hex(profiles[i], profiles[i + 1])

# Assign tip blade boundaries
Boundaries.assign_boundaries("blade", profiles[i], [[0, 3, 2, 1]])

# Getting vertices and edges from 2D classes, and hexes from 3D classes
for profile in profiles:
    edges.extend(profile.get_splines())

for block in blocks:
    hexes.extend(block.get_hex())

BlockMesh.add_to_verts(Vertices.verts)
BlockMesh.add_to_hex(hexes)
BlockMesh.add_to_edges(edges)
BlockMesh.add_to_boundaries(Boundaries.get_boundaries())
BlockMesh.create_blockmeshdict()

# ==================================================================================================================== #
print("Done")
# ==================================================================================================================== #
