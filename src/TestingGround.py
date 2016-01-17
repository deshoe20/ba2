'''
Created on 11.01.2016

@author: Albert
'''
import CanonicalLexicon
import re
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
PATTERN = re.compile('^([0-9]+)\s+(\w+)\s+(\w{3})\s+(\(.*\))\s*$', re.UNICODE)


def process(l):
    m = PATTERN.match(l)
    LEX.append(m.group(1), CanonicalLexiconTree(m.group(2), []))
        
def main():
    f = open('res/freq-parser-lexicon-tag.txt', 'r')
    for line in f:
        process(line)
        break

if __name__ == '__main__':
    main()
        
