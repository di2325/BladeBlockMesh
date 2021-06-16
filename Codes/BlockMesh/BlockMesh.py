import os


class BlockMesh:
    verts = []
    hex = []
    edges = []
    boundaries = []
    vertCount = 0

    @staticmethod
    def add_to_verts(target):
        for line in target:
            line = list(line)
            for i in range(len(line)):
                line[i] = round(line[i], 4)
            BlockMesh.verts.append(f"\n\t({line[0]}   \t{line[1]}   \t{line[2]})\t\t//{BlockMesh.vertCount}")
            BlockMesh.vertCount += 1

    @staticmethod
    def add_to_hex(target):
        for line in target:
            BlockMesh.hex.append(line)

    @staticmethod
    def add_to_edges(target):
        for line in target:
            BlockMesh.edges.append(line)

    @staticmethod
    def add_to_boundaries(target):
        for line in target:
            BlockMesh.boundaries.append(line)

    @staticmethod
    def create_blockmeshdict():
        # ==================================================
        # -----Writing blockMeshDict-----
        # ==================================================
        if os.path.exists('../output/blockMeshDict'):
            os.remove('../output/blockMeshDict')
        output = open(os.path.abspath('../output/blockMeshDict'), "a")
        # =======================================|
        # ____Header_____________________________|
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write(
            "// * * * * * * * * * * * * * * * * * * * "
            "* * * * * * * * * * * * * * * * * * //\n"
            "FoamFile\n"
            "{\n"
            "\tversion     2.0;\n"
            "\tformat      ascii;\n"
            "\tclass       dictionary;\n"
            "\tobject      blockMeshDict;\n"
            "}\n"
            "// * * * * * * * * * * * * * * * * * * * "
            "* * * * * * * * * * * * * * * * * * //"
        )
        # =======================================|

        # =======================================|
        # ____Vertices___________________________|
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\nconvertToMeters 1;\n")  # ~|
        output.write("\nvertices\n(")  # ~~~~~~~~~~|
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        for line in BlockMesh.verts:
            output.write(f"{line}")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n);")  # ~~~~~~~~~~~~~~~~~~~|
        # =======================================|

        # =======================================|
        # ____Blocks_____________________________|
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n\nblocks\n(")  # ~~~~~~~~~~|
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        for line in BlockMesh.hex:
            output.write(f"{line}")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n);")  # ~~~~~~~~~~~~~~~~~~~|
        # =======================================|

        # =======================================|
        # ____Edges______________________________|
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n\nedges\n(")  # ~~~~~~~~~~~|
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        for line in BlockMesh.edges:
            output.write(f"{line}")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n);")  # ~~~~~~~~~~~~~~~~~~~|
        # =======================================|

        # =======================================|
        # ____Boundary___________________________|
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n\nboundary\n(")  # ~~~~~~~~|
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        # for line in self.boundariesToPrint:
        #     output.write(f"{line}")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n);")  # ~~~~~~~~~~~~~~~~~~~|
        # =======================================|

        # #=======================================|
        # #____MergePatch_________________________|
        # #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        # output.write("\nmergePatchPairs\n(")#~~~|
        # #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        # output.write("\n\t(interfaceIn0 interfaceOut0)")
        # output.write("\n\t(interfaceIn1 interfaceOut1)")
        # output.write("\n\t(interfaceIn2 interfaceOut2)")
        # output.write("\n\t(interfaceInHubTop interfaceOutHubTop)")
        # output.write("\n\t(interfaceInHubBot interfaceOutHubBot)")
        # #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        # output.write("\n);")#~~~~~~~~~~~~~~~~~~~|
        # #=======================================|

        output.write("\n// **********************"
        "****************************************"
                                "*********** //")
        output.close()
