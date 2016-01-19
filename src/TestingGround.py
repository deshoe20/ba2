'''
Created on 11.01.2016

@author: Albert
'''
import re, logging, CanonicalLexicon
from CanonicalLexiconTree import CanonicalLexiconTree

#1    lassen    ADJ    (VP-HD^null_x (VP-HD^x_null* )(VP-*T2*-RE^x_x (PP-*T1*-OP^x_null! )(VP-HD^x_x (NP-OA[acc]^x_null! )(VP-HD^x_x (VP-OC^x_null! )(VP-HD^x_x (VZ-HD^x_x (PTKZU-PM^x_null! )(VZ-HD^x_x (VVINF-HD^x_x lassen<>))))))))

LEX = CanonicalLexicon.CanonicalLexicon()

'''
regular expression splitting the lexicon file lines into four groups
    first group is only the leading number in each line e.g. '1'
    second group is the entry string e.g. 'word' 
    third group is the elementary tree type e.g. 'ARG'
    fourth group is the tree structure for this word e.g. everything between the outer brackets      
'''
LINEPATTERN = re.compile('^([0-9]+)\s+(\w+)\s+(\w{3})\s+(\(.*\))\s*$', re.UNICODE)
BO = '('
BC = ')'

#test if string is well formed
def getTree(s):
    result = []
    isopen = False
    r = ""
    i = 0
    t = None
    while (i < len(s)):
        c = s[i]
        if isopen:
            if c == BO:
                t = CanonicalLexiconTree(r, []) if t == None else t
                t.extend(getTree(s[i:]))
                i = i + (s.find(BC, i) - i)
            elif c == BC:
                t = CanonicalLexiconTree(r, []) if t == None else t
                result.append(t)
                break
            else:
                r += c  
        elif c == BO:
            isopen = True 
        i += 1 
    return result

def process(l):
    m = LINEPATTERN.match(l)
    if m:
        t = getTree(m.group(2))
        if t:
            LEX.append(m.group(1), t[0])
    else:
        logging.warning("Line failed to comply: %s" % l)
            
        
def main():
    f = open('res/freq-parser-lexicon-tag.txt', 'r')
    i = 0
    for line in f:
        process(line)
        i += 1
        if i > 12319:
            break
    print("Length of lexicon: %d" % len(LEX))
    LEX['ablassen'].draw()

if __name__ == '__main__':
    main()
        

