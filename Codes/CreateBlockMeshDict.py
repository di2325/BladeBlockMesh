import os, sys
class BlockMesh:
    def __init__(self, vertCount = 0, sigFig = 4):
        self.vertToPrint = []
        self.hexToPrint = []
        self.edgesToPrint = []
        self.boundariesToPrint = []
        self.vertCount = vertCount
        self.sigFig = sigFig
        
        
    def AddToVertToPrint(self, target):
        for line in target:
            line = list(line)
            for i in range(len(line)):
                line[i] = round(line[i], self.sigFig)
            self.vertToPrint.append(f"\n\t({line[0]}   \t{line[1]}   \t{line[2]})\t\t//{self.vertCount}")
            self.vertCount += 1
    
    
    def AddToHexToPrint(self, target):
        for line in target:
            self.hexToPrint.append(line)
            
            
    def AddToEdgesToPrint(self, target):
        for line in target:
            self.edgesToPrint.append(line)
            
            
    def AddToBoundariesToPrint(self, target):
        for line in target:
            self.boundariesToPrint.append(line)
            
            
    
    def CreateBlockMeshDict(self):
        #==================================================
        #-----Writing blockMeshDict-----
        #==================================================
        if os.path.exists('../output/blockMeshDict'):
            os.remove('../output/blockMeshDict')
        output = open(os.path.abspath('../output/blockMeshDict'), "a")
        #=======================================|
        #____Header_____________________________|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\
FoamFile\n\
{\n\
    version     2.0;\n\
    format      ascii;\n\
    class       dictionary;\n\
    object      blockMeshDict;\n\
}\n\
// * * * * * * * * * * * * * * * * * * * \
* * * * * * * * * * * * * * * * * * //")
        #=======================================|
        
        #=======================================|
        #____Vertices___________________________|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\nconvertToMeters 1;\n")#~|
        output.write("\nvertices\n(")#~~~~~~~~~~|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        for line in self.vertToPrint:
            output.write(f"{line}")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n);")#~~~~~~~~~~~~~~~~~~~|
        #=======================================|
        
        #=======================================|
        #____Blocks_____________________________|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n\nblocks\n(")#~~~~~~~~~~|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        for line in self.hexToPrint:
            output.write(f"{line}")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n);")#~~~~~~~~~~~~~~~~~~~|
        #=======================================|
        
        #=======================================|
        #____Edges______________________________|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n\nedges\n(")#~~~~~~~~~~~|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        for line in self.edgesToPrint:
            output.write(f"{line}")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n);")#~~~~~~~~~~~~~~~~~~~|
        #=======================================|
        
        #=======================================|
        #____Boundary___________________________|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n\nboundary\n(")#~~~~~~~~|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        for line in self.boundariesToPrint:
            output.write(f"{line}")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n);")#~~~~~~~~~~~~~~~~~~~|
        #=======================================|
        #=======================================|
        #____MergePatch_________________________|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\nmergePatchPairs\n(")#~~~|
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n\t(interfaceIn0 interfaceOut0)")
        output.write("\n\t(interfaceIn1 interfaceOut1)")
        output.write("\n\t(interfaceIn2 interfaceOut2)")
        output.write("\n\t(interfaceInHubTop interfaceOutHubTop)")
        output.write("\n\t(interfaceInHubBot interfaceOutHubBot)")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
        output.write("\n);")#~~~~~~~~~~~~~~~~~~~|
        #=======================================|
        output.write("\n// *********************\
****************************************\
************ //")
        output.close()