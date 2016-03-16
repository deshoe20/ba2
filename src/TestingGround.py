# -*- coding: utf-8 -*-
"""
Created on 11.01.2016

@author: Albert
"""
import sys
from os.path import dirname, abspath, join
sys.path.append(join(dirname(dirname(abspath(__file__))), 'res'))

import re, logging, pickle
from PLTAGTree import PLTAGTree
from PredictionLexicon import PredictionLexicon
from ElementaryLexicon import ElementaryLexicon
from nltk import tree
from Util import Util

#1    lassen    ADJ    (VP-HD^null_x (VP-HD^x_null* )(VP-*T2*-RE^x_x (PP-*T1*-OP^x_null! )(VP-HD^x_x (NP-OA[acc]^x_null! )(VP-HD^x_x (VP-OC^x_null! )(VP-HD^x_x (VZ-HD^x_x (PTKZU-PM^x_null! )(VZ-HD^x_x (VVINF-HD^x_x lassen<>))))))))

LEX = None

"""
regular expression splitting the lexicon file lines into four groups
    first group is only the leading number in each line e.g. '1'
    second group is the entry string e.g. 'word' 
    third group is the elementary tree type e.g. 'ARG'
    fourth group is the tree structure for this word e.g. everything between the outer brackets      
"""
         
def main():
    """
    11033
    89174
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    #convert
#    LEX = Util.loadPredictionLexicon(True)
    LEX = Util.loadElementaryLexicon(True)

    logging.info("Length of lexicon: %d" % len(LEX))
#    LEX[10449][1].draw()
    cf = LEX['liebe'][4][1].getCurrentFringe(True)
    print("Current fringe:\t%s" % str(cf))
    LEX['liebe'][4][1].draw()
#    cf[2].set_label("HANT")
#    LEX['Amaru'][0][1].draw()
#    print(str(LEX['tot'][5][1].isCurrentRoot))
#    print(str(LEX['gehört'][0][1][1][0].isCurrentRoot))
#    t = tree.Tree.fromstring('(S (S (NP[nom] (PPER Ich))(VP (VP (VP (VVFIN liebe))(NP[acc] (DP[acc] (PDAT dieses))(NP[acc] (NN Land))))(AVP (ADV sehr))))($. .))')
#    t.draw()

if __name__ == '__main__':
    main()
        

