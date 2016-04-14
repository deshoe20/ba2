# -*- coding: utf-8 -*-
"""
Created on 04.04.2016

@author: Benjamin Kosmehl
"""
import logging

class PredictionLexicon(list):
    """
    PLTAG prediction lexicon class
    """


    def __init__(self):
        """
        Constructor
        """
        list.__init__(self, [])
        
    def sortMe(self):
        """
        Sorts all the trees in order of the heuristics value in the first place.
        Lexicon entries are sorted after call to this method.
        """
        self.sort(key = lambda x: int(x[0]), reverse = True)

    def compatibleAppending(self, key, value):
        
        """
        Compatible appending of lexicon entry.
        
        Args:
            key: not used - should be "prediction"
            value: entry payload as tuple of integer and PLTAGTree
        """
        if key != "prediction:":
            logging.error("Given dataset doesn't seem to be of prediction type: %s", str(key))
        self.append(value)
        