"""
"""
from Codes.BlockMesh.Vertices import Vertices

# Real value divided by 2:
SHELL_WIDTH = 3
SHELL_HEIGHT = 3


# Airfoil structure:
# 7----------4
# --3------0--
# --2------1--
# 6-----------5


class Hollow(Vertices):
    def __init__(self, i):
        # Initialise variables
        self.verts = []
        self.verts_id = []
        self.top = []
        self.left = []
        self.right = []
        self.bot = []
        self.blocks = []
        self.b_splines = []
        self.arc_splines = []
        # Extract vertices and splines
        self.prepare_verts()
        self.prepare_shell()
        self.prepare_blocks(i)
        self.prepare_splines()

    def prepare_verts(self):
        inner_length = 0.5
        self.set_verts([(-inner_length,  inner_length, 65),
                         (-inner_length, -inner_length, 65),
                         ( inner_length, -inner_length, 65),
                         ( inner_length,  inner_length, 65)])

    def prepare_shell(self):
        z = (self.verts[0][2] + self.verts[1][2] + self.verts[2][2] + self.verts[3][2]) / 4

        shell = [[-SHELL_WIDTH,  SHELL_HEIGHT, z],
                 [-SHELL_WIDTH, -SHELL_HEIGHT, z],
                 [ SHELL_WIDTH, -SHELL_HEIGHT, z],
                 [ SHELL_WIDTH,  SHELL_HEIGHT, z]]

        self.set_verts(shell)

    def prepare_blocks(self, i):
        self.blocks = [[self.verts_id[0], self.verts_id[3], self.verts_id[7], self.verts_id[4]],
                       [self.verts_id[1], self.verts_id[0], self.verts_id[4], self.verts_id[5]],
                       [self.verts_id[2], self.verts_id[1], self.verts_id[5], self.verts_id[6]],
                       [self.verts_id[3], self.verts_id[2], self.verts_id[6], self.verts_id[7]]]
        if i >= 16:
            self.blocks.append([self.verts_id[3], self.verts_id[0], self.verts_id[1], self.verts_id[2]])

    def prepare_splines(self):
        pass
        # self.b_splines = [[self.verts_id[1], self.verts_id[0], self.right],
        #                   [self.verts_id[0], self.verts_id[3], self.top],
        #                   [self.verts_id[3], self.verts_id[2], self.left],
        #                   [self.verts_id[2], self.verts_id[1], self.bot]]
