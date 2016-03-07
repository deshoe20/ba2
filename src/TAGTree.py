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
from builtins import isinstance


class TAGTree(tree.Tree):
    """
    classdocs
    
    TodoNotes:
    remove str catch in loops and override draw
    solve the reflexive changes problem through appropriate cloning 
    """

    morph = MorphCase.UNDEF
    nodeType = NodeType.UNDEF
    upperNodeHalf = None
    lowerNodeHalf = None
    isCurrentRoot = False

    # TODO : comment THEONEREGEX - ONE REGEX TO RULE THEM ALL! TO FIND THEM
    # ALL!
    THEONEPATTERN = re.compile(
        '^([^\-]+)(\-([^\[\$]+)(\[([^\]\$]+)\])?(\$.*\$)?)?\^([^_]+)_([\S]+)(\s+(.+)<>)?(\s+-)?\s*$', re.UNICODE)

    def __init__(self, node, children=None):
        """
        Constructor
        """
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
            elif lowerNodeHalfMarker.endswith('*'):
                self.nodeType = NodeType.FOOT
            self.set_label(self.label() + str(self.nodeType))
        # try to determine and extract lexical leaf data
        if lexicalPayload:
            self.append(lexicalPayload)

    def adjunction(self, other, markAsPredicted = False):
        """
        Adjoins the TAGTree other onto self. Adds other children to self and self children to the corresponding foot node in other.
        Blank adjoin - meaning checkup for validity and correctness should be in the calling method.
        """
        n = self._fetchAdjunctionFoot(other, self.get_label())
        if n is None:
            logging.error(
                "Adjunction failed - could not find corresponding node in %s" % str(other))
            #raise RuntimeError("Adjunction failed - could not find corresponding node in %s" % str(self))
        elif n.nodeType is NodeType.FOOT:
            c = []
            if markAsPredicted:
                self.lowerNodeHalf = other.mark() # mark the adjoined subtree and the lower node half of the current node
            c.extend(self)
            self.clear()
            self.extend(other)
            self.nodeType = NodeType.INNER                
            if (n.label().endswith("*")):
                n.set_label(n.label[:-1])
            n.extend(c)
            n.nodeType = NodeType.INNER  # TODO : hug erm debug me
        else:
            logging.warn(
                "Can't adjoin on tree node with type: %s" % self.nodeType)

    def _fetchAdjunctionFoot(self, other, label):
        result = None
        if other.isLeaf() and (other.get_label() == label):
            result = self
        else:
            for c in other:
                if result is not None:
                    logging.error(
                        "Adjunction restriction violation at %s" % str(other))
                    #raise RuntimeError("Adjunction restriction violation at %s" % str(self))
                result = c._gimmeLeafNodeWithLabel(label)
        return result

    def substitution(self, other, markAsPredicted = False):
        """
        Substitutes the TAGTree other onto self if possible. Therefore checking if self is of NodeType.SUBST. 
        Does not check for correct morphological information or correct structure of the tree to join. 
        This should be done in the calling method if required.
        Blank substitution - meaning checkup for validity and correctness should be in the calling method.
        """
        if self.nodeType is NodeType.SUBST:
            self.extend(other)
            if (self.label().endswith("!")):
                self.set_label(self.label()[:-1])
            if markAsPredicted:
                self.mark()
            if len(self) > 0:
                # changes node type to NodeType.INNER if substitution was
                # successful and at least one child was added.
                self.nodeType = NodeType.INNER
        else:
            logging.warn(
                "Can't substitute on tree node with type: %s" % self.nodeType)
            
    def findFirstMarker(self, other, exclude = []):
        """
        Searches for the first occurrence of a marked node and returns marker integer value or none.
        Optional parameter exclude takes a list of integer to be excluded as potential markers.
        """
        result = None
        if self.matches(other, True): # a possible first marked node must atleast match the other root label
            if len(self) > 0: # a prediction tree with Sonly one node does not make any sense
                if isinstance(self.lowerNodeHalf, int) and (self.lowerNodeHalf != self.upperNodeHalf): # the marker 
                    if self.lowerNodeHalf not in exclude:
                        result = self.lowerNodeHalf
        if result is None:
            for c in self:
                if not isinstance(c, str):
                    result = c.findFirstMarker(other, exclude)
                    if result is not None:
                        break
        return result
    
    def getNodesWithMarker(self, marker, level = 0):
        """
        
        """
        result = []
        if ((self.lowerNodeHalf == marker) or (self.upperNodeHalf == marker)):
            result.append((self, level))
            level += 1
        for c in self:
            if not isinstance(c, str):
                result.extend(c.getNodesWithMarker(marker, level)) 
        return result
    
    def findCorrespondence(self, other, marker):
        """
        Kill Me With Fire
        """
        result = False
        mN = self.getNodesWithMarker(marker) # only works with well marked trees i.e. via the mark method
        oN = TAGTree.tolist(other)
        upper = False
        i = 0
        maxLvl = max([x[1] for x in oN])
        possibleCorrelatingParent = []
        currentParent = []
        currentLvl = 0
        for n in mN:
            foundCorrelation = False
            if (currentLvl != 0) and (n[1] <= currentLvl):
                currentParent.pop()
            currentLvl = n[1]
            while(not foundCorrelation and (i < len(oN))):
                check = n[0].matches(oN[i][0], True) and (currentLvl == oN[i][1])
                if (upper and (n[0].upperNodeHalf == marker)):
                    if check:
                        if ((n[0].isLeaf() and oN[i][0].isLeaf()) or (n[1] == maxLvl)):
                            i += 1
                        else:
                            upper = False
                        foundCorrelation = True
                    else:
                        possibleCorrelatingParent.append((currentParent[-1], oN[i]))
                        i += 1
                elif (upper and (n[0].upperNodeHalf != marker and n[0].lowerNodeHalf == marker)) or ((not upper) and (n[0].upperNodeHalf == marker)): # verification tree mismatch
                        logging.info("Verification tree mismatch for %s against marker %s and %s" % (str(self), str(marker), str(other)))
                        break
                if ((not upper) and (n[0].lowerNodeHalf == marker)):
                    if check:
                        upper = True
                        foundCorrelation = True
                    else:
                        possibleCorrelatingParent.append((currentParent[-1], oN[i]))
                    i += 1
            currentParent.append(n[0])
        else: # loop finished successfully
            if oN[i][1] == maxLvl: 
                currentParent[-1].extend([x[0] for x in oN[i:] if x[1] == maxLvl])
            elif oN[i][1] == (maxLvl + 1):
                mN[-1].extend([x[0] for x in oN[i:] if x[1] == (maxLvl + 1)])
            for e in possibleCorrelatingParent:
                e[0].append(e[1])
            self._removeMark(marker)
            result = True            
        return result

    def verify(self, other):
        markers = []
        result = False
        while(not result and (markers[-1] if len(markers) > 0 else True)): # implicit test for result is None as in no new not yet tested markers could be found overall
            marker = self.findFirstMarker(other, markers)
            result = self.findCorrespondence(other, marker)
            markers.append(marker)
        return result

    def matches(self, other, onlyMarked = False):  # TODO : implement me
        result = False
        if (isinstance(self.upperNodeHalf, int) or isinstance(self.lowerNodeHalf, int)):
            trimmedSelfLabel = self.label()[:-1] if (self.label().endswith("!") or self.label().endswith("*")) else self.label()
            trimmedOtherLabel = other.label()[:-1] if (other.label().endswith("!") or other.label().endswith("*")) else other.label()
            result = (trimmedSelfLabel == trimmedOtherLabel)
        elif(not onlyMarked):
            result = self.label() == other.label()
        return result

    def mark(self, marker=None):
        markedRoot = False
        if marker is None:
            marker = Util.uid()
            markedRoot = True
        if not self.isLeaf():
            self.lowerNodeHalf = marker
        if not markedRoot:
            self.upperNodeHalf = marker
        for c in self:
            if not isinstance(c, str):
                c.mark(marker)
        return marker
            
    def _removeMark(self, marker):
        self.upperNodeHalf = 'x' if self.upperNodeHalf == marker else self.upperNodeHalf
        self.lowerNodeHalf = 'x' if self.lowerNodeHalf == marker else self.lowerNodeHalf
        for c in self:
            if not isinstance(c, str):
                c._removeMark(marker)
            

    def hasNoMarkers(self):
        result = True
        if (isinstance(self.upperNodeHalf, int) or isinstance(self.lowerNodeHalf, int)):
            result = False
        else:
            for c in self: # its 05:30 a.m. and i got an error with string here - gn8
                if not isinstance(c, str):
                    result = c.hasNoMarkers()
                    if not result:
                        break
        return result
    
    def hasNoMarker(self):
        return not (isinstance(self.upperNodeHalf, int) or isinstance(self.lowerNodeHalf, int))

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
            if (fs[ci][0].isCurrentRoot and fs[ci][1]) or (fs[ci][0].isLeaf() and not fs[ci][0].isLexicalLeaf() and not fs[ci][1]):
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
        return (self.isLexicalLeaf() or self.isEmpty())
    
    def isLexicalLeaf(self):
        return True if ((len(self) == 1) and isinstance(self[0], str)) else False

    @staticmethod
    def tolist(tree, result=None, lvl=0):
        if result is None:
            result = []
        result.append((tree, lvl))
        for c in tree:
            if not isinstance(c, str):
                TAGTree.tolist(c, result, lvl + 1)
        return result
