"""
Created on 27.02.2016

@author: Albert
"""
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
        self.assertTrue(self.p.LEX['dieses'][0][0] == '143')

if __name__ == "__main__":
    unittest.main(sortTestMethodsUsing=False, failfast=True)
    
    