# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 15:53:10 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import numpy as np
def  computeCreakiness(pitch, windowSizeMs):

# Nigel Ward and Paola Gallardo, December 2014
# Looks for evidence of creak in effects on computed F0, in two ways: 
#  1. the presence of octave jumps and
#  2. the presence of other frame-to-frame pitch jumps (jitter). 
#pitch is a column vector; returns a column vector

    framesPerWindow = int(windowSizeMs / 10)
    
    ratios = np.divide(pitch[1:],pitch[:len(pitch)-1])
    np.set_printoptions(threshold=np.nan)
    #print(ratios)
   
    octaveUp = ((ratios > 1.90)) & ((ratios < 2.10))
    #print("octaveup")
    #print(octaveUp)
    octaveDown = ((ratios > .475)) & ((ratios < .525))
    #print("octavedown")
    #print(octaveDown)
    #enormous jumps are probably more due to noise than creaky voice
    smallUp = ((ratios > 1.05))  & ((ratios < 1.25))
    #print("smallup")
    #print(smallUp)
    smallDown = ((ratios <  .95)) & ((ratios > .80))
    #print("smallDown")
    #print(smallDown)
    creakiness = octaveUp + octaveDown + smallUp + smallDown
    #print("Creakiness")
    #print(creakiness.shape)
    #creakiness[1] is the creakiness centered at 15ms, 
    #since the first two pitch points are at 10 and 20 ms
    
    integralImage =np.insert(np.cumsum(creakiness),0,0)
    #print(integralImage.shape)
    creakinessPerWindow = np.subtract(integralImage[(framesPerWindow):],integralImage[:(len(integralImage)-framesPerWindow)])
    #print(creakinessPerWindow.shape)
    #print("creakinessPerWindow")
    #print(creakinessPerWindow)
    #pad it in front and at end 
    #if framesPerWindow is an even number, the first value returned is at 15ms
    #if odd, it's at 10ms
    headFramesToPad = int(np.ceil((framesPerWindow - 1) / 2))
    tailFramesToPad = int(np.ceil((framesPerWindow ) / 2))
    #print(headFramesToPad)
    #print(tailFramesToPad)
    
    creakArray=np.concatenate((np.zeros(headFramesToPad,),creakinessPerWindow,np.zeros(tailFramesToPad,)),axis=0)
    
    creakValues =  np.divide(creakArray,framesPerWindow)
   
    return creakValues
#!!!!!!!!!!!!!! should speaker-normalize, to exclude the effects of
#speaker-voice physiology etc, like this:
#creakValues = creakValues / avg(creakValues)


#test cases 
#y = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1.1,0.8,1.0,.9,1,1,1,1.01,1.02,1.01,2,1,2,1,.5,.5,.5,1,1,1,1])
##print(y.shape)
#creakValues=computeCreakiness(y, 50)
##creakValues=computeCreakiness(y, 30)
##creakValues=computeCreakiness(y, 100)
#print(creakValues)
