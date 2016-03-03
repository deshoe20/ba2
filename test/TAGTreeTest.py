"""
Created on 27.02.2016

@author: Albert
"""
import unittest
import TAGTree
import pickle

"""
%%% 26494
Ich liebe dieses Land sehr .
PPER Ich    VVFIN liebe    PDAT dieses    NN Land    ADV sehr    $. .
(S (S (NP[nom] (PPER Ich))(VP (VP (VP (VVFIN liebe))(NP[acc] (DP[acc] (PDAT dieses))(NP[acc] (NN Land))))(AVP (ADV sehr))))($. .))

%%% 26494
prediction:    ARG    (NP-OA[acc]^null_1 (DP-NK[acc]^1_null! )(NP-HD[acc]^1_1 ))
Ich ich    ARG    (NP-SB[nom]^null_x (PPER-NKHD^x_x Ich<>))    1.nom.sg.*    
liebe lieben    ARG    (S-HD^null_x (NP-SB[nom]^x_null! )(VP-HD^x_x (VP-HD^x_x (VVFIN-HD^x_x liebe<>))(NP-OA[acc]^x_null! )))    1.sg.pres.ind    
dieses dieser    ARG    (DP-NK[acc]^null_x (PDAT-HD^x_x dieses<>))    acc.sg.neut    
Land Land    ARG    (NP-OA[acc]^null_x (DP-NK[acc]^x_null! )(NP-HD[acc]^x_x (NN-NKHD^x_x Land<>)))    acc.sg.neut    
sehr sehr    ADJ    (VP-HD^null_x (VP-HD^x_null* )(AVP-MO^x_x (ADV-HD^x_x sehr<>)))    --    
. .    ADJ    (S-HD^null_x (S^x_null* )($.^x_x .<>))    --    
"""

class TAGTreeTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        f = open("../res/pickeledTAGlexicon.pick", 'rb')
        self.LEX = pickle.load(f)
        f.close()
    
    def testSubstitution(self):
        self.ich = self.LEX['Ich'][0][1]
        self.liebe = self.LEX['liebe'][4][1]
        self.liebe[0].substitution(self.ich)
        self.ich.draw()
        self.liebe.draw()
    
    def testSubstitution2(self):
        self.ich = self.LEX['Ich'][0][1]
        self.liebe = self.LEX['liebe'][4][1]
        self.liebe[0].substitution(self.ich)
        self.ich.draw()
        self.liebe.draw()
    
    def testPredictionSubstitution(self):
        self.ich = self.LEX['Ich'][0][1]
        self.liebe = self.LEX['liebe'][4][1]
        self.liebe[0].substitution(self.ich)
        self.ich.draw()
        self.liebe.draw()
    
    def testVerify(self):
        self.ich = self.LEX['Ich'][0][1]
        self.liebe = self.LEX['liebe'][4][1]
        self.liebe[0].substitution(self.ich)
        self.ich.draw()
        self.liebe.draw()
    
    def testAdjunction(self):
        self.ich = self.LEX['Ich'][0][1]
        self.liebe = self.LEX['liebe'][4][1]
        self.liebe[0].substitution(self.ich)
        self.ich.draw()
        self.liebe.draw()
        
    def testClone(self):
        pass
        #self.LEX['liebe'][0][1].draw()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    