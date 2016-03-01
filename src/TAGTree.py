"""
Created on 04.01.2016

@author: Albert
"""
from nltk import tree
import re
import logging
from Enum import MorphCase, NodeType
import copy
from Util import Util


class TAGTree(tree.Tree):
    """
    classdocs
    """

    morph = MorphCase.UNDEF
    isLexicalLeaf = False
    isLeaf = False  # FIXME : kill me
    nodeType = NodeType.UNDEF
    upperNodeHalf = None
    lowerNodeHalf = None
    isCurrentRoot = False

    # TODO : REMOVE US
    MORPHINFOPATTERN = re.compile('.*\[([a-z]{3})\].*', re.UNICODE)
    CATEGORYPATTERN = re.compile(
        '^([A-Z0-9$,.*]{1,10})[^a-zA-Z0-9$,.*].*$', re.UNICODE)
    LEXICALLEAFPATTERN = re.compile('\s(\S+)<>', re.UNICODE)
    INTEGRATIONPATTERN = re.compile('_\w+([*!])\s+', re.UNICODE)

    # TODO : comment THEONEREGEX - ONE REGEX TO RULE THEM ALL! TO FIND THEM
    # ALL!
    THEONEPATTERN = re.compile(
        '^([^\-]+)(\-([^\[\$]+)(\[([^\]\$]+)\])?(\$.*\$)?)?\^([^_]+)_([\S]+)(\s+(.+)<>)?(\s+-)?\s*$', re.UNICODE)

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
                logging.error(
                    "Failed to extract valid tree from string: %s" % node)
                #raise RuntimeError("No valid category found for %s" % s)
                return
            self.process(m)
        else:
            super().__init__(node, children)

    def process(self, match):
        """

        """
        # functionalCategory = match.group(3)  # TODO : REMOVE ME
        morphologicalInfo = match.group(6)
        upperNodeHalfMarker = match.group(7)
        lowerNodeHalfMarker = match.group(8)
        lexicalPayload = match.group(10)
        # try to get the optional morphological information in the tree string
        # s
        if morphologicalInfo:
            self.morph = MorphCase.fromString(morphologicalInfo)
        # try to get and set upper node marker
        if upperNodeHalfMarker:
            self.upperNodeHalf = upperNodeHalfMarker
        # try to set node type and extend label with corresponding symbol -
        # only the lower node half marker can carry a type symbol
        if lowerNodeHalfMarker:
            if lowerNodeHalfMarker.endswith('!'):
                self.nodeType = NodeType.SUBST
                self.isLeaf = True
            elif lowerNodeHalfMarker.endswith('*'):
                self.nodeType = NodeType.FOOT
                # FIXME : check if it is the case in all cases
                self.isLeaf = True
            self.set_label(self.label() + str(self.nodeType))
        # try to determine and extract lexical leaf data
        if lexicalPayload:
            self.isLexicalLeaf = True
            self.isLeaf = True
            self.append(lexicalPayload)

    def adjunction(self, other):
        """
        Adjoins the TAGTree other onto self. Adds other children to self and self children to the corresponding foot node in other.
        Blank adjoin - meaning checkup for validity and correctness should be in the calling method.
        """
        if self.nodeType is NodeType.FOOT:
            n = self._fetchAdjunctionFoot(other, self.getlabel)
            if n is None:
                logging.error(
                    "Adjunction failed - could not find corresponding node in %s" % str(other))
                #raise RuntimeError("Adjunction failed - could not find corresponding node in %s" % str(self))
            else:
                c = []
                c.extend(self)
                self.clear()
                self.extend(other)
                self.nodeType = NodeType.INNER
                n.extend(c)
                n.nodeType = NodeType.INNER  # TODO : debug me
        else:
            logging.warn(
                "Can't adjoin on tree node with type: %s" % self.nodeType)

    def _fetchAdjunctionFoot(self, other, label):
        result = None
        if other.isLeaf() and (other.getlabel() == label):
            result = self
        else:
            for c in other:
                if result is not None:
                    logging.error(
                        "Adjunction restriction violation at %s" % str(other))
                    #raise RuntimeError("Adjunction restriction violation at %s" % str(self))
                result = c._gimmeLeafNodeWithLabel(label)
        return result

    def substitution(self, other):
        """
        Substitutes the TAGTree other onto self if possible. Therefore checking if self is of NodeType.SUBST. 
        Does not check for correct morphological information or correct structure of the tree to join. 
        This should be done in the calling method if required.
        Blank substitution - meaning checkup for validity and correctness should be in the calling method.
        """
        if self.nodeType is NodeType.SUBST:
            self.extend(other)
            if len(self) > 0:
                # changes node type to NodeType.INNER if substitution was
                # successful and at least one child was added.
                self.nodeType = NodeType.INNER
        else:
            logging.warn(
                "Can't substitute on tree node with type: %s" % self.nodeType)

    def verify(self, other):
        result = []
        if not isinstance(self.upperNodeHalf, int) and isinstance(self.lowerNodeHalf, int) and self.equals(other):
            wholeother = TAGTree.tolist(other)
            mark = self.lowerNodeHalf
            currentUpper = True
            currentOther = wholeother[0]
            levelOther = wholeother[1]
            levelSelf = 1

            def corress2(self):
                if ((currentUpper and (self.upperNodeHalf == mark)) or (not currentUpper and (self.lowerNodeHalf == mark))) and (currentOther.getlabel() == self.getlabel()):
                    result.append(self)
        else:
            for c in self:
                c.verify(other)
        return result

    def equals(self, other):  # TODO : implement me
        return self.getlabel() == other.getlabel()

    def mark(self, idfier=None):  # TODO : FIXME
        if idfier is None:
            idfier = Util.uid()
        if not self.isLeaf():
            self.lowerNodeHalf = idfier
        if not self.isCurrentRoot:
            self.upperNodeHalf = idfier
        for c in self:
            c.mark(idfier)

    def hasNoMarkers(self):
        return (self.upperNodeHalf is None and self.lowerNodeHalf is None)

    def currentFringe(self):
        """
        Computes the fringe starting at the rightmost lexical leaf to either the next non lexical leaf or the root node.
        Searches for conditions met in the reversed list of all fringes of the self tree.
        return list of TAGTree nodes
        """
        i = 0
        v = 0
        fs = self.getFringes()
        for ci in range(len(fs) - 1, -1, -1):
            if (fs[ci][0].isCurrentRoot and fs[ci][1]) or (fs[ci][0].isLeaf and not fs[ci][0].isLexicalLeaf and not fs[ci][1]):
                v = ci
            # TODO : implement has no markers
            if fs[ci][0].isLexicalLeaf and fs[ci][1]:
                i = ci
                break
        return [x[0] for x in fs[i:v + 1]]

    def getFringes(self):
        result = [(self, False)]
        for c in self:
            if type(c) is not TAGTree:
                break  # the string of a lexicalLeaf
            result.extend(c.getFringes())
        result.append((self, True))
        return result

    def clone(self):  # TODO : testme
        """
        Computes and returns an exact copy of new objects of self.
        """
        return copy.deepcopy(self)

    def getSpine(self):  # TODO : implement me
        result = []
        return result

    def isEmpty(self):
        return not (self.isLexicalLeaf or (len(self) > 0))

    def isLeaf(self):
        return (self.isLexicalLeaf or self.isEmpty())


def tolist(tree, result=None, lvl=0):
    if result is None:
        result = []
    result.append(tree, lvl)
    for c in tree:
        tolist(c, result, lvl + 1)
    return result
