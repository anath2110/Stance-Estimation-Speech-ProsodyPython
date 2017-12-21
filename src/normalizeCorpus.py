# -*- coding: utf-8 -*-
"""
Created on Thur Dec 14 15:30:49 2017

@author: modified from Alonso's by Anindita Nath
University of Texas at ElPaso
"""
from prosodizeCorpus import prosodizeCorpus
from concatenateFeatures import concatenateFeatures
from getfeaturespec import getfeaturespec

import numpy as np
import scipy
def normalizeCorpus(corpus, means, stddevs):
    for i in range(len(corpus)):
        segment = corpus[i]
        segment.features = normalizeSegmentPatches(segment.features, means, stddevs)
    return corpus

def normalizeSegmentPatches(features, means, stddevs):
    npatches = np.shape(features)[0]
    nfeatures = np.shape(features)[1]
    normalized = np.zeros((npatches, nfeatures))
    for f in range (nfeatures):
        normalized[:, f] = ((features[:, f] - means[f] ) / stddevs[f] )
    return normalized

#segData= prosodizeCorpus('stance-master/testeng/audio/', 'stance-master/testeng/annotations/', getfeaturespec('stance-master/src/mono4.fss'), 100)
#allpatches=concatenateFeatures(segData,-1)
#means = np.mean(allpatches,axis=0)
#stddevs = np.std(allpatches,axis=0)
#normalized=normalizeCorpus(segData,means,stddevs)
#np.set_printoptions(threshold=np.inf)
#scipy.io.savemat('normCorpuspy.mat', {'normCorpuspy': normalized})
#print(normalized.shape)