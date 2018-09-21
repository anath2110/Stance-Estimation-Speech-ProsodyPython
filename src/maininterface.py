# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 12:27:19 2017

@author:Anindita Nath
University of Texas at ElPaso
"""
import argparse
from makePPM import makePPM
from regressionTest import regressionTest
    
def main():
    parser = argparse.ArgumentParser(description='Predict Stance from Prosody ')
    parser.add_argument('-audio', '--audio', help='Path to the audio directory', required=True)
    parser.add_argument('-annotations', '--annotations', help='Path to the annotations directory', required=True)
    parser.add_argument('-featurefile', '--featurefile', help='Featurefile', required=True)
    parser.add_argument('-ppmfile', '--model', help='Path to Model', required=True)
    parser.add_argument('-langAbb', '--langAbb', help='Abbreviation for the name of the audio language', required=True)
   
    args = parser.parse_args()
        
    audio_dir  = args.audio
    anno_dir = args.annotations
    feature_file = args.featurefile
    ppmfile = args.model
    lang=args.langAbb
    model= makePPM(audio_dir, anno_dir,feature_file,ppmfile,lang)
    predictionsfinal = regressionTest(audio_dir, anno_dir, ppmfile,lang)
    
if __name__ == "__main__":
    main()