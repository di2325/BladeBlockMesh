def GetLastVert(target):
    maxLength = len(target)
    maxVert = len(target[maxLength-1].vertCount)
    return target[maxLength-1].vertCount[maxVert-1] + 1