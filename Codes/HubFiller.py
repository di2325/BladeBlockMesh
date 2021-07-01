from CustomMath import Sin, Cos, RotateOnAngle
class HubFiller:
    def __init__(self, latestVertCount,  rad, length, invert = 1):
        self.vertCount = [latestVertCount + i for i in range(16)]
        self.rad = rad
        self.invert = invert
        self.length = length * invert
        self.shell = []
        self.CalculateVerts()
        self.meshCoeff = 0.4
        
        
    def CalculateVerts(self):
        x = self.rad
        y = self.length
        z = self.rad
        self.shell.append((-x/2, y, 0))
        self.shell.append((0, y, z/2))
        self.shell.append((x/2, y, 0))
        self.shell.append((0, y, -z/2))
        self.shell.append((-x/2, 25*self.invert, 0))
        self.shell.append((0, 25*self.invert, z/2))
        self.shell.append((x/2, 25*self.invert, 0))
        self.shell.append((0, 25*self.invert, -z/2))
        self.shell.append((-x, y, 0))
        self.shell.append((0, y, z))
        self.shell.append((x, y, 0))
        self.shell.append((0, y, -z))
        self.shell.append((-x, 25*self.invert, 0))
        self.shell.append((0, 25*self.invert, z))
        self.shell.append((x, 25*self.invert, 0))
        self.shell.append((0, 25*self.invert, -z))
        
    def ExportHubFillerCover(self):
        output = []
        meshCoeff = self.meshCoeff
        output.append(self.CreateHexCover([0, 1, 2, 3], self.Cells([20, 20, 15], meshCoeff)))
        output.append(self.CreateHexCover([0, 3, 11, 8], self.Cells([20, 20, 15], meshCoeff)))
        output.append(self.CreateHexCover([3, 2, 10, 11], self.Cells([20, 20, 15], meshCoeff)))
        output.append(self.CreateHexCover([2, 1, 9, 10], self.Cells([20, 20, 15], meshCoeff)))
        output.append(self.CreateHexCover([1, 0, 8, 9], self.Cells([20, 20, 15], meshCoeff)))
        return output
    
    
    def CreateHexCover(self, n, cells = [10, 10, 10], grading = [1, 1, 1]):
        vert = self.vertCount
        if self.length > 0:
            return f"\n\thex ({vert[n[0]]} {vert[n[1]]} {vert[n[2]]} {vert[n[3]]} "+\
                                f"{vert[n[0]+4]} {vert[n[1]+4]} {vert[n[2]+4]} {vert[n[3]+4]}) rotatingZone "+\
                                f"({cells[0]} {cells[1]} {cells[2]}) simpleGrading "+\
                                f"({grading[0]} {grading[1]} {grading[2]})"
        else:
            return f"\n\thex ({vert[n[0]+4]} {vert[n[1]+4]} {vert[n[2]+4]} {vert[n[3]+4]} "+\
                                f"{vert[n[0]]} {vert[n[1]]} {vert[n[2]]} {vert[n[3]]}) rotatingZone "+\
                                f"({cells[0]} {cells[1]} {cells[2]}) simpleGrading "+\
                                f"({grading[0]} {grading[1]} {grading[2]})"
    
    def Cells(self, cells, meshCoeff):
        x = round(cells[0]*meshCoeff)
        y = round(cells[1]*meshCoeff)
        z = round(cells[2]*meshCoeff)
        return [x, y, z]
    
    
    def ExportEdges(self):
        output = []
        rad = self.rad
        length = self.length
        vert = self.vertCount
        output.append(f"\narc {vert[9]} {vert[8]} ({-rad*Cos(45)} {length} {rad*Sin(45)})")
        output.append(f"\narc {vert[11]} {vert[8]} ({-rad*Cos(45)} {length} {-rad*Sin(45)})")
        output.append(f"\narc {vert[10]} {vert[9]} ({rad*Cos(45)} {length} {rad*Sin(45)})")
        output.append(f"\narc {vert[11]} {vert[10]} ({rad*Cos(45)} {length} {-rad*Sin(45)})")
        output.append(f"\narc {vert[13]} {vert[12]} ({-rad*Cos(45)} {25*self.invert} {rad*Sin(45)})")
        output.append(f"\narc {vert[15]} {vert[12]} ({-rad*Cos(45)} {25*self.invert} {-rad*Sin(45)})")
        output.append(f"\narc {vert[14]} {vert[13]} ({rad*Cos(45)} {25*self.invert} {rad*Sin(45)})")
        output.append(f"\narc {vert[15]} {vert[14]} ({rad*Cos(45)} {25*self.invert} {-rad*Sin(45)})")
        return output
    
    
    def ExportBoundaries(self):
        output = []
        vert = self.vertCount
        if self.length > 0:
            output.append(f"\n\t\t({vert[3]} {vert[2]} {vert[1]} {vert[0]})")
            output.append(f"\n\t\t({vert[1]} {vert[2]} {vert[10]} {vert[9]})")
            output.append(f"\n\t\t({vert[0]} {vert[1]} {vert[9]} {vert[8]})")
            output.append(f"\n\t\t({vert[3]} {vert[0]} {vert[8]} {vert[11]})")
            output.append(f"\n\t\t({vert[2]} {vert[3]} {vert[11]} {vert[10]})")
        else:
            output.append(f"\n\t\t({vert[0]} {vert[1]} {vert[2]} {vert[3]})")
            output.append(f"\n\t\t({vert[2]} {vert[1]} {vert[9]} {vert[10]})")
            output.append(f"\n\t\t({vert[1]} {vert[0]} {vert[8]} {vert[9]})")
            output.append(f"\n\t\t({vert[0]} {vert[3]} {vert[11]} {vert[8]})")
            output.append(f"\n\t\t({vert[3]} {vert[2]} {vert[10]} {vert[11]})")
        return output
    
    def ExportBoundariesInterface(self):
        output = []
        vert = self.vertCount
        if self.length > 0:
            output.append(f"\n\t\t({vert[8]} {vert[9]} {vert[13]} {vert[12]})")
            output.append(f"\n\t\t({vert[11]} {vert[8]} {vert[12]} {vert[15]})")
            output.append(f"\n\t\t({vert[10]} {vert[11]} {vert[15]} {vert[14]})")
            output.append(f"\n\t\t({vert[9]} {vert[10]} {vert[14]} {vert[13]})")
        else:
            output.append(f"\n\t\t({vert[12]} {vert[13]} {vert[9]} {vert[8]})")
            output.append(f"\n\t\t({vert[15]} {vert[12]} {vert[8]} {vert[11]})")
            output.append(f"\n\t\t({vert[14]} {vert[15]} {vert[11]} {vert[10]})")
            output.append(f"\n\t\t({vert[13]} {vert[14]} {vert[10]} {vert[9]})")
        return output
    
    def ExportFrontOut(self, i):
        output = []
        vert = self.vertCount
        if i == 1:
            output.append(f"\n\t\t({vert[4]} {vert[5]} {vert[6]} {vert[7]})")
            output.append(f"\n\t\t({vert[6]} {vert[5]} {vert[13]} {vert[14]})")
            output.append(f"\n\t\t({vert[7]} {vert[6]} {vert[14]} {vert[15]})")
            output.append(f"\n\t\t({vert[4]} {vert[7]} {vert[15]} {vert[12]})")
            output.append(f"\n\t\t({vert[5]} {vert[4]} {vert[12]} {vert[13]})")
        elif i == 3:
            output.append(f"\n\t\t({vert[7]} {vert[6]} {vert[5]} {vert[4]})")
            output.append(f"\n\t\t({vert[5]} {vert[6]} {vert[14]} {vert[13]})")
            output.append(f"\n\t\t({vert[6]} {vert[7]} {vert[15]} {vert[14]})")
            output.append(f"\n\t\t({vert[7]} {vert[4]} {vert[12]} {vert[15]})")
            output.append(f"\n\t\t({vert[4]} {vert[5]} {vert[13]} {vert[12]})")
        return output