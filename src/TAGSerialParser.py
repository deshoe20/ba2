# -*- coding: utf-8 -*-
"""
Created on 10.04.2016

@author: Benjamin Kosmehl
"""
from nltk.tokenize import sent_tokenize, word_tokenize
from Util import Util
import logging
import timeit
from queue import Queue
from PrefixTreeScanParser import PrefixTreeScanParser


class TAGSerialParser(object):
    """
    Some tag serial parser class.
    """
    
    def __init__(self, text=None):
        """
        Constructor
        
        Args:
            text: optional text to be parsed 
        """
        self.LEX = Util.getELEX()
        self.LEX.sortMe()
        self.parseText(text)
        #TODO: insert try counter

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
        Tries to compute parse tree for a given sentence not using the PLTAG formalism.
        
        Args:
            sentence: the sentence to be parsed as string
            
        Returns:
            list of PLTAGTree as parse tree for given input or None if none could be found
        """
        t1 = timeit.default_timer()
        tokens = word_tokenize(sentence, Util.getConfigEntry()['language'])
        logging.debug(
            "Sentence: %s\t%d tokens found: %s", sentence, len(tokens), str(tokens))
        result = self.parseTokens(tokens, 0)
        logging.info("Parsed sentence %s in %s seconds",
                     sentence, str(timeit.default_timer() - t1))
        logging.debug("Resulting parse tree:\n%s", str(result))
        return result

    def parseTokens(self, tokens, tokensIndex, prefixTree=None):
        """
        Recursively parses list of tokens into prefixTree.
        
        Args:
            tokens: list of string
            tokensIndex: index for tokens list
            prefixTree: the current prefix tree
            
        Returns:
            parse tree as PLTAGTree
        """
        result = None
        eTs = [x[1] for x in self.LEX[tokens[tokensIndex]]]
        for eT in eTs:
            if prefixTree is None:
                result = self.parseTokens(tokens, tokensIndex + 1, eT)
            else:
                q = Queue()
                t = PrefixTreeScanParser(prefixTree, eT, q)
                t.start()
                t.join()
                if not q.empty():
                    if tokensIndex == (len(tokens) - 1):
                        result = q.get()
                    else:
                        result = self.parseTokens(tokens, tokensIndex + 1, q.get())
            if result is not None:
                break
        else:
            logging.warning(
                "Failed to find any compatible tree to integrate %s", tokens[tokensIndex])
        return result
