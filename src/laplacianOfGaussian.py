# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:09:40 2017

@author: Anindita Nath
University of Texas at ElPaso
"""
import numpy as np
import math
#Laplacian of Gaussian
#converted from original by Nigel Ward, University of Texas at El Paso and Kyoto University
#January 2016

#This is to be used for peak spotting.

def  laplacianOfGaussian(sigma):

    #if longer, slows things down a little in the subsequent convolution
    #if shorter, insufficient consideration of local context to see if it's a real peak 
    length = sigma * 5   
    
    sigmaSquare = sigma * sigma
    sigmaFourth = sigmaSquare * sigmaSquare
    #print(sigmaSquare)
    #print(sigmaFourth)
    vec = np.zeros(length,)
    center = int(math.floor(length / 2))
    #print(center)
    
    for i in range(length):
        x = i - (center -1)
        yprime = ((x * x) / sigmaFourth - 1 / sigmaSquare) 
        y=yprime* math.exp( (-x * x) / (2 * sigmaSquare))
           
        #print(yprime)
        vec[i] = - y
        #vec[i]=round(vec[i],6)  
    #print(vec.shape)  
    return vec


#test
#x = rand(1,200)
#x(30:35) = 1
#x(32) = 2
#x(70:80) = 3
#vec = laplacianOfGaussian(10)
#np.set_printoptions(threshold=np.inf)
#print(vec)
#print(vec.shape)
#c = conv(x, vec, 'same')
#plot(1:200, c)
