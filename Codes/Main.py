# ==============================================================================
# Importing libraries
# ==============================================================================
import os
# ==============================================================================
# Importing Classes
# ==============================================================================
from CreateBlockMeshDict import BlockMesh
from Parent import Parent
from Hub import Hub
from Airfoil import Airfoil
from Blade import Blade
# ==============================================================================
# Core variables
# ==============================================================================
numberOfBlades = 3
Parent.hubRad = 4
Parent.hubHeight = 3
Parent.meshCoeff = 2
# ==============================================================================
# Instances of other variables
# ==============================================================================
numberOfAirfoils = 0
numberOfHubs = 0
Parent.vertCount = 0
Parent.verts = []
Parent.hex = []
Parent.edges = {'BSpline': [], 'arc': []}
Parent.boundaries = {}
# ==============================================================================
# Calculating number of airfoils and hub connections
for file in os.listdir(os.path.abspath('../Coordinates')):
    if file.startswith('airfoil'):
        numberOfAirfoils += 1
# ==============================================================================
hub = Hub()
hub.ExportVerts()
hub.ExportHex()
hub.ExportEdges()
hub.ExportBound()
blade0 = Blade()
blade1 = Blade(False)
blade2 = Blade(False)
for i in range(numberOfAirfoils):
    blade0.airfoil.append(Airfoil(i))
for i in range(numberOfAirfoils):
    blade1.airfoil.append(Airfoil(i, blade0.airfoil[i], 120))
for i in range(numberOfAirfoils):
    blade2.airfoil.append(Airfoil(i, blade0.airfoil[i], -120))

blade0.ExportVerts()
blade1.ExportVerts()
blade2.ExportVerts()

blade0.ExportHex()
blade1.ExportHex()
blade2.ExportHex()

blade0.ExportEdges()
blade1.ExportEdges()
blade2.ExportEdges()

blade0.ExportBound()
blade1.ExportBound()
blade2.ExportBound()
# ==============================================================================
BlockMesh.verts = Parent.ExportVerts()
BlockMesh.hex = Parent.ExportHex()
BlockMesh.edges = Parent.ExportEdges()
BlockMesh.bound = Parent.ExportBound()
BlockMesh.CreateBlockMeshDict()
print("Done")
# ==============================================================================
