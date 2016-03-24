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
    classdocs
    """

    def __init__(self, text=None):
        """
        Constructor
        """
        self.LEX = Util.loadElementaryLexicon(True)
        self.LEX.sortMe()
        self.PRED = Util.loadPredictionLexicon(True)
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
        logging.debug("Sentence: {}\t{} tokens found: {}".format(
            sentence, len(tokens), str(tokens)))
        #self.cache.add(Util.uid(), tokens)
        prefixTrees = None
        for i in range(len(tokens)):
            newWord = tokens[i]
            eTs = [x[1] for x in self.LEX[newWord]]  # list of elementaryTree
            logging.debug(
                "Found {} elementary trees for word \"{}\"".format(len(eTs), newWord))
            if len(eTs) == 0:
                logging.warning(
                    "Cannot find any elementary tree for: %s" % newWord)
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
                        "New stack size (approximately): {}".format(len(prefixTrees)))
                else:
                    logging.error(
                        "Failed to find any compatible tree to integrate {}".format(newWord))
        logging.info("Parsed sentence {} in {} seconds".format(
            sentence, str(timeit.default_timer() - t1)))
        logging.debug("Three random parse elements:\n{}\n{}\n{}".format(str(prefixTrees[random.randint(0, len(prefixTrees))]), str(
            prefixTrees[random.randint(0, len(prefixTrees))]), str(prefixTrees[random.randint(0, len(prefixTrees))])))
        return result

    def tryTntegrateTrees(self, prefixTree, canonicalTrees):
        """
        integrate
        if none remove
        """
        results = Queue()
        scanThreads = []
        result = []
        for cT in canonicalTrees:
            logging.debug("Trying to add tree {} to current fringe {} on current prefix tree {}".format(
                str(cT), str(prefixTree.getCurrentFringe()), str(prefixTree)))
            scanThreads.append(PrefixTreeScanParser(prefixTree, cT, results))
            scanThreads[-1].start()
        for t in scanThreads:
            t.join()
        while(not results.empty()):
            result.append(results.get())
        return result
