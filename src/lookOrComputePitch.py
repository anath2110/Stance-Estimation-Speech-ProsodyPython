# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:54:04 2017
modified on Mon Feb 19 13:00:12 2018
@author: Anindita Nath
University ofTexas at El Paso
"""
from __future__ import unicode_literals
from datetime import datetime
#import pickle
import _pickle as pickle
import os.path
import numpy as np
import scipy
import scipy.io as sio
from pathlib import Path
#import amfm_decompy.pYAAPT as pYAAPT
import amfm_decompy.pYAAPT_MATLABver as pYAAPT
#import amfm_decompy.basic_tools as basic
import readau_structobject as austruct

def  lookupOrComputePitch(directory,audio,side,signal):    

#Savekey encodes the audio filename and the track.
#If a cached pitch file exists, then use that data 
#otherwise compute pitch and save it 
#Return a vector of pitch points and a vector of where they are, in ms

    
    savekey=audio + side
    pitchCacheDir = directory + 'pitchCachePython'
    
    if not os.path.exists(pitchCacheDir):
        os.makedirs(pitchCacheDir)  
   
    #pitchFileName = pitchCacheDir + '/pitchpython' + savekey + '.mat'
    
    #name the pickle file
    pitchFileName = pitchCacheDir + '/pitchpython' + savekey + '.pkl'
    if (Path(pitchFileName).is_file()==False):
        
    # pitch mat file doe not exist   
      print('computing pitch for ' + savekey)
     
      #signal = basic.SignalObj(directory + audio)
      #signal = austruct.SignalObj(directory + audio)
      if (signal.channels==2): # if a stereo
          if(side=='l'):# take signal values of left track 
              signal.data=signal.data[:,0]
          elif(side=='r'):# take signal values of right track 
              signal.data=signal.data[:,1]
      #scipy.io.savemat(pitchCacheDir + '/signal_pyyaapt', {'signal_pyaapt': signal}) 
      # saving signal values in .mat, not need - memory burden
      #sio.savemat(pitchCacheDir + '/signal_pyyaapt', {'signal_pyaapt': signal}) 
      pitch = pYAAPT.yaapt(signal)
      pitchvals=pitch.samp_values
      #print(pitchvals.shape)
      pitch_centres = pitch.frames_pos
      time_stamp_in_seconds = pitch_centres/signal.fs #by mspeframe, matlab compatibility
         
      
       # save as .mat        
#      scipy.io.savemat(pitchFileName, {'pitchpy': pitch,'pitchsamples': pitchvals,\
#      'pitch_centres': pitch_centres,'time_stamp_in_seconds': time_stamp_in_seconds})  
      #save as pickle file
      with open(pitchFileName, 'wb') as outfile:
          #pickle.dump([pitchvals,pitch_centres,time_stamp_in_seconds],outfile, pickle.HIGHEST_PROTOCOL)
          pickle.dump([pitchvals,pitch_centres,time_stamp_in_seconds],outfile, protocol=2)
    
    else:
      if file1isOlder(pitchFileName, directory + audio):    
        print('recomputing pitch for' +  savekey)
        #signal = austruct.SignalObj(directory + audio)
        if (signal.channels==2): # if a stereo
          if(side=='l'):# take signal values of left track 
              signal.data=signal.data[:,0]
          elif(side=='r'):# take signal values of right track 
              signal.data=signal.data[:,1]
        # saving signal values in .mat, not need - memory burden
        #scipy.io.savemat(pitchCacheDir + '/signal_pyyaapt', {'signal_pyaapt': signal}) 
        pitch = pYAAPT.yaapt(signal)
        pitchvals=pitch.samp_values
        pitch_centres = pitch.frames_pos
        time_stamp_in_seconds = pitch_centres/signal.fs #by mspeframe, matlab compatibility
        
        # save as .mat  
#        scipy.io.savemat(pitchFileName, {'pitchpy': pitch,'pitchsamples': pitchvals,\
#        'pitch_centres': pitch_centres,'time_stamp_in_seconds': time_stamp_in_seconds}) 
      
      #save as pickle file
        with open(pitchFileName, 'wb') as outfile:
          #pickle.dump([pitchvals,pitch_centres],outfile, pickle.HIGHEST_PROTOCOL)
          pickle.dump([pitchvals,pitch_centres,time_stamp_in_seconds],outfile, protocol=2)
    

      else: 
        print('reading cached pitch file '+ pitchFileName)
        #read .mat files
#        pitchpy=scipy.io.loadmat(pitchFileName)
#        pitchsamples=pitchpy['pitchsamples'] 
#        pitch_centres = pitchpy['pitch_centres']   
#        print(pitchsamples.shape)   
        with open(pitchFileName, 'rb') as f:
            pitch = pickle.load(f)
            
        pitchvals = np.array(pitch[0])       
        pitch_centres = np.array(pitch[1])
    
    #msPerSample = 1000 / signal.fs
    #The first pitch point fxrapt returns is for a frame from 15ms to 25ms, 
    #thus centered at 20ms into the signal.
    #The last one is similarly short of the end of the audio file. 
    #So we pad. 
    
    paddedPitch = np.insert(pitchvals,0,np.nan)
    paddedPitch=np.append(paddedPitch,np.nan)
    
   # pitchCenters = 0.5 * (startsAndEnds[:,1] + startsAndEnds[:,2]) * msPerSample
    #we know that pitchpoints are 80 milliseconds apart
    paddedCenters = np.insert(pitch_centres,0,pitch_centres[0] - 80) 
    paddedCenters=np.append(paddedCenters,pitch_centres[len(pitch_centres)-1] + 80)
    
    # saving the padded ones in .mat- not needed,memory burden
    #scipy.io.savemat(pitchCacheDir + '/padded', {'padpitch': paddedPitch,'padcentre': paddedCenters})  
   
    return paddedPitch,paddedCenters
   


#------------------------------------------------------------------
def file1isOlder(file1, file2):
    try:
        file1time = os.path.getmtime(file1)
        #print(file1time)
        file2time = os.path.getmtime(file2)
        #print(file2time)
    except OSError:
        file1time = 0
        file2time = 0
        file1time = datetime.fromtimestamp(file1time)
        file2time = datetime.fromtimestamp(file2time)
        #print(file1time)
        #print(file2time)
  
    isOlder = file1time < file2time
    #print(isOlder)
    return isOlder


 #test with 
#signal = austruct.SignalObj('../testeng/audio/ChevLocalNewsJuly3.au')
#paddedPitch,paddedCenters=lookupOrComputePitch('../testeng/audio/','ChevLocalNewsJuly3.au','l',signal)
#print(paddedPitch.shape)
#paddedPitch,paddedCenters=lookupOrComputePitch('stance-master/testeng/audio/','f0a_01.au','l')