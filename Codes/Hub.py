# ==============================================================================
# Hub class creates solid hub from 5 blocks using following methods:
#     ExportVerts:
#         Calculates vertex coordinates and export them to Parent.AddVerts
#     ExportHex:
#         Divides vertex IDs into to and send them to Parent.AddHex
#     ExportEdges:
#         Sends vertices of required edges to Parent.AddEdges
#     ExportBound:
#         Send boundaries to Parent.AddBound
# ==============================================================================
from Parent import Parent
from CustomMath import Sin, Cos
# ==============================================================================
class Hub(Parent):
    def __init__(self):
        self.vertCount = [Parent.vertCount + i for i in range(16)]
        Parent.vertCount += 16

    # ==============================================================================
    def ExportVerts(self):
        rad = Parent.hubRad
        height = Parent.hubHeight
        x = (0.5 * rad * Cos(45), -0.5 * rad * Cos(45), \
             rad * Cos(45), -1 * rad * Cos(45))
        z = (0.5 * rad * Sin(45), -0.5 * rad * Sin(45), \
             rad * Sin(45), -1 * rad * Sin(45))
        y = (height, -height)
        vert = self.vertCount

        Parent.AddVerts(x[1], y[1], z[1], vert[0])
        Parent.AddVerts(x[1], y[1], z[0], vert[1])
        Parent.AddVerts(x[0], y[1], z[0], vert[2])
        Parent.AddVerts(x[0], y[1], z[1], vert[3])

        Parent.AddVerts(x[3], y[1], z[3], vert[4])
        Parent.AddVerts(x[3], y[1], z[2], vert[5])
        Parent.AddVerts(x[2], y[1], z[2], vert[6])
        Parent.AddVerts(x[2], y[1], z[3], vert[7])

        Parent.AddVerts(x[1], y[0], z[1], vert[8])
        Parent.AddVerts(x[1], y[0], z[0], vert[9])
        Parent.AddVerts(x[0], y[0], z[0], vert[10])
        Parent.AddVerts(x[0], y[0], z[1], vert[11])

        Parent.AddVerts(x[3], y[0], z[3], vert[12])
        Parent.AddVerts(x[3], y[0], z[2], vert[13])
        Parent.AddVerts(x[2], y[0], z[2], vert[14])
        Parent.AddVerts(x[2], y[0], z[3], vert[15])

    # ==============================================================================
    def ExportHex(self):
        vert0 = self.vertCount[:8]
        vert1 = self.vertCount[8:]
        a = round(Parent.hubRad * Sin(45))
        r = Parent.hubRad // 2
        h = Parent.hubHeight * 2

        Parent.AddHex(vert0, vert1, [0, 1, 2, 3], [a, a, h])
        Parent.AddHex(vert0, vert1, [4, 5, 1, 0], [a, r, h])
        Parent.AddHex(vert0, vert1, [5, 6, 2, 1], [a, r, h])
        Parent.AddHex(vert0, vert1, [6, 7, 3, 2], [a, r, h])
        Parent.AddHex(vert0, vert1, [7, 4, 0, 3], [a, r, h])

    # ==============================================================================
    def ExportEdges(self):
        vert = self.vertCount

        Parent.AddEdges(vert[4], vert[5], [0, -Parent.hubHeight, Parent.hubRad], 'arc')
        Parent.AddEdges(vert[5], vert[6], [0, -Parent.hubHeight, Parent.hubRad], 'arc')
        Parent.AddEdges(vert[6], vert[7], [0, -Parent.hubHeight, -Parent.hubRad], 'arc')
        Parent.AddEdges(vert[7], vert[4], [0, -Parent.hubHeight, -Parent.hubRad], 'arc')

        Parent.AddEdges(vert[12], vert[13], [0, Parent.hubHeight, Parent.hubRad], 'arc')
        Parent.AddEdges(vert[13], vert[14], [0, Parent.hubHeight, Parent.hubRad], 'arc')
        Parent.AddEdges(vert[14], vert[15], [0, Parent.hubHeight, -Parent.hubRad], 'arc')
        Parent.AddEdges(vert[15], vert[12], [0, Parent.hubHeight, -Parent.hubRad], 'arc')

    # ==============================================================================
    def ExportBound(self):
        Parent.AddBound('hub', '(0 1 5 4)')
        Parent.AddBound('hub', '(1 2 6 5)')
        Parent.AddBound('hub', '(2 3 7 6)')
        Parent.AddBound('hub', '(3 0 4 7)')
        Parent.AddBound('hub', '(3 2 1 0)')

        Parent.AddBound('hub', '(12 13 8 9)')
        Parent.AddBound('hub', '(13 14 10 9)')
        Parent.AddBound('hub', '(14 15 11 10)')
        Parent.AddBound('hub', '(15 12 8 11)')
        Parent.AddBound('hub', '(8 9 10 11)')

        Parent.AddBound('hub', '(4 5 13 12)')
        Parent.AddBound('hub', '(5 6 14 13)')
        Parent.AddBound('hub', '(6 7 15 14)')
        Parent.AddBound('hub', '(7 4 12 15)')
# ==============================================================================
