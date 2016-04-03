# -*- coding: utf-8 -*-
"""
Created on 04.01.2016

@author: Albert
"""
import logging

class PredictionLexicon(list):
    """
    classdocs
    """


    def __init__(self):
        """
        Constructor
        """
        list.__init__(self, [])

    def compatibleAppending(self, key, value):
        """
        Compatible appending.
        """
        if key != "prediction:":
            logging.error("Given dataset doesn't seem to be of prediction type: %s", str(key))
        self.append(value)
        