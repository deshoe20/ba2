'''
Created on 04.01.2016

@author: Albert
'''
from nltk.tree import Tree
from nltk.tokenize import sent_tokenize, word_tokenize
from Util import Util

class PLTAGParser(object):
    '''
    classdocs
    '''
    

    def __init__(self, params):
        '''
        Constructor
        '''
        
        
    def parseText(self, text):
        result = []
        sentences = sent_tokenize(text, Util.getLang())
        for sent in sentences:
            result.append(self.parseSentence(sent))
        return result
    
    def parseSentence(self, sentence):
        result = Tree("s")
        tokens = word_tokenize(sentence, Util.getLang())
        #self.cache.add(Util.uid(), tokens)
        for token in tokens:
            #PrefixTreeScanParser.parse(result, token)
            result = []
        return result
    
    