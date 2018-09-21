# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 12:27:19 2017

@author:Anindita Nath
University of Texas at ElPaso
"""
import argparse
#from makePPM import makePPM
from new_noAnno_API import noAnnoAPI

def main():
    

    parser = argparse.ArgumentParser(description='Make model and Test ')
#    parser.add_argument('-audio', '--audio', help='Path to the audio directory', required=True)
#    parser.add_argument('-annotations', '--annotations', help='Path to the annotations directory', required=True)
#    parser.add_argument('-featurefile', '--featurefile', help='Featurefile', required=True)
    parser.add_argument('-ppmfile', '--ppm', help='Path to Model', required=True)
    parser.add_argument('-language', '--lang', help='Mention the type of language', required=True)
    
    parser.add_argument('-testaudiodir', '--testaudio', help='Path to the test audio directory', required=True)
    parser.add_argument('-predictionsfile', '--pred', help='Name of the file where output predictions are to saved', required=True)
    parser.add_argument('-start', '--startsec', help='Cut a segmnet from this start sec of the audio', required=False)
    parser.add_argument('-end', '--endsec', help='Cut a segment up to this end sec of the audio', required=False)
   
    args = parser.parse_args()
        
#    audio_dir  = args.audio
#    anno_dir = args.annotations
#    feature_file = args.featurefile
    ppmfile = args.ppm
    language=args.lang
    #ppmmodel= makePPM(audio_dir, anno_dir,feature_file,ppmfile,language)
    
    outputFile=args.pred
    testaudiodir=args.testaudio
    start=args.startsec
    end=args.endsec
    noAnnoAPI(testaudiodir,ppmfile,outputFile,language,start,end)

if __name__ == "__main__":
    main()