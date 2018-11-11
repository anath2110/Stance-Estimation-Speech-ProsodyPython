# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 17:03:00 2017

@author: Anindita Nath
University of Texas at ElPaso
"""


import numpy as np
#import collections
#import pandas as pd
import hdf5storage
from makeTrackSpecs import makeTrackspec
from getAudioInfo_noAnnoAPI import getAudioInfo
#import numbers
import math
#import scipy
import os
from makeTrackMonster import makeTrackMonster
#from getSegInfo import getSegInfo
#from getfeaturespec import getfeaturespec
import segDataObject_noAnnoAPI as clssegobj
def prosodizeCorpus(audioDir,featurespec, stride,lang,fssfile,**kwargs):
    # translated and modified from original by Nigel Ward, UTEP, June 2017
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
        
    # for an audio with no annotations 
    
    starts, ends, aufiles = getAudioInfo(audioDir,**kwargs)
    
    
    print('in prosodize corpus')
    nsegments = len(starts)
    print('nsegments %d' %nsegments)
    segData=[]  
  
    for i in range(nsegments): 
        
        print('in segment =%d' %i)
        print('auname=%s' %aufiles[i])
        segData.append(clssegobj.segDataObj(i,aufiles[i], starts[i], ends[i],featurespec, audioDir, stride,lang,nsegments,fssfile))     
          
        
   
        
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
def featuresForSegment(i,aufile, startTime, endTime, featurespec, audioDir, stride,lang,nsegments,fssfile):
    # aufile = char(aufile)
    monster = findTrackMonster(i,aufile, audioDir, featurespec,lang,nsegments,fssfile)
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

def findTrackMonster(i,base, directory, featurespec,lang,nsegments,fssfile):
   #print(i)
    global savedMonsters
    #global savedkeyindex
    
    #base=base.decode('UTF-8') # it otherwise appears in byte form, with a 'b' prefixed at front
    #file = base +'.au' #if its already string, previous line throws error    
    file = base # no need to add .au since audio name is directly retrieved from 
                #audio itself and not annotations, so name already has extensions
#if the monster exists and it is made of same featurefile and \
#same audios, just load the .mat and read values
    savemonsmat='monster' + lang # name of the .mat file
    
    if(os.path.exists(savemonsmat + '.mat')):
       #print("reading saved monster")
       monstermat=hdf5storage.loadmat(savemonsmat)
       featurefilename=monstermat['featurefilename'] 
       if(featurefilename==fssfile):
             #print("featurefile matched")
             if(file in list(monstermat.keys())):                  
                 #print("audio matched with key")
                 #savedkeyindex=file
                 monster=monstermat[file]                
                 
                 return monster
                 
             else:
                #print(i)
                if (i==0):   
                    savedMonsters = {}# to save the monster features\
                                      # with corresponding audioname in this dictionary 
                    trackspec = makeTrackspec('l', file,directory) 
                    # monster called
                    #print('monster called')
                    fcframe,newMonster = makeTrackMonster(trackspec, featurespec) 
                    monstDictkey = '%s' % file  
                    savedMonsters[monstDictkey] = newMonster                             
                    monster=newMonster       
            
                else:        
                    keys=list(savedMonsters.keys()) 
                    index=len(savedMonsters)-1
                    if file==keys[index]:
                                #print('filename' + ' ' + file)
                                #print('key' + ' ' + keys[index])
                                #print('filename same as key name as saved file')
                                monster = savedMonsters[keys[index]]                 
                    else:
                            trackspec = makeTrackspec('l', file,directory) 
                            # monster called
                            #print('monster called when dict not empty')
                            fcframe,newMonster = makeTrackMonster(trackspec, featurespec) 
                            monstDictkey = '%s' % file  
                            savedMonsters[monstDictkey] = newMonster                             
                            monster=newMonster 
                   
       
                if(i==(nsegments-1)):
                #save as .mat  
                    #print('saving in .mat')               
                    #savemonsmat='monster' + lang # name of the .mat file 
                    #scipy.io.savemat(savemonsmat, {savemonsmat: savedMonsters})
                    #'appendmat' appends'.mat' extension,truncate_existing=False appends to existing else overwrites 
                    # can store in version >=7.3, needed for large .mat files
                    hdf5storage.savemat(savemonsmat, savedMonsters,appendmat=True,format='7.3',truncate_existing=False)
                        
    else:            
   
        if (i==0):  
            savedMonsters={}
            savedMonsters[u'featurefilename']=fssfile  
          # to save the monster features\
                              # with corresponding audioname in this dictionary 
            trackspec = makeTrackspec('l', file,directory) 
            # monster called
            #print('monster called')
            fcframe,newMonster = makeTrackMonster(trackspec, featurespec) 
            monstDictkey = '%s' % file  
            savedMonsters[monstDictkey] = newMonster                             
            monster=newMonster       
            
        else:        
            keys=list(savedMonsters.keys()) 
            index=len(savedMonsters)-1
            if file==keys[index]:
                        #print('filename' + ' ' + file)
                        #print('key' + ' ' + keys[index])
                        #print('filename same as key name as saved file')
                        monster = savedMonsters[keys[index]]                 
            else:
                    trackspec = makeTrackspec('l', file,directory) 
                    # monster called
                    #print('monster called when dict not empty')
                    fcframe,newMonster = makeTrackMonster(trackspec, featurespec) 
                    monstDictkey = '%s' % file  
                    savedMonsters[monstDictkey] = newMonster                             
                    monster=newMonster 
                   
       
        if(i==(nsegments-1)): # save only once when you reach the last index, one short of length in python
        #save as .mat  
            #print('saving in .mat')               
            #savemonsmat='monster' + lang # name of the .mat file 
            #scipy.io.savemat(savemonsmat, {savemonsmat: savedMonsters})
            #'appendmat' appends'.mat' extension,truncate_existing=False appends to existing else overwrites 
            # can store in version >=7.3, needed for large .mat files
            hdf5storage.savemat(savemonsmat, savedMonsters,appendmat=True,format='7.3',truncate_existing=False)
                
        
        #save as pickle- inbuilt python library to persist variables between sessions    
                
            #savemons='monster' + lang +'.pkl'
            #for appending in existing pickle file,doesnot work
    #        if os.path.exists(savemons):
    #            with open(savemons, 'rb') as infile:
    #              savemonsDict = pickle.load(infile)
    #            savemonsDict.append(savedMonsters)
    #        else:
    #        with open(savemons, 'wb') as outfile:
    #          pickle.dump([savedMonsters],outfile, protocol=3)
   
    return monster






