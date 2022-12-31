#imports
import enum
from stack import stack
from Errors import (IncorrectTypeError, UndeclaredError, RedefinedError)

#global variables
SCOPE = stack()


class IncorrectTypeError(Exception):
    pass

#vocab for all terminals in grammar
class Vocab(enum.Enum):
    EOS = ""
    OPEN_PAREN = "("
    CLOSE_PAREN = ")"
    OPEN_BRACE = "{"
    CLOSE_BRACE = "}"
    OPEN_SQPAR = "["
    CLOSE_SQPAR = "]"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    ID = "id"
    AND = "&&"
    OR = "||"
    ASSIGN = "="
    EQ = "=="
    NEQ = "!="
    LTEQ = "<="
    GTEQ = ">="
    LT = "<"
    GT = ">"
    PLUS = "+"
    MINUS = "-"
    NUM = "integer"
    REAL = "float"
    TRUE = "true"
    FALSE = "false"
    NOT = "!"
    MUL = "*"
    DIV = "/"
    BASIC = "basic"
    SEMICOLON = ";"
    DOT = "."
    ROVER = "rover"
    PRINT_MAP = "print_map"
    SWITCH_MAP = "switch_map"
    INFO = "info"
    PRINT_POS = "print_pos"
    LOOKING = "looking"
    FACING = "facing"
    TURNLEFT = "turnLeft"
    TURNRIGHT = "turnRight"
    MOVE_TILE = "move_tile"
    DRILL = "drill"
    PRINT_INV = "print_inv"
    ENVSCAN = "envScan"
    BOMB = "bomb"
    WAYPOINT_SET = "waypoint_set"
    MOVETO_WAYPOINT = "moveto_waypoint"
    CACHE_MAKE = "cache_make"
    CACHE_DUMP = "cache_dump"
    CHARGE = "charge"


#vocab for all non terminals in grammar
class NonTerminals(enum.Enum):
    TERMINAL = 0
    PROGRAM = 1
    BLOCK = 2
    DECLS = 3
    DECL = 4
    TYPE = 5
    TYPECL = 6
    STMT = 7
    STMTS = 7
    LOC = 8
    LOCCL = 9
    BOOL = 10
    BOOLCL = 11
    JOIN = 12
    JOINCL = 13
    EQUALITY = 14
    EQUALCL = 15
    REL = 16
    RELTAIL = 17
    EXPR = 18
    EXPRCL = 19
    TERM = 20
    TERMCL = 21
    UNARY = 22
    FACTOR = 23
    FEATURE = 24



class Token:
    def __init__(self, value=0, ttype=Vocab.EOS):
        self.value = value
        self.ttype = ttype

    def __eq__(self, other_token):
        return self.value == other_token.value

    def __hash__(self):
        return hash(self.value)


class Node:
    def __init__(self, token):
        self.token = token
        self.children = []

    @property
    def is_token(self):
        return isinstance(self.token, Token)

    @property
    def is_nonterminal(self):
        return not self.is_token

    def add_child(self, node):
        self.children.append(node)

    def print(self, indent=0):
        symbol = self.print_val()
        if self.is_nonterminal:
            print(f"{' ' * indent} < {symbol} >")
        else:
            print(f"{' ' * indent} < {symbol} >")
        for child in self.children:
            child.print(indent=indent+2)
        if self.is_nonterminal:
            print(f"{' ' * indent} </ {symbol} >")

    def print_val(self):
        if not self.is_nonterminal:
            return self.token.value
        return self.print_nonterminal()

    def print_nonterminal(self):
        if self.token == NonTerminals.PROGRAM:
            return "program"
        elif self.token == NonTerminals.BLOCK:
            return "block"
        elif self.token == NonTerminals.DECLS:
            return "decls"
        elif self.token == NonTerminals.DECL:
            return "decl"
        elif self.token == NonTerminals.TYPE:
            return "type"
        elif self.token == NonTerminals.TYPECL:
            return "typecl"
        elif self.token == NonTerminals.STMTS:
            return "stmts"
        elif self.token == NonTerminals.STMT:
            return "stmt"
        elif self.token == NonTerminals.LOC:
            return "loc"
        elif self.token == NonTerminals.LOCCL:
            return "loccl"
        elif self.token == NonTerminals.BOOL:
            return "bool"
        elif self.token == NonTerminals.BOOLCL:
            return "boolcl"
        elif self.token == NonTerminals.JOIN:
            return "join"
        elif self.token == NonTerminals.JOINCL:
            return "joincl"
        elif self.token == NonTerminals.EQUALITY:
            return "equality"
        elif self.token == NonTerminals.EQUALCL:
            return "equalitycl"
        elif self.token == NonTerminals.REL:
            return "rel"
        elif self.token == NonTerminals.RELTAIL:
            return "reltail"
        elif self.token == NonTerminals.EXPR:
            return "expr"
        elif self.token == NonTerminals.EXPRCL:
            return "exprcl"
        elif self.token == NonTerminals.TERM:
            return "term"
        elif self.token == NonTerminals.TERMCL:
            return "termcl"
        elif self.token == NonTerminals.UNARY:
            return "unary"
        elif self.token == NonTerminals.FACTOR:
            return "factor"
        elif self.token == NonTerminals.FEATURE:
            return "feature"
        else:
            return "???"

    def get_types(self):
        raise Exception(f"Not implemented for {self.__class__.__name__}")

    # def match_types(self, target_types):
    #     my_types = self.get_types()
    #     if any(
    #         ttype in my_types
    #         for ttype in target_types
    #         ):
    #         return True
    #     return False

    # #def raise_type_mismatch_error(self, target):
    #     raise IncorrectTypeError(
    #         f"Expected these types {self.get_types()}, "
    #         f"but found {target}"
    #     )#

    def check_semantics(self):
        """Checks the semantics of the tree."""
        self.check_scopes()
        self.check_types()

    def check_types(self):
        for child in self.children:
            child.check_types()

    def check_scopes(self):
        for child in self.children:
            child.check_scopes()

    def run(self):
        for child in self.children:
            child.run()

#first node. starts the run
class ProgramNode(Node):
    def run(self, scope):
        global SCOPE
        SCOPE = scope

        result = -9
        for child in self.children:
            result = child.run()
        if result in (0,):
            print(f"Successfully ran the program, exited with: {result}")
        else:
            print(f"Failed to run program, exited with: {result}")

#feature node

class FeatureNode(Node):
    #no semantics to check since all are terminals
    def check_semantics(self):
        pass

    #determines which vocab the token is. calls that method in rover
    def run(self, rover):
        tok = self.children[0].token.ttype
        if tok == Vocab.PRINT_MAP:
            rover.print_map()
        elif tok == Vocab.SWITCH_MAP:
            rover.switch_map(int(self.children[1].token.value))
        elif tok == Vocab.INFO:
            rover.info()
        elif tok == Vocab.PRINT_POS:
            rover.print_pos()
        elif tok == Vocab.LOOKING:
            rover.looking()
        elif tok == Vocab.FACING:
            rover.facing()
        elif tok == Vocab.TURNLEFT:
            rover.turnLeft()
        elif tok == Vocab.TURNRIGHT:
            rover.turnRight()
        elif tok == Vocab.MOVE_TILE:
            rover.move_tile()
        elif tok == Vocab.DRILL:
            rover.drill()
        elif tok == Vocab.PRINT_INV:
            rover.print_inv()
        elif tok == Vocab.ENVSCAN:
            rover.envScan()
        elif tok == Vocab.BOMB:
            rover.bomb()
        elif tok == Vocab.WAYPOINT_SET:
            rover.waypoint_set()
        elif tok == Vocab.MOVETO_WAYPOINT:
            rover.moveto_waypoint()
        elif tok == Vocab.CACHE_MAKE:
            rover.cache_make()
        elif tok == Vocab.CACHE_DUMP:
            rover.cache_dump()
        elif tok == Vocab.CHARGE:
            rover.charge()

#factor node
class FactorNode(Node):
    #check semantics for factor
    def check_semantics(self):
        #if first child is bool non terminal, call semantics for node
        if isinstance(self.children[0], BoolNode):
            return self.children[0].check_semantics()

        #if first child is loc non terminal, call semantics for node
        elif isinstance(self.children[0], LocNode):
            type = self.children[0].check_semantics()

            #if type is an array raise error
            if type['arr']:
                raise IncorrectTypeError('basic type', 'array')
            return type

        #if first child is NUM terminal, return info for a NUM
        elif self.children[0].token.ttype == Vocab.NUM:
            return {'ttype': 'int',
                    'arr': False,
                    'dimen': 0,
                    'val': None}

        #if first child is REAL terminal, return info for a REAL
        elif self.children[0].token.ttype == Vocab.REAL:
            return {'ttype': 'double',
                    'arr': False,
                    'dimen': 0,
                    'val': None}

        #if first child is TRUE or FALSE terminal, return info for a TRUE or FALSE
        elif self.children[0].token.ttype == Vocab.TRUE or self.children.token.ttype == Vocab.FALSE:
            return {'ttype': 'bool',
                    'arr': False,
                    'dimen': 0,
                    'val': None}

    #run the code from factor
    def run(self, rover):
    
        #if first child is bool non terminal, call run method for node
        if isinstance(self.children[0], BoolNode):
            return self.children[0].run(rover)

        #if first child is loc non terminal, call run method for node
        elif isinstance (self.children[0], LocNode):
            info = self.children[0].run(rover)

            #if variable isnt an array, get value
            if len(info['arr']) == 0:
                value = info['val']

            #if variable is an array, get index, get value
            else:
                #gets index for an array
                arr = info['val']
                for i in info['arr'][0:-1]:
                    arr = arr[i]
                value = arr[info['arr'][-1]]
            return value

        #if first child is NUM terminal, get value of token, cast as int and return
        elif self.children[0].token.ttype == Vocab.NUM:
            return int(self.children[0].token.value)

        #if first child is REAL terminal, get value of token, cast as double, return
        elif self.children[0].token.ttype == Vocab.REAL:
            return float(self.children[0].token.value)

        #if first child is TRUE terminal, return true
        elif self.children[0].token.ttype == Vocab.TRUE:
            return True

        #if first child is FALSE terminal, return false
        elif self.children[0].token.ttype == Vocab.FALSE:
            return False

#Unary node
class UnaryNode(Node):
    #check semantics for unary
    def check_semantics(self):
        #if unary only has 1 child, check semantics for it
        if len(self.children) == 1:
            return self.children[0].check_semantics()

        #if unary has more than 1 child
        else:
            #check semantics
            info = self.children[1].check_semantics()

            #get operator
            operator = self.children[0].token.value

            #get type of unary node
            type = info['ttype']

            #if operator and type match, return unary node
            #else return nothing
            if (operator == '!' and type == 'bool') or (operator == '-' and (type == 'int' or type == 'double')):
                return info

    #run code from unary node
    def run(self, rover):
        #if unary only has 1 child, run child
        if len(self.children) == 1:
            return self.children[0].run(rover)

        #if unary has more than 1 child
        else:
            #run next unary node
            obj = self.children[1].run(rover)

            #get operator
            operator = self.children[0].token.value

            #if operator is !, return not of object
            if operator == '!':
                return not obj

            #if operator is -, return negative of object
            else:
                return - obj

#termcl node
class TermclNode(Node):
    #check semantics of termcl
    def check_semantics(self):
        #if termcl has no children, return nothing
        if len(self.children) == 0:
            return None

        #if termcl has children
        else:
            #check semantics for non terminal children
            unary = self.children[1].check_semantics()
            termcl = self.children[2].check_semantics()

            #if termcl child node returns None return unary
            if termcl == None:
                return unary
            
            #get node types
            unaryType = unary['ttype']
            termclType = termcl['ttype']

            #if either nodes are bool, raise error
            if unaryType == 'bool' or termclType == 'bool':
                raise IncorrectTypeError('int,double','bool')
            
            #if both nodes are int or double, make unary double
            if (unaryType == 'int' or unaryType == 'double') and  (termclType == 'int' or termclType == 'double'):
                unary['ttype'] = 'double'

            return unary

    #run code from termcl
    def run(self, rover, term):
        #if termcl has no children, return term
        if len(self.children) == 0:
            return term

        #if termcl has children
        else:
            #get operator
            operator = self.children[0].token.value

            #run unary node can get vlaue
            unaryVal = self.children[1].run(rover)

            #if operator is *, multiply term by value of unary
            if operator == '*':
                unaryVal = term * unaryVal

            #if operator is /
            else:
                #if nominator is 0, raise error
                if unaryVal == 0:
                    raise ZeroDivisionError

                #divide term by value of unary
                unaryVal = term/unaryVal

            #run termcl node and get value
            termclVal = self.children[2].run(rover, unaryVal)

            return termclVal

#term node
class TermNode(Node):
    #check semantics for term node
    def check_semantics(self):
        #check semantics for non terminal children
        unary = self.children[0].check_semantics()
        term = self.children[1].check_semantics()

        #if term node returned nothing, return unary node
        if term == None:
            return unary
            
        #get node types
        unaryType = unary['ttype']
        termType = term['ttype']

        #if either node is bool, raise erorr
        if unaryType == 'bool' or termType == 'bool':
            raise IncorrectTypeError('int,double','bool')
            
        #if both nodes are int or double, make unary double
        if (unaryType == 'int' or unaryType == 'double') and  (termType == 'int' or termType == 'double'):
            unary['ttype'] = 'double'

        return unary

    #run code from term node
    def run(self, rover):
        #run children
        unaryObj = self.children[0].run(rover)
        termObj = self.children[1].run(rover, unaryObj)

        return termObj

#exprcl node
class ExprclNode(Node):
    #check semantics for exprcl node
    def check_semantics(self):
        #if exprcl has no children, return None
        if len(self.children) == 0:
            return None

        #if exprcl has children
        else:
            #check semantics for children
            term = self.children[1].check_semantics()
            exprcl = self.children[2].check_semantics()

            #if term is None, return exprcl node
            if exprcl == None:
                return term
            
            #get node types
            termTtype = term['ttype']
            exprclType = exprcl['ttype']

            #if either node is bool, raise error 
            if termTtype == 'bool' or exprclType == 'bool':
                raise IncorrectTypeError('int,double', 'bool')
            
            #if either node is int or double, make term double
            if (termTtype == 'int' or termTtype == 'double') and  (exprclType == 'int' or exprclType == 'double'):
                term['ttype'] = 'double'

            return term

    #run code from exprcl node
    def run(self, rover, expr):
        #if exprcl has no children, return expr
        if len(self.children) == 0:
            return expr

        #if exprcl has children
        else:
            #get operator
            operator = self.children[0].token.value

            #run term node
            term = self.children[1].run(rover)

            #if oeprator is +, add expr to term
            if operator == '+':
                term = expr + term
            
            #if operator is -, subtract term from expr
            else:
                term = expr - term

            #run exprcl node
            exprclObj = self.children[2].run(rover, term)

            return exprclObj

#expr node
class ExprNode(Node):
    #checks semantics for expr node
    def check_semantics(self):
        #check semantics for children
        term = self.children[0].check_semantics()
        expr = self.children[1].check_semantics()

        #if term is Node, return expr
        if expr == None:
            return term
            
        #get node types
        termType = term['ttype']
        exprType = expr['ttype']

        #if either nodes are bool, raise error
        if termType == 'bool' or exprType == 'bool':
            raise IncorrectTypeError('int,double', 'bool')

        #if both types are the same, return term
        if termType == exprType:
            return term
            
        #if either nodes are int or double, make term double
        if (termType == 'int' or termType == 'double') and  (exprType == 'int' or exprType == 'double'):
            term['ttype'] = 'double'

        return term

    #run code from expr node
    def run(self, rover):
        #run children nodes
        term = self.children[0].run(rover)
        expr = self.children[1].run(rover, term)

        return expr

#reltail Node
class ReltailNode(Node):
    #check semantics for reltail node
    def check_semantics(self):
        #if expr has no children, return None
        if len(self.children) == 0:
            return None

        #if expr has children
        else:
            #check semantics of children
            expr = self.children[1].check_semantics()
            return expr

    #runs code from reltail
    def run(self, rover, expr):
        #if expr node has no children, return expr
        if len(self.children) == 0:
            return expr

        #if expr has children
        else:
            #get operator
            operator =  self.children[0].token.value

            #run children nodes
            exprObj = self.children[1].run(rover)

            #if operator is <=, do boolean
            if operator == '<=':
                return expr <= exprObj

            #if operator is >=, do boolean
            elif operator == '>=':
                return expr >= exprObj

            #if operator is <, do boolean
            elif operator == '<':
                return expr < exprObj

            #if operator is >, do boolean
            elif operator == '>':
                return expr > exprObj

#rel node
class RelNode(Node):
    #check semantics for rel node
    def check_semantics(self):
        #semantics for children
        expr = self.children[0].check_semantics()
        reltail = self.children[1].check_semantics()

        #if reltail is emtpy, then return expr
        if reltail == None:
            return expr

        #if either is bool, raise error
        if expr == 'bool' and reltail == 'bool':
            raise IncorrectTypeError('int,double', 'bool')
        
        #set expr type to bool
        expr['ttype'] = 'bool'
        return expr

    #run code from rel node
    def run(self, rover):
        #run children
        expr = self.children[0].run(rover)
        reltail = self.children[1].run(rover, expr)
        return reltail

#equalcl node
class EqualclNode(Node):
    #check semantics for equalcl node
    def check_semantics(self):
        #if equalcl node has no children, return none
        if len(self.children) == 0:
            return None

        #if equalcl node has children
        else:
            #check semantics for children
            rel = self.children[1].check_semantics()
            equalcl = self.children[2].check_semantics()

            #if equalcl is none, return none
            if equalcl == None:
                return rel

            #rel and equalcl types are the same or either are int and double, raise error
            if not (
                rel['ttype'] == equalcl['ttype'] or
                (rel['ttype'] in ['int','double'] and equalcl['ttype'] in ['int','double'])
            ):
                raise IncorrectTypeError(rel['ttype'], equalcl['ttype'])

            #set rel type to bool
            rel['ttype'] = 'bool'
            return rel

    #run code from equalcl
    def run(self, rover, rel):
        #if equalcl node has no children, return rel
        if len(self.children) == 0:
            return rel

        #if equalcl node has children
        else:
            #get operator
            operator = self.children[0].token.value

            #run rel child node
            relObj = self.children[1].run(rover)

            #if operator is ==, do boolean
            if operator == '==':
                relObj = rel == relObj

            #if operator is !=, do boolean
            elif operator == '!=':
                relObj = rel != relObj

            #run equalcl child node
            equalcl = self.children[2].run(rover, relObj)
            return equalcl

#equality node
class EqualityNode(Node):
    #check semantics for equality node
    def check_semantics(self):
        #semantics for children nodes
        rel = self.children[0].check_semantics()
        equalcl = self.children[1].check_semantics()

        #if equalcl is None, return rel
        if equalcl == None:
            return rel

        #rel and equalcl types are the same or either are int and double, raise error
        if not (
                rel['ttype'] == equalcl['ttype'] or
                (rel['ttype'] in ['int', 'double'] and equalcl['ttype'] in ['int', 'double'])
        ):
            raise IncorrectTypeError(rel['ttype'], equalcl['ttype'])

        #set type of rel child as bool
        rel['ttype'] = 'bool'
        return rel
    
    #run code from equality node
    def run(self, rover):
        #run children nodes
        relObj = self.children[0].run(rover)
        equalclObj = self.children[1].run(rover, relObj)
        return equalclObj

#joincl node
class JoinclNode(Node):
    #check semantics for joincl node
    def check_semantics(self):
        #if joincl node has no children, return None
        if len(self.children) == 0:
            return None
        
        #if joincl node has children
        else:
            #check semantics for children nodes
            equality = self.children[1].check_semantics()
            joincl = self.children[2].check_semantics()

            #if joincl is None, return equality
            if joincl == None:
                return equality

            #if either child node is bool, raise error
            if not (equality['ttype'] == 'bool' and joincl['ttype'] == 'bool'):
                raise IncorrectTypeError('bool', 'int,double')

            return equality

    #run code from joincl node
    def run(self, rover, join):
        #if joincl node has no children, return join
        if len(self.children) == 0:
            return join
        
        #if joincl node has children
        else:
            #run equality child node
            equalityObj = self.children[1].run(rover)

            #do boolean
            equalityObj = join and equalityObj

            #run joincl child node
            joinclObj = self.children[2].run(rover, equalityObj)
            return joinclObj

#join node
class JoinNode(Node):
    #check semantics for join node
    def check_semantics(self):
        #check semantics for children nodes
        equality = self.children[0].check_semantics()
        joincl = self.children[1].check_semantics()
        
        #if joincl is None, return equality
        if joincl == None:
            return equality

        #if either is type bool, raise error
        if not (equality['ttype'] == 'bool' and joincl['ttype'] == 'bool'):
            raise IncorrectTypeError('bool', 'int,double')

        return joincl

    #run code from join node
    def run(self, rover):
        #run children nodes
        equalityObj = self.children[0].run(rover)
        joinclObj = self.children[1].run(rover, equalityObj)
        return joinclObj

#boolcl node
class BoolclNode(Node):
    #check semantics for boolcl node
    def check_semantics(self):
        #if boolcl node has no children, return None
        if len(self.children) == 0:
            return None

        #if boolcl has children
        else:
            #check semantics for children nodes
            join = self.children[1].check_semantics()
            boolcl = self.children[2].check_semantics()

            #if boolcl is None, return join
            if boolcl == None:
                return join

            #if either child node is bool, raise error
            if not (join['ttype'] == 'bool' and boolcl['ttype'] == 'bool'):
                raise IncorrectTypeError('bool', 'int,double')

            return join

    #run code from boolcl node
    def run(self, rover, boolcl):
        #if boolcl node has no children, return boolcl input
        if len(self.children) == 0:
            return boolcl

        #if boolclnode has children
        else:
            #run join child node
            joinObj = self.children[1].run(rover)

            #do boolean
            joinObj = boolcl or joinObj

            #run boolcl child node
            boolclObj = self.children[2].run(rover, joinObj)
            return boolclObj

#bool node
class BoolNode(Node):
    #check semantics for bool node
    def check_semantics(self):
        #check semantics for children nodes
        join = self.children[0].check_semantics()
        boolcl = self.children[1].check_semantics()

        #if boolcl is None, return join
        if boolcl == None:
            return join

        #if either child is type bool, raise error
        if not (join['ttype'] == 'bool' and boolcl['ttype'] == 'bool'):
            raise IncorrectTypeError('bool', 'int,double')

        return boolcl

    #run code from bool node
    def run(self, rover):
        #run child nodes
        joinObj = self.children[0].run(rover)
        boolclObj = self.children[1].run(rover, joinObj)
        return boolclObj

#loccl node
class LocclNode(Node):
    #check semantics for loccl node
    def check_semantics(self):
        #if loccl node has no children, return info for ID var
        if len(self.children) == 0:
            return {'ttype': None,
                    'arr': False,
                    'dimen': 0,
                    'val': None}

        #if loccl node has children
        else:
            #check semantics for child node
            index = self.children[0].check_semantcis()
           
           #if first child node is not int, raise error
            if index['ttype'] != 'int':
                raise IncorrectTypeError('int', index['ttype'])

            #check semantics for child node
            locclInfo = self.children[1].check_semantics()

            #get info from loccl child node
            locclInfo['dimen'] = locclInfo['dimen'] + 1
            locclInfo['arr'] = True
            return locclInfo

    #run node from loccl node
    def run(self, rover):
        #if loccl node has no children, return Nonde
        if len(self.children) == 0:
            return None

        #if loccl node has children
        else:
            #run child nodes
            boolObj = self.children[0].run(rover)
            locclObj = self.children[1].run(rover)

            #if loccl child node is None, return bool child node
            if locclObj == None:
                return [boolObj]

            #if loccl child node is not None, return bool child node and loccl child node
            else:
                return [boolObj] + locclObj

#loc node
class LocNode(Node):
    #check semantics for loc node
    def check_semantics(self):
        #get variables
        global SCOPE
        id = self.children[0].token.value

        #check if ID is in stack
        SCOPE.checkScopes(id)

        #if ID not in stack, raise error
        if not SCOPE.checkScopes(id):
            raise UndeclaredError(id)

        symbol = SCOPE.getId(id)

        #check semantics for type child node and get info
        type = self.children[1].check_semantics()
        typeDimen = symbol[id]['dimen'] - type['dimen']

        #if dimen is less than 0, raise error
        if typeDimen < 0:
            raise IncorrectTypeError('valid subscript','invalid subscript')

        #if dimen is greater than 0, set arr to true, else arr to false
        if typeDimen > 0: 
            arr = True
        else:
            arr = False

        #return info for ID
        return {'ttype': symbol[id]['ttype'],
                'arr': arr,
                'dimen': typeDimen,
                'val': None}

    #run code from lock
    def run(self, rover):
        #get variables
        global SCOPE
        id = self.children[0].token.value
        obj = SCOPE.getId(id)

        #run child node
        arr = self.children[1].run(rover)

        #if ID is not arr, return info for array
        if arr == None:
            return {'id': id,
                    'val': obj[id]['val'],
                    'ttype': obj[id]['ttype'],
                    'arr': []}

        #if ID is arr, return info for basic var
        else:
            return {'id': id,
                    'val': obj[id]['val'],
                    'ttype': obj[id]['ttype'],
                    'arr': arr}

#stmt node
class StmtNode(Node):
    #check semantics for stmt node
    def check_semantics(self):
        #if node is loc
        if isinstance(self.children[0], LocNode):
            #check semantics for children nodes
            symbol = self.children[0].check_semantics()
            type = self.children[2].check_semantics()

            #if not symbol and type are same type/symbol & type are double and int/symbol is arr, raise error
            if (not
            (symbol['ttype'] == type['ttype'] or (symbol['ttype'] == 'double' and type['ttype'] == 'int'))
            or symbol['arr']
            ):
                raise IncorrectTypeError(symbol['ttype'],type['ttype'])

        #if node is block, check semantics
        elif isinstance(self.children[0], BlockNode):
            self.children[0].check_semantics()

        #if node is rover, check semantics for next node
        elif self.children[0].token.value == Vocab.ROVER:
            self.children[1].check_semantics()

        #if node is IF or WHILE
        elif self.children[0].token.value == Vocab.IF or self.children[0].token.value == Vocab.WHILE:
            #check semantics for condition
            condition = self.children[1].check_semantics()

            #if condition isnt bool, raise error
            if condition['ttype'] != 'bool':
                raise IncorrectTypeError('bool',condition['ttype'])
            
            #check semantics for next node
            self.children[2].check_semantics()

            #if there are more than 3 nodes (ELSE), check semantics for else statement
            if len(self.children) > 3:
                self.children[4].check_semantics()

    #run code from stmt node
    def run(self, rover):
        global SCOPE
        #if node is loc
        if isinstance(self.children[0], LocNode):
            #get variables
            id = self.children[0].run(rover)
            val = self.children[2].run(rover)

            #assign value to variable
            SCOPE.assign(id, val)

        #if node is block, run node
        elif isinstance(self.children[0], BlockNode):
            self.children[0].run(rover)

        #if node is rover, run next node
        elif self.children[0].token.ttype == Vocab.ROVER:
            self.children[1].run(rover)

        #if node is IF
        elif self.children[0].token.ttype == Vocab.IF:
            #run condition
            boolObj = self.children[1].run(rover)

            #if condition is true, run next node
            if boolObj:
                self.children[2].run(rover)

            #if condition is false and stmt has more than 3 nodes, run else statment
            elif len(self.children) > 3 and not boolObj:
                self.children[4].run(rover)

        #if node is WHILE
        elif self.children[0].token.ttype == Vocab.WHILE:
            while True:
                #run condition node; is false, break
                if not (self.children[1].run(rover)):
                    break

                #else, run statements
                self.children[2].run(rover)

#stmts node
class StmtsNode(Node):
    #check semantics for stmts node
    def check_semantics(self):
        #if stmts node has children,check semantics
        if len(self.children) > 0:
            self.children[0].check_semantics()
            self.children[1].check_semantics()

    #run code from stmts node
    def run(self, rover):
        #if stmts node has children, run children nodes
        if len(self.children) > 0:
            self.children[0].run(rover)
            self.children[1].run(rover)

#typecl node
class TypeclNode(Node):
    #check semantics for typecl Node
    def check_semantics(self):
        #if typecl node has no children, return info for basic var
        if len(self.children) == 0:
            return {'ttype': None,
                    'arr': False,
                    'dimen': 0,
                    'val': None}

        #if typecl node has children, return info for arr
        else:
            type = self.children[1].check_semantics()
            type['dimen'] = type['dimen'] + 1
            type['arr'] = True
            return type

    #run code from typecl node
    def run(self, rover):
        #if typecl node has no children, return None
        if len(self.children) == 0:
            return None
        
        #if typecl node has children
        else:
            #get variables
            length = int(self.children[0].token.value)
            val = self.children[1].run(rover)
            newArr = []

            #set new arr with values found length times
            for i in range(0, length):
                newArr.append(val)

            return newArr

#type node
class TypeNode(Node):
    #check semantics for type node
    def check_semantics(self):
        #check semantics for child node
        typecl = self.children[1].check_semantics()

        #set type to value of first child node
        typecl['ttype'] = self.children[0].token.value

        return typecl

    #run code from type node
    def run(self, rover):
        #get value of first child node
        ttype = self.children[0].token.value

        #run second child node
        arr = self.children[1].run(rover)

        #if arr is None, return info
        if arr == None:
            return {'ttype': ttype, 'val': arr}

#decl node
class DeclNode(Node):
    #check semantics for decl node
    def check_semantics(self):
        global SCOPE

        #check semantics of child node
        type = self.children[0].check_semantics()

        #get value of child node
        id = self.children[1].token.value

        if id in SCOPE.top():
            raise RedefinedError(id)

        #set type
        SCOPE.top()[id] = type

    #run code from decl node
    def run(self, rover):
        global SCOPE

        #run child node
        typeObj = self.children[0].run(rover)

        #get value of child node
        id = self.children[1].token.value

        #st type
        SCOPE.top()[id] = typeObj

#decls node
class DeclsNode(Node):
    #check semantics for decls node
    def check_semantics(self):
        #if decls node has children, check semantics
        if len(self.children) > 0:
            self.children[0].check_semantics()
            self.children[1].check_semantics()

    #run code from decls node
    def run(self, rover):
        #if decls node has children, run nodes
        if len(self.children) > 0:
            self.children[0].run(rover)
            self.children[1].run(rover)

#block node
class BlockNode(Node):
    #check semantics for block node
    def check_semantics(self):
        global SCOPE
        #push new dict
        SCOPE.push({})

        #check semantics for children nodes
        self.children[0].check_semantics()
        self.children[1].check_semantics()

        #pop dict when done
        SCOPE.pop()

    #run code from block node
    def run(self, rover):
        global SCOPE
        #push new dict
        SCOPE.push({})

        #run children nodes
        self.children[0].run(rover)
        self.children[1].run(rover)

        #pop dict when done
        SCOPE.pop()