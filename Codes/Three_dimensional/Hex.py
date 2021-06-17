"""
Class Hex:
    Contains 3D information (blocks), gained from two profiles

    Attributes:
        boundaries                  library, which stores all boundaries from all instances of Hex class

        self.blocks1,               stores block information of each profile
        self.blocks2

        self.bound1,                stores boundaries of each profile
        self.bound2

    Methods:
        self.assign_boundaries      combines information from self.bound1 and self.bound2 and stores them in boundaries

        self.get_hex                exports IDs of vertices in the ready for BlockMesh from

        get_boundaries              export all boundaries in the ready for BlockMesh form
"""
class Hex:
    boundaries = {}

    def __init__(self, profile1, profile2):
        self.blocks1 = profile1.blocks
        self.blocks2 = profile2.blocks
        self.bound1 = profile1.boundaries
        self.bound2 = profile2.boundaries
        self.assign_boundaries()

    def assign_boundaries(self):
        for boundary in self.bound1:
            if boundary not in Hex.boundaries:
                Hex.boundaries[boundary] = []
            for i in range(len(self.bound1[boundary])):
                Hex.boundaries[boundary].append([self.bound1[boundary][i][0], self.bound1[boundary][i][1],
                                                 self.bound2[boundary][i][1], self.bound2[boundary][i][0]])

    def get_hex(self):
        output = []
        for i in range(len(self.blocks1)):
            output.append(
                (f"\n\thex ({self.blocks1[i][0]} {self.blocks1[i][1]} {self.blocks1[i][2]} {self.blocks1[i][3]} "
                 f"{self.blocks2[i][0]} {self.blocks2[i][1]} {self.blocks2[i][2]} {self.blocks2[i][3]}) rotatingZone "
                 f"({10} {10} {10}) simpleGrading "
                 f"({1} {1} {1})"))
        return output

    @staticmethod
    def get_boundaries():
        output = []
        for boundary in Hex.boundaries:
            output.append(f"\n\t{boundary}")
            output.append("\n\t{")
            output.append("\n\t\ttype wall;")
            output.append("\n\t\tfaces")
            output.append("\n\t\t(")
            for i in range(len(Hex.boundaries[boundary])):
                output.append(f"\n\t\t\t({Hex.boundaries[boundary][i][0]} {Hex.boundaries[boundary][i][1]} "
                              f"{Hex.boundaries[boundary][i][2]} {Hex.boundaries[boundary][i][3]})")
            output.append("\n\t\t);")
            output.append("\n\t}")
        return output
