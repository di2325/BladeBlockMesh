from CustomMath import Sin, Cos, ASin, ACos, RotateOnAngle
class SimpleFiller:
    def __init__(self, latestVertCount):
        self.vertCount = [latestVertCount + i for i in range(36)]
        self.shell = []
        self.meshCoeff = 0.5
        self.CalculateVerts()
        
        
    def CalculateVerts(self):
        p = self.shell
        y = -25
        p.append((-8, y, 8.1823))#0
        p.append((-8, y, 65))#1
        p.append((-8, y, 74.5721))#2
        p.append((8, y, 74.5721))#3
        p.append((8, y, 65))#4
        p.append((8, y, 8.1823))#5
        p.append(RotateOnAngle(p[0], -120))#6
        p.append(RotateOnAngle(p[1], -120))#7
        p.append(RotateOnAngle(p[2], -120))#8
        p.append(RotateOnAngle(p[3], -120))#9
        p.append(RotateOnAngle(p[4], -120))#10
        p.append(RotateOnAngle(p[5], -120))#11
        p.append(RotateOnAngle(p[0], 120))#12
        p.append(RotateOnAngle(p[1], 120))#13
        p.append(RotateOnAngle(p[2], 120))#14
        p.append(RotateOnAngle(p[3], 120))#15
        p.append(RotateOnAngle(p[4], 120))#16
        p.append(RotateOnAngle(p[5], 120))#17
        y = 25
        p.append((-8, y, 8.1823))#18
        p.append((-8, y, 65))#19
        p.append((-8, y, 74.5721))#20
        p.append((8, y, 74.5721))#21
        p.append((8, y, 65))#22
        p.append((8, y, 8.1823))#23
        p.append(RotateOnAngle(p[18], -120))#24
        p.append(RotateOnAngle(p[19], -120))#25
        p.append(RotateOnAngle(p[20], -120))#26
        p.append(RotateOnAngle(p[21], -120))#27
        p.append(RotateOnAngle(p[22], -120))#28
        p.append(RotateOnAngle(p[23], -120))#29
        p.append(RotateOnAngle(p[18], 120))#30
        p.append(RotateOnAngle(p[19], 120))#31
        p.append(RotateOnAngle(p[20], 120))#32
        p.append(RotateOnAngle(p[21], 120))#33
        p.append(RotateOnAngle(p[22], 120))#34
        p.append(RotateOnAngle(p[23], 120))#35
    
    def ExportBoundaryTip(self):
        output = []
        vert = self.vertCount
        output.append(f"\nOutTip0")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[1]} {vert[19]} {vert[22]} {vert[4]})")
        output.append("\n\t);")
        output.append("\n}")
        output.append(f"\nOutTip2")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[7]} {vert[25]} {vert[28]} {vert[10]})")
        output.append("\n\t);")
        output.append("\n}")
        output.append(f"\nOutTip1")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[13]} {vert[31]} {vert[34]} {vert[16]})")
        output.append("\n\t);")
        output.append("\n}")\
        
        output.append(f"\nOutSectorLeft0")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[23]} {vert[22]} {vert[4]} {vert[5]})")
        output.append("\n\t);")
        output.append("\n}")
        output.append(f"\nOutSectorMiddle0")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[18]} {vert[35]} {vert[17]} {vert[0]})")
        output.append("\n\t);")
        output.append("\n}")
        output.append(f"\nOutSectorRight0")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[19]} {vert[18]} {vert[0]} {vert[1]})")
        output.append("\n\t);")
        output.append("\n}")
        
        output.append(f"\nOutSectorLeft1")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[35]} {vert[34]} {vert[16]} {vert[17]})")
        output.append("\n\t);")
        output.append("\n}")
        output.append(f"\nOutSectorMiddle1")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[30]} {vert[29]} {vert[11]} {vert[12]})")
        output.append("\n\t);")
        output.append("\n}")
        output.append(f"\nOutSectorRight1")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[31]} {vert[30]} {vert[12]} {vert[13]})")
        output.append("\n\t);")
        output.append("\n}")
        
        output.append(f"\nOutSectorLeft2")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[29]} {vert[28]} {vert[10]} {vert[11]})")
        output.append("\n\t);")
        output.append("\n}")
        output.append(f"\nOutSectorMiddle2")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[24]} {vert[23]} {vert[5]} {vert[6]})")
        output.append("\n\t);")
        output.append("\n}")
        output.append(f"\nOutSectorRight2")
        output.append("\n{")
        output.append("\n\ttype patch;")
        output.append("\n\tfaces")
        output.append("\n\t(")        
        output.append(f"\n\t\t({vert[25]} {vert[24]} {vert[6]} {vert[7]})")
        output.append("\n\t);")
        output.append("\n}")
        
        return output
        
        
    def ExportEdges(self):
        output = []
        vert = self.vertCount
        center0 = (0, -25, -65)
        center1 = (0, 25, -65)
        output.append(f"\narc {vert[1]} {vert[16]} ({center0[0]} {center0[1]} {center0[2]})")
        output.append(f"\narc {vert[19]} {vert[34]} ({center1[0]} {center1[1]} {center1[2]})")
        output.append(f"\narc {vert[4]} {vert[7]} ({center0[0]} {center0[1]} {center0[2]})")
        output.append(f"\narc {vert[22]} {vert[25]} ({center1[0]} {center1[1]} {center1[2]})")
        output.append(f"\narc {vert[10]} {vert[13]} ({center0[0]} {center0[1]} {center0[2]})")
        output.append(f"\narc {vert[28]} {vert[31]} ({center1[0]} {center1[1]} {center1[2]})")
        center0 = (0, -25, -75)
        center1 = (0, 25, -75)
        output.append(f"\narc {vert[2]} {vert[15]} ({center0[0]} {center0[1]} {center0[2]})")
        output.append(f"\narc {vert[20]} {vert[33]} ({center1[0]} {center1[1]} {center1[2]})")
        output.append(f"\narc {vert[3]} {vert[8]} ({center0[0]} {center0[1]} {center0[2]})")
        output.append(f"\narc {vert[21]} {vert[26]} ({center1[0]} {center1[1]} {center1[2]})")
        output.append(f"\narc {vert[9]} {vert[14]} ({center0[0]} {center0[1]} {center0[2]})")
        output.append(f"\narc {vert[27]} {vert[32]} ({center1[0]} {center1[1]} {center1[2]})")
        center0 = (0, -25, 75)
        center1 = (0, 25, 75)
        output.append(f"\narc {vert[3]} {vert[2]} ({center0[0]} {center0[1]} {center0[2]})")
        output.append(f"\narc {vert[21]} {vert[20]} ({center1[0]} {center1[1]} {center1[2]})")
        output.append(f"\narc {vert[14]} {vert[15]} ({center0[0]} {center0[1]} {center0[2]})")
        output.append(f"\narc {vert[32]} {vert[33]} ({center1[0]} {center1[1]} {center1[2]})")
        output.append(f"\narc {vert[9]} {vert[8]} ({center0[0]} {center0[1]} {center0[2]})")
        output.append(f"\narc {vert[27]} {vert[26]} ({center1[0]} {center1[1]} {center1[2]})")
        return output
        
        
    
    def ExportHex(self):
        output = []
        meshCoeff = self.meshCoeff
        output.append(self.CreateHex([1, 2, 3, 4], self.Cells([20, 20, 50], meshCoeff)))
        output.append(self.CreateHex([7, 8, 9, 10], self.Cells([20, 20, 50], meshCoeff)))
        output.append(self.CreateHex([13, 14, 15, 16], self.Cells([20, 20, 50], meshCoeff)))
        output.append(self.CreateHex([17, 16, 1, 0], self.Cells([80, 40, 50], meshCoeff)))
        output.append(self.CreateHex([7, 6, 5, 4], self.Cells([80, 40, 50], meshCoeff)))
        output.append(self.CreateHex([13, 12, 11, 10], self.Cells([80, 40, 50], meshCoeff)))
        output.append(self.CreateHex([16, 15, 2, 1], self.Cells([20, 40, 50], meshCoeff)))
        output.append(self.CreateHex([10, 9, 14, 13], self.Cells([20, 40, 50], meshCoeff)))
        output.append(self.CreateHex([4, 3, 8, 7], self.Cells([20, 40, 50], meshCoeff)))
        return output
    
    
    def CreateHex(self, n, cells = [10, 10, 10], grading = [1, 1, 1]):
        vert = self.vertCount
        return f"\n\thex ({vert[n[0]]} {vert[n[1]]} {vert[n[2]]} {vert[n[3]]} "+\
                            f"{vert[n[0]+18]} {vert[n[1]+18]} {vert[n[2]+18]} {vert[n[3]+18]}) rotatingZone "+\
                            f"({cells[0]} {cells[1]} {cells[2]}) simpleGrading "+\
                            f"({grading[0]} {grading[1]} {grading[2]})"
    
    def Cells(self, cells, meshCoeff):
        x = round(cells[0]*meshCoeff)
        y = round(cells[1]*meshCoeff)
        z = round(cells[2]*meshCoeff)
        return [x, y, z]
    
    
    def ExportFrontOut(self, i):
        output = []
        vert = self.vertCount
        if i == 1:
            output.append(f"\n\t\t({vert[20]} {vert[21]} {vert[22]} {vert[19]})")
            output.append(f"\n\t\t({vert[26]} {vert[27]} {vert[28]} {vert[25]})")
            output.append(f"\n\t\t({vert[32]} {vert[33]} {vert[34]} {vert[31]})")
            output.append(f"\n\t\t({vert[33]} {vert[20]} {vert[19]} {vert[34]})")
            output.append(f"\n\t\t({vert[21]} {vert[26]} {vert[25]} {vert[22]})")
            output.append(f"\n\t\t({vert[28]} {vert[27]} {vert[32]} {vert[31]})")
            output.append(f"\n\t\t({vert[34]} {vert[19]} {vert[18]} {vert[35]})")
            output.append(f"\n\t\t({vert[22]} {vert[25]} {vert[24]} {vert[23]})")
            output.append(f"\n\t\t({vert[31]} {vert[30]} {vert[29]} {vert[28]})")
        elif i == 2:
            output.append(f"\n\t\t({vert[2]} {vert[3]} {vert[21]} {vert[20]})")
            output.append(f"\n\t\t({vert[3]} {vert[8]} {vert[26]} {vert[21]})")
            output.append(f"\n\t\t({vert[8]} {vert[9]} {vert[27]} {vert[26]})")
            output.append(f"\n\t\t({vert[9]} {vert[14]} {vert[32]} {vert[27]})")
            output.append(f"\n\t\t({vert[14]} {vert[15]} {vert[33]} {vert[32]})")
            output.append(f"\n\t\t({vert[15]} {vert[2]} {vert[20]} {vert[33]})")
        elif i == 3:
            output.append(f"\n\t\t({vert[1]} {vert[4]} {vert[3]} {vert[2]})")
            output.append(f"\n\t\t({vert[7]} {vert[10]} {vert[9]} {vert[8]})")
            output.append(f"\n\t\t({vert[16]} {vert[15]} {vert[14]} {vert[13]})")
            output.append(f"\n\t\t({vert[1]} {vert[2]} {vert[15]} {vert[16]})")
            output.append(f"\n\t\t({vert[7]} {vert[8]} {vert[3]} {vert[4]})")
            output.append(f"\n\t\t({vert[13]} {vert[14]} {vert[9]} {vert[10]})")
            output.append(f"\n\t\t({vert[0]} {vert[1]} {vert[16]} {vert[17]})")
            output.append(f"\n\t\t({vert[6]} {vert[7]} {vert[4]} {vert[5]})")
            output.append(f"\n\t\t({vert[12]} {vert[13]} {vert[10]} {vert[11]})")
        return output