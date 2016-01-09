'''
Created on 04.01.2016

@author: Albert
'''
from nltk import tree

class MyNLTKTree(tree.Tree):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__(self, params)
        
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