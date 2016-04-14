# -*- coding: utf-8 -*-
"""
Created on 16.03.2016

@author: Benjamin Kosmehl
"""
import sys
from os.path import dirname, abspath, join

sys.path.append(join(dirname(dirname(abspath(__file__))), 'src'))
sys.path.append(join(dirname(dirname(abspath(__file__))), 'res'))

import unittest
from Util import Util

"""
%%% 26494 (26490 in TIGER 2.1)
Ich liebe dieses Land sehr.
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

class PLTAGTreeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUp(cls)
        cls.LEX = Util.loadElementaryLexicon(True)
        cls.PREDLEX = Util.loadPredictionLexicon(True)
        cls.ich = None
        cls.liebe = None
        cls.pred = None
        cls.dieses = None
        cls.land = None
        cls.sehr = None
        cls.fullstop = None
        
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.p = PLTAGTreeTest
    
    def test_01_Substitution(self):
        self.p.ich = self.p.LEX['Ich'][0][1].clone()
        self.p.liebe = self.p.LEX['liebe'][4][1].clone()
        self.p.liebe[0].substitution(self.p.ich)
        self.p.liebe.draw()    
    
    def test_02_PredictionSubstitution(self):
        self.p.pred = self.p.PREDLEX[8101][1].clone()
        self.p.liebe[1][1].substitution(self.p.pred, True)
        self.p.liebe.draw()    
    
    def test_03_Substitution(self):
        self.p.dieses = self.p.LEX['dieses'][1][1].clone()
        self.p.liebe[1][1][0].substitution(self.p.dieses)
        self.p.liebe.draw()    
    
    def test_04_Verify(self):
        self.p.land = self.p.LEX['Land'][10][1].clone()
        self.assertTrue(self.p.liebe.verification(self.p.land))
        self.p.liebe.draw()    
    
    def test_05_Adjunction(self):
        self.p.sehr = self.p.LEX['sehr'][33][1].clone()
        self.p.liebe[1].adjunction(self.p.sehr)
        self.p.liebe.draw()    
        
    def test_06_Adjunction(self):
        self.p.fullstop = self.p.LEX['.'][24][1].clone()
        self.p.liebe.adjunction(self.p.fullstop)
        self.p.fullstop.draw()    
        
    def test_07_Clone(self):
        c = self.p.ich.clone()
        self.assertTrue(c.matches(self.p.ich))
        self.assertNotEqual(id(c), id(self.p.ich))
        self.assertNotEqual(id(c[0]), id(self.p.ich[0]))

if __name__ == "__main__":
    unittest.main()
    
    