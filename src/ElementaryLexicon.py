# -*- coding: utf-8 -*-
"""
Created on 16.03.2016

@author: Benjamin Kosmehl
"""


class ElementaryLexicon(dict):
    """
    LTAG elementary lexicon class.
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

    def sortMe(self):
        """
        Sorts all the trees for all entries in heuristic order.
        Lexicon entries are sorted after call to this method.
        """
        for c in self.items():
            c[1].sort(key=(lambda x: x[0]), reverse=True)

    def compatibleAppending(self, key, value):
        """
        Compatible appending of lexicon entry.
        
        Args:
            key: entry key
            value: entry payload as tuple of integer and PLTAGTree
        """
        if key in self:
            self[key].append(value)
        else:
            self[key] = [value]
