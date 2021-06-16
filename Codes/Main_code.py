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
hex1 = Hex(airfoil2, airfoil3)

BlockMesh.add_to_verts(Vertices.export_coord())
BlockMesh.create_blockmeshdict()
# =============================================================================
print("Done")
# =============================================================================
