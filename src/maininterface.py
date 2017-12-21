# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 12:27:19 2017

@author:Anindita Nath
University of Texas at ElPaso
"""
import argparse
from makePPM import makePPM
from regressionTest import regressionTest
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make model and Test ')
    parser.add_argument('-audio', '--audio', help='Path to the audio directory', required=True)
    parser.add_argument('-annotations', '--annotations', help='Path to the annotations directory', required=True)
    parser.add_argument('-featurefile', '--featurefile', help='Featurefile', required=True)
    parser.add_argument('-modelfile', '--model', help='Path to Model', required=True)
   
    args = parser.parse_args()
        
    audio_dir  = args.audio
    anno_dir = args.annotations
    feature_file = args.featurefile
    model_file = args.model
    model= makePPM(audio_dir, anno_dir,feature_file,model_file)
    predictionsfinal = regressionTest(audio_dir, anno_dir, model_file +'.mat')
