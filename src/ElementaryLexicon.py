# -*- coding: utf-8 -*-
"""
Created on 04.01.2016

@author: Albert
"""

class ElementaryLexicon(dict):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
    
    def sortMe(self):
        for c in self.items():
            c[1].sort(key = lambda x: int(x[0]), reverse = True)    
        
    def compatibleAppending(self, key, value):
        if key in self:
            self[key].append(value)
        else:
            self[key] = [value]
        
    