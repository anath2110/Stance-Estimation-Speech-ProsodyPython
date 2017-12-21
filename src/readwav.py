# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 14:25:44 2017

@author:Anindita Nath 
        University of Texas at ElPaso
"""
import numpy as np
import wave

'''Function to read sound files with .wav extension'''

def readwav(audiofile):
    f=wave.Wave_read(audiofile)
    channels=f.getnchannels()
  
    rate=f.getframerate()
    #f.getparams()
    nframes=f.getnframes()
    audio_data = np.fromstring(f.readframes(nframes),dtype=np.int16)
    #np.set_printoptions(threshold=np.nan)
    #print(audio_data)
    #print(audio_data.shape)
    return audio_data,channels,rate


###Test###
#[audiodata,channels,rate]=readwav('2ndWeekendNewscastJuly292012.wav')
#np.set_printoptions(threshold=np.nan)
#print(channels,rate)



