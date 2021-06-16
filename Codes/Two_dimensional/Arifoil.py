from Codes.Two_dimensional.Vertices import Vertices

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
        self.verts = []
        self.verts_id = []
        self.top = []
        self.left = []
        self.right = []
        self.bot = []
        self.get_airfoil_data(i)
        self.create_shell()

    def create_shell(self):
        center = [(self.verts[0][0] + self.verts[1][0] + self.verts[2][0] + self.verts[3][0]) / 4,
                  (self.verts[0][1] + self.verts[1][1] + self.verts[2][1] + self.verts[3][1]) / 4,
                  (self.verts[0][2] + self.verts[1][2] + self.verts[2][2] + self.verts[3][2]) / 4]

        shell = [[center[0] - SHELL_WIDTH, center[1] + SHELL_HEIGHT, center[2]],
                 [center[0] - SHELL_WIDTH, center[1] - SHELL_HEIGHT, center[2]],
                 [center[0] + SHELL_WIDTH, center[1] - SHELL_HEIGHT, center[2]],
                 [center[0] + SHELL_WIDTH, center[1] + SHELL_HEIGHT, center[2]]]

        self.save_verts(shell)

    def get_verts(self):
        output = []
        for i in range(len(self.verts)):
            output.append(f"\n\t({round(self.verts[i][0], 4)}   \t{round(self.verts[i][1], 4)}   "
                          f"\t{round(self.verts[i][2], 4)})\t\t//{self.verts_id[i]}")
        return output

    def get_spline(self):
        output = self.b_spline(self.verts_id[1], self.verts_id[0], self.right)
        output.extend(self.b_spline(self.verts_id[0], self.verts_id[3], self.top))
        output.extend(self.b_spline(self.verts_id[3], self.verts_id[2], self.left))
        output.extend(self.b_spline(self.verts_id[2], self.verts_id[1], self.bot))
        return output
