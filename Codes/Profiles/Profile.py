"""
class Profile:
    self.verts          local list of coordinates

    self.verts_id       local list of IDs of the coordinates

    self.b_splines,     local list of splines in the following form: [vertex id, vertex id, list of splines]
    self.arc_splines
"""


class Profile:
    def __init__(self):
        # Initialise variables
        self.verts = []
        self.verts_id = []
        self.b_splines = []
        self.arc_splines = []

    def set_b_splines(self, v1, v2, spline):
        self.b_splines.append([self.verts_id[v1], self.verts_id[v2], spline])

    def set_arc_splines(self, v1, v2, spline):
        self.arc_splines.append([self.verts_id[v1], self.verts_id[v2], spline])
