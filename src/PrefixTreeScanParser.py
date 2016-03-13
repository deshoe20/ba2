"""
Created on 07.01.2016

@author: Albert
"""
from threading import Thread

class PrefixTreeScanParser(Thread):
    """
    classdocs
    """


    def __init__(self, prefixTree, elementaryTree, result):
        """
        Constructor
        """
        super().__init__(self)
        
        # if none try prediction and again