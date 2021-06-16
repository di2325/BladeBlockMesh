import os
from CustomMath import Sin, Cos, ASin, ACos, RotateOnAngle
class Cover:
    def __init__(self, airfoil, airfoilNumber, latestVertCount = 0, refHub = None, angle = 0):
        self.airfoil = airfoil
        self.airfoilNumber = airfoilNumber
        firstVert = latestVertCount + (16 * self.airfoilNumber)
        self.vertCount = [firstVert + i for i in range(16)]
        self.shell = []
        self.arc = []
        if refHub == None:
            self.CalculateShell()
        else:
            self.CopyVerts(refHub, angle)

            
         
    def CalculateShell(self):
        center = [-1.0964, 0, self.airfoil.center[2]]#0.035
        outerBound = 3
        x = [-8,\
             center[0] - outerBound*Cos(45),\
             center[0],\
            8]
        y = [25,\
             outerBound,\
             center[1] + outerBound*Sin(45)]
        z = center[2]

        self.shell.append((x[3], y[1], z))#0
        self.shell.append((x[2], y[1], z))#1
        self.shell.append((x[1], y[2], z))#2
        self.shell.append((x[1], -y[2], z))#3
        self.shell.append((x[2], -y[1], z))#4
        self.shell.append((x[3], -y[1], z))#5
        
        self.shell.append((x[3], y[0], z))#6
        self.shell.append((x[2], y[0], z))#7
        self.shell.append((x[1], y[0], z))#8
        self.shell.append((x[0], y[0], z))#9
        self.shell.append((x[0], y[2], z))#10
        self.shell.append((x[0], -y[2], z))#11
        self.shell.append((x[0], -y[0], z))#12
        self.shell.append((x[1], -y[0], z))#13
        self.shell.append((x[2], -y[0], z))#14
        self.shell.append((x[3], -y[0], z))#15
        self.arc.append((center[0] - outerBound*Cos(60), center[1] + outerBound*Sin(60), z))
        self.arc.append((center[0] - outerBound, center[1], z))
        self.arc.append((center[0] - outerBound*Cos(60), center[1] - outerBound*Sin(60), z))
            
        
        
    def CopyVerts(self, refHub, angle):
        self.shell = [RotateOnAngle(line, angle) for line in refHub.shell]
        self.arc = [RotateOnAngle(line, angle) for line in refHub.arc]
    
                
    def ExportVerts(self):
        output = []
        for line in self.shell:
            output.append(line)
        return output
    
    
    def ExportEdges(self):
        output = []
        vert = self.vertCount
        arc = self.arc
        output.append(f"\narc {vert[1]} {vert[2]} ({arc[0][0]} {arc[0][1]} {arc[0][2]})")
        output.append(f"\narc {vert[2]} {vert[3]} ({arc[1][0]} {arc[1][1]} {arc[1][2]})")
        output.append(f"\narc {vert[3]} {vert[4]} ({arc[2][0]} {arc[2][1]} {arc[2][2]})")
        return output