# -*- coding: utf-8 -*-
"""
Created on 16.03.2016

@author: Benjamin Kosmehl
"""
import re
import logging
import pickle
import Util


class TAGLexiconReader(object):
    """
    Tree-adjoining grammar lexicon reader.
    """

    LINEPATTERN = re.compile(
        r'^([0-9]+)\s+(\S+)\s+(\w{3})\s+(\(.+\))\s*$', re.UNICODE)
    """
    LINEPATTERN: parses lexicon lines to extract tree data
    
    The four resulting groups are:
      (1)  tree heuristics as number: i.e. 5
      (2)  lexical anchor of the tree as string: i.e. 'Land'
      (3)  type of tree as string: ARG for initial tree, ADJ for auxiliary tree and MOD for modifier
      (4) complete tree string in bracketing format: (NE-PNC^null_x Lidl<>)
    """
    TREESTRINGPATTERN = re.compile(r'^\(.+\)$', re.UNICODE)

    def __init__(self, lexCls, treeCls):
        """
        Constructor

        Args:
            lexCls: lexicon class
            treeCls: tree class
        """
        self.lexType = lexCls
        self.treeType = treeCls
        self.lex = None

    def getTree(self, treeString):
        """
        Recursively extract the a tree node string from a given input string.
        
        Loops over all characters in the given string. Each character encountered is saved.
        If an opening bracket is encountered enters one level of recursion for child nodes.
        Creates tree node after encountering a closing bracket and returns one level or 
        completes if string is completely processed.
        
        Args:
            treeString: the tree data input as string
        """
        i = 0

        def getInnerTrees(treeS):
            nonlocal i # uses non-local index to keep track at which point the processing is in the string 
            result = []
            isopen = False
            r = ""
            t = None
            while (i < len(treeS)):
                c = treeS[i]
                if isopen:
                    if c == Util.Util.BO:
                        t = t if t else self.treeType(r, [])
                        t.extend(getInnerTrees(treeS))
                        i = i + (treeS.find(Util.Util.BC, i) - i)
                    elif c == Util.Util.BC:
                        t = t if t else self.treeType(r, [])
                        result.append(t)
                        break
                    else:
                        r += c
                elif c == Util.Util.BO:
                    isopen = True
                i += 1
            return result
        return getInnerTrees(treeString)

    def process(self, lexLine):
        """
        Creates a PLTAGTree tree out of the given lexicon file line and stores it to the lexicon object. 
        
        Args:
            lexLine: the line of text of the lexicon file as string
        """
        m = self.LINEPATTERN.match(lexLine)
        if m:
            ts = m.group(4)
            comply = self.TREESTRINGPATTERN.match(ts)
            if comply:
                t = self.getTree(ts)
                if t:
                    if len(t) > 1:
                        logging.error(
                            "Lexicon tree entry has more than 1 root node: %s\nFor line [%s]", str(t), lexLine)
                    else:
                        t[0].setAsCurrentRoot(m.group(3))
                        predictionOrdigit = m.group(1)
                        if predictionOrdigit.isdigit():
                            predictionOrdigit = int(predictionOrdigit)
                        self.lex.compatibleAppending(
                            m.group(2), (predictionOrdigit, t[0]))
                else:
                    logging.warning("getTree returned empty for: %s", ts)
            else:
                logging.warning("Line has no valid tree group: %s", ts)
        else:
            logging.warning(
                "Line failed to comply with expected line pattern: %s", lexLine)

    def convertTAGLexiconToPython(self, fileName):
        """
        Converts lexicon in given file to PLTAGTree objects and stores them into a TAG lexicon object.

        Args:
            fileName: the file name of the lexicon file to be read in

        Returns:
            created lexicon object
        """
        f = open(
            fileName, 'r', encoding=Util.Util.getConfigEntry()['encoding'])
        self.lex = self.lexType()
        for line in f:
            self.process(line)
        logging.info("Length of lexicon: %s", len(self.lex))
        f.close()
        return self.lex

    def pickleLexicon(self, fileName):
        """
        Pickles the currently loaded lexicon into serial format and stores it under given file name.
        
        Args:
            fileName: the file name for the resulting pickeled lexicon
        """
        if self.lex is None:
            logging.error(
                "Lexicon not yet compiled - use convertTAGLexiconToPython first.")
            return
        f = open(fileName, 'wb')
        pickle.dump(self.lex, f)
        f.close()
