# -*- coding: utf-8 -*-
"""
Created on 14.03.2016

@author: Albert
"""
import re, logging, pickle
import Util

class TAGLexiconReader(object):
    """
    classdocs
    """
    LINEPATTERN = re.compile('^([0-9]+)\s+(\S+)\s+(\w{3})\s+(\(.+\))\s*$', re.UNICODE)
    TREESTRINGPATTERN = re.compile('^\(.+\)$', re.UNICODE)

    def __init__(self, lexCls, treeCls):
        """
        Constructor
        
        Args:
            lexCls: lexicon class
            treeCls: tree class
        """
        self.lexType = lexCls
        self.treeType = treeCls
            
        
    def getTree(self, s):
        i = 0
        def getInnerTrees(s):
            nonlocal i
            result = []
            isopen = False
            r = ""
            t = None
            while (i < len(s)):
                c = s[i]
                if isopen:
                    if c == Util.Util.BO:
                        t = t if t else self.treeType(r, [])
                        t.extend(getInnerTrees(s))
                        i = i + (s.find(Util.Util.BC, i) - i)
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
        return getInnerTrees(s)
    
    def process(self, l, lex):
        m = self.LINEPATTERN.match(l)
        if m:
            ts = m.group(4)
            comply = self.TREESTRINGPATTERN.match(ts)
            if comply:
                t = self.getTree(ts)
                if t:
                    if len(t) > 1:
                        logging.error("Lexicon tree entry has more than 1 root node: %s\nFor line [%s]" % (str(t), l))
                    else:
                        t[0].setAsCurrentRoot(m.group(3))
                        lex.compatibleAppending(m.group(2), (m.group(1), t[0]))
                else:
                    logging.warning("getTree returned empty for: %s" % ts)
            else:
                logging.warning("Line has no valid tree group: %s" % ts)
        else:
            logging.warning("Line failed to comply: %s" % l)
    
    def convertTAGLexiconToPython(self, fileName):
        f = open(fileName, 'r', encoding=Util.Util.getConfigEntry()['encoding'])
        self.lex = self.lexType()
        for line in f:
            self.process(line, self.lex)
        logging.info("Length of lexicon: %d" % len(self.lex))
        f.close()
        return self.lex
        
    def pickleLexicon(self, fileName):
        if self.lex is None:
            logging.error("Lexicon not yet compiled - use convertTAGLexiconToPython first.")
            return
        f = open(fileName, 'wb')
        pickle.dump(self.lex, f)
        f.close()
    
    