# -*- coding: utf-8 -*-
"""
Created on 16.03.2016

@author: Benjamin Kosmehl
"""
from nltk.tokenize import sent_tokenize, word_tokenize
from Util import Util
import logging
import timeit
from queue import Queue
from PrefixTreeScanParser import PrefixTreeScanParser
import random


class PLTAGParser(object):
    """
    Psycholinguistically Motivated Tree-Adjoining Grammar Parser

    Loops through everything trying to get the parse tree.
    
    CLASS UNDER CONSTRUCTION
    """

    def __init__(self, text=None):
        """
        Constructor
        
        Args:
            text: optional text to be parsed 
        """
        self.LEX = Util.getELEX()
        self.LEX.sortMe()
        if text is not None:
            self.parseText(text)

    def parseText(self, text):
        """
        Tries to compute parse trees for given input text.
        
        Args:
            text: text to be parsed
            
        Returns:
            text parse trees as list of sentence parse trees - list of PLTAGTree
        """
        result = []
        sentences = sent_tokenize(text, Util.getConfigEntry()['language'])
        for sent in sentences:
            result.append(self.parseSentence(sent))
        return result

    def parseSentence(self, sentence):
        """
        Tries to compute parse tree for a given sentence using the PLTAG formalism.
        
        Args:
            sentence: the sentence to be parsed as string
            
        Returns:
            list of PLTAGTree as parse tree for given input or None if none could be found
        """
        t1 = timeit.default_timer()
        result = None
        tokens = word_tokenize(sentence, Util.getConfigEntry()['language'])
        logging.debug("Sentence: %s\t%d tokens found: %s",
                      sentence, len(tokens), str(tokens))
        #self.cache.add(Util.uid(), tokens)
        prefixTrees = None
        for i in range(len(tokens)):
            newWord = tokens[i]
            # list of elementaryTree - no copy here!
            eTs = [x[1] for x in self.LEX[newWord]]
            logging.debug(
                "Found %d elementary trees for word \"%s\"", len(eTs), newWord)
            if len(eTs) == 0:
                logging.warning(
                    "Cannot find any elementary tree for: %s", newWord)
                break  # TODO: use default
            elif prefixTrees is None:
                prefixTrees = eTs
            else:
                newPrefixTrees = []
                threads = []
                resultsQue = Queue()
                for pT in prefixTrees:
                    threads.extend(self.tryTntegrateTrees(pT, eTs, resultsQue))
                for t in threads:
                    t.join()
                while(not resultsQue.empty()):
                    newPrefixTrees.append(resultsQue.get())
                if len(newPrefixTrees) > 0:
                    prefixTrees = self.prune(newPrefixTrees)
                    logging.info("New stack size: %d", len(prefixTrees))
                    
                else:
                    logging.error(
                        "Failed to find any compatible tree to integrate %s", newWord)
        logging.info("Parsed sentence %s in %s seconds",
                     sentence, str(timeit.default_timer() - t1))
        if len(prefixTrees) > 1:
            logging.debug("Three random parse elements:\n%s\n%s\n%s", str(prefixTrees[random.randint(0, len(prefixTrees))]), str(
                prefixTrees[random.randint(0, len(prefixTrees))]), str(prefixTrees[random.randint(0, len(prefixTrees))]))
            result = prefixTrees[random.randint(0, len(prefixTrees))] # here you go
        return result

    def tryTntegrateTrees(self, prefixTree, elementaryTrees, que):
        """
        Tries to integrate a given set of trees with a given prefix tree.
        Creates and starts a thread per try.
        
        Args:
            prefixTree: the prefix tree to be fixed up
            elementaryTrees: list of PLTAGTree to be tried
            que: asynchronous Queue object to hold return values
            
        Returns:
            started threads as PrefixTreeScanParser objects
        """
        scanThreads = []
        for cT in elementaryTrees:
            logging.debug("Trying to add tree %s to current fringe %s on current prefix tree %s",
                          str(cT), str(prefixTree.getCurrentFringe()), str(prefixTree))
            scanThreads.append(PrefixTreeScanParser(prefixTree, cT, que))
            scanThreads[-1].start()
        return scanThreads
    
    def prune(self, prefixTrees):
        """
        Collects all trees with the same current fringe in one position and filters out redundant trees.
        
        Args:
            prefixTrees: prefix trees as list of PLTAGTree
            
        Returns:
            pruned prefix trees as list of PLTAGTree
        """
        # implement me
        return prefixTrees
