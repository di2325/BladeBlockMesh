# ==============================================================================
from Parent import Parent


class Blade(Parent):
    def __init__(self, main=True):
        self.main = main
        self.airfoil = []

    # ==============================================================================
    def ExportVerts(self):
        for airfoil in self.airfoil:
            vert = airfoil.vertCount
            n = airfoil.verts

            for i in range(11):
                Parent.AddVerts(n[i][0], n[i][1], n[i][2], vert[i])

    # ==============================================================================
    def ExportHex(self):
        n = len(self.airfoil) - 1
        for i in range(n):
            v0 = self.airfoil[i].vertCount
            v1 = self.airfoil[i + 1].vertCount

            t = 2
            b = 2
            l = 3

            Parent.AddHex(v0, v1, [0, 1, 8, 7], [b, t, l])
            Parent.AddHex(v0, v1, [1, 2, 9, 8], [b, t, l])
            Parent.AddHex(v0, v1, [2, 3, 10, 9], [b, t, l])
            Parent.AddHex(v0, v1, [3, 4, 5, 10], [b, t, l])
            Parent.AddHex(v0, v1, [9, 10, 5, 6], [b, t, l])
            Parent.AddHex(v0, v1, [8, 9, 6, 7], [b, t, l])
        # ==============================================================================

    def ExportEdges(self):
        for airfoil in self.airfoil:
            vert = airfoil.vertCount

            Parent.AddEdges(vert[1], vert[0], airfoil.top0, 'BSpline')
            Parent.AddEdges(vert[2], vert[1], airfoil.top1, 'BSpline')
            Parent.AddEdges(vert[3], vert[2], airfoil.top2, 'BSpline')
            Parent.AddEdges(vert[4], vert[3], airfoil.top3, 'BSpline')
            Parent.AddEdges(vert[5], vert[4], airfoil.bot3, 'BSpline')
            Parent.AddEdges(vert[6], vert[5], airfoil.bot2, 'BSpline')
            Parent.AddEdges(vert[7], vert[6], airfoil.bot1, 'BSpline')
            Parent.AddEdges(vert[0], vert[7], airfoil.bot0, 'BSpline')

    # ==============================================================================
    def ExportBound(self):
        if self.main:
            blade = 'blade1'
            merge = 'bladeToHub'
        else:
            blade = 'blade'
            merge = 'bladeToHub'
        n = len(self.airfoil) - 1
        for i in range(n):
            v0 = self.airfoil[i].vertCount
            v1 = self.airfoil[i + 1].vertCount

            Parent.AddBound(blade, f'({v0[0]} {v0[1]} {v1[1]} {v1[0]})')
            Parent.AddBound(blade, f'({v0[1]} {v0[2]} {v1[2]} {v1[1]})')
            Parent.AddBound(blade, f'({v0[2]} {v0[3]} {v1[3]} {v1[2]})')
            Parent.AddBound(blade, f'({v0[3]} {v0[4]} {v1[4]} {v1[3]})')
            Parent.AddBound(blade, f'({v0[4]} {v0[5]} {v1[5]} {v1[4]})')
            Parent.AddBound(blade, f'({v0[5]} {v0[6]} {v1[6]} {v1[5]})')
            Parent.AddBound(blade, f'({v0[6]} {v0[7]} {v1[7]} {v1[6]})')
            Parent.AddBound(blade, f'({v0[7]} {v0[0]} {v1[0]} {v1[7]})')
            if i == 0:
                Parent.AddBound(merge, f'({v0[7]} {v0[8]} {v0[1]} {v0[0]})')
                Parent.AddBound(merge, f'({v0[7]} {v0[6]} {v0[9]} {v0[8]})')
                Parent.AddBound(merge, f'({v0[8]} {v0[9]} {v0[2]} {v0[1]})')
                Parent.AddBound(merge, f'({v0[6]} {v0[5]} {v0[10]} {v0[9]})')
                Parent.AddBound(merge, f'({v0[9]} {v0[10]} {v0[3]} {v0[2]})')
                Parent.AddBound(merge, f'({v0[10]} {v0[5]} {v0[4]} {v0[3]})')
            if i == n - 1:
                Parent.AddBound(blade, f'({v1[0]} {v1[1]} {v1[8]} {v1[7]})')
                Parent.AddBound(blade, f'({v1[1]} {v1[2]} {v1[9]} {v1[8]})')
                Parent.AddBound(blade, f'({v1[8]} {v1[9]} {v1[6]} {v1[7]})')
                Parent.AddBound(blade, f'({v1[9]} {v1[10]} {v1[5]} {v1[6]})')
                Parent.AddBound(blade, f'({v1[2]} {v1[3]} {v1[10]} {v1[9]})')
                Parent.AddBound(blade, f'({v1[3]} {v1[4]} {v1[5]} {v1[10]})')
# ==============================================================================
