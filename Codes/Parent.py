# ==============================================================================
# Parent class contains global variables, like:
#     int: hubRad, hubHeight, vertCount, meshCoeff
#     list: verts, hex, 
#     libs: edges, boundaries
# Add functions:
#     AddVerts:
#         Takes x, y, z, and ID of a vertex
#         Rounds coordinates and stores as string
#     AddHex:
#         Takes all vertex IDs, required IDs, length of an edge, and grading
#         Multiplies length of an edge to get amount of cells and rounds it
#         Stores all points as tuple in the following order:
#             first face IDs -> second face IDs -> cells -> grading
#     AddEdges:
#         Takes IDs of vertices of an edge, edge crossing points, and edge type
#         Store everything as list in required library
#     AddBound:
#         Takes name of a boundary and vertex IDs of a face
#         Check if boundary is allready present
#         Add face to existing or newly created boundary
# Export functions:
#     ExportVerts:
#         Outputs verts
#     ExportHex:
#         Outputs hex in required form
#     ExportEdges:
#         Outputs all arcs and all BSplines
#     ExportBound:
#         Outputs all boundaries
# ==============================================================================
class Parent():
    # ==============================================================================
    def FindPoint(target, where):
        delta = 1000
        for line in where:
            if delta > abs(target - line[0]):
                output = line
                delta = abs(target - line[0])
        return output

    # ==============================================================================
    # Add functions
    # ==============================================================================
    def AddVerts(x, y, z, v):
        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)
        Parent.verts.append(f"\n\t({x}   \t{y}   \t{z})\t\t//{v}")

    # ==============================================================================
    def AddHex(vert0, vert1, n, cells=[1, 1, 1], grading=[1, 1, 1]):
        cells = (round(cells[0] * Parent.meshCoeff), \
                 round(cells[1] * Parent.meshCoeff), \
                 round(cells[2] * Parent.meshCoeff))
        Parent.hex.append((vert0[n[0]], vert0[n[1]], vert0[n[2]], vert0[n[3]], \
                           vert1[n[0]], vert1[n[1]], vert1[n[2]], vert1[n[3]], \
                           cells[0], cells[1], cells[2], \
                           grading[0], grading[1], grading[2]))

    # ==============================================================================
    def AddEdges(node1, node2, point, edge):
        Parent.edges[edge].append((node1, node2, point))

    # ==============================================================================
    def AddBound(name, face):
        if not name in Parent.boundaries:
            Parent.boundaries[name] = [face]
        else:
            Parent.boundaries[name].append(face)

    # ==============================================================================
    # Export functions
    # ==============================================================================
    def ExportVerts():
        return Parent.verts

    # ==============================================================================
    def ExportHex():
        output = []
        for i in Parent.hex:
            output.append(f"\n\thex ({i[0]} {i[1]} {i[2]} {i[3]} " + \
                          f"{i[4]} {i[5]} {i[6]} {i[7]}) bladeZone " + \
                          f"({i[8]} {i[9]} {i[10]}) simpleGrading " + \
                          f"({i[11]} {i[12]} {i[13]})")
        return output

    # ==============================================================================
    def ExportEdges():
        output = []
        for edge in Parent.edges['arc']:
            output.append(f"\n\tarc {edge[0]} {edge[1]} ({edge[2][0]} {edge[2][1]} {edge[2][2]})")
        for edge in Parent.edges['BSpline']:
            output.append(f"\nBSpline {edge[0]} {edge[1]}")
            output.append("\n(")
            for line in edge[2]:
                output.append(f"\n\t({line[0]} {line[1]} {line[2]})")
            output.append("\n)")
        return output

    # ==============================================================================
    def ExportBound():
        output = []
        for boundary in Parent.boundaries:
            output.append(f"\n\t{boundary}")
            output.append("\n\t{")
            output.append("\n\t\ttype wall;")
            output.append("\n\t\tfaces")
            output.append("\n\t\t(")
            for i in Parent.boundaries[boundary]:
                output.append(f"\n\t\t\t{i}")
            output.append("\n\t\t);")
            output.append("\n\t}")
        return output
# ==============================================================================
