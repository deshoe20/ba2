# -*- coding: utf-8 -*-
"""
Created on 04.01.2016

@author: Albert
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
    
    loop horror:
        sent in text
            word in sent
                prefix tree out of all current prefix trees
                    for each elementary tree start thread
                        (additional layers for potential prediction tree combinations)
    --> (5 + prediction depth)-layer loop               
    
    """

    def __init__(self, text=None):
        """
        Constructor
        """
        self.LEX = Util.getELEX()
        self.LEX.sortMe()
        self.parseText(text)

    def parseText(self, text):
        result = []
        sentences = sent_tokenize(text, Util.getConfigEntry()['language'])
        for sent in sentences:
            result.append(self.parseSentence(sent))
        return result

    def parseSentence(self, sentence):
        t1 = timeit.default_timer()
        result = None
        tokens = word_tokenize(sentence, Util.getConfigEntry()['language'])
        logging.debug("Sentence: %s\t%d tokens found: %s", 
            sentence, len(tokens), str(tokens))
        #self.cache.add(Util.uid(), tokens)
        prefixTrees = None
        for i in range(len(tokens)):
            newWord = tokens[i]
            eTs = [x[1] for x in self.LEX[newWord]]  # list of elementaryTree #TODO: do you copy?
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
                for pT in prefixTrees:
                    newPrefixTrees.extend(self.tryTntegrateTrees(pT, eTs))
                if len(newPrefixTrees) > 0:
                    prefixTrees = newPrefixTrees
                    logging.info(
                        "New stack size (approximately): %d", len(prefixTrees))
                else:
                    logging.error(
                        "Failed to find any compatible tree to integrate %s", newWord)
        logging.info("Parsed sentence %s in %s seconds", sentence, str(timeit.default_timer() - t1))
        logging.debug("Three random parse elements:\n%s\n%s\n%s", str(prefixTrees[random.randint(0, len(prefixTrees))]), str(
            prefixTrees[random.randint(0, len(prefixTrees))]), str(prefixTrees[random.randint(0, len(prefixTrees))]))
        return result

    def tryTntegrateTrees(self, prefixTree, elementaryTrees):
        """
        integrate
        if none remove
        """
        results = Queue()
        scanThreads = []
        result = []
        for cT in elementaryTrees:
            logging.debug("Trying to add tree %s to current fringe %s on current prefix tree %s", 
                str(cT), str(prefixTree.getCurrentFringe()), str(prefixTree))
            scanThreads.append(PrefixTreeScanParser(prefixTree, cT, results))
            scanThreads[-1].start()
        for t in scanThreads:
            t.join() #TODO: move join one layer up
        while(not results.empty()):
            result.append(results.get())
        return result
