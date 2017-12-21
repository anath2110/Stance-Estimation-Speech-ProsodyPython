# -*- coding: utf-8 -*-
"""
Created on Tue Nov 7 14:25:44 2017

@author:Anindita Nath 
        University of Texas at ElPaso
"""
'''Function to create sound file objects'''

class SignalObj(object):

    def __init__(self, *args):

        if len(args) == 1:
            try:
               # from scipy.io import wavfile
               from readau import readau
            except:
                #print("ERROR: Wav modules could not loaded!")
                print("ERROR: Au modules could not loaded!")
                raise KeyboardInterrupt
            self.fs, self.data,self.channels = readau(args[0])
            self.fs = float(self.fs)
            self.nbits = int(16)         
            self.name = args[0]
        elif len(args) == 2:
            self.data = args[0]
            self.fs = args[1]

        self.size = len(self.data)
#
#        if self.size == self.data.size/2:
#            print("Warning: stereo au file. Converting it to mono for the analysis.")
#            self.data = (self.data[:,0]+self.data[:,1])/2

