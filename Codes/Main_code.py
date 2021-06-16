# =============================================================================
# Importing libraries
# =============================================================================
import os
# =============================================================================
# Importing Classes
# =============================================================================
from Codes.Two_dimensional.Arifoil import Airfoil
# =============================================================================
# Importing BlockMesh
# =============================================================================
from Codes.BlockMesh.BlockMesh import BlockMesh
from Codes.Two_dimensional.Vertices import Vertices
from Codes.Three_dimensional.Hex import Hex
# =============================================================================
# Core variables
# =============================================================================
NUMBER_OF_BLADES = 3
HUB_RAD = 4
HUB_LENGTH = 3
# =============================================================================
# Instances of classes
# =============================================================================
blockMesh = BlockMesh()
# =============================================================================
# Instances of other variables
# =============================================================================
number_of_hub_airfoils = 0
number_of_airfoils = 0

verts = []
hexes = []
edges = []
# =============================================================================
# Calculating number of airfoils and hub connections
for file in os.listdir(os.path.abspath('../Coordinates')):
    if file.startswith('hub'):
        number_of_hub_airfoils += 1
    elif file.startswith('airfoil'):
        number_of_airfoils += 1
# =============================================================================
airfoil1 = Airfoil(5)
airfoil2 = Airfoil(6)
airfoil3 = Airfoil(7)

hex1 = Hex(airfoil1, airfoil2)
hex2 = Hex(airfoil2, airfoil3)

verts.extend(airfoil1.get_verts())
verts.extend(airfoil2.get_verts())
verts.extend(airfoil3.get_verts())

edges.extend(airfoil1.get_spline())
edges.extend(airfoil2.get_spline())
edges.extend(airfoil3.get_spline())

hexes.extend(hex1.get_hex())
hexes.extend(hex2.get_hex())

BlockMesh.add_to_verts(verts)
BlockMesh.add_to_hex(hexes)
BlockMesh.add_to_edges(edges)
BlockMesh.create_blockmeshdict()
# =============================================================================
print("Done")
# =============================================================================
