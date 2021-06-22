"""
Class Hex:
    Contains 3D information (blocks), gained from two profiles

    Attributes:
        self.blocks1,               stores block information of each profile
        self.blocks2

        self.bound1,                stores boundaries of each profile
        self.bound2

    Methods:
        self.get_hex                exports IDs of vertices in the ready for BlockMesh from
"""


class Hex:

    def __init__(self, profile1, profile2):
        self.blocks1 = profile1.blocks
        self.blocks2 = profile2.blocks

    def get_hex(self):
        output = []
        for i in range(len(self.blocks1)):
            output.append(
                (f"\n\thex ({self.blocks1[i][0]} {self.blocks1[i][1]} {self.blocks1[i][2]} {self.blocks1[i][3]} "
                 f"{self.blocks2[i][0]} {self.blocks2[i][1]} {self.blocks2[i][2]} {self.blocks2[i][3]}) rotatingZone "
                 f"({10} {10} {10}) simpleGrading "
                 f"({1} {1} {1})"))
        return output
