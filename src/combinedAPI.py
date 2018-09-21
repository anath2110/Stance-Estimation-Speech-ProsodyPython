# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 17:03:20 2018

@author: Anindita Nath
"""
import warnings
import time
import cProfile, pstats, io
import sys
from regressionTest import regressionTest
from makePPM import makePPM
# following line ensures run time warnings donot print on standard output
# else code's run time is rendered slow
warnings.filterwarnings("ignore")
#audio language 
language=input("Enter the Language Abbreviation,'E' for English, 'M' for Mandarin and 'T' for Turkish: ") 

#following does the profiling of the code 
pr = cProfile.Profile()
pr.enable()
startc=time.time()#timer starts to create ppmfile
## all the standard outpt while creating the ppmfile is saved in \
##the following text file
sys.stdout = open('ppm' + language +'.txt', 'w') 
print('creating the model')
#
##following are the various instances for creating ppmfiles corresponding to different languages
#
#model= makePPM('../../EnglishDataset/Audio/converted/', '../../EnglishDataset/Annotations/TRAIN/', '../testeng/featurefile/mono4.fss', 'ppmEngpy',lang=language)
model= makePPM('../../EnglishDataset/Audio/converted/', '../../EnglishDataset/Annotations/', '../testeng/featurefile/mono4.fss', 'ppmEngpy',lang=language)
#model= makePPM('../../mandarin/audio/', '../../mandarin/trainAnnotationsCSV/', '../testeng/featurefile/mono4.fss', 'ppmMan',lang=language)
#model= makePPM('../../mandarin/audio/', '../../mandarin/annotations/', '../testeng/featurefile/mono4.fss', 'ppmMan',lang=language)
#model= makePPM('../../Turkish/Modified_name_TurkishAUFiles/audios/', '../../Turkish/All_Annotations/TRAIN/', '../testeng/featurefile/mono4.fss', 'ppmaudiosturkishpy', lang=language)
#model= makePPM('../../Turkish/Modified_name_TurkishAUFiles/audios/', '../../Turkish/All_Annotations/annotations/', '../testeng/featurefile/mono4.fss', 'ppmaudiosturkishpy', lang=language)
#model= makePPM('../testeng/audio/', '../testeng/annotations/train/', '../testeng/featurefile/mono4.fss', 'ppmbtesteng',lang=language)
endc=time.time()# stop timer for creating ppmfile
durcreation=endc-startc # time needed to create ppmfile
#
print('Time taken to create the model :' + str(durcreation) + '  secs')
starte=time.time()#timer starts to generate and evaluate predicitons
# all the standard outpt while running the evaluation code is saved in \
#the following text file
sys.stdout = open('evaluate' + language +'.txt', 'w')#timer starts to generate and evaluate predictions
print('evaluating the model')

#following are the various instances for generating and evaluating predicitons corresponding to different languages

#predictionsfinal = regressionTest('../../EnglishDataset/Audio/converted/', '../../EnglishDataset/Annotations/TEST/', 'ppmEngpy',lang=language)
predictionsfinal = regressionTest('../../EnglishDataset/Audio/converted/', '../../EnglishDataset/Annotations/', 'ppmEngpy',lang=language)
#predictionsfinal = regressionTest('../../mandarin/audio/', '../../mandarin/testAnnotationsCSV/', 'ppmMan',lang=language)
#predictionsfinal = regressionTest('../../mandarin/audio/', '../../mandarin/annotations/', 'ppmMan',lang=language)
#predictionsfinal = regressionTest('../../Turkish/Modified_name_TurkishAUFiles/audios/', '../../Turkish/All_Annotations/TEST/', 'ppmaudiosturkishpy',lang=language)
#predictionsfinal = regressionTest('../../Turkish/Modified_name_TurkishAUFiles/audios/', '../../Turkish/All_Annotations/annotations/', 'ppmaudiosturkishpy',lang=language)
#predictionsfinal = regressionTest('../EnglishDataset/Audio/converted/', '../EnglishDataset/Annotations/TEST/', 'ppmaudiosengpy')
#predictionsfinal = regressionTest('../testeng/audio/', '../testeng/annotations/test/', 'ppmbtesteng',lang=language)
ende=time.time()# stop timer to generate and evaluate predicitons
durevaluation=ende-starte # time needed to generate and evaluate predicitons
print('Time taken to evaluate the model :' + str(durevaluation) + '  secs')
pr.disable()
s = io.StringIO()
scaller=io.StringIO()
sortby = 'tottime' # profile sorted by total internal time of each function
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)#profile timing 
pscaller = pstats.Stats(pr, stream=scaller).sort_stats(sortby)# generates profiling with parent and child function info
#ps.print_stats()
#ps.dump_stats('stats.dmp')
sys.stdout = open('profile' + language +'_callers.txt', 'w') #profiling including function callers saved in text file
pscaller.print_callers()
print(scaller.getvalue())
sys.stdout = open('profile' + language +'.txt', 'w')# profiling info saved in text file
ps.print_stats()
print(s.getvalue())