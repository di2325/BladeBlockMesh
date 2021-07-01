from CustomMath import Sin, Cos, RotateOnAngle
class Filler:
    def __init__(self, blade0, blade1, i, angle = 0):
        self.blade0 = blade0
        self.blade1 = blade1
        self.i = i
        self.rad0 = (blade0.hub[0 + i].shell[9][0]**2 + blade0.hub[0 + i].shell[9][2]**2)**0.5
        self.rad1 = (blade0.hub[1 + i].shell[9][0]**2 + blade0.hub[1 + i].shell[9][2]**2)**0.5
        self.angle = angle
        self.meshCoeff = 0.4
        
    
    def ExportHex(self):
        output = []
        meshCoeff = self.meshCoeff
        output.append(self.CreateHex([4, 15, 8, 7], self.Cells([5, 10, 10], meshCoeff)))
        output.append(self.CreateHex([15, 14, 9, 8], self.Cells([10, 10, 10], meshCoeff)))
        output.append(self.CreateHex([14, 13, 10, 9], self.Cells([5, 10, 10], meshCoeff)))
        output.append(self.CreateHex([16, 4, 7, 19], self.Cells([15, 10, 10], meshCoeff)))
        output.append(self.CreateHex([13, 23, 20, 10], self.Cells([15, 10, 10], meshCoeff)))
        return output
    
    
    def CreateHex(self, n, cells = [10, 10, 10], grading = [1, 1, 1]):
        vert00 = self.blade0.hub[0 + self.i].vertCount
        vert01 = self.blade0.hub[1 + self.i].vertCount
        vert10 = self.blade1.hub[0 + self.i].vertCount
        vert11 = self.blade1.hub[1 + self.i].vertCount
        return f"\n\thex ({vert00[n[0]]} {vert00[n[1]]} {vert10[n[2]]} {vert10[n[3]]} "+\
                            f"{vert01[n[0]]} {vert01[n[1]]} {vert11[n[2]]} {vert11[n[3]]}) rotatingZone "+\
                            f"({cells[0]} {cells[1]} {cells[2]}) simpleGrading "+\
                            f"({grading[0]} {grading[1]} {grading[2]})"
    
    def Cells(self, cells, meshCoeff):
        x = round(cells[0]*meshCoeff)
        y = round(cells[1]*meshCoeff)
        z = round(cells[2]*meshCoeff)
        return [x, y, z]
    
    
    def ExportEdges(self):
        output = []
        outerBound = 3
        rad = 4
        vert00 = self.blade0.hub[0 + self.i].vertCount
        vert01 = self.blade0.hub[1 + self.i].vertCount
        vert10 = self.blade1.hub[0 + self.i].vertCount
        vert11 = self.blade1.hub[1 + self.i].vertCount
        center00 = RotateOnAngle([0, -outerBound, self.rad0], self.angle)
        center01 = RotateOnAngle([0, self.blade0.hub[0].shell[11][1], self.rad0], self.angle)
        center02 = RotateOnAngle([0, self.blade0.hub[0].shell[10][1], self.rad0], self.angle)
        center03 = RotateOnAngle([0, outerBound, self.rad0], self.angle)
        center10 = RotateOnAngle([0, -outerBound, self.rad1], self.angle)
        center11 = RotateOnAngle([0, self.blade0.hub[1].shell[11][1], self.rad1], self.angle)
        center12 = RotateOnAngle([0, self.blade0.hub[1].shell[10][1], self.rad1], self.angle)
        center13 = RotateOnAngle([0, outerBound, self.rad1], self.angle)
        if self.i == 0:
            output.append(f"\narc {vert10[7]} {vert00[4]} ({center00[0]} {center00[1]} {center00[2]})")
            output.append(f"\narc {vert10[8]} {vert00[15]} ({center01[0]} {center01[1]} {center01[2]})")
            output.append(f"\narc {vert10[9]} {vert00[14]} ({center02[0]} {center02[1]} {center02[2]})")
            output.append(f"\narc {vert10[10]} {vert00[13]} ({center03[0]} {center03[1]} {center03[2]})")
            output.append(f"\narc {vert10[19]} {vert00[16]} ({center00[0]} {-25} {center00[2]})")
            output.append(f"\narc {vert10[20]} {vert00[23]} ({center03[0]} {25} {center03[2]})")
            output.append(f"\narc {vert11[7]} {vert01[4]} ({center10[0]} {center10[1]} {center10[2]})")
            output.append(f"\narc {vert11[8]} {vert01[15]} ({center11[0]} {center11[1]} {center11[2]})")
            output.append(f"\narc {vert11[9]} {vert01[14]} ({center12[0]} {center12[1]} {center12[2]})")
            output.append(f"\narc {vert11[10]} {vert01[13]} ({center13[0]} {center13[1]} {center13[2]})")
            output.append(f"\narc {vert11[19]} {vert01[16]} ({center10[0]} {-25} {center10[2]})")
            output.append(f"\narc {vert11[20]} {vert01[23]} ({center13[0]} {25} {center13[2]})")
        return output
    
    def ExportBoundariesHub(self):
        output = []
        vert0 = self.blade0.hub[0].vertCount
        vert1 = self.blade1.hub[0].vertCount
        output.append(f"\n\t\t({vert0[15]} {vert0[4]} {vert1[7]} {vert1[8]})")
        output.append(f"\n\t\t({vert0[14]} {vert0[15]} {vert1[8]} {vert1[9]})")
        output.append(f"\n\t\t({vert0[13]} {vert0[14]} {vert1[9]} {vert1[10]})")
        return output
    
    def ExportBoundariesInterfaceHub(self, top = True):
        output = []
        vert0 = self.blade0.hub[0].vertCount
        vert1 = self.blade1.hub[0].vertCount
        if top:
            output.append(f"\n\t\t({vert0[23]} {vert0[13]} {vert1[10]} {vert1[20]})")
        else:
            output.append(f"\n\t\t({vert0[4]} {vert0[16]} {vert1[19]} {vert1[7]})")
        return output
    
    
    def ExportBoundariesInSectorMiddle(self):
        output = []
        vert0 = self.blade0.hub[2].vertCount
        vert1 = self.blade1.hub[2].vertCount
        output.append(f"\n\t\t({vert0[13]} {vert0[23]} {vert1[20]} {vert1[10]})")
        output.append(f"\n\t\t({vert0[14]} {vert0[13]} {vert1[10]} {vert1[9]})")
        output.append(f"\n\t\t({vert0[15]} {vert0[14]} {vert1[9]} {vert1[8]})")
        output.append(f"\n\t\t({vert0[4]} {vert0[15]} {vert1[8]} {vert1[7]})")
        output.append(f"\n\t\t({vert0[16]} {vert0[4]} {vert1[7]} {vert1[19]})")
        return output
    
    
    def ExportFrontOut(self, i, ii):
        output = []
        vert00 = self.blade0.hub[0 + i].vertCount
        vert01 = self.blade0.hub[1 + i].vertCount
        vert10 = self.blade1.hub[0 + i].vertCount
        vert11 = self.blade1.hub[1 + i].vertCount
        if ii == 1:
            output.append(f"\n\t\t({vert00[23]} {vert01[23]} {vert11[20]} {vert10[20]})")
        else:
            output.append(f"\n\t\t({vert00[16]} {vert01[16]} {vert11[19]} {vert10[19]})")
        return output