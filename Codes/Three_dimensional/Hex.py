from Codes.BlockMesh.BlockMesh import BlockMesh


class Hex:
    def __init__(self, airfoil1, airfoil2):
        self.vert1 = airfoil1.verts_id
        self.vert2 = airfoil2.verts_id
        hex = [self.convert_to_hex([0, 3, 7, 4]),
               self.convert_to_hex([1, 0, 4, 5]),
               self.convert_to_hex([2, 1, 5, 6]),
               self.convert_to_hex([3, 2, 6, 7])]
        BlockMesh.add_to_hex(hex)

    def convert_to_hex(self, i):
        return (f"\n\thex ({self.vert1[i[0]]} {self.vert1[i[1]]} {self.vert1[i[2]]} {self.vert1[i[3]]} "
                f"{self.vert2[i[0]]} {self.vert2[i[1]]} {self.vert2[i[2]]} {self.vert2[i[3]]}) rotatingZone "
                f"({10} {10} {10}) simpleGrading "
                f"({1} {1} {1})")
