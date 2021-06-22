"""
Class Hexes:
    Contains 3D information (blocks), gained from two profiles

    Attributes:
        self.blocks1,               stores block information of each profile
        self.blocks2

        self.bound1,                stores boundaries of each profile
        self.bound2

    Methods:
        self.get_hex                exports IDs of vertices in the ready for BlockMesh from
"""


class Hexes:
    hexes = []

    @staticmethod
    def set_hexes(profile1, profile2):
        block1 = profile1.blocks
        block2 = profile2.blocks
        for i in range(len(block1)):
            Hexes.hexes.append(
                (f"\n\thex ({block1[i][0]} {block1[i][1]} {block1[i][2]} {block1[i][3]} "
                 f"{block2[i][0]} {block2[i][1]} {block2[i][2]} {block2[i][3]}) rotatingZone "
                 f"({10} {10} {10}) simpleGrading "
                 f"({1} {1} {1})"))

    @staticmethod
    def get_hexes():
        return Hexes.hexes
