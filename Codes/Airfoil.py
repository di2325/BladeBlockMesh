# ==============================================================================
# Points of an airfoil:
#     self.verts[0] = most left
#     self.verts[1] = top left
#     self.verts[2] = most top
#     self.verts[3] = top right
#     self.verts[4] = most right
#     self.verts[5] = bot right
#     self.verts[6] = most bot
#     self.verts[7] = bot left
#     self.verts[8] = chord left
#     self.verts[9] = center
#     self.verts[10] = chord right
# ==============================================================================
import os
from Parent import Parent
from CustomMath import RotateOnAngle
# ==============================================================================
class Airfoil(Parent):
    def __init__(self, airfoilNumber, target=None, angle=0):
        self.vertCount = [Parent.vertCount + i for i in range(11)]
        Parent.vertCount += 11

        self.verts = [0] * 11

        self.top0 = []
        self.top1 = []
        self.top2 = []
        self.top3 = []

        self.bot0 = []
        self.bot1 = []
        self.bot2 = []
        self.bot3 = []
        if target == None:
            self.CreateVerts(airfoilNumber)
        else:
            self.CopyAirfoil(target, angle)

# ==============================================================================
    def CreateVerts(self, airfoilNumber):
        coord = []
        index = []
        top = []
        bot = []

        # Searching for airfoil files
        for line in open(os.path.abspath( \
                f'../Coordinates/airfoil{airfoilNumber}' \
                ), "r"):
            # Assing Coordinates
            if line.startswith('v'):
                coord.append([round(float(line.split()[1]), 4), \
                              round(float(line.split()[2]), 4), \
                              round(-1.0 * float(line.split()[3]), 4)])
            # Assign Indices
            elif line.startswith('l'):
                index.append((int(line.split()[1]) - 1, int(line.split()[2]) - 1))

        # if airfoilNumber == 0:
        #    for i in range(len(coord)):
        #        coord[i][2] = coord[i][2] + 0.5

        # Finding most left and right points
        self.verts[4] = (1000, 0, 0)
        self.verts[0] = (-1000, 0, 0)
        for line in coord:
            if line[0] < self.verts[4][0]:
                self.verts[4] = line
            if line[0] > self.verts[0][0]:
                self.verts[0] = line

        # Finding upper point from MostRight
        for line in index:
            if coord[line[0]] == self.verts[4]:
                if coord[line[1]][1] > self.verts[4][1]:
                    previousPoint = self.verts[4]
                    currentPoint = coord[line[1]]
                    break
            if coord[line[1]] == self.verts[4]:
                if coord[line[0]][1] > self.verts[4][1]:
                    previousPoint = self.verts[4]
                    currentPoint = coord[line[0]]
                    break

                    # Assing coordinates to Top and Bot
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
            if currentPoint == self.verts[4]:
                break
            if not onTop:
                bot.append(currentPoint)
            elif currentPoint == self.verts[0]:
                onTop = False

        self.verts[1] = top[round(len(top) * 0.7)]  # 83
        self.verts[2] = top[round(len(top) * 0.5)]
        self.verts[3] = top[round(len(top) * 0.25)]  # 13
        self.verts[5] = bot[round(len(bot) * 0.75)]  # 83
        self.verts[6] = bot[round(len(bot) * 0.5)]
        self.verts[7] = bot[round(len(bot) * 0.3)]  # 13
        self.verts[8] = [0, 0, 0]
        self.verts[9] = [0, 0, 0]
        self.verts[10] = [0, 0, 0]

        CLT = top[round(len(top) * 0.66)]
        CLB = bot[round(len(bot) * 0.33)]
        CRT = top[round(len(top) * 0.3)]
        CRB = bot[round(len(bot) * 0.66)]

        for i in range(3):
            self.verts[8][i] = (CLT[i] + CLB[i]) / 2
            self.verts[9][i] = (self.verts[2][i] + self.verts[6][i]) / 2
            self.verts[10][i] = (CRT[i] + CRB[i]) / 2

        for line in top:
            if line != self.verts[1] and \
                    line != self.verts[2] and line != self.verts[3]:
                if line[0] > self.verts[1][0]:
                    self.top0.append(line)
                elif line[0] > self.verts[2][0]:
                    self.top1.append(line)
                elif line[0] > self.verts[3][0]:
                    self.top2.append(line)
                else:
                    self.top3.append(line)

        for line in bot:
            if line != self.verts[7] and \
                    line != self.verts[6] and line != self.verts[5]:
                if line[0] > self.verts[7][0]:
                    self.bot0.append(line)
                elif line[0] > self.verts[6][0]:
                    self.bot1.append(line)
                elif line[0] > self.verts[5][0]:
                    self.bot2.append(line)
                else:
                    self.bot3.append(line)

# ==============================================================================

    def CopyAirfoil(self, target, angle):
        for i in range(11):
            self.verts[i] = RotateOnAngle(target.verts[i], angle)

        for line in target.top0:
            self.top0.append(RotateOnAngle(line, angle))
        for line in target.top1:
            self.top1.append(RotateOnAngle(line, angle))
        for line in target.top2:
            self.top2.append(RotateOnAngle(line, angle))
        for line in target.top3:
            self.top3.append(RotateOnAngle(line, angle))

        for line in target.bot0:
            self.bot0.append(RotateOnAngle(line, angle))
        for line in target.bot1:
            self.bot1.append(RotateOnAngle(line, angle))
        for line in target.bot2:
            self.bot2.append(RotateOnAngle(line, angle))
        for line in target.bot3:
            self.bot3.append(RotateOnAngle(line, angle))
# ==============================================================================
