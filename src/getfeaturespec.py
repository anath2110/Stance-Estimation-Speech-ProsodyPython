# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:21:46 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import numpy as np
import scipy
import os
from collections import namedtuple
import featureSpecObject as featureobj
def  getfeaturespec(crunchspec):
    # from the crunchspec (features set specification file), 
    #parse out the descriptions of what features we need
    #and return that information as an array of structs
    
    # converted from the original code by Nigel Ward, 2014
    
    #test with 'toyFiles/dummyCrunchSpec.fs'
    #and with  'crunchspec.fs'
    np.set_printoptions(threshold=np.nan)
    validFeatures = np.array(['vo', 'ph', 'pr', 'sr', 'lp', 'hp', 'cr', 'fp',
    'np', 'wp', 'tl', 'th', 'vf', 'sf', 're', 'en', 'le', 'pd', 'le', 'vr','ts', \
    'te', 'ns', 'ne', 'rf', 'mi', 'ju', 'go', 'gf', 'ga', 'gl', 'gr', 'gu', 'gd'])
    #print(validFeatures)
    #vo = intensity (volume)
    #
    #vf = voicing fraction
    #sf = speaking fraction 
    #
    #ph = (old) pitch height
    #lp = low pitch 
    #hp = high pitch 
    #tl = truly-low pitch 
    #th = truly-high pitch 
    #cr = creaky
    #pr = (old) pitch range 
    #fp = flat pitch
    #np = narrow pitch 
    #wp = wide pitch 
    #
    #re = cepstral blandness (articulatory reduction)
    #en = cepstral distinctiveness (articulatory precision, enunciation)
    #le = lengthening
    #pd = peak disalignment
    #vr = voiced-unvoiced intensity ratio
    #
    #ts = time since start of recording
    #te = time until end of recording 
    #
    #rf = running fraction
    #mi = motion initiation count
    #ju = jump count 
    #
    #go = gaze on or off (boolean)
    #gu = gaze up
    #gd = gaze down
    #gl = gaze left
    #gr = gaze right
    #gf = gaze face  % old
    #ga = gaze awayness (distance)    
    
    print('reading' +  crunchspec)
    if os.path.isfile(crunchspec): # if the file exists
        
        with open(crunchspec,"r") as fid:# open in read mode
            flist=[]
            flag=0
            for tline in fid:
                #print (tline)
               
                if(~tline.isdigit()):
                   if tline.isspace():
                       #print("Empty")#is an empty or whitespace-only line, so skip it
                       pass
                   elif tline[0] == '#': # is a comment line, so skip it
                       #print("Comment")
                       pass                        
                   else:
                        
                        #process the line, painfully, because strread is uncooperative 
                        fields = tline.split( ) # split the whitspaces  
                        #print(fields)
                        featurecell = fields[0]
                        #print(featurecell)
                        #validatestring(feat, validFeatures, 'getfeaturespec', tline)
                        for i,elt in enumerate(validFeatures):
                            if(elt==featurecell):
                                flag=flag+1
                        if flag>0:
                            startms = int(fields[1])                     
                            endms = int(fields[3])
                            sidecell = fields[4]#'self' or 'inte' 
                            plotcolor = 0  # default is not to plot it 
                            if len(fields) > 5:
                                 colorstring  = fields[5]                           
                                 if(colorstring!="#"): # it's not a comment
                                  plotcolor = colorstring   # must be 'k', 'm', 'b', 'c', 'g', 'r', etc.
                            
                            duration = endms - startms
                            if (duration < 0 or duration > 10000):
                                print('strange duration %d in getfeaturespec; check file format', duration)
                            #print(duration)                                                                 
                            
                            if (startms >= 0):
                                startcode = '+' + str(startms)
                            else:		    
                                startcode = str(startms)
                         
                            if (endms >= 0):
                                endcode = '+' + str(endms)
                            else:		    
                                endcode = str(endms)
                            #for example se-vo-100-50 or in-vo+100+200
                            abbrev =  sidecell[:2] + ' ' + featurecell + ' ' + startcode + ' ' + endcode                        
                            #fliststruct = namedtuple('fliststruct', 'featname startms endms duration side plotcolor abbrev')
                            #fs=fliststruct(featurecell,startms,endms,duration,sidecell,plotcolor,abbrev)
                            #flist.append(fs) 
                            flist.append(featureobj.featureSpecObj(featurecell,startms,endms,duration,sidecell,plotcolor,abbrev)) 
           
    else:    
        print('Feature file doesnot exist' + crunchspec)   
    fid.close()
    return flist

#flist=getfeaturespec('../testeng/featurefile/mono4.fss')
#print(flist)

#durationlist=[]
###print(len(flist))
#for fs in range(len(flist)):
#  durationlist.append(flist[fs].duration)
#durationlist=np.asarray(durationlist)
#scipy.io.savemat('featurespec.mat', {'flistpy': flist})
#fs=scipy.io.loadmat('featurespec.mat')
#fsob=fs['flistpy']

#print(fsob.shape)
