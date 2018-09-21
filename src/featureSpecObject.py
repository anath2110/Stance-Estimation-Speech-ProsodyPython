# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:24:44 2017

@author:Anindita Nath 
        University of Texas at ElPaso
"""
'''Function to create feature-spec objects from .fss files  in getfeaturespec.py'''

class featureSpecObj(object):

    def __init__(self, *args):        
                        
            self.featname=args[0]
            self.startms =args[1]
            self.endms =args[2] 
            self.duration =args[3]    
            self.side =args[4] 
            self.plotcolor=args[5]
            self.abbrev =args[6] 
   
        
       
