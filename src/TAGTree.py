"""
Created on 04.01.2016

@author: Albert
"""
from nltk import tree
import re, logging
from Enum import MorphCase, NodeType

class TAGTree(tree.Tree):
    """
    classdocs
    """

    morph = MorphCase.UNDEF
    isLexicalLeaf = False
    isLeaf = False
    nodeType = NodeType.UNDEF
    upperNodeHalf = None
    lowerNodeHalf = None
    isCurrentRoot = False
    
    # TODO : REMOVE US
    MORPHINFOPATTERN = re.compile('.*\[([a-z]{3})\].*', re.UNICODE)
    CATEGORYPATTERN = re.compile('^([A-Z0-9$,.*]{1,10})[^a-zA-Z0-9$,.*].*$', re.UNICODE)
    LEXICALLEAFPATTERN = re.compile('\s(\S+)<>', re.UNICODE)
    INTEGRATIONPATTERN = re.compile('_\w+([*!])\s+', re.UNICODE)
     
    # TODO : comment THEONEREGEX - ONE REGEX TO RULE THEM ALL! TO FIND THEM ALL!
    THEONEPATTERN = re.compile('^([^\-]+)(\-([^\[\$]+)(\[([^\]\$]+)\])?(\$.*\$)?)?\^([^_]+)_([\S]+)(\s+(.+)<>)?(\s+-)?\s*$', re.UNICODE)

    def __init__(self, node, children=None):
        """
        Constructor
        """
        # TODO : check for valid tree string
        if isinstance(node, str):
            # get phrasal category and set it as label for this tree
            m = self.__class__.THEONEPATTERN.match(node)
            if m:
                super().__init__(m.group(1), children)
            else:
                logging.error("Failed to extract valid tree from string: %s" % node)
                #raise RuntimeError("No valid category found for %s" % s)
                return
            self.process(m)
        else:
            super().__init__(node, children)

    
    def process(self, match):
        """
        
        """
        #functionalCategory = match.group(3)  # TODO : REMOVE ME
        morphologicalInfo = match.group(6)
        upperNodeHalfMarker = match.group(7)
        lowerNodeHalfMarker = match.group(8)
        lexicalPayload = match.group(10)
        # try to get the optional morphological information in the tree string s
        if morphologicalInfo:
            self.morph = MorphCase.fromString(morphologicalInfo)
        # try to get and set upper node marker
        if upperNodeHalfMarker:
            self.upperNodeHalf = upperNodeHalfMarker
        # try to set node type and extend label with corresponding symbol - only the lower node half marker can carry a type symbol
        if lowerNodeHalfMarker:
            if lowerNodeHalfMarker.endswith('!'):
                self.nodeType = NodeType.SUBST
                self.isLeaf = True # FIXME : check if it is the case in all cases
            elif lowerNodeHalfMarker.endswith('*'):
                self.nodeType = NodeType.FOOT
                self.isLeaf = True # FIXME : check if it is the case in all cases
            self.set_label(self.label() + str(self.nodeType))
        # try to determine and extract lexical leaf data
        if lexicalPayload:
            self.isLexicalLeaf = True
            self.append(lexicalPayload)
        
    def adjunction(self, selfNode, other):
        """for n in reversed(self.nodes):
            if n == node:
                n.initMarkers()"""
        #selfNode.initMarkers()
        

    def substitution(self, other):
        """for n in reversed(self.nodes):
            if n == selfNode:
                n = other.root
                _resetNodes(self.root)
                exit"""
        selfNode = other.root
        self._resetNodes(self.root)

    def _resetNodes(self, root):
        self.root = root;
        self.nodes = [self.root]
        self._getem(self.root, self.nodes)

    def _getem(self, n, r):
        for c in n.children:
            r.add(c)
            r.add(self._getem(c, r))
        return r
    
    def hasNoMarkers(self):
        result = False
        if (self.upperNodeHalf is None and self.lowerNodeHalf is None): result = True
        return result

    
    def currentFringe(self):
        """
        Computes the fringe starting at the rightmost lexical leaf to either the next non lexical leaf or the root node.
        return list of TAGTree nodes
        """
        i = 0
        v = 0
        fs = self.getFringes()
        for ci in range(len(fs) - 1, -1, -1):
            if (fs[ci][0].isCurrentRoot and fs[ci][1]) or (fs[ci][0].isLeaf and not fs[ci][0].isLexicalLeaf and not fs[ci][1]):
                v = ci
            if fs[ci][0].isLexicalLeaf and fs[ci][1]:
                i = ci
                break
        return [x[0] for x in fs[i:v+1]]
                

    def getFringes(self):
        result = [(self, False)]
        for c in self:
            if type(c) is not TAGTree: break
            result.extend(c.getFringes())
        result.append((self, True))
        return result
    
"""    def getSpine(self):
        result = []
        for c in self:
            result.add(self.getFringes(c))
        return result"""
        