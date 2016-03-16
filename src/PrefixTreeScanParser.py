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
        
    def lookForSubstitution(self, t1, t2):
        for i in range(len(t1.getCurrentFringe())):
            n = t1.getCurrentFringe()[i]
            if n.nodeType == NodeType.SUBST:
                if n.match(t2):
                    newN = n.clone()
                    newN.substitution(t2)
                    self.result.put(newN)
                    logging.debug("Integrated {} with {} via substitution".format(str(t1), str(t2)))
    
    def lookForAdjunction(self):
        return False
    
    def lookForVerification(self):
        return False
    
    def lookForPrediction(self):
        return False
    
    