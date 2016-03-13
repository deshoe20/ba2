"""
Created on 04.01.2016

@author: Albert
"""

import pickle

class Util(object):
    """
    classdocs
    """


    def __init__(self, params):
        """
        Constructor
        """
       
    
    @classmethod
    def getLang(cls): # TODO : heal me from da magic
        return "german" 
    
    i = 0;
    @staticmethod
    def uid():
        result = Util.i
        Util.i += 1 
        return result;
    
    @staticmethod
    def objMatch(cls, s):
        return getattr(cls, s.upper(), None)
    
    @staticmethod
    def _loadLexicon(fileName, mode):
        f = open(fileName, mode)
        result = pickle.load(f)
        f.close()
        return result
    
    @staticmethod
    def loadElementaryLexicon():
        return Util._loadLexicon("../res/pickeledTAGlexicon.pick", 'rb')
    
    @staticmethod
    def loadPredictionLexicon():
        return Util._loadLexicon("../res/pickeledTAGPredictionlexicon.pick", 'rb')
    
        