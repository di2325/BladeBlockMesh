from CustomMath import Sin, Cos, RotateOnAngle
class Blade:
    def __init__(self,):
        self.meshCoeff = 0.4
    
#==================================================   
    def ExportHexHub(self, i):
        output = []
        meshCoeff = self.meshCoeff
        output.append(self.CreateHex(i, [0, 15, 4, 5], self.Cells([10, 5, 10], meshCoeff)))
        output.append(self.CreateHex(i, [1, 0, 5, 6], self.Cells([10, 5, 10], meshCoeff)))
        output.append(self.CreateHex(i, [8, 1, 6, 7], self.Cells([10, 5, 10], meshCoeff)))
        output.append(self.CreateHex(i, [9, 2, 1, 8], self.Cells([10, 10, 10], meshCoeff)))
        output.append(self.CreateHex(i, [10, 11, 2, 9], self.Cells([10, 5, 10], meshCoeff)))
        output.append(self.CreateHex(i, [11, 12, 3, 2], self.Cells([10, 5, 10], meshCoeff)))
        output.append(self.CreateHex(i, [12, 13, 14, 3], self.Cells([10, 5, 10], meshCoeff)))
        output.append(self.CreateHex(i, [3, 14, 15, 0], self.Cells([10, 10, 10], meshCoeff)))
        output.append(self.CreateHex(i, [5, 4, 16, 17], self.Cells([10, 15, 10], meshCoeff)))
        output.append(self.CreateHex(i, [6, 5, 17, 18], self.Cells([10, 15, 10], meshCoeff)))
        output.append(self.CreateHex(i, [7, 6, 18, 19], self.Cells([10, 15, 10], meshCoeff)))
        output.append(self.CreateHex(i, [20, 21, 11, 10], self.Cells([10, 15, 10], meshCoeff)))
        output.append(self.CreateHex(i, [21, 22, 12, 11], self.Cells([10, 15, 10], meshCoeff)))
        output.append(self.CreateHex(i, [22, 23, 13, 12], self.Cells([10, 15, 10], meshCoeff)))
        return output
    
    
    def CreateHex(self, i, n, cells = [10, 10, 10], grading = [1, 1, 1]):
        vert0 = self.hub[0+i].vertCount
        vert1 = self.hub[1+i].vertCount
        return f"\n\thex ({vert0[n[0]]} {vert0[n[1]]} {vert0[n[2]]} {vert0[n[3]]} "+\
                            f"{vert1[n[0]]} {vert1[n[1]]} {vert1[n[2]]} {vert1[n[3]]}) rotatingZone "+\
                            f"({cells[0]} {cells[1]} {cells[2]}) simpleGrading "+\
                            f"({grading[0]} {grading[1]} {grading[2]})"
    
    def ExportBoundariesHubToAirfoil(self):
        output = []
        vert = self.hub[2].vertCount
        output.append(f"\n\t\t({vert[5]} {vert[4]} {vert[16]} {vert[17]})")
        output.append(f"\n\t\t({vert[6]} {vert[5]} {vert[17]} {vert[18]})")
        output.append(f"\n\t\t({vert[7]} {vert[6]} {vert[18]} {vert[19]})")
        output.append(f"\n\t\t({vert[8]} {vert[1]} {vert[6]} {vert[7]})")
        output.append(f"\n\t\t({vert[1]} {vert[0]} {vert[5]} {vert[6]})")
        output.append(f"\n\t\t({vert[0]} {vert[15]} {vert[4]} {vert[5]})")
        output.append(f"\n\t\t({vert[3]} {vert[14]} {vert[15]} {vert[0]})")
        output.append(f"\n\t\t({vert[9]} {vert[2]} {vert[1]} {vert[8]})")
        output.append(f"\n\t\t({vert[10]} {vert[11]} {vert[2]} {vert[9]})")
        output.append(f"\n\t\t({vert[11]} {vert[12]} {vert[3]} {vert[2]})")
        output.append(f"\n\t\t({vert[12]} {vert[13]} {vert[14]} {vert[3]})")
        output.append(f"\n\t\t({vert[22]} {vert[23]} {vert[13]} {vert[12]})")
        output.append(f"\n\t\t({vert[21]} {vert[22]} {vert[12]} {vert[11]})")
        output.append(f"\n\t\t({vert[20]} {vert[21]} {vert[11]} {vert[10]})")
        return output
#==================================================    
    def ExportHexAirfoil(self, i, main = False):
        output = []
        meshCoeff = self.meshCoeff
        if main:
            tail = 10
            boundaryLayers = 20
            between = 10
            backAirfoil = 20
            frontAirfoil = 20
            output.append(self.CreateHexAirfoil(i, [0, 4, 5, 6], self.Cells([tail, boundaryLayers, between], meshCoeff), [1, 30, 1]))
            output.append(self.CreateHexAirfoil(i, [1, 0, 6, 7], self.Cells([backAirfoil, boundaryLayers, between], meshCoeff), [1, 30, 1]))
            output.append(self.CreateHexAirfoil(i, [2, 1, 7, 8], self.Cells([frontAirfoil, boundaryLayers, between], meshCoeff), [1, 30, 1]))
            output.append(self.CreateHexAirfoil(i, [3, 2, 8, 9], self.Cells([frontAirfoil, boundaryLayers, between], meshCoeff), [1, 30, 1]))
            output.append(self.CreateHexAirfoil(i, [0, 3, 9, 10], self.Cells([backAirfoil, boundaryLayers, between], meshCoeff), [1, 30, 1]))
            output.append(self.CreateHexAirfoil(i, [4, 0, 10, 11], self.Cells([tail, boundaryLayers, between], meshCoeff), [1, 30, 1]))
        else:
            tail = 10
            boundaryLayers = 10
            between = 10
            backAirfoil = 10
            frontAirfoil = 10
            output.append(self.CreateHexAirfoil(i, [0, 4, 5, 6], self.Cells([tail, boundaryLayers, between], meshCoeff), [1, 1, 1]))
            output.append(self.CreateHexAirfoil(i, [1, 0, 6, 7], self.Cells([backAirfoil, boundaryLayers, between], meshCoeff), [1, 1, 1]))
            output.append(self.CreateHexAirfoil(i, [2, 1, 7, 8], self.Cells([frontAirfoil, boundaryLayers, between], meshCoeff), [1, 1, 1]))
            output.append(self.CreateHexAirfoil(i, [3, 2, 8, 9], self.Cells([frontAirfoil, boundaryLayers, between], meshCoeff), [1, 1, 1]))
            output.append(self.CreateHexAirfoil(i, [0, 3, 9, 10], self.Cells([backAirfoil, boundaryLayers, between], meshCoeff), [1, 1, 1]))
            output.append(self.CreateHexAirfoil(i, [4, 0, 10, 11], self.Cells([tail, boundaryLayers, between], meshCoeff), [1, 1, 1]))
        if i == 14:
            output.append(self.CreateHexAirfoil(i, [0, 1, 2, 3], self.Cells([backAirfoil, frontAirfoil, between], meshCoeff)))
        return output
    
    
    def CreateHexAirfoil(self, i, n, cells = [10, 10, 10], grading = [1, 1, 1]):
        vert0 = self.airfoil[0+i].vertCount
        vert1 = self.airfoil[1+i].vertCount
        return f"\n\thex ({vert0[n[0]]} {vert0[n[1]]} {vert0[n[2]]} {vert0[n[3]]} "+\
                            f"{vert1[n[0]]} {vert1[n[1]]} {vert1[n[2]]} {vert1[n[3]]}) rotatingZone "+\
                            f"({cells[0]} {cells[1]} {cells[2]}) simpleGrading "+\
                            f"({grading[0]} {grading[1]} {grading[2]})"
    
    
    def ExportBoundariesAirfoil(self, i):
        output = []
        vert0 = self.airfoil[0 + i].vertCount
        vert1 = self.airfoil[1 + i].vertCount
        for ii in range(6):
            output.append(f"\n\t\t({vert0[5 + ii]} {vert0[6 + ii]} {vert1[6 + ii]} {vert1[5 + ii]})")
        return output
    def ExportBoundariesAirfoilToHub(self):
        output = []
        vert = self.airfoil[0].vertCount
        output.append(f"\n\t\t({vert[6]} {vert[5]} {vert[4]} {vert[0]})")
        output.append(f"\n\t\t({vert[7]} {vert[6]} {vert[0]} {vert[1]})")
        output.append(f"\n\t\t({vert[8]} {vert[7]} {vert[1]} {vert[2]})")
        output.append(f"\n\t\t({vert[9]} {vert[8]} {vert[2]} {vert[3]})")
        output.append(f"\n\t\t({vert[10]} {vert[9]} {vert[3]} {vert[0]})")
        output.append(f"\n\t\t({vert[11]} {vert[10]} {vert[0]} {vert[4]})")
        vert = self.cover[0].vertCount
        output.append(f"\n\t\t({vert[0]} {vert[1]} {vert[7]} {vert[6]})")
        output.append(f"\n\t\t({vert[1]} {vert[2]} {vert[8]} {vert[7]})")
        output.append(f"\n\t\t({vert[2]} {vert[10]} {vert[9]} {vert[8]})")
        output.append(f"\n\t\t({vert[3]} {vert[11]} {vert[10]} {vert[2]})")
        output.append(f"\n\t\t({vert[13]} {vert[12]} {vert[11]} {vert[3]})")
        output.append(f"\n\t\t({vert[14]} {vert[13]} {vert[3]} {vert[4]})")
        output.append(f"\n\t\t({vert[15]} {vert[14]} {vert[4]} {vert[5]})")
        return output
#================================================== 
    def ExportHexCover(self, i):
        output = []
        meshCoeff = self.meshCoeff
        output.append(self.CreateHexCover(i, [1, 0, 6, 7], self.Cells([10, 15, 10], meshCoeff)))
        output.append(self.CreateHexCover(i, [2, 1, 7, 8], self.Cells([5, 15, 10], meshCoeff)))
        output.append(self.CreateHexCover(i, [10, 2, 8, 9], self.Cells([10, 15, 10], meshCoeff)))
        output.append(self.CreateHexCover(i, [3, 2, 10, 11], self.Cells([10, 10, 10], meshCoeff)))
        output.append(self.CreateHexCover(i, [3, 11, 12, 13], self.Cells([10, 15, 10], meshCoeff)))
        output.append(self.CreateHexCover(i, [4, 3, 13, 14], self.Cells([5, 15, 10], meshCoeff)))
        output.append(self.CreateHexCover(i, [5, 4, 14, 15], self.Cells([10, 15, 10], meshCoeff)))
        return output
    
    
    def CreateHexCover(self, i, n, cells = [10, 10, 10], grading = [1, 1, 1]):
        vert0 = self.cover[0+i].vertCount
        vert1 = self.cover[1+i].vertCount
        return f"\n\thex ({vert0[n[0]]} {vert0[n[1]]} {vert0[n[2]]} {vert0[n[3]]} "+\
                            f"{vert1[n[0]]} {vert1[n[1]]} {vert1[n[2]]} {vert1[n[3]]}) rotatingZone "+\
                            f"({cells[0]} {cells[1]} {cells[2]}) simpleGrading "+\
                            f"({grading[0]} {grading[1]} {grading[2]})"
    
    
    def ExportBoundariesCover(self, i):
        output = []
        vert0 = self.cover[0 + i].vertCount
        vert1 = self.cover[1 + i].vertCount
        for ii in range(5):
            output.append(f"\n\t\t({vert0[1 + ii]} {vert0[0 + ii]} {vert1[0 + ii]} {vert1[1 + ii]})")
        return output
#================================================== 
    def Cells(self, cells, meshCoeff):
        x = round(cells[0]*meshCoeff)
        y = round(cells[1]*meshCoeff)
        z = round(cells[2]*meshCoeff)
        return [x, y, z]
    
    
    def ExportBoundariesBladeAirfoil(self, i):
        output = []
        vert0 = self.airfoil[0 + i].vertCount
        vert1 = self.airfoil[1 + i].vertCount
        if i != 14:
            output.append(f"\n\t\t({vert0[1]} {vert0[0]} {vert1[0]} {vert1[1]})")
            output.append(f"\n\t\t({vert0[2]} {vert0[1]} {vert1[1]} {vert1[2]})")
            output.append(f"\n\t\t({vert0[3]} {vert0[2]} {vert1[2]} {vert1[3]})")
            output.append(f"\n\t\t({vert0[0]} {vert0[3]} {vert1[3]} {vert1[0]})")
        else:
            output.append(f"\n\t\t({vert0[3]} {vert0[2]} {vert0[1]} {vert0[0]})")
        return output
    
    
    def ExportBoundariesBladeHub(self, i):
        output = []
        vert0 = self.hub[0 + i].vertCount
        vert1 = self.hub[1 + i].vertCount
        output.append(f"\n\t\t({vert0[1]} {vert0[0]} {vert1[0]} {vert1[1]})")
        output.append(f"\n\t\t({vert0[2]} {vert0[1]} {vert1[1]} {vert1[2]})")
        output.append(f"\n\t\t({vert0[3]} {vert0[2]} {vert1[2]} {vert1[3]})")
        output.append(f"\n\t\t({vert0[0]} {vert0[3]} {vert1[3]} {vert1[0]})")
        return output
    
    
    def ExportBoundariesHub(self):
        output = []
        vert = self.hub[0].vertCount
        output.append(f"\n\t\t({vert[4]} {vert[15]} {vert[0]} {vert[5]})")
        output.append(f"\n\t\t({vert[5]} {vert[0]} {vert[1]} {vert[6]})")
        output.append(f"\n\t\t({vert[6]} {vert[1]} {vert[8]} {vert[7]})")
        output.append(f"\n\t\t({vert[1]} {vert[2]} {vert[9]} {vert[8]})")
        output.append(f"\n\t\t({vert[2]} {vert[11]} {vert[10]} {vert[9]})")
        output.append(f"\n\t\t({vert[3]} {vert[12]} {vert[11]} {vert[2]})")
        output.append(f"\n\t\t({vert[14]} {vert[13]} {vert[12]} {vert[3]})")
        output.append(f"\n\t\t({vert[15]} {vert[14]} {vert[3]} {vert[0]})")
        return output
    
    
    def ExportBoundariesInterfaceHub(self, top = True):
        output = []
        vert = self.hub[0].vertCount
        if top:
            output.append(f"\n\t\t({vert[23]} {vert[22]} {vert[12]} {vert[13]})")
            output.append(f"\n\t\t({vert[22]} {vert[21]} {vert[11]} {vert[12]})")
            output.append(f"\n\t\t({vert[21]} {vert[20]} {vert[10]} {vert[11]})")
        else:
            output.append(f"\n\t\t({vert[4]} {vert[5]} {vert[17]} {vert[16]})")
            output.append(f"\n\t\t({vert[5]} {vert[6]} {vert[18]} {vert[17]})")
            output.append(f"\n\t\t({vert[6]} {vert[7]} {vert[19]} {vert[18]})")
        return output
    
    
    def ExportBoundariesInSectorLeft(self, i):
        output = []
        vc0 = self.cover[0 + i].vertCount
        vc1 = self.cover[1 + i].vertCount
        va0 = self.airfoil[0 + i].vertCount
        va1 = self.airfoil[1 + i].vertCount
        output.append(f"\n\t\t({va0[4]} {va0[5]} {va1[5]} {va1[4]})")
        output.append(f"\n\t\t({va0[11]} {va0[4]} {va1[4]} {va1[11]})")
        output.append(f"\n\t\t({vc0[0]} {vc0[6]} {vc1[6]} {vc1[0]})")
        output.append(f"\n\t\t({vc0[15]} {vc0[5]} {vc1[5]} {vc1[15]})")
        return output

    def ExportBoundariesInSectorRight(self, i):
        output = []
        vc0 = self.cover[0 + i].vertCount
        vc1 = self.cover[1 + i].vertCount
        output.append(f"\n\t\t({vc0[9]} {vc0[10]} {vc1[10]} {vc1[9]})")
        output.append(f"\n\t\t({vc0[10]} {vc0[11]} {vc1[11]} {vc1[10]})")
        output.append(f"\n\t\t({vc0[11]} {vc0[12]} {vc1[12]} {vc1[11]})")
        return output
    
    
    def ExportBoundariesInTip(self):
        output = []
        va = self.airfoil[15].vertCount
        vc = self.cover[15].vertCount
        output.append(f"\n\t\t({va[0]} {va[1]} {va[2]} {va[3]})")
        output.append(f"\n\t\t({va[0]} {va[4]} {va[5]} {va[6]})")
        output.append(f"\n\t\t({va[1]} {va[0]} {va[6]} {va[7]})")
        output.append(f"\n\t\t({va[2]} {va[1]} {va[7]} {va[8]})")
        output.append(f"\n\t\t({va[3]} {va[2]} {va[8]} {va[9]})")
        output.append(f"\n\t\t({va[0]} {va[3]} {va[9]} {va[10]})")
        output.append(f"\n\t\t({va[4]} {va[0]} {va[10]} {va[11]})")
        output.append(f"\n\t\t({vc[1]} {vc[0]} {vc[6]} {vc[7]})")
        output.append(f"\n\t\t({vc[2]} {vc[1]} {vc[7]} {vc[8]})")
        output.append(f"\n\t\t({vc[10]} {vc[2]} {vc[8]} {vc[9]})")
        output.append(f"\n\t\t({vc[11]} {vc[3]} {vc[2]} {vc[10]})")
        output.append(f"\n\t\t({vc[12]} {vc[13]} {vc[3]} {vc[11]})")
        output.append(f"\n\t\t({vc[13]} {vc[14]} {vc[4]} {vc[3]})")
        output.append(f"\n\t\t({vc[14]} {vc[15]} {vc[5]} {vc[4]})")
        return output
    
    
    def ExportFrontOut(self, i,ii):
        output = []
        vert0 = self.cover[0 + i].vertCount
        vert1 = self.cover[1 + i].vertCount
        if ii == 1:
            output.append(f"\n\t\t({vert0[6]} {vert0[7]} {vert1[7]} {vert1[6]})")
            output.append(f"\n\t\t({vert0[7]} {vert0[8]} {vert1[8]} {vert1[7]})")
            output.append(f"\n\t\t({vert0[8]} {vert0[9]} {vert1[9]} {vert1[8]})")
        elif ii == 3:
            output.append(f"\n\t\t({vert0[14]} {vert0[15]} {vert1[15]} {vert1[14]})")
            output.append(f"\n\t\t({vert0[13]} {vert0[14]} {vert1[14]} {vert1[13]})")
            output.append(f"\n\t\t({vert0[12]} {vert0[13]} {vert1[13]} {vert1[12]})")
        return output
    
    
    def ExportFrontOutHub(self, i,ii):
        output = []
        vert0 = self.hub[0 + i].vertCount
        vert1 = self.hub[1 + i].vertCount
        if ii == 1:
            output.append(f"\n\t\t({vert0[20]} {vert0[21]} {vert1[21]} {vert1[20]})")
            output.append(f"\n\t\t({vert0[21]} {vert0[22]} {vert1[22]} {vert1[21]})")
            output.append(f"\n\t\t({vert0[22]} {vert0[23]} {vert1[23]} {vert1[22]})")
        elif ii == 3:
            output.append(f"\n\t\t({vert0[18]} {vert0[19]} {vert1[19]} {vert1[18]})")
            output.append(f"\n\t\t({vert0[17]} {vert0[18]} {vert1[18]} {vert1[17]})")
            output.append(f"\n\t\t({vert0[16]} {vert0[17]} {vert1[17]} {vert1[16]})")
        return output