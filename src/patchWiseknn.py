import numpy as np
import numpy.matlib
from sklearn.neighbors import NearestNeighbors

#Translated on Python by Alonso Granados 11/22/2017
def patchwiseKNN(segmentData, modelPatchesProsody, modelPatchesProps, k):
    #see ../doc/UTEP-prosody-overview.docx and Inferring Stance from Prosody
    #derived from Jason's regSegmentKNN.m
    # - changeed variable names and comments to be clearer
    # - changed it to run faster using vpa(???)
    #segmentData is the prosody of the patches of the segment to classify
    #modelPatchesProsody and modelPatchesProps are the model to use in classifying
    #k is the number of neighbors to find

    #propPredictions is the output that matters
    #votePerPatch and patchNeighbors are just for tracing purposes

    #Conver input into numpy arrays
    segmentData = np.array(segmentData)
    segmentData =np.nan_to_num(segmentData)
    modelPatchesProsody = np.array(modelPatchesProsody)
    #print(modelPatchesProsody.shape)
    modelPatchesProps = np.array(modelPatchesProps)
    modelPatchesProsody =np.nan_to_num(modelPatchesProsody)
    #print(modelPatchesProsody.shape)
    # for English corpus:
    # when digits = 6, vpa takes 8-10 minutes, knn takes 3 seconds, unchanged
    # when digits = 3, vpa takes 10 minutes, knn takes .7 seconds vs .4 sec
    nproperties = np.shape(modelPatchesProps)[1]
    npatches = np.shape(segmentData)[0]
    votePerPatch = np.zeros((npatches, nproperties))

    #Knn Search
    neigh = NearestNeighbors(n_neighbors=k,algorithm='brute') 
    neigh.fit(modelPatchesProsody)
    distances, patchNeighbors = neigh.kneighbors(segmentData)

    dsquared = np.square(distances) + 0.0000000001

    # accumulate votes from all the patches
    for row in range(npatches):
        kDistances = dsquared[row,:]

        kIndices = patchNeighbors[row,:]

        kPropVals = modelPatchesProps[kIndices,:] # size is k by nproperties
        #print(kPropVals.shape)
        kWeights = (1/ kDistances)
        #print(kWeights.shape)

        kWeightsMat = np.transpose(np.matlib.repmat(kWeights, nproperties, 1))
        #print(kWeightsMat.shape)

        # weighted average = sum(value_i * weight_i) / sum(weight_i) for all i
        vals = kPropVals * kWeightsMat

        summedEvidence = sum(vals, 0) # summed evidence from all k of the neighbors

        # normalize to compensate for local sparsity/density
        patchVotes = summedEvidence / (np.sum(kWeights, axis=0))
        votePerPatch[row,:] = patchVotes

    propPredictions = np.mean(votePerPatch,axis=0)
    #print(propPredictions.shape)
    #print(votePerPatch.shape)
    #print(patchNeighbors.shape)
    return propPredictions, votePerPatch, patchNeighbors
# Test case
#print(patchwiseKNN([[4.1,4],[5.1,4]], [[1,1], [2,2.1],[3,3], [4,4], [5,5]], [[0],[0],[0],[1],[1]],2))
