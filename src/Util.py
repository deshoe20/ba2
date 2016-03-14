"""
Created on 04.01.2016

@author: Albert
"""

import pickle
from Enum import ConfigType
from configparser import ConfigParser
from os import path
import inspect
import PLTAGTree
import ElementaryLexicon
import logging

class Util(object):
    """
    classdocs
    """
    profileT = ConfigType.DEFAULT
    profile = None
    tlexicon = None
    plexicon = None
    BO = '('
    BC = ')'

    def __init__(self, params):
        """
        Constructor
        """
    
    i = 0;
    @staticmethod
    def uid():
        result = Util.i
        Util.i += 1 
        return result;
    
    @staticmethod
    def objMatch(cls, s):
        return getattr(cls, s.upper(), None)
    
    @staticmethod
    def loadElementaryLexicon():
        lexPath = "../res/pickeledTAGlexicon.pick"
        pltagTreeCls = inspect.getfile(PLTAGTree.PLTAGTree)
        eleLexCls = inspect.getfile(ElementaryLexicon.ElementaryLexicon)
        tmpLex = path.getmtime(lexPath)
        tmpPLTAGTree = path.getmtime(pltagTreeCls)
        tmpEleLex = path.getmtime(eleLexCls)
        if tmpPLTAGTree > tmpLex:
            logging.warn("PLTAGTree class file was recently changed and is newer than pickled lexicon version!")
        if tmpEleLex > tmpLex:
            logging.warn("ElementaryLexicon class file was recently changed and than pickled lexicon version!")         
        return Util.loadLexicon(lexPath, 'rb')
    
    @staticmethod
    def loadPredictionLexicon():
        return Util.loadLexicon("../res/pickeledTAGPredictionlexicon.pick", 'rb')
    
    @staticmethod
    def loadLexicon(fileName):
        if not path.exists(fileName):
            logging.error("\"{}\" not found - maybe not yet compiled".format(fileName))
        f = open(fileName, 'rb')
        try:
            lex = pickle.load(f)
        except Exception as e:
            logging.error("Something went wrong loading pickled lexicon - maybe class-files changed since last compile?: {}".format(e))
        f.close()
        return lex
    
    @staticmethod
    def setConfigProfile(profileType):
        Util.profile = profileType
    
    @staticmethod
    def getConfigEntry(profileType = None):
        if Util.profile is None:
            Util.config = ConfigParser().read("../res/config.ini")[Util.profile if profileType is None else profileType]
        return Util.config
        
    
        