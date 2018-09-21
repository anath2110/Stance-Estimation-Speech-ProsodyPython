# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 13:59:00 2017

@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso
"""


from predEval import predEval
import numpy as np
import scipy
#import pickle
import _pickle as pickle



def regressionTest(pathtoaudiodir,pathtoannodir,ppmfile,lang):   

    results, MSE = predEval(pathtoaudiodir, pathtoannodir, ppmfile,lang)
    #save in .mat
    #regresionmat='testregression' + lang + '.mat'
#    predictionsfile=scipy.io.loadmat(regresionmat,struct_as_record=False)
#    predictions =predictionsfile['predictionspy']   

    regresionpickle='testregression' + lang + '.pkl'
    with open(regresionpickle, 'rb') as f:
            predictionsfile = pickle.load(f)
            
    predictions = np.array(predictionsfile[0])       
      

    permissibleError = 0.1 # on a scale from 0 to 2
    largestError = abs((np.max(results - predictions)))

    if largestError > permissibleError:
        print('regression test succeeded: values matched')
    else:
        print("regression test failed; something changed %d" %largestError)
    return results

#testing
#
#pr = cProfile.Profile()
#pr.enable()
#startc=time.time()
#print('creating the model')
#model= makePPM('../../EnglishDataset/Audio/converted/', '../../EnglishDataset/Annotations/TRAIN/', '../testeng/featurefile/mono4.fss', 'ppmaudiosengpy')
##model= makePPM('../Turkish stance data/Turkish/Modified_name_TurkishAUFiles/audios/', '../Turkish stance data/Turkish/All_Annotations/TRAIN/', '../testeng/featurefile/mono4.fss', 'ppmaudiosturkishpy')
#
##model= makePPM('../EnglishDataset/problems/audios/', '../EnglishDataset/problems/annotations/2audiosonly/', '../testeng/featurefile/mono4.fss', 'ppmbadengaudio')
#endc=time.time()
#durcreation=endc-startc
#print('Time taken to create the model :' + str(durcreation) + '  secs')
#starte=time.time()
#print('evaluating the model')
#predictionsfinal = regressionTest('../../EnglishDataset/Audio/converted/', '../../EnglishDataset/Annotations/TEST/', 'ppmaudiosengpy.mat')
##predictionsfinal = regressionTest('../Turkish stance data/Turkish/Modified_name_TurkishAUFiles/audios/', '../Turkish stance data/Turkish/All_Annotations/TEST/', 'ppmaudiosturkishpy.mat')
##predictionsfinal = regressionTest('../EnglishDataset/Audio/converted/', '../EnglishDataset/Annotations/TEST/', 'ppmaudiosengpy.mat')
##predictionsfinal = regressionTest('../EnglishDataset/problems/audios/', '../EnglishDataset/problems/annotations/2audiosonly/', 'ppmbadengaudio.mat')
#ende=time.time()
#durevaluation=ende-starte
#print('Time taken to evaluate the model :' + str(durevaluation) + '  secs')
#pr.disable()
#s = io.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
##ps.dump_stats('stats.dmp')
#sys.stdout = open('profile_ENG.txt', 'w')
#print(s.getvalue())

#testing
#startc=time.time()
#print('creating the model')
#model= makePPM('../EnglishDataset_partial/Audio/', '../EnglishDataset_partial/Annotations/Train/', '../testeng/featurefile/mono4.fss', 'ppmpartialengpy')
#endc=time.time()
#durcreation=endc-startc
#print('Time taken to create the model :' + str(durcreation) + '  secs')
#starte=time.time()
#print('evaluating the model')
#predictionsfinal = regressionTest('../EnglishDataset_partial/Audio/', '../EnglishDataset_partial/Annotations/Test/', 'ppmpartialengpy.mat')
#ende=time.time()
#durevaluation=ende-starte
#print('Time taken to evaluate the model :' + str(durevaluation) + '  secs')
