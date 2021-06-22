"""
class Boundaries:
    hexes                   List of all boundaries

    set_hexes()             Takes profiles and converts them to the correct form

    get_hexes()             Exports boundaries in the correct form
"""


class Hexes:
    hexes = []

    @staticmethod
    def set_hexes(profile1, profile2, block, cells=(10, 10, 10), grading=(1, 1, 1)):
        hex1 = [profile1.verts_id[block[0]], profile1.verts_id[block[1]],
                profile1.verts_id[block[2]], profile1.verts_id[block[3]]]
        hex2 = [profile2.verts_id[block[0]], profile2.verts_id[block[1]],
                profile2.verts_id[block[2]], profile2.verts_id[block[3]]]
        Hexes.hexes.append(
                (f"\n\thex ({hex1[0]} {hex1[1]} {hex1[2]} {hex1[3]} "
                 f"{hex2[0]} {hex2[1]} {hex2[2]} {hex2[3]}) rotatingZone "
                 f"({cells[0]} {cells[1]} {cells[2]}) simpleGrading "
                 f"({grading[0]} {grading[1]} {grading[2]})"))

    @staticmethod
    def get_hexes():
        return Hexes.hexes
