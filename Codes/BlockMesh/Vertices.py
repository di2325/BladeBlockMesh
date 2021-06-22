"""
class Vertices:
    verts                   List of all boundaries

    vert_count              Amount of vertices

    set_verts()             Takes vertices, saves them to local list of verts,
                            fills local list of verts_id,
                            saves vertices to the global verts list in the correct form

    get_verts()             Exports vertices from the global verts list
"""


class Vertices:
    verts = []
    vert_count = 0

    @staticmethod
    def set_verts(profile, verts):
        profile.verts.extend(verts)
        profile.verts_id.extend(list(range(Vertices.vert_count, Vertices.vert_count + len(verts))))
        for vert in verts:
            Vertices.verts.append(f"\n\t({round(vert[0], 4)}   \t{round(vert[1], 4)}   "
                                  f"\t{round(vert[2], 4)})\t\t//{Vertices.vert_count}")
            Vertices.vert_count += 1

    @staticmethod
    def get_verts():
        return Vertices.verts
