'''
Created on 18.01.2016

@author: Albert
'''
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