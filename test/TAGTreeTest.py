'''
Created on 27.02.2016

@author: Albert
'''
import unittest
import TAGTree
import pickle


class TAGTreeTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        f = open("res/pickeledTAGlexicon.pick", 'rb')
        self.LEX = pickle.load(f)
        f.close()

    def testclone(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()