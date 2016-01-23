'''
Created on 16.01.2016

@author: Albert
'''
from enum import Enum

class PhrasalCategory(Enum):
    UNDEF = 1 #&lt;not bound&gt;
    AA = 2 #superlative phrase with "am"
    AP = 3 #adjektive phrase
    AVP = 4 #adverbial phrase
    CAC = 5 #coordinated adposition
    CAP = 6 #coordinated adjektive phrase
    CAVP = 7 #coordinated adverbial phrase
    CCP = 8 #coordinated complementiser
    CH = 9 #chunk
    CNP = 10 #coordinated noun phrase
    CO = 11 #coordination
    CPP = 12 #coordinated adpositional phrase
    CS = 13 #coordinated sentence
    CVP = 14 #coordinated verb phrase (non-finite)
    CVZ = 15 #coordinated zu-marked infinitive
    DL = 16 #discourse level constituent
    ISU = 17 #idiosyncratis unit
    MTA = 18 #multi-token adjective
    NM = 19 #multi-token number
    NP = 20 #noun phrase
    PN = 21 #proper noun
    PP = 22 #adpositional phrase
    QL = 23 #quasi-language
    S = 24 #sentence
    VP = 25 #verb phrase (non-finite)
    VZ = 26 #zu-marked infinitive
    VROOT = 27 #unbound feature value of a virtual root
    
    def __str__(self):
        return str(self.name)

class FunctionalCategory(Enum):
    '''
    classdocs
    '''
    UNDEF = 1 #&lt;not bound&gt;
    AC = 2 #adpositional case marker
    ADC = 3 #adjective component
    AG = 4 #genitive attribute
    AMS = 5 #measure argument of adj
    APP = 6 #apposition
    AVC = 7 #adverbial phrase component
    CC = 8 #comparative complement
    CD = 9 #coordinating conjunction
    CJ = 10 #conjunct
    CM = 11 #comparative concjunction
    CP = 12 #complementizer
    CVC = 13 #collocational verb construction (Funktionsverbgefüge)
    DA = 14 #dative
    DH = 15 #discourse-level head
    DM = 16 #discourse marker
    EP = 17 #expletive es
    HD = 18 #head
    JU = 19 #junctor
    MC = 20 #comitative
    MI = 21 #instrumental
    ML = 22 #locative
    MNR = 23 #postnominal modifier
    MO = 24 #modifier
    MR = 25 #rhetorical modifier
    MW = 26 #way (directional modifier)
    NG = 27 #negation
    NK = 28 #noun kernel modifier
    NMC = 29 #numerical component
    OA = 30 #accusative object
    OA2 = 31 #second accusative object
    OC = 32 #clausal object
    OG = 33 #genitive object
    OP = 34 #prepositional object
    PAR = 35 #parenthesis
    PD = 36 #predicate
    PG = 37 #phrasal genitive
    PH = 38 #placeholder
    PM = 39 #morphological particle
    PNC = 40 #proper noun component
    RC = 41 #relative clause
    RE = 42 #repeated element
    RS = 43 #reported speech
    SB = 44 #subject
    SBP = 45 #passivised subject (PP)
    SP = 46 #subject or predicate
    SVP = 47 #separable verb prefix
    UC = 48 #unit component
    VO = 49 #vocative
    
    def __str__(self):
        return str(self.name)
    
class ElementaryTreeType(Enum):
    '''
    classdocs
    '''
    ARG = 1 #initial tree
    MOD = 2 #modifier tree
    ADJ = 3 #auxiliary tree
    
    def __str__(self):
        return str(self.name)
    
class MorphCase(Enum):
    NOM = 1
    GEN = 2
    ACC = 3
    DAT = 4
    UNDEF = 5
    
    def __str__(self):
        return str(self.name)
    
    @classmethod
    def fromString(cls, s):
        return getattr(cls, s.upper(), None)
    
class NodeType(Enum):
    ROOT = 1
    INNER = 2
    SUBST = 3
    FOOT = 4
    UNDEF = 5
    
    def __str__(self):
        return "!" if self == NodeType.SUBST else "*" if self == NodeType.FOOT else ""
    