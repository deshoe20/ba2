"""
Created on 04.01.2016

@author: Albert
"""

class Util(object):
    """
    classdocs
    """


    def __init__(self, params):
        """
        Constructor
        """
       
    
    @classmethod
    def getLang(cls):
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
        