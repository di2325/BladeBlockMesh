from Codes.Two_dimensional.Splines import airfoil_splines, create_spline
from Codes.Two_dimensional.Vertices import Vertices
from Codes.BlockMesh.BlockMesh import BlockMesh

# Real value divided by 2:
SHELL_WIDTH = 3
SHELL_HEIGHT = 2.5


# Airfoil structure:
# 7----------4
# --3------0--
# --2------1--
# 6-----------5


class Airfoil(Vertices):
    def __init__(self, i):
        self.verts_id = []
        self.shell = []
        splines = airfoil_splines(i)
        self.verts = splines["verts"]
        self.top = splines["top"]
        self.left = splines["left"]
        self.right = splines["right"]
        self.bot = splines["bot"]
        self.verts_id.extend(self.add_vert(self.verts))
        self.create_shell()
        self.create_spline()

    def create_shell(self):
        center = [(self.verts[0][0] + self.verts[1][0] + self.verts[2][0] + self.verts[3][0]) / 4,
                  (self.verts[0][1] + self.verts[1][1] + self.verts[2][1] + self.verts[3][1]) / 4,
                  (self.verts[0][2] + self.verts[1][2] + self.verts[2][2] + self.verts[3][2]) / 4]

        self.shell = [[center[0] - SHELL_WIDTH, center[1] + SHELL_HEIGHT, center[2]],
                      [center[0] - SHELL_WIDTH, center[1] - SHELL_HEIGHT, center[2]],
                      [center[0] + SHELL_WIDTH, center[1] - SHELL_HEIGHT, center[2]],
                      [center[0] + SHELL_WIDTH, center[1] + SHELL_HEIGHT, center[2]]]

        self.verts_id.extend(self.add_vert(self.shell))

    def create_spline(self):
        BlockMesh.add_to_edges(create_spline(self.verts_id[1], self.verts_id[0], self.right))
        BlockMesh.add_to_edges(create_spline(self.verts_id[0], self.verts_id[3], self.top))
        BlockMesh.add_to_edges(create_spline(self.verts_id[3], self.verts_id[2], self.left))
        BlockMesh.add_to_edges(create_spline(self.verts_id[2], self.verts_id[1], self.bot))
