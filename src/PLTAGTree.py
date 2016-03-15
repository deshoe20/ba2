"""
Created on 04.01.2016

@author: Albert
"""
from nltk import tree
import re
import logging
from Enum import MorphCase, NodeType
import copy
import Util
from builtins import isinstance
from TAGTreeUI import TAGTreeUI


class PLTAGTree(tree.Tree):
    """
    Psycholinguistically Motivated Tree-Adjoining Grammar Tree
    implemented after the works of Vera Demberg (Saarland University), Frank Keller (University of Edinburgh) and Alexander Koller (University of Potsdam):
    'Incremental, Predictive Parsing with Psycholinguistically Motivated Tree-Adjoining Grammar' (2013)
    
    Imported tree data and therefore the datamodel of this PLTAG trees class is heavily based on the work of Miriam Kaeshammer (Saarland University):
    'A German Treebank and Lexicon for Tree-Adjoining Grammars' (2012)
    Which in turn is based on the therein used TIGER treebank (http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger.en.html).
    
    Technically this class inherits from python data structure 'list' via its direct inheritance from the nltk.tree.Tree class:
    Natural Language Toolkit: Text Trees
    Copyright (C) 2001-2015 NLTK Project
    Author: Edward Loper <edloper@gmail.com>
            Steven Bird <stevenbird1@gmail.com>
            Peter Ljunglöf <peter.ljunglof@gu.se>
            Nathan Bodenstab <bodenstab@cslu.ogi.edu> (tree transforms)
    URL: <http://nltk.org/>
    Its redistributed and modified here under its license (http://www.apache.org/licenses/LICENSE-2.0) by Benjamin Kosmehl

    The PLTAG describes a set of methods and rules for combining phrase structure trees as an approach for human language-processing modeling.
    PLTAG trees can be combined with each other using the substitution, adjunction or verification method.
    While substitution and adjunction are also defined in 'normal' TAG, the verification method is chief in this grammar variation.
    Correctly implemented (yet to be tested) it is used to verify as predicted marked structure with the corresponding tree structure of a newly encountered word.
    Trees can be displayed using tkinter and nltk code.
    Every tree of this class can at the same time be a node as it is composed of PLTAG trees as children or parent. 
    As its a list of trees and a tree in itself. Inherited from its superclass it consists basically of a list with a label.
    THe PLTAG trees have in addition to that its subsequent methods of the grammar and additional feature data.

    ToDoNotes:
    remove str catch in loops and therefore override draw
    solve the reflexive changes problem through appropriate cloning 
    too much documentation
    """

    THEONEPATTERN = re.compile('^([^\-]+)(\-([^\[\$]+)(\[([^\]\$]+)\])?(\$.*\$)?)?\^([^_]+)_([\S]+)(\s+(.+)<>)?(\s+-)?\s*$', re.UNICODE)
    """
    THEONEPATTERN: parses tree data strings for one single tree node
    
    example strings: NP-SB[nom]^x_null!    or    *T1*-DA^1_1 -    or    S-CJ$$NP-SB[nom]$$$$VVFIN-HD$$$$NP-OA[acc]$$^null_1      or    CARD-NK^x_x 1493<>
    
    In the following are listed the different extraction groups - but it should be noted that not all groups in the regex are listed as some are merely functional: 
      the leading number in brackets is the regex internal group number used in code - the trailing phrase 'if any' marks an optional group
      (1) the pattern begins with the group for the character before the first minus sign encountered atleast one character: i.e. 'NP', 'S' or *T1*
      (3) next group is the characters till the opening square brackets if any: i.e. 'SB' or 'HD'
      (5) followed by the group for the morphological information of the node in square brackets also if any: i.e. 'nom' or 'acc'
      (6) followed sometimes by a group for the secondary edge marker node information between '$'-symbols if any: i.e. $$NP-SB[nom]$$
      next is the upper and lower node half marking for each node - the second consistent
      (7) the first group for the upper marking stands between a '^' and the underscore - possible group value is: 'null', 'null!', 'null*', a digit or 'x'
      (8) the second group for the lower marking between the underscore and some whitespace - it has the same possible values as above:  'null', 'null!', 'null*', a digit or 'x'
      (10) the second to last group is anything before the '<>' lexical leaf marking - the lexical payload as such - if any: i.e. 'liebe', '1493' or '20-Milliarden-Mark-Defizits'
      (11) the last group is a possible minus sign in case of a trace if any: i.e. '-'
    Please note that all phrasal/functional codes (like 'NP', 'HD' or 'VVFIN') are a compilation from GOLD tags and those of the TIGER treebank: 
    (http://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/TagSets/stts-table.html)
    For further in-depth information please refer to Kaeshammer (2012) mentioned above.
    """

    def __init__(self, nodeString, children=None):
        """
        Constructor
        
        Args:
            nodeString: string data for the tree to be constructed out of (i.e. 'VVPP-HD^x_x abgeklärt<>')
            children: list of trees to be appended to self
        
        Returns:
            self
        """
        #(VP-HD^null_x (VP-HD^x_null* )(VP-*T2*-RE^x_x (PP-*T1*-OP^x_null! )(VP-HD^x_x (NP-OA[acc]^x_null! )(VP-HD^x_x (VP-OC^x_null! )(VP-HD^x_x (VZ-HD^x_x (PTKZU-PM^x_null! )(VZ-HD^x_x (VVINF-HD^x_x lassen<>))))))))
        if isinstance(nodeString, str):
            # get phrasal category and set it as label for this tree
            m = self.__class__.THEONEPATTERN.match(nodeString)
            if m:
                super().__init__(m.group(1), children)

            else:
                logging.error(
                    "Failed to extract valid tree from string: %s" % nodeString)
                #raise RuntimeError("No valid category found for %s" % s)
                return
            self.init()
            self.process(m)
        else:
            super().__init__(nodeString, children)

    def init(self):
        """
        Initialize instance fields.
        """
        # morphological information i.e. nom (->nominative), gen (->genitive), acc
        # (->accusative) or dat (->dative)
        self.morph = MorphCase.UNDEF
        self.nodeType = NodeType.UNDEF  # current status of the node
        self.isCurrentRoot = False # the root node has no further parent nodes above it
        self.upperNodeHalf = None # prediction or node status marking for the upper half of the current node
        self.lowerNodeHalf = None # prediction or node status marking for the lower half of the current node

    def process(self, match):
        """
        Parses the given tree string to fill in data fields.
        
        Args:
            match: regex match of the one pattern against the given tree string
        """
        # functionalCategory = match.group(3)  # TODO : REMOVE ME
        morphologicalInfo = match.group(5)
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

    def adjunction(self, other, markAsPredicted=False):
        """
        Adjoins the PLTAGTree other onto self. Adds other children to self and self children to the corresponding foot node in other.
        Blank adjoin - meaning checkup for validity and correctness should be in the calling method.
        
        Args:
            other: the tree to be adjoined onto self (should have a appropriate foot node)
        """
        n = other._fetchAdjunctionFoot()
        if n is None:
            logging.error(
                "Adjunction failed - could not find corresponding node in %s" % str(other))
            #raise RuntimeError("Adjunction failed - could not find corresponding node in %s" % str(self))
        elif n.nodeType is NodeType.FOOT:
            c = []
            if markAsPredicted:
                # mark the adjoined subtree and the lower node half of the
                # current node
                self.lowerNodeHalf = other.mark()
            c.extend(self)
            self.clear()
            self.extend(other)
            self.nodeType = NodeType.INNER
            if (n.label().endswith("*")):
                n.set_label(n.label()[:-1])
            n.extend(c)
            n.nodeType = NodeType.INNER  # TODO : hug erm debug me
        else:
            logging.warn(
                "Can't adjoin on tree node with type: %s" % self.nodeType)

    def _fetchAdjunctionFoot(self, root=None):
        """
        Utility method to recursively fetch the foot/leaf node that matches the calling trees root.
        Used in adjunction to append the lowered subtree.
        
        Args:
            root: optional define the node that should be used to look for a matching leaf
            
        Returns:
            the matching foot/leaf node
        
        """
        result = None
        root = self if root is None else root
        if self.isLeaf() and self.match(root, True):
            result = self
        else:
            for c in self:
                if not isinstance(c, str):
                    result = c._fetchAdjunctionFoot(root)
                    if result is not None:
                        break
        return result

    def substitution(self, other, markAsPredicted=False):
        """
        Substitutes the PLTAGTree other onto self if possible. Therefore checking if self is of NodeType.SUBST. 
        Does not check for correct morphological information or correct structure of the tree to join. 
        This should be done in the calling method if required.
        Blank substitution - meaning checkup for validity and correctness should be in the calling method.
        
        Args:
            other: the PLTAG tree to be substituted
            markAsPredicted: whether or not the substituted node should be marked as predicted
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

    def findFirstMarker(self, other=None, exclude=[]):
        """
        Searches for the first occurrence of a marked node and returns marker integer value or none.
        
        Args:
            other: optional node which the first found node in self should match
            exclude: optional parameter takes a list of integer to be excluded as potential markers.
        """
        result = None
        # a possible first marked node must atleast match the other root label
        if (other is None) or self.match(other, True):
            # a prediction tree with Sonly one node does not make any sense
            if len(self) > 0:
                # the marker
                if isinstance(self.lowerNodeHalf, int) and (self.lowerNodeHalf != self.upperNodeHalf):
                    if self.lowerNodeHalf not in exclude:
                        result = self.lowerNodeHalf
        if result is None:
            for c in self:
                if not isinstance(c, str):
                    result = c.findFirstMarker(other, exclude)
                    if result is not None:
                        break
        return result

    def getNodesWithMarker(self, marker, level=0):
        """
        Recursively fetches all nodes with a given marker either at the lower or upper node half or both.
        The resulting list can be viewed as the tree nodes halves of a predicted subtree in their original order. 
        Only works with well marked trees i.e. via the mark method.
        
        Args:
            marker: integer value as identifier for predicted node halves in self
            level: not needed - will be used by the recursion
        
        Returns:
            list of tuple of found nodes and their corresponding level or an empty list if none could be found
        """
        result = []
        if ((self.lowerNodeHalf == marker) or (self.upperNodeHalf == marker)):
            result.append((self, level))
            level += 1 # is used in recursion for the children
        for c in self:
            if not isinstance(c, str):
                result.extend(c.getNodesWithMarker(marker, level))
        return result

    def findCorrespondence(self, other, marker):
        """
        A method.
        
        The overall functional aim of the this methods is to verify a predicted structure through a new word and adding this words structure.
        
        Method tries to compute a corresponding subtree in self to a given other tree regarding given marker marked nodes.
        Marked nodes are originally of one single prediction tree that got integrated with another tree. Further parsing 
        progress could then have scattered those marked node halves all over self. Could have. So taken out of the work of 
        Demberg, Keller and Koller (2013) there are some criteria to look for in order to establish a valid correspondence:
          - for every single node half in the other tree there must be a corresponding node half with marker in self
          - every of those node halves must occur in T(self) in the same order as in T(other) even if the halves got pushed apart 
            and are now part of different tree nodes (top to bottom and left to right criterium)
          - that means that for any two node halves h1 and h2, if h1 is above h2 in T(self), then the node half f(h1) is above 
            the node half f(h2) in T(other) on the vertical (f stands for the mapping) 
          - and on the horizontal for any two node halves h1 and h2, if h1 precedes h2, then f(h1) precedes f(h2)
          - for each node half h, the node labels of h and f (h) are the same
          - for each lower (upper) node half h, f(h) is also a lower (upper) node half
          - if a node u in T(other) has two halves and one half match something then the other half must also match something
          - from left to right and from upper to lower each tree node half mapping cannot be discontinuous
            --> this means that any node/half in T(other) that is not in T(self) can only be as children to the right of their 
            sibling(s) even if there are none - i.e. also nodes that are the only children of their parents
        So not every node half in T(other) has to match a node half in T(self). Only the other way round with the marked node 
        halves. Every node in T(other) that has no correspondence in T(self) is later added to T(self). They are added as 
        children to those nodes in T(self) where their last sibling correspondence was found. To put it technical: 
          - if some node u in T(other) with children u1, ..., un (from left to right) match a (lower) node half h, 
            and u1, ..., uk but not uk+1, ..., un match (upper) node halves in T(self) (i.e., upper node halves of children of h), 
            then the subtrees of T(other) below uk+1, ..., un are added to T(self) as the k + 1-st to n-th child of h.
        In addition to adding the non correlating nodes in T(other) to self all markers of the given marker are removed from self.
        (maybe it does all that) # TODO : remove
        
        For further documentation about PLTAG correspondence please refer to Demberg, Keller and Koller (2013).
        
        Args:
            other: the other tree structure used to verify the predicted sub tree structure in self
            marker: a given marker of all the marked nodes of the predicted sub tree in self
        
        Returns:
            True if a valid correspondence based on the given marker was found
            
        ToDo:
            Come up with additional valid loop breaks to find mismatching T(self) with T(other) early.
            
        """
        result = False
        # both self or rather only the nodes in self with marked node halves are converted into a list of tuple
        # each tuple consist of the respective node and the level the node is in its original tree
        # the serial processing of the lists fulfills the top to bottom and left to right criterium
        mN = self.getNodesWithMarker(marker) # self(of marker) as a list of tuple (#NODE, #LEVEL): i.e. mN[i][0] == someNode 
        oN = PLTAGTree.tolist(other) # other as a list of tuple (#NODE, #LEVEL): i.e. mN[i][1] == someLevel 
        upper = False # whether or not the current yet to be mapped node half is upper or lower - as it starts at the root it only has a lower
        i = 0 # iterator over the list of T(other)
        maxLvl = max([x[1] for x in mN]) # the maximal level depth in the to be verified tree in self
        possibleAddees = [] # list to store the found non correlating nodes in T(other) to be added to self upon success
        currentParent = [] # list to keep track which is the current parent - which is always currentParent[-1] if any
        currentLvl = 0 # current level in self(of marker) subtree
        for n in mN: # cycle through marked nodes in self top to bottom, left to right
            foundCorrelation = False # whether or not of n and oN[i] was found
            # removes the last parent node from list if a level change from lower to upper happened or a sibling of the last is the current parent node
            if (currentLvl != 0) and (n[1] <= currentLvl): 
                currentParent.pop()
            currentLvl = n[1]
            while(not foundCorrelation and (i < len(oN))): # cycles through nodes of T(other) as long as no complete correlation to n was found
                check = n[0].match(oN[i][0], True) and (currentLvl == oN[i][1]) # fulfillment of label and structure identity criteria
                if (upper and (n[0].upperNodeHalf == marker)): # check for marker if upper marker is search focus
                    if check:
                        # determine which kind of node half is expected next
                        if (oN[i][0].isLeaf() or (n[1] == maxLvl)):
                            i += 1
                        else:
                            upper = False
                        foundCorrelation = True
                    else:  # if node n is marked but oN[i] doesn't fit
                        # it means oN[i] should be added to self if correspondence for mN could be completed onwards
                        possibleAddees.append((currentParent[-1], oN[i]))
                        i += 1 # and try against next node in T(other)
                # verification tree mismatch
                elif (upper and (n[0].upperNodeHalf != marker and n[0].lowerNodeHalf == marker)) or ((not upper) and (n[0].upperNodeHalf == marker)):
                    logging.info("Verification tree mismatch for %s against marker %s and %s" % (str(self), str(marker), str(other)))
                    break
                if ((not upper) and (n[0].lowerNodeHalf == marker)): # check for marker if lower marker is search focus
                    if check:
                        upper = True
                        foundCorrelation = True
                    else: # see above
                        possibleAddees.append((currentParent[-1], oN[i]))
                    i += 1
            currentParent.append(n[0])
        else:  # loop finished successfully
            if oN[i][1] == maxLvl: # next unmatched node from other is on the same level as the last correspondence
                # add only those outstanding nodes on the same level as siblings of that last correspondence
                # as all additional nodes in oN then children of those added
                currentParent[-1].extend([x[0] for x in oN[i:] if x[1] == maxLvl])
            elif oN[i][1] == (maxLvl + 1): # next unmatched node from other is on the next level as the last correspondence
                # get only those nodes to append to self from other that are directly below the last corresponding node
                mN[-1][0].extend([x[0] for x in oN[i:] if x[1] == (maxLvl + 1)])
            for e in possibleAddees: # add all intermediately found unmatched nodes of T(other) to their already determined parent nodes in self
                e[0].append(e[1])
            self._removeMark(marker)
            result = True
        return result

    def verify(self, other):
        """
        PLTAG verify method. 
        Used to verify a previously predicted structure/subtree with the structure provided by a newly encounter word during parsing.
        In order to verify this method tries to find a correspondence of a subtree in a tree to another tree.
        
        Therefore cycles through all possible integer markers found in self tree structure (all children and children's children).
        Tries to establish a corresponding correlation with each marker found in turn. 
        Does that till no more markers could be found or a valid correspondence appears.
        If a valid correspondence (see findCorrespondence doc) is found the completion of the verification process is also done 
        inside the findCorrespondence method due to local availability of parameters needed.
        
        For further documentation about PLTAG verification please refer to Demberg, Keller and Koller (2013).
        
        Returns:
            True if a corresponding subtree could be found and verification completed successfully
        """
        markers = []
        result = False
        # implicit test for result is None as in no new not yet tested markers could be found overall
        while(not result and (markers[-1] if len(markers) > 0 else True)):
            marker = self.findFirstMarker(other, markers)
            result = self.findCorrespondence(other, marker)
            markers.append(marker)
        return result

    def match(self, other, ignoreAffix=False):  # TODO : implement me
        """
        Matches this tree node with a given other to check if they are similar enough to be considered equal.
        
        Args:
            other: the other PLTAG tree node to be tried for a match
            ignoreAffix: optional whether or not a possible affix '!' or '*' regarding the node label should be ignored
            
        Returns:
            True if self matches other with the given conditions
        """
        result = False
        if (ignoreAffix):
            trimmedSelfLabel = self.label()[:-1] if (self.label().endswith("!") or self.label().endswith("*")) else self.label()
            trimmedOtherLabel = other.label()[:-1] if (other.label().endswith("!") or other.label().endswith("*")) else other.label()
            result = (trimmedSelfLabel == trimmedOtherLabel)
        else:
            result = self.label() == other.label()
        return result

    def mark(self, marker=None):
        """
        Sets all node halves of this tree to a common marker.
        Sets only the lower node half of the first/root node and only the upper for each leaf or more 
        specifically each child without children of its own or only lexical payload.
        
        Args:
            marker: optional integer value to be used to mark this tree - will be Util.uid if none given
            
        Returns:
            the marker used for marking this tree
        """
        markedRoot = False
        if marker is None:
            marker = Util.Util.uid()
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
        """
        Removes all given marker marker from each node half in self and recursively from our children.
        
        Args:
            marker: integer value to be removed from this PLTAG tree
        """
        self.upperNodeHalf = 'x' if self.upperNodeHalf == marker else self.upperNodeHalf
        self.lowerNodeHalf = 'x' if self.lowerNodeHalf == marker else self.lowerNodeHalf
        for c in self:
            if not isinstance(c, str):
                c._removeMark(marker)

    def hasNoMarkers(self):
        """
        Determines whether or not this tree has any markings on its node halves.
        
        Returns:
            True if no marker has been found on this node and its children
        """
        result = True
        if (isinstance(self.upperNodeHalf, int) or isinstance(self.lowerNodeHalf, int)):
            result = False
        else:
            # its 05:30 a.m. and i got an error with string here - gn8
            for c in self:
                if not isinstance(c, str):
                    result = c.hasNoMarkers()
                    if not result:
                        break
        return result

    def hasNoMarker(self):
        """
        Determines whether or not this node without regard to any children has a marking.
        
        Returns:
            True if no marker has been found on either node half of self
        """
        return not (isinstance(self.upperNodeHalf, int) or isinstance(self.lowerNodeHalf, int))

    def getCurrentFringe(self):
        """
        Computes the fringe starting at the rightmost lexical leaf to either the next non lexical leaf or the root node.
        Searches for conditions met in the reversed list of all fringes of the self tree.
        
        Returns:
            list of PLTAGTree nodes
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
            if type(c) is not PLTAGTree:
                break  # the string of a lexicalLeaf
            result.extend(c.getFringes())
        result.append((self, True))
        return result

    def clone(self):  # TODO : testme
        """
        Computes and returns an exact copy of new objects of self.
        
        Returns:
            deep copy of self
        """
        return copy.deepcopy(self)

    def getSpine(self):  # TODO : implement me
        result = []
        return result

    def isEmpty(self):
        return not (self.isLexicalLeaf() or (len(self) > 0))

    def isLeaf(self):
        return self.isEmpty()

    def isLexicalLeaf(self):
        return True if ((len(self) == 1) and isinstance(self[0], str)) else False

    def draw(self):
        TAGTreeUI(self).mainloop()

    @staticmethod
    def tolist(tree, lvl=0):
        """
        Transforms a given PLTAG tree into a top to bottom, left to right representation of itself.
        First item is the root node then roots first child then roots first child first child and so on.
        
        Args:
            tree: the PLTAG tree to be transformed with its children and children's children
            lvl: optional depth level of recursion into the tree
        """
        result = []
        result.append((tree, lvl))
        for c in tree:
            if not isinstance(c, str):
                result.extend(PLTAGTree.tolist(c, lvl + 1))
        return result
