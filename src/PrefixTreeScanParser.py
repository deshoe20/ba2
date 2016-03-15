# -*- coding: utf-8 -*-
"""
Created on 07.01.2016

@author: Albert
"""
from threading import Thread
from Util import Util

class PrefixTreeScanParser(Thread):
    """
    classdocs
    """


    def __init__(self, prefixTree, elementaryTree, result):
        """
        Constructor
        """
        super().__init__()
        self.prefixTree = prefixTree
        self.elementaryTree = elementaryTree
        self.result = result
        self.predictionDepth = int(Util.getConfigEntry()['predictionDepth'])
        
    def run(self):
        # if none try prediction and again
        pass
        
    def lookForSubstitution(self):
        return False
    
    def lookForAdjunction(self):
        return False
    
    def lookForVerification(self):
        return False
    
    def lookForPrediction(self):
        return False
    
    