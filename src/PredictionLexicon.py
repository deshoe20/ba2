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
    
    def compatibleAppending(self, key , value):
        if key != "prediction:":
            logging.error("Given dataset doesn't seem to be of prediction type: %s" % str(key))
        self.append(value)  