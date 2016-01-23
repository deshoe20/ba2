'''
Created on 04.01.2016

@author: Albert
'''
from nltk import tree
import re, logging
from Enum import MorphCase, NodeType

class TAGTree(tree.Tree):
    '''
    classdocs
    '''


    morph = MorphCase.UNDEF
    isLexicalLeaf = False
    nodeType = NodeType.UNDEF
    
    MORPHINFOPATTERN = re.compile('.*\[([a-z]{3})\].*', re.UNICODE)
    CATEGORYPATTERN = re.compile('^([A-Z0-9$,.*]{1,10})[^a-zA-Z0-9$,.*].*$', re.UNICODE)
    LEXICALLEAFPATTERN = re.compile('\s(\S+)<>', re.UNICODE)
    INTEGRATIONPATTERN = re.compile('_\w+([*!])\s+', re.UNICODE)

    def __init__(self, node, children=None):
        '''
        Constructor
        '''
        # TODO : check for valid tree string
        if isinstance(node, str):
            # get phrasal category and set it as label for this tree
            m = self.__class__.CATEGORYPATTERN.match(node)
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
        m = self.__class__.MORPHINFOPATTERN.match(s)
        if m:
            self.morph = MorphCase.fromString(m.group(1))
        # try to determine and extract lexical leaf data
        m = self.__class__.LEXICALLEAFPATTERN.search(s)
        if m:
            self.isLexicalLeaf = True
            self.append(m.group(1))
        # try to set node type and extend label with corresponding symbol
        m = self.__class__.INTEGRATIONPATTERN.search(s)
        if m:
            if m.group(1) == "!":
                self.nodeType = NodeType.SUBST
            elif m.group(1) == "*":
                self.nodeType = NodeType.FOOT
            self.set_label(self.label() + str(self.nodeType))
        
    def adjunction(self, selfNode, other):
        """for n in reversed(self.nodes):
            if n == node:
                n.initMarkers()"""
        #selfNode.initMarkers()
        

    def substitution(self, other, selfNode):
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

    def currentFringe(self):
        i = 0
        v = len(self.fringes)
        for n in reversed(self.fringes):
            if n.isLexicalLeaf:
                i = self.fringes.index(n)
        for n in self.fringes[i+1:]:
            if n.isLeaf:
                v = self.fringes.index(v)
        return self.fringes[i:v+1]
                

    def getFringes(self, n):
        result = [n]
        for c in n.children:
            result.add(self.getFringes(c))
        result.add(n)
        return result
    
'''    def getSpine(self):
        result = []
        for c in self:
            result.add(self.getFringes(c))
        return result'''
        