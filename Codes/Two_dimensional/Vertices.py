class Vertices:
    vert_count = 0
    verts = []

    @staticmethod
    def add_vert(verts):
        if type(verts[0]) != list and type(verts[0]) != tuple:
            verts = [verts]
        Vertices.verts.extend(verts)
        output = list(range(Vertices.vert_count, Vertices.vert_count + len(verts)))
        Vertices.vert_count += len(verts)
        return output

    @staticmethod
    def get_vert(i):
        return Vertices.verts[i]

    @staticmethod
    def export_coord():
        return Vertices.verts
