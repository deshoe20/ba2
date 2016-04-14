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

class ElementaryLexiconTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUp(cls)
        cls.LEX = Util.loadElementaryLexicon()
        
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.p = ElementaryLexiconTest
    
    def test_01_SortMe(self):
        self.p.LEX.sortMe()
        self.assertTrue(self.p.LEX['dieses'][0][0] == 143)

if __name__ == "__main__":
    unittest.main(sortTestMethodsUsing=False, failfast=True)
    
    