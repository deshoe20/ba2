from nltk.tokenize import word_tokenize
import const

class Parser:

    

    #tree = Tree('A')

    def __init__(self):
        self.TESTTOKENS = word_tokenize(const.TESTSTRING)
        self.cursor = 0

    def setTESTSTRING(self, s):
        self.TESTSTRING = s

    def scan(self):
        currentItem = self.TESTTOKENS[self.cursor]
        print(currentItem)

        #stuff happening

        self.cursor += 1
        
