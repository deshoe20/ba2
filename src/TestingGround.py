"""
Created on 11.01.2016

@author: Albert
"""
import re, logging, pickle
from PLTAGTree import PLTAGTree
from PredictionLexicon import PredictionLexicon
from ElementaryLexicon import ElementaryLexicon
from nltk import tree

#1    lassen    ADJ    (VP-HD^null_x (VP-HD^x_null* )(VP-*T2*-RE^x_x (PP-*T1*-OP^x_null! )(VP-HD^x_x (NP-OA[acc]^x_null! )(VP-HD^x_x (VP-OC^x_null! )(VP-HD^x_x (VZ-HD^x_x (PTKZU-PM^x_null! )(VZ-HD^x_x (VVINF-HD^x_x lassen<>))))))))

LEX = None

"""
regular expression splitting the lexicon file lines into four groups
    first group is only the leading number in each line e.g. '1'
    second group is the entry string e.g. 'word' 
    third group is the elementary tree type e.g. 'ARG'
    fourth group is the tree structure for this word e.g. everything between the outer brackets      
"""
LINEPATTERN = re.compile('^([0-9]+)\s+(\S+)\s+(\w{3})\s+(\(.+\))\s*$', re.UNICODE)
TREESTRINGPATTERN = re.compile('^\(.+\)$', re.UNICODE)
BO = '('
BC = ')'

#TODO : move this into PLTAGTree class if possible (simpler attribute allocation)
def getTree(s, treecls):
    i = 0
    def getInnerTrees(s):   
        #logging.info("Tree for %s" % s)     
        nonlocal i
        result = []
        isopen = False
        r = ""
        t = None
        while (i < len(s)):
            c = s[i]
            if isopen:
                if c == BO:
                    t = t if t else treecls(r, [])
                    t.extend(getInnerTrees(s))
                    i = i + (s.find(BC, i) - i)
                elif c == BC:
                    t = t if t else treecls(r, [])
                    result.append(t)
                    break
                else:
                    r += c  
            elif c == BO:
                isopen = True 
            i += 1 
        return result
    return getInnerTrees(s)

def process(l, lex, treecls):
    m = LINEPATTERN.match(l)
    if m:
        ts = m.group(4)
        comply = TREESTRINGPATTERN.match(ts)
        if comply:
            t = getTree(ts, treecls)
            if t:
                if len(t) > 1:
                    logging.error("Canonical lexicon tree entry has more than 1 root node: %s\nFor line [%s]" % (str(t), l))
                else:
                    t[0].isCurrentRoot = True
                    lex.compatibleAppending(m.group(2), (m.group(1), t[0]))
            else:
                logging.warning("getTree returned empty for: %s" % ts)
        else:
            logging.warning("Line has no valid tree group: %s" % ts)
    else:
        logging.warning("Line failed to comply: %s" % l)

def convertTAGLexiconToPython(lexcls, filename):
    f = open(filename, 'r', encoding='utf-8')
    lex = lexcls()
#    i = 0
    for line in f:
        process(line, lex, PLTAGTree)
#        i += 1
#        if i > 192256:
#            break
    logging.info("Length of lexicon: %d" % len(lex))
    f.close()
    return lex

    
def pickleLexicon(filename, lex):
    f = open(filename, 'wb')
    pickle.dump(lex, f)
    f.close()

def loadLexicon(filename):
    f = open(filename, 'rb')
    lex = pickle.load(f)
    f.close()
    return lex
            
def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    #convert
    LEX = convertTAGLexiconToPython(PredictionLexicon, '../res/freq-parser-lexicon-prediction.txt')
    LEX2 = convertTAGLexiconToPython(ElementaryLexicon, '../res/freq-parser-lexicon-tag.txt')

    #pickle
    pickleLexicon('../res/pickeledTAGPredictionlexicon.pick', LEX)
    pickleLexicon('../res/pickeledTAGlexicon.pick', LEX2)
    
    #test
#    LEX = loadLexicon('../res/pickeledTAGPredictionlexicon.pick')
#    LEX = loadLexicon('../res/pickeledTAGlexicon.pick')

    logging.info("Length of lexicon: %d" % len(LEX))
#    LEX[10449][1].draw()
#    cf = LEX['Amaru'][0][1].currentFringe()
#    print("Current fringe:\t%s" % str(cf))
#    LEX['Amaru'][0][1].draw()
#    cf[2].set_label("HANT")
#    LEX['Amaru'][0][1].draw()
#    print(str(LEX['tot'][5][1].isCurrentRoot))
#    print(str(LEX['gehört'][0][1][1][0].isCurrentRoot))
#    t = tree.Tree.fromstring('(S (S (NP[nom] (PPER Ich))(VP (VP (VP (VVFIN liebe))(NP[acc] (DP[acc] (PDAT dieses))(NP[acc] (NN Land))))(AVP (ADV sehr))))($. .))')
#    t.draw()

if __name__ == '__main__':
    main()
        

