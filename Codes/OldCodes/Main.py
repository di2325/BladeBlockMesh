# ==================================================
# Importing libraries
# ==================================================
import os
# ==================================================
# Importing Functions
# ==================================================
from BlockMeshFunc import GetLastVert
# ==================================================
# Importing BlockMesh
# ==================================================
from Codes.BlockMesh.BlockMesh import BlockMesh
from Airfoil import Airfoil
from Cover import Cover
from Blade import Blade
from Hub import Hub
from Fillers import Fillers
from Filler import Filler
from HubFiller import HubFiller
from SimpleFiller import SimpleFiller
# ==================================================
# Core variables
# ==================================================
numberOfBlades = 3
hubRad = 4
hubLength = 3
# ==================================================
# Instances of classes
# ==================================================
blockMesh = BlockMesh()
# ==================================================
# Instances of other variables
# ==================================================
numberOfHubAirfoils = 0
numberOfAirfoils = 0
hubVert = []
hubHex = []
hubEdges = []
hubBoundaries = []
# ==================================================
# Calculating number of airfoils and hub connections
for file in os.listdir(os.path.abspath('../../Coordinates')):
    if file.startswith('hub'):
        numberOfHubAirfoils += 1
    elif file.startswith('airfoil'):
        numberOfAirfoils += 1
# ==================================================

blade = []
for i in range(numberOfBlades):
    blade.append(Blade())
    blade[i].hub = []
    blade[i].airfoil = []
    blade[i].cover = []

for i in range(numberOfHubAirfoils):
    blade[0].hub.append(Hub(i))

for i in range(numberOfHubAirfoils):
    blade[1].hub.append(Hub(i, GetLastVert(blade[0].hub), blade[0].hub[i], 120))

for i in range(numberOfHubAirfoils):
    blade[2].hub.append(Hub(i, GetLastVert(blade[1].hub), blade[0].hub[i], -120))

# ==================================================
fillers = []
for i in range(2):
    fillers.append(Fillers())
    fillers[i].filler = []
    fillers[i].filler.append(Filler(blade[0], blade[1], i))
    fillers[i].filler.append(Filler(blade[1], blade[2], i, 120))
    fillers[i].filler.append(Filler(blade[2], blade[0], i, -120))
# ==================================================
for i in range(numberOfAirfoils):
    blade[0].airfoil.append(Airfoil(i, GetLastVert(blade[2].hub)))
for i in range(numberOfAirfoils):
    blade[1].airfoil.append(Airfoil(i, GetLastVert(blade[0].airfoil), blade[0].airfoil[i], 120))
for i in range(numberOfAirfoils):
    blade[2].airfoil.append(Airfoil(i, GetLastVert(blade[1].airfoil), blade[0].airfoil[i], -120))
# ==================================================
for i in range(numberOfAirfoils):
    blade[0].cover.append(Cover(blade[0].airfoil[i], i, GetLastVert(blade[2].airfoil)))
for i in range(numberOfAirfoils):
    blade[1].cover.append(Cover(None, i, GetLastVert(blade[0].cover), blade[0].cover[i], 120))
for i in range(numberOfAirfoils):
    blade[2].cover.append(Cover(None, i, GetLastVert(blade[1].cover), blade[0].cover[i], -120))
# ==================================================
for i in range(numberOfBlades):
    for ii in range(numberOfHubAirfoils):
        hubVert += [line for line in blade[i].hub[ii].ExportVerts()]
for i in range(numberOfBlades):
    for ii in range(numberOfHubAirfoils - 1):
        hubHex += [line for line in blade[i].ExportHexHub(ii)]
for i in range(numberOfBlades):
    for ii in range(numberOfHubAirfoils):
        hubEdges += [line for line in blade[i].hub[ii].ExportEdges()]

for i in range(numberOfBlades):
    for ii in range(numberOfAirfoils):
        hubVert += [line for line in blade[i].airfoil[ii].ExportVerts()]
for i in range(numberOfBlades):
    for ii in range(numberOfAirfoils - 1):
        if i == 0:
            hubHex += [line for line in blade[i].ExportHexAirfoil(ii)]  # , True)]
        else:
            hubHex += [line for line in blade[i].ExportHexAirfoil(ii)]
for i in range(numberOfBlades):
    for ii in range(numberOfAirfoils):
        hubEdges += [line for line in blade[i].airfoil[ii].ExportEdges()]
for i in range(numberOfBlades):
    hubBoundaries.append(f"\ninterfaceIn{i}")
    hubBoundaries.append("\n{")
    hubBoundaries.append("\n\ttype patch;")
    hubBoundaries.append("\n\tfaces")
    hubBoundaries.append("\n\t(")
    for ii in range(numberOfAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportBoundariesAirfoil(ii)]
    hubBoundaries.append("\n\t);")
    hubBoundaries.append("\n}")

for i in range(numberOfBlades):
    for ii in range(numberOfAirfoils):
        hubVert += [line for line in blade[i].cover[ii].ExportVerts()]
for i in range(numberOfBlades):
    for ii in range(numberOfAirfoils - 1):
        hubHex += [line for line in blade[i].ExportHexCover(ii)]
for i in range(numberOfBlades):
    for ii in range(numberOfAirfoils):
        hubEdges += [line for line in blade[i].cover[ii].ExportEdges()]

for i in range(numberOfBlades):
    hubBoundaries.append(f"\ninterfaceOut{i}")
    hubBoundaries.append("\n{")
    hubBoundaries.append("\n\ttype patch;")
    hubBoundaries.append("\n\tfaces")
    hubBoundaries.append("\n\t(")
    for ii in range(numberOfAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportBoundariesCover(ii)]
    hubBoundaries.append("\n\t);")
    hubBoundaries.append("\n}")

hubBoundaries.append(f"\nblade1")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype wall;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
for i in range(1):
    for ii in range(numberOfAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportBoundariesBladeAirfoil(ii)]
    for ii in range(numberOfHubAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportBoundariesBladeHub(ii)]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

hubBoundaries.append(f"\nblade")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype wall;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
for i in range(1, numberOfBlades):
    for ii in range(numberOfAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportBoundariesBladeAirfoil(ii)]
    for ii in range(numberOfHubAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportBoundariesBladeHub(ii)]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

fillers.append(HubFiller(GetLastVert(blade[2].cover), hubRad, hubLength))
hubVert += [line for line in fillers[2].shell]
hubHex += [line for line in fillers[2].ExportHubFillerCover()]
hubEdges += [line for line in fillers[2].ExportEdges()]

fillers.append(HubFiller(GetLastVert(fillers), hubRad, hubLength, -1))
hubVert += [line for line in fillers[3].shell]
hubHex += [line for line in fillers[3].ExportHubFillerCover()]
hubEdges += [line for line in fillers[3].ExportEdges()]

hubBoundaries.append(f"\nhub")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype wall;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
for i in range(numberOfBlades):
    hubBoundaries += [line for line in blade[i].ExportBoundariesHub()]
    hubBoundaries += [line for line in fillers[0].filler[i].ExportBoundariesHub()]
hubBoundaries += [line for line in fillers[2].ExportBoundaries()]
hubBoundaries += [line for line in fillers[3].ExportBoundaries()]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

hubBoundaries.append(f"\ninterfaceInHubTop")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype patch;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
hubBoundaries += [line for line in fillers[2].ExportBoundariesInterface()]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

hubBoundaries.append(f"\ninterfaceInHubBot")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype patch;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
hubBoundaries += [line for line in fillers[3].ExportBoundariesInterface()]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

hubBoundaries.append(f"\ninterfaceOutHubTop")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype patch;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
for i in range(numberOfBlades):
    hubBoundaries += [line for line in blade[i].ExportBoundariesInterfaceHub()]
    hubBoundaries += [line for line in fillers[0].filler[i].ExportBoundariesInterfaceHub()]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

hubBoundaries.append(f"\ninterfaceOutHubBot")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype patch;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
for i in range(numberOfBlades):
    hubBoundaries += [line for line in blade[i].ExportBoundariesInterfaceHub(False)]
    hubBoundaries += [line for line in fillers[0].filler[i].ExportBoundariesInterfaceHub(False)]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

for i in range(numberOfBlades):
    hubBoundaries.append(f"\ninterfaceOutAirfoilToHub{i}")
    hubBoundaries.append("\n{")
    hubBoundaries.append("\n\ttype patch;")
    hubBoundaries.append("\n\tfaces")
    hubBoundaries.append("\n\t(")
    hubBoundaries += [line for line in blade[i].ExportBoundariesAirfoilToHub()]
    hubBoundaries.append("\n\t);")
    hubBoundaries.append("\n}")

for i in range(numberOfBlades):
    hubBoundaries.append(f"\ninterfaceInAirfoilToHub{i}")
    hubBoundaries.append("\n{")
    hubBoundaries.append("\n\ttype patch;")
    hubBoundaries.append("\n\tfaces")
    hubBoundaries.append("\n\t(")
    hubBoundaries += [line for line in blade[i].ExportBoundariesHubToAirfoil()]
    hubBoundaries.append("\n\t);")
    hubBoundaries.append("\n}")

for i in range(numberOfBlades):
    hubBoundaries.append(f"\nInSectorLeft{i}")
    hubBoundaries.append("\n{")
    hubBoundaries.append("\n\ttype patch;")
    hubBoundaries.append("\n\tfaces")
    hubBoundaries.append("\n\t(")
    for ii in range(numberOfAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportBoundariesInSectorLeft(ii)]
    hubBoundaries.append("\n\t);")
    hubBoundaries.append("\n}")
    hubBoundaries.append(f"\nInSectorRight{i}")
    hubBoundaries.append("\n{")
    hubBoundaries.append("\n\ttype patch;")
    hubBoundaries.append("\n\tfaces")
    hubBoundaries.append("\n\t(")
    for ii in range(numberOfAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportBoundariesInSectorRight(ii)]
    hubBoundaries.append("\n\t);")
    hubBoundaries.append("\n}")
    hubBoundaries.append(f"\nInSectorMiddle{i}")
    hubBoundaries.append("\n{")
    hubBoundaries.append("\n\ttype patch;")
    hubBoundaries.append("\n\tfaces")
    hubBoundaries.append("\n\t(")
    hubBoundaries += [line for line in fillers[1].filler[i].ExportBoundariesInSectorMiddle()]
    hubBoundaries.append("\n\t);")
    hubBoundaries.append("\n}")
    hubBoundaries.append(f"\nInTip{i}")
    hubBoundaries.append("\n{")
    hubBoundaries.append("\n\ttype patch;")
    hubBoundaries.append("\n\tfaces")
    hubBoundaries.append("\n\t(")
    hubBoundaries += [line for line in blade[i].ExportBoundariesInTip()]
    hubBoundaries.append("\n\t);")
    hubBoundaries.append("\n}")

simpleFiller = []
simpleFiller.append(SimpleFiller(GetLastVert(fillers)))
hubVert += [line for line in simpleFiller[0].shell]
hubHex += [line for line in simpleFiller[0].ExportHex()]
hubBoundaries += [line for line in simpleFiller[0].ExportBoundaryTip()]
hubEdges += [line for line in simpleFiller[0].ExportEdges()]

hubHex += [line for line in fillers[0].filler[0].ExportHex()]
hubHex += [line for line in fillers[0].filler[1].ExportHex()]
hubHex += [line for line in fillers[0].filler[2].ExportHex()]

hubEdges += [line for line in fillers[0].filler[0].ExportEdges()]
hubEdges += [line for line in fillers[0].filler[1].ExportEdges()]
hubEdges += [line for line in fillers[0].filler[2].ExportEdges()]

hubHex += [line for line in fillers[1].filler[0].ExportHex()]
hubHex += [line for line in fillers[1].filler[1].ExportHex()]
hubHex += [line for line in fillers[1].filler[2].ExportHex()]

hubEdges += [line for line in fillers[1].filler[0].ExportEdges()]
hubEdges += [line for line in fillers[1].filler[1].ExportEdges()]
hubEdges += [line for line in fillers[1].filler[2].ExportEdges()]

hubBoundaries.append(f"\nfrontOut3")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype patch;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
hubBoundaries += [line for line in simpleFiller[0].ExportFrontOut(1)]
for i in range(numberOfBlades):
    for ii in range(numberOfAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportFrontOut(ii, 1)]
    for ii in range(numberOfHubAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportFrontOutHub(ii, 1)]
        hubBoundaries += [line for line in fillers[0].filler[i].ExportFrontOut(ii, 1)]
hubBoundaries += [line for line in fillers[2].ExportFrontOut(1)]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

hubBoundaries.append(f"\nfrontOut2")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype patch;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
hubBoundaries += [line for line in simpleFiller[0].ExportFrontOut(2)]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

hubBoundaries.append(f"\nfrontOut1")
hubBoundaries.append("\n{")
hubBoundaries.append("\n\ttype patch;")
hubBoundaries.append("\n\tfaces")
hubBoundaries.append("\n\t(")
hubBoundaries += [line for line in simpleFiller[0].ExportFrontOut(3)]
for i in range(numberOfBlades):
    for ii in range(numberOfAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportFrontOut(ii, 3)]
    for ii in range(numberOfHubAirfoils - 1):
        hubBoundaries += [line for line in blade[i].ExportFrontOutHub(ii, 3)]
        hubBoundaries += [line for line in fillers[0].filler[i].ExportFrontOut(ii, 3)]
hubBoundaries += [line for line in fillers[3].ExportFrontOut(3)]
hubBoundaries.append("\n\t);")
hubBoundaries.append("\n}")

blockMesh.AddToVertToPrint(hubVert)
blockMesh.AddToHexToPrint(hubHex)
blockMesh.AddToEdgesToPrint(hubEdges)
blockMesh.AddToBoundariesToPrint(hubBoundaries)
blockMesh.CreateBlockMeshDict()
print("Done")