"""
Created on 14.01.2016

@author: Albert
"""
import re, logging
from Enum import MorphCase, NodeType
from TAGTree import TAGTree

class CanonicalLexiconTree(TAGTree):
    """
    classdocs
    """
    morph = MorphCase.UNDEF
    isLexicalLeaf = False
    nodeType = NodeType.UNDEF
    
    MORPHINFOPATTERN = re.compile('.*\[([a-z]{3})\].*', re.UNICODE)
    CATEGORYPATTERN = re.compile('^([A-Z0-9$,.*]{1,10})[^a-zA-Z0-9$,.*].*$', re.UNICODE)
    LEXICALLEAFPATTERN = re.compile('\s(\S+)<>', re.UNICODE)
    INTEGRATIONPATTERN = re.compile('_\w+([*!])\s+', re.UNICODE)

    def __init__(self, node, children=None):
        """
        Constructor
        """
        # TODO : check for valid tree string
        if isinstance(node, str):
            # get phrasal category and set it as label for this tree
            m = CanonicalLexiconTree.CATEGORYPATTERN.match(node)
            if m:
                super().__init__(m.group(1), children)
            else:
                logging.error("No valid category found for %s" % node)
                #raise RuntimeError("No valid category found for %s" % s)
                return
            self.process(node)
        else:
            super().__init__(node, children)

         
    def process(self, s):
        # try to get the optional morphological information in the tree string s
        m = CanonicalLexiconTree.MORPHINFOPATTERN.match(s)
        if m:
            self.morph = MorphCase.fromString(m.group(1))
        # try to determine and extract lexical leaf data
        m = CanonicalLexiconTree.LEXICALLEAFPATTERN.search(s)
        if m:
            self.isLexicalLeaf = True
            self.append(m.group(1))
        # try to set node type and extend label with corresponding symbol
        m = CanonicalLexiconTree.INTEGRATIONPATTERN.search(s)
        if m:
            if m.group(1) == "!":
                self.nodeType = NodeType.SUBST
            elif m.group(1) == "*":
                self.nodeType = NodeType.FOOT
            self.set_label(self.label() + str(self.nodeType))
    
    
    