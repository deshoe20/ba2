# -*- coding: utf-8 -*-
"""
Created on 04.01.2016

@author: Albert
"""

from os import path
import pickle
from configparser import ConfigParser
import inspect
import logging
from Enum import ConfigType
import PLTAGTree
import ElementaryLexicon
import TAGLexiconReader
import PredictionLexicon


class Util(object):
    """
    classdocs
    """
    _profileT = ConfigType.DEFAULT
    _loadedconfig = None
    _tlexicon = None
    _plexicon = None
    BO = '('
    BC = ')'

    def __init__(self, params):
        """
        Constructor
        """

    i = 0

    @staticmethod
    def uid():
        result = Util.i
        Util.i += 1
        return result

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
                logging.warning(
                    "%s class file was recently changed and is newer than pickled lexicon version!", treeCls.__name__)
                changed = True
            if tmpEleLex > tmpLex:
                logging.warning(
                    "%s class file was recently changed and than pickled lexicon version!", lexCls.__name__)
                changed = True
        else:  # no lexicon compiled yet
            logging.warning("Pickled lexicon not found!")
            changed = True
            r = True
        if changed and r:
            logging.warning(
                "Reloading %s - this may take a while ...", lexCls.__name__)
            reader = TAGLexiconReader.TAGLexiconReader(lexCls, treeCls)
            reader.convertTAGLexiconToPython(rawLexPath)
            reader.pickleLexicon(lexPath)
            logging.warning("... finished reloading %s", lexCls.__name__)

    @staticmethod
    def loadElementaryLexicon(reloadIfChanged=False):
        rawLexPath = "../res/freq-parser-lexicon-tag.txt"
        lexPath = "../res/pickeledTAGlexicon.pick"
        pltagTreeCls = PLTAGTree.PLTAGTree
        eleLexCls = ElementaryLexicon.ElementaryLexicon
        Util._reloadIfChanged(
            reloadIfChanged, lexPath, rawLexPath, pltagTreeCls, eleLexCls)
        return Util.loadLexicon(lexPath)

    @staticmethod
    def loadPredictionLexicon(reloadIfChanged=False):
        rawLexPath = "../res/freq-parser-lexicon-prediction.txt"
        lexPath = "../res/pickeledTAGPredictionlexicon.pick"
        pltagTreeCls = PLTAGTree.PLTAGTree
        eleLexCls = PredictionLexicon.PredictionLexicon
        Util._reloadIfChanged(
            reloadIfChanged, lexPath, rawLexPath, pltagTreeCls, eleLexCls)
        return Util.loadLexicon(lexPath)

    @staticmethod
    def loadLexicon(fileName):
        if not path.exists(fileName):
            logging.error(
                "\"%s\" not found - maybe not yet compiled", fileName)
        f = open(fileName, 'rb')
        try:
            lex = pickle.load(f)
        except Exception as e:
            logging.error(
                "Something went wrong loading pickled lexicon - maybe class-files changed since last compile?: %s", e)
        f.close()
        return lex

    @staticmethod
    def setConfigProfile(profileType):
        Util._profileT = profileType

    @staticmethod
    def getConfigEntry(profileType=None):
        if Util._loadedconfig is None:
            Util._loadedconfig = ConfigParser()
            Util._loadedconfig.read("../res/_loadedconfig.ini")
            Util._loadedconfig = Util._loadedconfig[
                str(Util._profileT if profileType is None else profileType)]
        return Util._loadedconfig
