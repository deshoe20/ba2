import Util
from NodeCategory import NodeCategory

"""
Class Node

Represents a node in a tree.

TODO : test and customize euquals mehode
"""
class Node:

    def __init__(self, label, parentTree = None, parent = None, children = None, category = None):
        self.label = label
        self.parentTree = parentTree
        self.children = children
        self.parent = parent
        self.category = category
        self.markerUpper = None
        self.markerLower = None

    def initMarkers(self):
        if self.markerUpper is None:
            self.markerUpper = Util.uid()
        if self.markerLower is None:
            self.markerLower = Util.uid()

    def resetParentTree(self, tree):
        self.parentTree = tree

    def isLeaf(self):
        return not self.children

    def isLexicalLeaf(self):
        return self.isLeaf() and (self.category == NodeCategory.lexical)

