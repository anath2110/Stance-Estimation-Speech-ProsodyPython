# -*- coding: utf-8 -*-
"""
Created on Thur Dec 14 13:30:49 2017

@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso"""


import numpy as np
#import collections
#import pandas as pd
from makeTrackSpecs import makeTrackspec
#import numbers
import math
import scipy
from makeTrackMonster import makeTrackMonster
from getSegInfo import getSegInfo
from getfeaturespec import getfeaturespec
import segDataObject as clssegobj
def prosodizeCorpus(audioDir, annotDir, featurespec, stride):
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
    starts, ends, aufiles = getSegInfo(audioDir, annotDir)
    nsegments = len(starts)
    #print(nsegments)
    segData=[]   
    for i in range(nsegments):    
        segData.append(clssegobj.segDataObj(i,aufiles[i], starts[i], ends[i],featurespec, audioDir, stride))     
      
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
def featuresForSegment(i,aufile, startTime, endTime, featurespec, audioDir, stride):
    # aufile = char(aufile)
    monster = findTrackMonster(i,aufile, audioDir, featurespec)
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

def findTrackMonster(i,base, directory, featurespec):
    global savedFile
    global savedMonster
   
    
    
    base=base.decode('UTF-8')
    file = base +'.au'
     
    if (i==0): 
        savedFile=file
        trackspec = makeTrackspec('l', file,directory) 
        fcframe,newMonster = makeTrackMonster(trackspec, featurespec)  
        savedMonster=newMonster
        monster=newMonster
    else:
        if(savedFile==file):
           monster= savedMonster  
        else:
            trackspec = makeTrackspec('l', file,directory) 
            fcframe,newMonster = makeTrackMonster(trackspec, featurespec)  
            savedMonster=newMonster
            monster=newMonster 
    #scipy.io.savemat('savedmon.mat', {'savedmon': savedMonster})

    return monster

    # test with
        # cd ppm / testeng or small - turkish etc.
#segData= prosodizeCorpus('stance-master/testeng/audio/', 'stance-master/testeng/annotations/', getfeaturespec('stance-master/src/mono4.fss'), 100)
#print(segData)
#np.set_printoptions(threshold=np.inf)





