from enum import Enum, unique
@unique
class NodeCategory(Enum):

    lexical = 1
    substitution = 2
    foot = 3
