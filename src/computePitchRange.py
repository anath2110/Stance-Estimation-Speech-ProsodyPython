# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 13:54:04 2017
@author: Anindita Nath
University ofTexas at El Paso
"""
import numpy as np
import scipy.io
import math
#import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.pYAAPT_MATLABver as pYAAPT
#import amfm_decompy.basic_tools as basic
import readau_structobject as austruct

def computePitchRange(pitch, windowSize,rangeType) :
#Calculates evidence for different types of pitch ranges
#i.e. f = flat   (within .99-1.0 difference)
#n = narrow (within .98-1.02 difference)
#w = wide   (within .70-.90 difference)
#
#The evidence is the number of pitch  neighbors which are in the desired
#relation to the centerpoint of the window.
#RelevantSpan is 1000 because being flat for more 1 second is probably rare,
#and increasing this value slows computation
#This feature peeks beyond the window boundaries, hence is inappropriate
#for online prediction

# converted from code by  Nigel Ward and Paola Gallardo, UTEP, February 2015

    #rangeCount =[]
    rangeCount = np.zeros(len(pitch))

    msPerWindow = 10
    framesPerWindow = int(windowSize/msPerWindow)
    relevantSpan = 1000
    framesPerHalfSpan = int(math.floor((relevantSpan / 2) / framesPerWindow))


    for i in range (len(pitch)):
        #get offset of 500 ms
        startNeighbors = i - framesPerHalfSpan
        endNeighbors = i + framesPerHalfSpan
        #control out of bounds
        if(startNeighbors < 1):
            startNeighbors = 1
        
        if(endNeighbors > len(pitch)):
            endNeighbors = len(pitch)-1
        
        
        #set of neighbors with pitch point in center
        #here we could take every other point, to save time, with probably
        #no performance penalty, since never changes much over just 10ms
        neighbors = pitch[startNeighbors:endNeighbors]
        #obtain evidence
        #print(neighbors)
        #print(pitch[i])
        ratios = neighbors/pitch[i]
        #based on ratio difference to center, count points with evidence
        #for specified pitch range
        if (rangeType=='f'):            
                 #does not seem to be usefully different from narrow
            #rangeCount.append( np.sum( np.any(ratios>=0.99) & np.any(ratios <=1.01)))
            rangeCount[i] = np.sum( (ratios>=0.99) & (ratios <=1.01))
        elif (rangeType=='n'):
             #rangeCount.append( np.sum( np.any(ratios>=0.98) & np.any(ratios <=1.02)))
         
            rangeCount[i] = np.sum((ratios>0.98) &(ratios<1.02))
        elif (rangeType=='w'):
                #if difference is <.70 or >1.3, most likely spurious pitch point
             #rangeCount.append( np.sum( np.any(ratios>=0.70) & np.any(ratios <=0.90)))
         
            rangeCount[i] = np.sum(((ratios>0.70) & (ratios<0.90))  | ((ratios >1.1) & (ratios<1.3)))
    
    rangeCount=np.asarray(rangeCount)
    ##same old trick of integral image
    integralImage = np.insert(np.cumsum(rangeCount),0,0)
   
    windowValues = integralImage[1+framesPerWindow:] - integralImage[:((len(integralImage)-1)-framesPerWindow)]
   
    paddingNeeded = framesPerWindow - 1
   
    # frontPadding = np.zeros(math.floor(paddingNeeded / 2))
    # tailPadding = np.zeros(math.ceil(paddingNeeded / 2))
    # ranges = np.concatenate((frontPadding, windowValues))
    # ranges=np.concatenate((ranges, tailPadding))
    ranges = np.zeros(math.floor(paddingNeeded / 2)+math.ceil(paddingNeeded / 2)+windowValues.shape[0])
    ranges[math.floor(paddingNeeded / 2):math.floor(paddingNeeded / 2)+windowValues.shape[0]]= windowValues

    ranges = ranges / framesPerWindow
    return ranges

##test cases
#signal = austruct.SignalObj('../testeng/audio/ChevLocalNewsJuly3.au')
#scipy.io.savemat('signalpy.mat', {'signalpy':signal})
#print(signal.data.shape)
#print(signal.channels)
#print(signal.fs)
#pitch = pYAAPT.yaapt(signal)
#scipy.io.savemat('pitchpy.mat', {'pitchpy':pitch})
#print(pitch.samp_values.shape)
#ranges= computePitchRange(pitch.samp_values,100,'w')
#scipy.io.savemat('compPitchRangepy.mat', {'rangespy':ranges})
#np.set_printoptions(threshold=np.nan)
#print(ranges)

#print(ranges.shape)

