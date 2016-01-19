'''
Created on 18.01.2016

@author: Albert
'''
from nltk.tree import Tree

BO = '('
BC = ')'

#test if string is well formed
def balanced_braces(s):
    result = []
    isopen = False
    r = ""
    i = 0
    t = None
    while (i < len(s)):
        c = s[i]
        if isopen:
            if c == BO:
                t = Tree(r, []) if t == None else t
                t.extend(balanced_braces(s[i:]))
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


if __name__ == '__main__':
    t1 = balanced_braces("(HPP(PD)(DS(SD)))")
    print(t1)
    t1[0].draw()