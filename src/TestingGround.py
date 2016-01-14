'''
Created on 11.01.2016

@author: Albert
'''
import CanonicalLexicon
from nltk.tree import Tree

#1    lassen    ADJ    (VP-HD^null_x (VP-HD^x_null* )(VP-*T2*-RE^x_x (PP-*T1*-OP^x_null! )(VP-HD^x_x (NP-OA[acc]^x_null! )(VP-HD^x_x (VP-OC^x_null! )(VP-HD^x_x (VZ-HD^x_x (PTKZU-PM^x_null! )(VZ-HD^x_x (VVINF-HD^x_x lassen<>))))))))

lex = CanonicalLexicon()


def process(l):
    lex.append(Tree(l[:2]))
        

if __name__ == '__main__':
    f = open('res/freq-parser-lexicon-tag.txt', 'r')
    for line in f:
        process(line)
        

