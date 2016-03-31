"""
Created on 24.03.2016

@author: Albert
"""
import sys
from os.path import dirname, abspath, join
from queue import Queue

sys.path.append(join(dirname(dirname(abspath(__file__))), 'src'))
sys.path.append(join(dirname(dirname(abspath(__file__))), 'res'))

import unittest
from Util import Util
from PrefixTreeScanParser import PrefixTreeScanParser


class PrefixTreeScanParserTest(unittest.TestCase):
    
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
        self.p = PrefixTreeScanParserTest

    def test_01_lookForSubstitutionDown(self):
        self.p.ich = self.p.LEX['Ich'][0][1]
        self.p.liebe = self.p.LEX['liebe'][4][1]
        result = Queue()
        t = PrefixTreeScanParser(self.p.ich, self.p.liebe, result)
        t.start()
        t.join()
        result.get().draw()


if __name__ == "__main__":
    unittest.main()