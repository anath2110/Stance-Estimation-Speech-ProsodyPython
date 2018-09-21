# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:59:03 2018

@author: Anindita Nath
University of Texas at El Paso
"""
import numpy as np
import warnings
from predEval_noAnnoAPI import predict
from makePPM import makePPM
warnings.filterwarnings("ignore")

def noAnnoAPI(audiodir,ppmfile_location,pyop_predictionsfile,lang,**kwargs):
    predictions=predict(audiodir,ppmfile_location,lang,**kwargs)
    # save the predicitons in  a text file
    np.savetxt(pyop_predictionsfile,predictions,fmt='%.1f',delimiter=', ')
    print("Successful")
  


#test
# if you want to create your own ppm model, uncomment the following line
#model= makePPM('C:/ANINDITA/EnglishDataset/Audio/converted/', 'C:/ANINDITA/EnglishDataset/Annotations/TRAIN/', '../testeng/featurefile/mono4.fss', 'ppmEngpy',lang='E')

# Uncomment the following line to get stance predictions wihtout the annotations
noAnnoAPI('../testAudio/','../test_ppmmodel_English/ppmEngpy','pypredictions_noAnno.txt',lang='E',startSec=[0,10,43],endSec=[10,43,0])# 2 optional arguments

#noAnnoAPI('../newNoAnnoAPI/testAudio/','../newNoAnnoAPI/test_ppmmodel_English/ppmEngpy','pypredictions_noAnno.txt',lang='E',startSec=[0,10],endSec=[10,0]) 

#noAnnoAPI('../testAudio/','ppm_noAnno_Eng.mat','pypredictions_noAnno.txt',lang='E')# 0 optional argument, entire audio as 1 segment
#noAnnoAPI('../testAudio/','ppm_noAnno_Eng.mat','pypredictions_noAnno.txt',lang='E',endSec=[150])# 1 optional argument, 5 secs from start
#noAnnoAPI('../testAudio/','ppm_noAnno_Eng.mat','pypredictions_noAnno.txt',lang='E', startSec=[8])# 1 optional argument,8 secs to the auido to end
