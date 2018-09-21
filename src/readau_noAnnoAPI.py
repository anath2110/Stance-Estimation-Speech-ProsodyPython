# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 14:25:44 2017

@author:Anindita Nath 
        University of Texas at ElPaso
"""
'''Function to read sound files with .au extension'''
import numpy as np
import socket
import sys
import sunau
import scipy
#import scikits.audiolab as al
#print (sys.byteorder)
def readau(audiofile):
    #print('audioname in  readau')
    #print(audiofile)
    f=sunau.Au_read(audiofile)
      
    channels=f.getnchannels()
    #print('channels in readau')
    #print(channels)
    rate=f.getframerate()
    #f.getparams()
    nframes=f.getnframes()
    duration=np.float32(nframes/rate)
    audio_databyte = f.readframes(nframes)
    #print(type(audio_databyte))
    #print(len(audio_databyte))
    #print(nframes)
    #print(channels)
    #audio_data=int.from_bytes(audio_databyte, byteorder='little', signed=True)
    #print(audio_databyte[:10])
    
    #audio_data=int.from_bytes(audio_databyte[:2], byteorder='little', signed=True)
    if(channels==2):
        audio_bytearray = np.ndarray(shape=(nframes,channels),dtype='<i2', buffer=audio_databyte)   
        audio_bytearraybigendian = np.ndarray(shape=(nframes,channels),dtype='>i2', buffer=audio_databyte) # works same as matlab
    
    elif(channels==1):
        audio_bytearray = np.ndarray(shape=(nframes,),dtype='<i2', buffer=audio_databyte)   
        audio_bytearraybigendian = np.ndarray(shape=(nframes,),dtype='>i2', buffer=audio_databyte) # works same as matlab
    
    audio_bytearray_swap=audio_bytearray.byteswap() # works with above same as matlab
    #audio_bytearraybigendian_swap=audio_bytearraybigendian.byteswap()
    #audio_data = np.fromstring(audio_databyte[:10],dtype=np.int16)
    #out_hex = ['{:02X}'.format(b) for b in audio_databyte[:2]]
    #print(out_hex)
    #for i in range(len(out_hex)) :
    #audiosckt=socket.htons(audio_data)
    #print(audiosckt)
   #audio_data = np.fromstring(audio_databyte[:10],dtype=np.dtype('b'))
   #audio_data = np.fromstring(f.readframes(nframes))
    #audio_data,  fs,  enc  =  al.auread(audiofile)
    #np.set_printoptions(threshold=np.nan)
    #print(audio_bytearray.shape)
    #print(audio_data.shape)
    #scipy.io.savemat('audio_channels.mat', {'audio_data': audio_data})
    #scipy.io.savemat('audio_bytearray.mat', {'audio_bytearray': audio_bytearray})
    #scipy.io.savemat('audio_bytearraybigendian.mat', {'audio_bytearraybigendian': audio_bytearraybigendian})
    #scipy.io.savemat('audio_bytearray_swap.mat', {'audio_bytearray_swap': audio_bytearray_swap})
    #scipy.io.savemat('audio_bytearraybigendian_swap.mat', {'audio_bytearraybigendian_swap': audio_bytearraybigendian_swap})
   
    return rate,audio_bytearraybigendian,channels,duration


###Test###
#rate,audio_bytearraybigendian=readau('2ndWeekendNewscastJuly292012.au')
#rate,audio_bytearraybigendian,channels=readau('f0a_01.au')
#np.set_printoptions(threshold=np.nan)
##print(channels)
#print(audio_bytearraybigendian.shape)
