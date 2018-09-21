# -*- coding: utf-8 -*-
"""
Created on Thur Dec 14 13:30:49 2017

@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso"""


import numpy as np
import os
from makeTrackSpecs import makeTrackspec
import cProfile, pstats, io
import math
import sys
import hdf5storage
#import pickle
import _pickle as pickle #cPickle package is so named in Python 3.x
import scipy
from makeTrackMonster import makeTrackMonster
from getSegInfo import getSegInfo
from getfeaturespec import getfeaturespec
import segDataObject as clssegobj
def prosodizeCorpus(audioDir, annotDir, featurespec, stride,lang):
    # converted from original by Nigel Ward, UTEP, June 2017
        # creates a nice data structure representing the prosodic information etc.
        # This data structure is the
        # inputs: audioDir, varies in format, UTEP or LDC
        # annotDir, ditto.  this function uses this only for
        # the news-segment boundaries, and for UTEP-format audio
        # featurespec
        # stride: time between patches, in milliseconds
        # output: prosodized is cell array of structures
        # this is segmentData format, see ../doc/UTEP-prosody-overview.docx
        # This function does not add props (annotation info);
        # since that is added later if needed.
        # Notice also that the output is not z-normalized; that's done later
        # test with x = prosodizeCorpus('testAudio', 'testAnnotations', ...
        # getfeaturespec('src/mono4.fss');
        # and then examine x{1}, x{2}, etc.
    starts, ends, aufiles = getSegInfo(audioDir, annotDir,lang)
    np.set_printoptions(threshold=np.inf)# print the entire array
    #sys.stdout = open('prosidize_1st3Train.txt', 'w')
    
    nsegments = len(starts)
    #print('nsegments %d' %nsegments)
    #print(aufiles)
    segData=[]  
    monsDict = {}# to save the monster features with corresponding audioname in a dictionary
    for i in range(nsegments): 
        #print('in prosodize corpus')
        #print(i)
        #print('in segment =%d' %i)
        #print('auname=%s' %aufiles[i])
        segData.append(clssegobj.segDataObj(i,aufiles[i], starts[i], ends[i],featurespec, audioDir, stride,lang,monsDict))     
        
        #segfeatures = featuresForSegment(i,aufiles[i], starts[i], ends[i],featurespec, audioDir, stride)
        # Converting to single saves diskspace for ppmfiles, maybe time too,
        # and gives the same answers, but it causes annoying warnings
        #when running knnsearch, so for now we don't do it
        # segfeatures = single(segfeatures);
        #features=(addTemporalFeatures(segfeatures, stride))
        #print(features.shape)
#        if(i==0):
#            segData = np.array(nsegments, dtype=[('features','f4',(14,19)),('startTime','i4'),('endTime','i4'),('broadcastName', 'S100'),('properties', 'S100')])
#            segData['features'][i] = features       
#            segData['startTime'][i]=int(starts[i])     
#            segData['endTime'][i]=int(ends[i])      
#            segData['broadcastName'][i]= aufiles[i].decode('UTF-8')     
#            segData['properties'][i]= ''# empty, possibly added later
#        else:
#            segData['features'][i] = features       
#            segData['startTime'][i]=int(starts[i])     
#            segData['endTime'][i]=int(ends[i])      
#            segData['broadcastName'][i]= aufiles[i].decode('UTF-8')     
#            segData['properties'][i]= ''# empty, possibly added later 
#        
        
    #scipy.io.savemat('segdatapy.mat', {'segdatapy': segData})
    return segData

# ----------------------------------------------------------------------------
# input: matrix of features, one every 100 ms
# output: same, plus two new columns for temporal features
# this function replaces Jason's addTimeFeatures
def addTemporalFeatures(features, stride):
    timeBetweenPatches = .001 * stride # seconds
    npatches = np.shape(features)[0]
    segmentDuration = npatches * timeBetweenPatches
    timesSinceStart = np.transpose(np.arange(npatches)*timeBetweenPatches -.050)
    timesUntilEnd = segmentDuration - timesSinceStart
    #print(features.shape)
    #print(timesSinceStart.shape)
    #print(timesUntilEnd.shape)
    augmentedFeatures = np.append(features, np.log(timesSinceStart).reshape([-1,1]),axis=1)
    #print(augmentedFeatures.shape)
    augmentedFeatures = np.append(augmentedFeatures,np.log(timesUntilEnd).reshape([-1,1]),axis = 1)
    #print(augmentedFeatures.shape)
    return augmentedFeatures

# ------------------------------------------------------------------
def featuresForSegment(i,aufile, startTime, endTime, featurespec, audioDir, stride,lang,monsDict):
    # aufile = char(aufile)
    monster = findTrackMonster(i,aufile, audioDir, featurespec,lang,monsDict)
    #print(monster.shape)
    framesPerSecond = 100 #what makeTrackMonster returns
    startFrame = max(0, int(math.floor(startTime * framesPerSecond)- 1))
    endFrame = int(math.floor(endTime * framesPerSecond))
    endFrame = twiddleEndFrame(aufile, startFrame, endFrame, np.shape(monster)[0])  
    segmentFrames = monster[startFrame:endFrame,:]
    #print(segmentFrames.shape)
    downsamplingRate = int((stride / 10))
    segmentSize = np.shape(segmentFrames)[0]

    features = segmentFrames[0:segmentSize:downsamplingRate,:]
    #print(features.shape)
    
    return features

# ------------------------------------------------------------------
def twiddleEndFrame(aufile, segStartFrame, segEndFrame, monsterEndFrame):
    newEndFrame = segEndFrame # the normal case
    if (segEndFrame == 0):
        newEndFrame = monsterEndFrame
        if (newEndFrame > segStartFrame + int(200 * 100)): # 200 seconds
            print('!!warning very long for %s: frames %f to %f!?\n', aufile, segStartFrame, segEndFrame)


    if (segEndFrame > monsterEndFrame):
        newEndFrame = monsterEndFrame
        if (segEndFrame > monsterEndFrame + int(0.5 * 100)): # half a second
            print('!!warning too short for %s: frames %f to %f!?\n', aufile, segStartFrame, segEndFrame)
   
    return newEndFrame

    # ------------------------------------------------------------------
    #lookup saved prosodic features in cache or compute the

def findTrackMonster(i,base, directory, featurespec,lang,monsDict):
    global savedFile
    global savedMonster
    #monsDict = {}
    #print(base)
   
    base=base.decode('UTF-8') # it otherwise appears in byte form, with a 'b' prefixed at front
    file = base +'.au'
    #print(file)
    if (i==0): 
        
        
        savedFile=file
        savedkey = '%s' % savedFile
        #print("in first if")        
        trackspec = makeTrackspec('l', file,directory) 
        fcframe,newMonster = makeTrackMonster(trackspec, featurespec) 
        
        
        #print("call monster")
        #print(i)        
        #print("file")
        #print(file)
        #print("savedFile")
        #print(savedFile)
        savedMonster=newMonster
        monster=newMonster
        monsDict[savedkey] = savedMonster
    else:
        if(savedFile==file):
           savedkey = '%s' % savedFile
           #print("in first else second if")
           #print("NO Monster")
#           print(i)
#           print("file")
#           print(file)
#           print("savedFile")
#           print(savedFile)
           monster= savedMonster
           monsDict[savedkey] = savedMonster
          
        else:
            
            savedFile=file
            savedkey = '%s' % savedFile
            trackspec = makeTrackspec('l', file,directory) 
            fcframe,newMonster = makeTrackMonster(trackspec, featurespec)  
            
            #print("in second else")
            #print("Call monster2")
            #print(i)
            #print("file")
            #print(file)
            savedMonster=newMonster
            monster=newMonster
            monsDict[savedkey] = savedMonster
                    
      #save as .mat                 
    savemonsmat='monster' + lang 
    #scipy.io.savemat(savemonsmat, {savemonsmat: monsDict})
    #hdf5storage.write(monsDict, '.', savemonsmat, matlab_compatible=True)
    #'appendmat' appends'.mat' extension,truncate_existing=False appends to existing else overwrites 
    # can store in version >=7.3, needed for large .mat files
    hdf5storage.savemat(savemonsmat, monsDict,appendmat=True,format='7.3',truncate_existing=False)
    

   #save as pickle- inbuilt python library to persist variables between sessions                
#    savemons='monster' + lang +'.pkl'
    #for appending in existing pickle file,doesnot work
#    if os.path.exists(savemons):
#        with open(savemons, 'rb') as infile:
#          savemonsDict = pickle.load(infile)
#        savemonsDict.append(monsDict)
#    else:
#         with open(savemons, 'wb') as outfile:
#          pickle.dump([monsDict],outfile, protocol=3)

    return monster

    # test with
        # cd ppm / testeng or small - turkish etc.
#segData= prosodizeCorpus('../testeng/audio/', '../testeng/annotations/', getfeaturespec('../testeng/featurefile/mono4.fss'), 100,'E')
#pr = cProfile.Profile()
#pr.enable()
#segData= prosodizeCorpus('C:/ANINDITA/EnglishDataset/Audio/converted/', 'C:/ANINDITA/EnglishDataset/Annotations/TRAIN/1st3/', getfeaturespec('../testeng/featurefile/mono4.fss'), 100,'E')
#pr.disable()
#s = io.StringIO()
#scaller=io.StringIO()
#sortby = 'tottime'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#pscaller = pstats.Stats(pr, stream=scaller).sort_stats(sortby)
#sys.stdout = open('profileProsodizeCorpus_callers.txt', 'w')
#pscaller.print_callers()
#print(scaller.getvalue())
#sys.stdout = open('profileProsodizeCorpus.txt', 'w')
#ps.print_stats()
#print(s.getvalue())
#segData= prosodizeCorpus('../../mandarin/7audio/', '../../mandarin/7audio/annotations/', getfeaturespec('../testeng/featurefile/mono4.fss'), 100)
#print(segData)






