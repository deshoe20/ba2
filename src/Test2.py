"""
Created on 18.01.2016

@author: Albert
"""
from nltk.tree import Tree
from Util import Util
from Enum import MorphCase

BO = '('
BC = ')'

#test if string is well formed
def hans(s):
    i = 0 # i need a 1-outer-scope counter for processing the string in recursive function calls - only reason for the inner function
    def balanced_braces(s):
        nonlocal i # s.a.
        result = []
        isopen = False
        r = ""
        t = None
        while (i < len(s)):
            c = s[i]
            if isopen:
                if c == BO:
                    t = Tree(r, []) if t == None else t
                    t.extend(balanced_braces(s))
                    i = i + (s.find(BC, i) - i)
                elif c == BC:
                    t = Tree(r, []) if t == None else t
                    result.append(t)
                    break
                else:
                    r += c  
            elif c == BO:
                isopen = True 
            i += 1 
        return result
    return balanced_braces(s)

if __name__ == '__main__':
    #t1 = hans("(1 (1.1)(1.2 (1.2.1)(1.2.2 (1.2.2.1 (1.2.2.1.1))(1.2.2.2 ))))")
    #t1 = hans("(AP-CJ^null_x (AP-HD^x_null* )(AP-CC^x_x (NM-HD^x_x (CARD-NMC^x_x 000<>))))")
    #print(t1)
    #t1[0].draw()
    
    #    else:
    #        logging.error("%s.%s morphological string does not comply" % (self.__class__.__name__, "process"))
    
    mo = Util.objMatch(MorphCase, "acc")
    print(type(mo))
    
    
"""
%%% 18297
prediction:    ADJ    (NP-PD[nom]^null_1 (NP-HD[nom]^1_null* )(NP-AG[gen]^1_1 (DP-NK[gen]^1_null! )(NP-HD[gen]^1_1 )))
Von von    ADJ    (S^null_x (PP-MO^x_x (PP-HD^x_x (PP-HD^x_x (APPR-AC^x_x Von<>))(NP-PC^x_null! ))(APZR-AC^x_null! ))(S-HD^x_null* ))    --    
1953 1953    ARG    (NP-PC^null_x (CARD-NKHD^x_x 1953<>))    --    
an an    ARG    (APZR-AC^null_x an<>)    --    
war sein    ARG    (S-HD^null_x (VP-HD^x_x (VP-HD^x_x (VAFIN-HD^x_x war<>))(NP-SB[nom]^x_null! ))(NP-PD[nom]^x_null! ))    3.sg.past.ind    
er er    ARG    (NP-SB[nom]^null_x (PPER-NKHD^x_x er<>))    3.nom.sg.masc    
Generaldirektor Generaldirektor    ARG    (NP-PD[nom]^null_x (NN-NKHD^x_x Generaldirektor<>))    nom.sg.masc    
des der    ARG    (DP-NK[gen]^null_x (ART-HD^x_x des<>))    gen.sg.neut    
Verteidigungsministeriums Verteidigungsministerium    ADJ    (NP-PD[nom]^null_x (NP-HD[nom]^x_null* )(NP-AG[gen]^x_x (DP-NK[gen]^x_null! )(NP-HD[gen]^x_x (NN-NKHD^x_x Verteidigungsministeriums<>))))    gen.sg.neut    
. .    ADJ    (S-HD^null_x (S^x_null* )($.^x_x .<>))    --    

Von 1953 an war er Generaldirektor des Verteidigungsministeriums .
APPR Von    CARD 1953    APZR an    VAFIN war    PPER er    NN Generaldirektor    ART des    NN Verteidigungsministeriums    $. .
(S (S (PP (PP (PP (APPR Von))(NP (CARD 1953)))(APZR an))(S (VP (VP (VAFIN war))(NP[nom] (PPER er)))(NP[nom] (NP[nom] (NN Generaldirektor))(NP[gen] (DP[gen] (ART des))(NP[gen] (NN Verteidigungsministeriums))))))($. .))
"""    
    
    
    
