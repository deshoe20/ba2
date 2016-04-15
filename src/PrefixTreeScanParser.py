# -*- coding: utf-8 -*-
"""
Created on 07.04.2016

@author: Benjamin Kosmehl
"""
from threading import Thread
from Util import Util
import logging
from Enum import NodeType


class PrefixTreeScanParser(Thread):
    """
    Tries to create a fit for two PLTAGTree.
    
    CLASS UNDER CONSTRUCTION
    """

    def __init__(self, prefixTree, elementaryTree, result):
        """
        Constructor
        
        Args:
            prefixTree: prefix tree
            elementaryTree: elementary tree
            result: asynchronous Queue for possible results
        """
        super().__init__()
        self.PRED = Util.getPLEX()
        self.PRED.sortMe()
        self.prefixTree = prefixTree
        self.elementaryTree = elementaryTree
        self.result = result
        self.predictionDepth = int(Util.getConfigEntry()['prediction_depth'])

    def run(self):
        """
        Tries.
        """
        # if none try prediction and again
        if (not self.prefixTree.isCurrentRoot) or (not self.elementaryTree.isCurrentRoot):
            logging.warning("WARNING - malformed tree detected!\n%s\n%s",
                            str(self.prefixTree), str(self.elementaryTree))
        self.lookForSubstitutionDown(self.prefixTree, self.elementaryTree)
        self.lookForSubstitutionUp(self.prefixTree, self.elementaryTree)
        self.lookForAdjunctionDown(self.prefixTree, self.elementaryTree)
        self.lookForAdjunctionUp(self.prefixTree, self.elementaryTree)

    def lookForSubstitutionDown(self, t1, t2):
        temp = t1.clone()
        for n in temp.getCurrentFringe():
            if (n.nodeType == NodeType.SUBST) and n.match(t2, True):
                n.substitution(t2)
                temp.reset()
                self.result.put(temp)
                logging.debug(
                    "Integrated %s onto %s via down substitution: %s", str(t2), str(t1), str(temp))
                break

    def lookForSubstitutionUp(self, t1, t2):
        temp = t2.clone()
        n = temp.getFringes()[0]  # all or only the first fringe?
        for f in n:
            if (f[0].nodeType == NodeType.SUBST) and f[0].match(t1, True):
                f[0].substitution(t1)
                temp.reset()
                self.result.put(temp)
                logging.debug(
                    "Integrated %s onto %s via up substitution: %s", str(t1), str(t2), str(temp))
                break

    # fix me: in left and right - currently incremental criterium violated
    def lookForAdjunctionDown(self, t1, t2):
        temp1 = t1.clone()
        temp2 = t2.clone()
        eligible = False
        n = temp2.getFringes()[0]
        for f in n:
            if (f[0].nodeType == NodeType.FOOT) and f[0].match(temp2, True):
                eligible = True
        if eligible:
            for n in temp1.getCurrentFringe():
                if (n.nodeType == NodeType.INNER) and n.match(temp2):
                    n.adjunction(temp2)
                    temp1.reset()
                    self.result.put(temp1)
                    logging.debug(
                        "Integrated %s onto %s via down adjunction: %s", str(t2), str(t1), str(temp2))
                    break

    def lookForAdjunctionUp(self, t1, t2):
        temp1 = t1.clone()
        temp2 = t2.clone()
        pos = None
        for n in temp1.getCurrentFringe():  # should it?
            # TODO: check if morphcase must be same or not
            if n.nodeType == NodeType.FOOT and n.match(t1, True):
                pos = n
        if pos is not None:
            n = temp2.getFringes()[0]
            for f in n:
                if (f[0].nodeType == NodeType.INNER) and f[0].match(pos, True):
                    f[0].adjunction(temp1)
                    temp2.reset()
                    self.result.put(temp2)
                    logging.debug(
                        "Integrated %s onto %s via up adjunction: %s", str(t1), str(t2), str(temp2))
                    break

    def lookForVerification(self):
        # implement me
        return False

    def lookForPrediction(self):
        # implement me
        return False
