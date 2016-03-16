# -*- coding: utf-8 -*-
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
import TAGLexiconReader
import PredictionLexicon

class Util(object):
    """
    classdocs
    """
    profileT = ConfigType.DEFAULT
    config = None
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
    def _reloadIfChanged(r, lexPath, rawLexPath, treeCls, lexCls):
        pltagTreeClsPath = inspect.getfile(treeCls)
        eleLexClsPath = inspect.getfile(lexCls)
        if (path.isfile(lexPath)):
            tmpLex = path.getmtime(lexPath)
            tmpPLTAGTree = path.getmtime(pltagTreeClsPath)
            tmpEleLex = path.getmtime(eleLexClsPath)
            changed = False
            if tmpPLTAGTree > tmpLex:
                logging.warning("{} class file was recently changed and is newer than pickled lexicon version!".format(treeCls.__name__))
                changed = True
            if tmpEleLex > tmpLex:
                logging.warning("{} class file was recently changed and than pickled lexicon version!".format(lexCls.__name__))     
                changed = True
        else: # no lexicon compiled yet
            logging.warning("Pickled lexicon not found!")
            changed = True
            r = True
        if changed and r:
            logging.warning("Reloading {} - this may take a while ...".format(lexCls.__name__))
            reader = TAGLexiconReader.TAGLexiconReader(lexCls, treeCls)
            reader.convertTAGLexiconToPython(rawLexPath)
            reader.pickleLexicon(lexPath)
            logging.warning("... finished reloading {}".format(lexCls.__name__))
    
    @staticmethod
    def loadElementaryLexicon(reloadIfChanged = False):        
        rawLexPath = "../res/freq-parser-lexicon-tag.txt"
        lexPath = "../res/pickeledTAGlexicon.pick"
        pltagTreeCls = PLTAGTree.PLTAGTree
        eleLexCls = ElementaryLexicon.ElementaryLexicon
        Util._reloadIfChanged(reloadIfChanged, lexPath, rawLexPath, pltagTreeCls, eleLexCls)
        return Util.loadLexicon(lexPath)
    
    @staticmethod
    def loadPredictionLexicon(reloadIfChanged = False):        
        rawLexPath = "../res/freq-parser-lexicon-prediction.txt"
        lexPath = "../res/pickeledTAGPredictionlexicon.pick"
        pltagTreeCls = PLTAGTree.PLTAGTree
        eleLexCls = PredictionLexicon.PredictionLexicon
        Util._reloadIfChanged(reloadIfChanged, lexPath, rawLexPath, pltagTreeCls, eleLexCls)
        return Util.loadLexicon(lexPath)
    
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
        Util.profileT = profileType
    
    @staticmethod
    def getConfigEntry(profileType = None):
        if Util.config is None:
            Util.config = ConfigParser()
            Util.config.read("../res/config.ini")
            Util.config = Util.config[str(Util.profileT if profileType is None else profileType)]
        return Util.config
        
    
        