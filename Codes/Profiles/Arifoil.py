"""
Class Airfoil (profile):
"""


class Airfoil:
    def __init__(self):
        # Initialise variables
        self.verts = []
        self.verts_id = []
        self.b_splines = []
        self.arc_splines = []

    def set_b_splines(self, v1, v2, spline):
        self.b_splines.append([self.verts_id[v1], self.verts_id[v2], spline])
