# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 17:46:50 2018

@author: Anindita Nath
University of Texas at ElPaso
"""
import warnings
import os
import sys
import numpy as np
from readau_noAnnoAPI import readau

def getAudioInfo(audioDir,**kwargs):
     # kwargs is a dict of the keyword (optional) args passed to the function
     # can be assigned None, empty or multiple during call
    #print(audioDir)
    starts=[]
    ends=[]
    aufiles=[]
    for path,dirs,files in os.walk(audioDir):       
        #print(files)
        for filename in files:
            #print(filename)
            #if(os.path.exists(audioDir+filename)==True):  # check to see audio exists in the directorypath \
            if filename.endswith(".au"):                                          #else error since tries to read .mat files of the pitchCache       
                audiopath= os.path.join(path,filename)
                #print(audiopath)
                #print(filename)
                _,_,_,duration=readau(audiopath)
                #print(duration)
                
                # if both the start and end timestamps are missing from optional,\ 
                #entire audio as 1 segment
                if("startSec" not in kwargs and "endSec" not in kwargs ):
                     starts.append([0])
                     ends.append(duration)
                     aufiles.append(filename)
                else:
                  # check individually if any 1 of the optional arguments present
                    if("startSec" in kwargs and "endSec" not in kwargs ):                       
                        ends.append(duration)
                        
                        if(all(i >= 0 for i in kwargs['startSec'])):
                            starts.append(kwargs['startSec'])
                        else:
                            print("Start timeStamp invalid")
                            #starts.append(0.00)
                            sys.exit()
                        aufiles.append(filename)
                        repeatau=len(kwargs['startSec'])
                        aufiles = [item for item in aufiles for i in range(repeatau)]
                                      
                    elif("endSec" in kwargs and "startSec" not in kwargs ):
                        starts.append([0])
                        if(all(i <=duration for i in kwargs['endSec'])):
                            ends.append(kwargs['endSec'])
                        else:
                            print("End timeStamp invalid")
                            #ends.append(duration)
                            sys.exit()
                        aufiles.append(filename)
                        repeatau=len(kwargs['endSec'])
                        aufiles = [item for item in aufiles for i in range(repeatau)]
                          
                          
                    else:
                         #print("Both given")
                         if(all(i >= 0 for i in kwargs['startSec'])):
                            starts.append(kwargs['startSec'])
                         else:
                            print("Start timeStamp invalid")
                            #starts.append(0.00)
                            sys.exit()
                         if(all(i <=duration for i in kwargs['endSec'])):
                            ends.append(kwargs['endSec'])
                         else:
                            print("End timeStamp invalid")
                            #ends.append(duration)
                            sys.exit()
                         
                         aufiles.append(filename)
                         repeatau=len(kwargs['startSec'])
                         aufiles = [item for item in aufiles for i in range(repeatau)]
                          
                        
                
            else:
                warnings.warn("No such audio file in the directory")
              
  
    #starts=np.unique(starts)
    starts=np.array(starts)
    starts=starts.flatten()
    ends=np.array(ends)
    ends=ends.flatten()
    #ends=np.unique(ends)
    aufiles=np.asarray(aufiles)
#    print(starts)
#    print(ends)
#    print(aufiles)
    return starts,ends,aufiles
        