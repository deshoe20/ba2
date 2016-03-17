# -*- coding: utf-8 -*-
"""
Created on 07.01.2016

@author: Albert
"""
from threading import Thread
from Util import Util
import logging
from Enum import NodeType

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
        if (not self.prefixTree.isCurrentRoot) or (not self.elementaryTree.isCurrentRoot):
            logging.warn("WARNING - malformed tree detected!\n{}\n{}".format(str(self.prefixTree), str(self.elementaryTree)))
        self.lookForSubstitution(self.prefixTree, self.elementaryTree)
        self.lookForSubstitution(self.elementaryTree, self.prefixTree)
        
    def lookForDownSubstitution(self, t1, t2):
        pass
                    
    def lookForUpSubstitution(self, t1, t2):
        pass
    
    def lookForAdjunction(self):
        return False
    
    def lookForVerification(self):
        return False
    
    def lookForPrediction(self):
        return False
    
    