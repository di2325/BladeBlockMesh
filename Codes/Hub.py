import os
from CustomMath import Sin, Cos, ASin, ACos, RotateOnAngle
class Hub:
    def __init__(self, airfoilNumber, latestVertCount = 0, refHub = None, angle = 0):
        self.airfoilNumber = airfoilNumber
        firstVert = latestVertCount + (24 * self.airfoilNumber)
        self.vertCount = [firstVert + i for i in range(24)]
        self.bLeft = []
        self.bTop = []
        self.bBot = []
        self.bRight = []
        self.shell = []
        self.arc = []
        if refHub == None:
            self.SplitVertsTo4Parts()
            self.CalculateShell()
        else:
            self.CopyVerts(refHub, angle)
        
        
    def SplitVertsTo4Parts(self):
        coord = []
        index = []
        top = []
        bot = []
        #Searching for airfoil files
        for line in open(os.path.abspath(f'../Coordinates/hub{self.airfoilNumber}'), "r"):
            #Assing Coordinates
            if line.startswith('v'):
                coord.append((round(float(line.split()[1]), 4),\
                                       round(float(line.split()[2]), 4),\
                                        round(-1.0 * float(line.split()[3]), 4)))
            #Assign Indices
            elif line.startswith('l'):
                index.append((int(line.split()[1])-1, int(line.split()[2])-1))
               
        #Finding most left and right points
        self.mostRight  = (1000, 0, 0)
        self.mostLeft = (-1000, 0, 0)
        for line in coord:
            if line[0] < self.mostRight[0]:
                self.mostRight = line
            if line[0] > self.mostLeft[0]:
                self.mostLeft= line
               
        #Finding upper point from MostRight
        for line in index:
            if coord[line[0]] == self.mostRight:
                if coord[line[1]][1] > self.mostRight[1]:
                    previousPoint = self.mostRight
                    currentPoint = coord[line[1]]
                    break
            if coord[line[1]] == self.mostRight:
                if coord[line[0]][1] > self.mostRight[1]:
                    previousPoint = self.mostRight
                    currentPoint = coord[line[0]]
                    break      
                    
        #Assing coordinates to Top and Bot
        onTop = True
        while True:
            if onTop:
                top.append(currentPoint)
            for line in index:
                if coord[line[0]] == currentPoint:
                    if coord[line[1]] != previousPoint:
                        previousPoint = currentPoint
                        currentPoint = coord[line[1]]
                        break
                if coord[line[1]] == currentPoint:
                    if coord[line[0]] != previousPoint:
                        previousPoint = currentPoint
                        currentPoint = coord[line[0]]
                        break
            if currentPoint == self.mostRight:
                break
            if not onTop:
                bot.append(currentPoint)
            elif currentPoint == self.mostLeft:
                onTop = False
                
        #Calculate Center point for the front circle       
        center1 = [self.mostRight[0] + 0.8*\
                        (self.mostLeft[0] - self.mostRight[0]),\
                         0, 0]
        center2 = [self.mostRight[0] + 0.2*\
                        (self.mostLeft[0] - self.mostRight[0]),\
                         0, 0]

        #Finding MostTop and MostBot
        delta = 1000
        for line in top:
            if delta > abs(center1[0] - line[0]):
                self.leftTop = line
                delta = abs(center1[0] - line[0])
        delta = 1000
        for line in bot:
            if delta > abs(center1[0] - line[0]):
                self.leftBot = line
                delta = abs(center1[0] - line[0])
        delta = 1000
        for line in top:
            if delta > abs(center2[0] - line[0]):
                self.rightTop = line
                delta = abs(center2[0] - line[0])
        delta = 1000
        for line in bot:
            if delta > abs(center2[0] - line[0]):
                self.rightBot = line
                delta = abs(center2[0] - line[0])
                
        #Dividing Top and Bot to TopLeft/TopRight/BotLeft/BotRight
        for line in top:
            if line[0] > self.leftTop[0]:
                self.bLeft.append(line)
            elif line[0] > self.rightTop[0]:
                self.bTop.append(line)
        for line in bot:
            if line[0] > self.leftBot[0]:
                self.bLeft.append(line)
            elif line[0] > self.rightBot[0]:
                self.bBot.append(line)
        for line in bot:
            if line[0] < self.rightBot[0]:
                self.bRight.append(line)
        for line in top:
            if line[0] < self.rightTop[0]:
                self.bRight.append(line)
         
    def CalculateShell(self):
        outerBound = 3
        rad = 4
        if self.airfoilNumber == 2:
            x = [(-8),\
             (self.rightBot[0]),\
             (self.leftBot[0]),\
             (8)]
        elif self.airfoilNumber == 1:
            x = [(-5.4014),\
                 (self.rightBot[0]),\
                 (self.leftBot[0]),\
                 (5.4014)]
        else:
            x = [(-outerBound),\
                 (self.rightBot[0]),\
                 (self.leftBot[0]),\
                 (outerBound)]
        if self.airfoilNumber == 0:
            z = [(rad*Sin(ACos(x[3]/rad))),\
                 (rad*Sin(ACos(x[1]/rad)))]
        else:
            z = [self.rightBot[2],\
                 self.rightBot[2]]
        self.shell.append((x[0], -outerBound, z[0]))#4
        self.shell.append((x[1], -outerBound, z[1]))#5
        self.shell.append((x[2], -outerBound, z[1]))#6
        self.shell.append((x[3], -outerBound, z[0]))#7
        self.shell.append((x[3], self.leftBot[1], z[0]))#8
        self.shell.append((x[3], self.leftTop[1], z[0]))#9
        self.shell.append((x[3], outerBound, z[0]))#10
        self.shell.append((x[2], outerBound, z[1]))#11
        self.shell.append((x[1], outerBound, z[1]))#12
        self.shell.append((x[0], outerBound, z[0]))#13
        self.shell.append((x[0], self.rightTop[1], z[0]))#14
        self.shell.append((x[0], self.rightBot[1], z[0]))#15
        self.shell.append((x[0], -25, z[0]))#16
        self.shell.append((x[1], -25, z[1]))#17
        self.shell.append((x[2], -25, z[1]))#18
        self.shell.append((x[3], -25, z[0]))#19
        self.shell.append((x[3], 25, z[0]))#20
        self.shell.append((x[2], 25, z[1]))#21
        self.shell.append((x[1], 25, z[1]))#22
        self.shell.append((x[0], 25, z[0]))#23
        if self.airfoilNumber == 0:
            x = 0
            y = [-outerBound,\
                 outerBound]
            z = rad
            self.arc.append((x, y[0], z))
            self.arc.append((x, y[0], z))
            self.arc.append((x, y[0], z))
            self.arc.append((x, y[1], z))
            self.arc.append((x, y[1], z))
            self.arc.append((x, y[1], z))
            self.arc.append((x, self.rightBot[1], z))
            self.arc.append((x, self.leftBot[1], z))
            self.arc.append((x, self.leftTop[1], z))
            self.arc.append((x, self.rightTop[1], z))
            self.arc.append((x, -25, z))
            self.arc.append((x, -25, z))
            self.arc.append((x, -25, z))
            self.arc.append((x, 25, z))
            self.arc.append((x, 25, z))
            self.arc.append((x, 25, z))
        
            
        
        
    def CopyVerts(self, refHub, angle):
        self.leftTop = RotateOnAngle(refHub.leftTop, angle)
        self.leftBot = RotateOnAngle(refHub.leftBot, angle)
        self.rightBot = RotateOnAngle(refHub.rightBot, angle)
        self.rightTop = RotateOnAngle(refHub.rightTop, angle)
        self.bLeft = [RotateOnAngle(line, angle) for line in refHub.bLeft]
        self.bRight = [RotateOnAngle(line, angle) for line in refHub.bRight]
        self.bTop = [RotateOnAngle(line, angle) for line in refHub.bTop]
        self.bBot = [RotateOnAngle(line, angle) for line in refHub.bBot]
        self.shell = [RotateOnAngle(line, angle) for line in refHub.shell]
        self.arc = [RotateOnAngle(line, angle) for line in refHub.arc]
    
                
    def ExportVerts(self):
        output = []
        output.append(self.rightBot)
        output.append(self.leftBot)
        output.append(self.leftTop)
        output.append(self.rightTop)
        for line in self.shell:
            output.append(line)
        return output
    
    
    def ExportEdges(self):
        output = []
        vert = self.vertCount
        output.append(f"\nBSpline {vert[0]} {vert[3]}")
        output.append("\n(")
        for line in self.bRight:
            output.append(f"\n\t({line[0]} {line[1]} {line[2]})")
        output.append("\n)")
        output.append(f"\nBSpline {vert[3]} {vert[2]}")
        output.append("\n(")
        for line in self.bTop:
            output.append(f"\n\t({line[0]} {line[1]} {line[2]})")
        output.append("\n)")
        output.append(f"\nBSpline {vert[1]} {vert[0]}")
        output.append("\n(")
        for line in self.bBot:
            output.append(f"\n\t({line[0]} {line[1]} {line[2]})")
        output.append("\n)")
        output.append(f"\nBSpline {vert[2]} {vert[1]}")
        output.append("\n(")
        for line in self.bLeft:
            output.append(f"\n\t({line[0]} {line[1]} {line[2]})")
        output.append("\n)")
        if self.airfoilNumber == 0:
            outerBound = 3
            rad = 4
            arc = self.arc
            vert = self.vertCount
            output.append(f"\narc {vert[4]} {vert[5]} ({arc[0][0]} {arc[0][1]} {arc[0][2]})")
            output.append(f"\narc {vert[5]} {vert[6]} ({arc[1][0]} {arc[1][1]} {arc[1][2]})")
            output.append(f"\narc {vert[7]} {vert[6]} ({arc[2][0]} {arc[2][1]} {arc[2][2]})")
            output.append(f"\narc {vert[13]} {vert[12]} ({arc[3][0]} {arc[3][1]} {arc[3][2]})")
            output.append(f"\narc {vert[12]} {vert[11]} ({arc[4][0]} {arc[4][1]} {arc[4][2]})")
            output.append(f"\narc {vert[10]} {vert[11]} ({arc[5][0]} {arc[5][1]} {arc[5][2]})")
            output.append(f"\narc {vert[15]} {vert[0]} ({arc[6][0]} {arc[6][1]} {arc[6][2]})")
            output.append(f"\narc {vert[8]} {vert[1]} ({arc[7][0]} {arc[7][1]} {arc[7][2]})")
            output.append(f"\narc {vert[9]} {vert[2]} ({arc[8][0]} {arc[8][1]} {arc[8][2]})")
            output.append(f"\narc {vert[14]} {vert[3]} ({arc[9][0]} {arc[9][1]} {arc[9][2]})")
            output.append(f"\narc {vert[16]} {vert[17]} ({arc[10][0]} {arc[10][1]} {arc[10][2]})")
            output.append(f"\narc {vert[17]} {vert[18]} ({arc[11][0]} {arc[11][1]} {arc[11][2]})")
            output.append(f"\narc {vert[19]} {vert[18]} ({arc[12][0]} {arc[12][1]} {arc[12][2]})")
            output.append(f"\narc {vert[23]} {vert[22]} ({arc[13][0]} {arc[13][1]} {arc[13][2]})")
            output.append(f"\narc {vert[22]} {vert[21]} ({arc[14][0]} {arc[14][1]} {arc[14][2]})")
            output.append(f"\narc {vert[20]} {vert[21]} ({arc[15][0]} {arc[15][1]} {arc[15][2]})")
        return output