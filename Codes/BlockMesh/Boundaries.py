"""

"""


class Boundaries:
    boundaries = {}

    @staticmethod
    def assign_boundaries(boundary, profile1, verts1, profile2=None, verts2=None):
        if boundary not in Boundaries.boundaries:
            Boundaries.boundaries[boundary] = []
        if profile2:
            for i in range(len(verts1)):
                Boundaries.boundaries[boundary].append([profile1.verts_id[verts1[i][0]],
                                                        profile1.verts_id[verts1[i][1]],
                                                        profile2.verts_id[verts2[i][0]],
                                                        profile2.verts_id[verts2[i][1]]])
        else:
            for vert in verts1:
                Boundaries.boundaries[boundary].append([profile1.verts_id[vert[0]],
                                                        profile1.verts_id[vert[1]],
                                                        profile1.verts_id[vert[2]],
                                                        profile1.verts_id[vert[3]]])

    @staticmethod
    def get_boundaries():
        output = []
        for boundary in Boundaries.boundaries:
            output.append(f"\n\t{boundary}")
            output.append("\n\t{")
            output.append("\n\t\ttype wall;")
            output.append("\n\t\tfaces")
            output.append("\n\t\t(")
            for i in range(len(Boundaries.boundaries[boundary])):
                output.append(
                    f"\n\t\t\t({Boundaries.boundaries[boundary][i][0]} {Boundaries.boundaries[boundary][i][1]} "
                    f"{Boundaries.boundaries[boundary][i][2]} {Boundaries.boundaries[boundary][i][3]})")
            output.append("\n\t\t);")
            output.append("\n\t}")
        return output
