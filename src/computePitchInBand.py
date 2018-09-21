# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:30:49 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import numpy as np
def computePitchInBand(percentiles, bandFlag, windowSizeMs):
    
    np.set_printoptions(threshold=np.nan)
#    compute evidence for the pitch being strongly in the specified band
#    bandflag 'l' is low pitch; 'h' is high pitch
#    'tl' and 'th' are "truly high" and "truly low", mosre strictly
#    in future, may have a mid-range band, etc. 
#    both percentils and bandValues are column vectors
    
    #converted from original by Nigel Ward February 2015
    
    #despite the name, percentiles is a vector of values from 0 to 1
    #with some NaNs mixed in.  As produced by percentalizePitch.m
    
    if bandFlag=='h':    
      #for computing evidence for high pitch, NaNs contribute nothing, same as 0s
      percentiles[np.isnan(percentiles)]=0.00
      evidenceVector = percentiles
    elif bandFlag=='l':   
      #for computing evidence for low pitch, NaNs contribute nothing, same as 1s
      percentiles[np.isnan(percentiles)]=1.00
      evidenceVector = 1 - percentiles  # the lower the pitch value, the more evidence
    elif bandFlag=='th':     
      #50th percentile counts a tiny bit "truly-high", below 50th percentile, not at all
      percentiles[np.isnan(percentiles)]=0.00
      percentiles[percentiles < 0.50] = 0.50
      evidenceVector = percentiles - 0.50
    elif bandFlag=='tl' :    
      #49th percentile counts a tiny bit "truly-low", above 50th percentile, not at all
      percentiles[np.isnan(percentiles)]=1.00
      percentiles[percentiles > 0.50]= 0.50
      evidenceVector = 0.50 - percentiles
    else:
      print('sorrry, unknown flag' + bandFlag); 
    
    
    integralImage =np.insert(np.cumsum(evidenceVector),0,0)
    framesPerWindow = int(windowSizeMs / 10)
    windowValues = np.subtract(integralImage[(framesPerWindow):],integralImage[:(len(integralImage)-framesPerWindow)])

    #add more padding to the front.
    #if framesPerWindow is even, this means the first value will be at 15ms
    #otherwise it will be at 10ms 
    paddingNeeded = framesPerWindow - 1
    frontPadding = np.zeros(int(np.floor(paddingNeeded / 2)),)
    tailPadding = np.zeros(int(np.ceil(paddingNeeded / 2)),)
    bandValues=np.concatenate((frontPadding,windowValues,tailPadding),axis=0)
    #now normalize, just so that when we plot them, the ones with longer windows are
    #not hugely higher than the rest
    bandValues = np.divide(bandValues,framesPerWindow)
    return bandValues

#pitchHighness test cases
#bandvalues=computePitchInBand(np.array([0, 0, 0, 0,np.nan,0,0,0,0,0,0,0.01]),'h', 90) #near zero
#bandvalues=computePitchInBand([ 1 1 1 .9 NaN .8 Nan Nan Nan Nan],'h', 90) % near one
#bandvalues=computePitchInBand([ 1 1 1 .9 NaN .8 .6 .5 .4 .6 ],   'h', 90) % nearer one
#bandvalues=computePitchInBand([ 1 1 1 .9 NaN .8 .9 1.0 .95 .95 ],'h', 90) % even nearer one
#
#pitchLowness test cases
#bandvalues=computePitchInBand([ 0 0 0 0 NaN 0 0 0 0 0 0 0.01],'l', 90)     % near one
#bandvalues=computePitchInBand([ 1 1 1 .9 NaN .8 .9 1.0 .95 .95 ],'l', 90)  % very near zero
#bandvalues=computePitchInBand([ 1 1 1 .9 NaN .8 Nan Nan Nan Nan ],'l', 90) % about the same
#bandvalues=computePitchInBand([ .5 .5 .5 .9 NaN .2 .6 .5 .4 .6 ],'l', 90)  % near .5
#bandvalues=computePitchInBand([ .5 .5 .5 .8 NaN .2 .6 .5 .4 .5 ],'l', 90)   % a little higher

#print(bandvalues)
