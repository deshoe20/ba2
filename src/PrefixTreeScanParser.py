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
        self.lookForSubstitutionDown(self.prefixTree, self.elementaryTree)
        self.lookForSubstitutionUp(self.prefixTree, self.elementaryTree)
        self.lookForAdjunctionDown(self.prefixTree, self.elementaryTree)
        self.lookForAdjunctionUp(self.prefixTree, self.elementaryTree)
        
    def lookForSubstitutionDown(self, t1, t2):
        temp = t1.clone()
        for n in temp.getCurrentFringe():
            if (n.nodeType == NodeType.SUBST) and n.match(t2, True):
                n.substitution(t2)
                self.result.put(temp)
                logging.debug("Integrated {} onto {} via down substitution: {}".format(str(t2), str(t1), str(temp)))
                break
                    
    def lookForSubstitutionUp(self, t1, t2):
        temp = t2.clone()
        for n in temp.getFringes(): # all or only the first fringe?
            for f in n:
                if (f[0].nodeType == NodeType.SUBST) and f[0].match(t1, True):
                    f[0].substitution(t1)
                    self.result.put(temp)
                    logging.debug("Integrated {} onto {} via up substitution: {}".format(str(t1), str(t2), str(temp)))
                        
    def lookForAdjunctionDown(self, t1, t2): #FIXME: in up and down - currently incremental criterium violated
        temp1 = t1.clone()
        temp2 = t2.clone()
        eligible = False
        for n in temp2.getFringes():
            for f in n:
                if (f[0].nodeType == NodeType.FOOT) and f[0].match(temp2, True):
                    eligible = True
        if eligible:
            for n in temp1.getCurrentFringe():
                if (n.nodeType == NodeType.INNER) and n.match(temp2):
                    n.adjunction(temp2)
                    self.result.put(temp1)
                    logging.debug("Integrated {} onto {} via down adjunction: {}".format(str(t2), str(t1), str(temp2)))
    
    def lookForAdjunctionUp(self, t1, t2):
        temp1 = t1.clone()
        temp2 = t2.clone()
        pos = None
        for n in temp1.getCurrentFringe(): # should it?
            if n.nodeType == NodeType.FOOT and n.match(t1, True): #TODO: check if morphcase must be same or not
                pos = n
        if pos is not None:
            for n in temp2.getFringes(): # all or only the first fringe?
                for f in n:
                    if (f[0].nodeType == NodeType.INNER) and f[0].match(pos, True):
                        f[0].adjunction(temp1)
                        self.result.put(temp2)
                        logging.debug("Integrated {} onto {} via up adjunction: {}".format(str(t1), str(t2), str(temp2)))
    
    def lookForVerification(self):
        return False
    
    def lookForPrediction(self):
        return False
    
    