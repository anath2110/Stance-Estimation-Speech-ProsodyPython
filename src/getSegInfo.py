import os.path
import numpy as np
from readStanceAnnotations import readStanceAnnotations 
def getSegInfo(audioDir, annotDir,lang):
    [a0, a1, starts, ends, aufiles, a5] = readStanceAnnotations(annotDir,lang)
    if not isUtepFormat(audioDir):
        for i in range(0,len(aufiles)):
            aufiles[i] = "concat" + aufiles[i]
            #print(aufiles[i])
    return starts, ends, aufiles

def isUtepFormat(audioDir):
    #Utep directories are flat; ldc directories have subdirectories
    result = True
    contents = dir(audioDir)
    for i in range(3,len(contents)):
        file = contents[i]
        if (not os.path.isdir(file)):
            continue
        if (file.name.find('pitchCache') >= 0):
            continue
        result = False
    return result

def extractIndexes(str1, str2):
    i = 0
    a = []
    while(i < len(str1) and i >= 0):
        if(str1.find(str2, i) == -1):
            break
        else:
            a.append(str1.find(str2, i) + 1)
            print(i)
            i = str1.find(str2, i) + 1
    return a

#Test extractIndexes
# str1 = "Find the starting indices of a pattern in a character vector"
# str2 = "in"
# a = extractIndexes(str1,str2)
# print(a)
#starts, ends, aufiles=getSegInfo('../../mandarin/audio/','../../mandarin/trainAnnotationsCSV/' )
#print(starts.shape)
#np.set_printoptions(threshold=np.inf)
#print(aufiles)