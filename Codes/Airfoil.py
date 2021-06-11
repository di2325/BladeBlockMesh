import os
from CustomMath import Sin, Cos, ASin, ACos, RotateOnAngle
class Airfoil:
    def __init__(self, airfoilNumber, latestVertCount = 0, refHub = None, angle = 0):
        self.airfoilNumber = airfoilNumber
        firstVert = latestVertCount + (12 * self.airfoilNumber)
        self.vertCount = [firstVert + i for i in range(12)]
        self.bLeftTop = []
        self.bRightTop = []
        self.bLeftBot = []
        self.bRightBot = []
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
        for line in open(os.path.abspath(f'../Coordinates/airfoil{self.airfoilNumber}'), "r"):
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
        self.center = [self.mostRight[0] + 0.2*\
                        (self.mostLeft[0] - self.mostRight[0]),\
                        (self.mostLeft[1] + self.mostRight[1])/2,\
                        (self.mostLeft[2] + self.mostRight[2])/2]

        #Finding MostTop and MostBot
        delta = 1000
        for line in top:
            if delta > abs(self.center[0] - line[0]):
                self.mostTop = line
                delta = abs(self.center[0] - line[0])
        delta = 1000
        for line in bot:
            if delta > abs(self.center[0] - line[0]):
                self.mostBot = line
                delta = abs(self.center[0] - line[0])
                
        #Dividing Top and Bot to TopLeft/TopRight/BotLeft/BotRight
        for line in top:
            if line[0] > self.mostTop[0]:
                self.bLeftTop.append(line)
            else:
                self.bRightTop.append(line)
        for line in bot:
            if line[0] > self.mostBot[0]:
                self.bLeftBot.append(line)
            else:
                self.bRightBot.append(line)
         
    def CalculateShell(self):
        center = [-1.0964, 0, self.center[2]]#0.035
        outerBound = 3
        if self.airfoilNumber == 0 or self.airfoilNumber == 15:
            x = [center[0] - outerBound,\
                 center[0],\
                 self.mostLeft[0] + (outerBound/2),\
                 8]
        else:
            x = [center[0] - outerBound,\
                 center[0],\
                 self.mostLeft[0],\
                 8]
        y = [-outerBound,\
             center[1],\
             outerBound]
        z = center[2]

        self.shell.append((x[3], self.mostLeft[1], z))#4
        self.shell.append((x[3], y[2], z))#5
        self.shell.append((x[2], y[2], z))#6
        self.shell.append((x[1], y[2], z))#7
        self.shell.append((x[0], y[1], z))#8
        self.shell.append((x[1], y[0], z))#9
        self.shell.append((x[2], y[0], z))#10
        self.shell.append((x[3], y[0], z))#11
        self.arc.append((center[0] - outerBound*Cos(45), center[1] + outerBound*Sin(45), z))
        self.arc.append((center[0] - outerBound*Cos(45), center[1] - outerBound*Sin(45), z))
            
        
        
    def CopyVerts(self, refHub, angle):
        self.mostLeft = RotateOnAngle(refHub.mostLeft, angle)
        self.mostRight = RotateOnAngle(refHub.mostRight, angle)
        self.mostTop = RotateOnAngle(refHub.mostTop, angle)
        self.mostBot = RotateOnAngle(refHub.mostBot, angle)
        self.bLeftTop = [RotateOnAngle(line, angle) for line in refHub.bLeftTop]
        self.bRightTop = [RotateOnAngle(line, angle) for line in refHub.bRightTop]
        self.bLeftBot = [RotateOnAngle(line, angle) for line in refHub.bLeftBot]
        self.bRightBot = [RotateOnAngle(line, angle) for line in refHub.bRightBot]
        self.shell = [RotateOnAngle(line, angle) for line in refHub.shell]
        self.arc = [RotateOnAngle(line, angle) for line in refHub.arc]
    
                
    def ExportVerts(self):
        output = []
        output.append(self.mostLeft)
        output.append(self.mostTop)
        output.append(self.mostRight)
        output.append(self.mostBot)
        for line in self.shell:
            output.append(line)
        return output
    
    
    def ExportEdges(self):
        output = []
        vert = self.vertCount
        arc = self.arc
        output.append(f"\nBSpline {vert[0]} {vert[3]}")
        output.append("\n(")
        for line in self.bLeftBot:
            output.append(f"\n\t({line[0]} {line[1]} {line[2]})")
        output.append("\n)")
        output.append(f"\nBSpline {vert[3]} {vert[2]}")
        output.append("\n(")
        for line in self.bRightBot:
            output.append(f"\n\t({line[0]} {line[1]} {line[2]})")
        output.append("\n)")
        output.append(f"\nBSpline {vert[2]} {vert[1]}")
        output.append("\n(")
        for line in self.bRightTop:
            output.append(f"\n\t({line[0]} {line[1]} {line[2]})")
        output.append("\n)")
        output.append(f"\nBSpline {vert[1]} {vert[0]}")
        output.append("\n(")
        for line in self.bLeftTop:
            output.append(f"\n\t({line[0]} {line[1]} {line[2]})")
        output.append("\n)")
        output.append(f"\narc {vert[7]} {vert[8]} ({arc[0][0]} {arc[0][1]} {arc[0][2]})")
        output.append(f"\narc {vert[8]} {vert[9]} ({arc[1][0]} {arc[1][1]} {arc[1][2]})")
        return output