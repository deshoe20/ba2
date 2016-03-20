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
        self.lookForDownSubstitution(self.prefixTree, self.elementaryTree)
        self.lookForUpSubstitution(self.prefixTree, self.elementaryTree)
        
    def lookForDownSubstitution(self, t1, t2):
        temp = t1.clone()
        for n in temp.getCurrentFringe():
            if (n.nodeType == NodeType.SUBST) and n.match(t2, True):
                n.substitution(t2)
                temp.reset()
                self.result.put(temp)
                logging.debug("Integrated {} with {} via down substitution: {}".format(str(t1), str(t2), str(temp)))
                break
                    
    def lookForUpSubstitution(self, t1, t2):
        temp = t2.clone()
        for n in temp.getFringes():
            for f in n:
                if (f[0].nodeType == NodeType.SUBST) and f[0].match(t1, True):
                    f[0].substitution(t1)
                    temp.reset()
                    self.result.put(temp)
                    logging.debug("Integrated {} with {} via up substitution: {}".format(str(t2), str(t1), str(temp)))
    
    def lookForAdjunction(self):
        return False
    
    def lookForVerification(self):
        return False
    
    def lookForPrediction(self):
        return False
    
    