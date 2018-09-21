# -*- coding: utf-8 -*-
"""
Created on Thur Dec 14:25:44 2017

@author:Anindita Nath 
        University of Texas at ElPaso
"""
'''Function to create segData objects for prosodizecorpus'''

class segDataObj(object):

    def __init__(self, *args):
        
#            try:
         
        from prosodizeCorpus import featuresForSegment
        from prosodizeCorpus import addTemporalFeatures
#            except:
#            
#                print("ERROR: Functions required for segData couldnot be loaded")
#                raise KeyboardInterrupt
        
        self.features= addTemporalFeatures(featuresForSegment(*args),args[6])
        self.startTime = int(args[2])
        #print(self.startTime)
        self.endTime = int(args[3])
        self.broadcastName =args[1].decode('UTF-8') 
        #print( self.broadcastName)
        self.properties = ''
        
       
