#imports
import enum
from stack import stack
from Errors import (IncorrectTypeError, UndeclaredError)

#global variables
SCOPE = stack()


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
    def semantics(self):
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
    def semantics(self):
        #if first child is bool non terminal, call semantics for node
        if isinstance(self.children[0], BoolNode):
            return self.children[0].semantics()

        #if first child is loc non terminal, call semantics for node
        elif isinstance(self.children[0], LocNode):
            type = self.children[0].semantics()

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
    def semantics(self):
        #if unary only has 1 child, check semantics for it
        if len(self.children) == 1:
            return self.children[0].semantics()

        #if unary has more than 1 child
        else:
            #check semantics
            info = self.children[1].semantics()

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
    def semantics(self):
        #if termcl has no children, return nothing
        if len(self.children) == 0:
            return None

        #if termcl has children
        else:
            #check semantics for non terminal children
            unary = self.children[1].semantics()
            termcl = self.children[2].semantics()

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
    def semantics(self):
        #check semantics for non terminal children
        unary = self.children[0].semantics()
        term = self.children[1].semantics()

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
    def semantics(self):
        #if exprcl has no children, return None
        if len(self.children) == 0:
            return None

        #if exprcl has children
        else:
            #check semantics for children
            term = self.children[1].semantics()
            exprcl = self.children[2].semantics()

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
    def semantics(self):
        #check semantics for children
        term = self.children[0].semantics()
        expr = self.children[1].semantics()

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
        termObj = self.children[0].run(rover)
        exprObj = self.children[1].run(rover, termObj)
        return exprObj

#reltail node
class ReltailNode(Node):
    def semantics(self):
        #if there are no children, the node is empty
        if len(self.children) == 0:
            return None
        #evaluates the expression
        else:
            exprInfo = self.children[1].semantics()
            return exprInfo
    #runs code from reltail node
    def run(self, rover, expr):
        if len(self.children) == 0:
            return expr

        else:
            operator =  self.children[0].token.value
            exprObj = self.children[1].run(rover)

            if operator == '<=':
                return expr <= exprObj

            elif operator == '>=':
                return expr >= exprObj

            elif operator == '<':
                return expr < exprObj

            elif operator == '>':
                return expr > exprObj

class RelNode(Node):
    def semantics(self):
        #check semantics for child nodes
        exprInfo = self.children[0].semantics()
        reltailInfo = self.children[1].semantics()
        #if reltail is empty, then there is only expr node remaining
        if reltailInfo == None:
            return exprInfo

        if exprInfo == 'bool' and reltailInfo == 'bool':
            raise IncorrectTypeError('int,double', 'bool')
        
        exprInfo['ttype'] = 'bool'
        return exprInfo

    def run(self, rover):
        exprObj = self.children[0].run(rover)
        reltailObj = self.children[1].run(rover, exprObj)
        return reltailObj

class EqualclNode(Node):
    def semantics(self):
        #if there are no children, node is empty
        if len(self.children) == 0:
            return None

        else:
            #evaluate children
            relInfo = self.children[1].semantics()
            equalclInfo = self.children[2].semantics()
            #return rel node if equalcl is empty
            if equalclInfo == None:
                return relInfo
            # both sides of the == must be int or double, otherwise error
            if not (
                relInfo['ttype'] == equalclInfo['ttype'] or
                (relInfo['ttype'] in ['int','double'] and equalclInfo['ttype'] in ['int','double'])
            ):
                raise IncorrectTypeError(relInfo['ttype'], equalclInfo['ttype'])

            relInfo['ttype'] = 'bool'
            return relInfo
    #runs code from equalcl node
    def run(self, rover, rel):
        #return rel if no more children
        if len(self.children) == 0:
            return rel
        else:
            #run children
            operator = self.children[0].token.value
            relObj = self.children[1].run(rover)

            if operator == '==':
                relObj = rel == relObj
            elif operator == '!=':
                relObj = rel != relObj

            equalclObj = self.children[2].run(rover, relObj)
            return equalclObj


class EqualityNode(Node):
    def semantics(self):
        #evaluate children
        relInfo = self.children[0].semantics()
        equalclInfo = self.children[1].semantics()
        #if equalcl is empty return rel, no children
        if equalclInfo == None:
            return relInfo
        #if ==, both sides of equation must be int or double, otherwise error
        if not (
                relInfo['ttype'] == equalclInfo['ttype'] or
                (relInfo['ttype'] in ['int', 'double'] and equalclInfo['ttype'] in ['int', 'double'])
        ):
            raise IncorrectTypeError(relInfo['ttype'], equalclInfo['ttype'])

        relInfo['ttype'] = 'bool'
        return relInfo
    
    def run(self, rover):
        #run children
        relObj = self.children[0].run(rover)
        equalclObj = self.children[1].run(rover, relObj)
        return equalclObj

class JoinclNode(Node):
    def semantics(self):
        #empty node if there are no children
        if len(self.children) == 0:
            return None
        #evaluate children
        else:
            equalityInfo = self.children[1].semantics()
            joinclInfo = self.children[2].semantics()
            #if joincl is empty return equality
            if joinclInfo == None:
                return equalityInfo
            #both sides of equation must be bool
            if not (equalityInfo['ttype'] == 'bool' and joinclInfo['ttype'] == 'bool'):
                raise IncorrectTypeError('bool', 'int,double')

            return equalityInfo

    def run(self, rover, join):
        #if node is empty, no children
        if len(self.children) == 0:
            return join
        #run children
        else:
            equalityObj = self.children[1].run(rover)
            equalityObj = join and equalityObj
            joinObj = self.children[2].run(rover, equalityObj)
            return joinObj

class JoinNode(Node):
    #evaluate children
    def semantics(self):
        equalityInfo = self.children[0].semantics()
        joinclInfo = self.children[1].semantics()
        # if joincl is empty return equality
        if joinclInfo == None:
            return equalityInfo
        #both sides of equation must be bool
        if not (equalityInfo['ttype'] == 'bool' and joinclInfo['ttype'] == 'bool'):
            raise IncorrectTypeError('bool', 'int,double')

        return joinclInfo

    def run(self, rover):
        #run children
        equalityObj = self.children[0].run(rover)
        joinclObj = self.children[1].run(rover, equalityObj)
        return joinclObj

class BoolclNode(Node):
    def semantics(self):
        #if no children, node is empty, return nothing
        if len(self.children) == 0:
            return None

        else:
            #evaluate children
            joinInfo = self.children[1].semantics()
            boolclInfo = self.children[2].semantics()
            #return join node is boolcl empty
            if boolclInfo == None:
                return joinInfo
            # or, both sides must be bool
            if not (joinInfo['ttype'] == 'bool' and boolclInfo['ttype'] == 'bool'):
                raise IncorrectTypeError('bool', 'int,double')

            return joinInfo

    def run(self, rover, boolcl):
        #return boolcl if no more children
        if len(self.children) == 0:
            return boolcl
        #run children
        else:
            joinObj = self.children[1].run(rover)
            joinObj = boolcl or joinObj

            boolclObj = self.children[2].run(rover, joinObj)
            return boolclObj

class BoolNode(Node):
    #evaluate children
    def semantics(self):
        joinInfo = self.children[0].semantics()
        boolclInfo = self.children[1].semantics()
        # if boolcl is empty return join
        if boolclInfo == None:
            return joinInfo
        #or, both sides of equation must be boolean
        if not (joinInfo['ttype'] == 'bool' and boolclInfo['ttype'] == 'bool'):
            raise IncorrectTypeError('bool', 'int,double')
        return boolclInfo
    #run children
    def run(self, rover):
        joinObj = self.children[0].run(rover)
        boolclObj = self.children[1].run(rover, joinObj)
        return boolclObj

class LocclNode(Node):
    def semantics(self):
        if len(self.children) == 0:
            return {'ttype': None,
                    'arr': False,
                    'dimen': 0,
                    'val': None}
#index of the array must be of type int
        else:
            index = self.children[0].check_semantcis()
           
            if index['ttype'] != 'int':
                raise IncorrectTypeError('int', index['ttype'])

            locclInfo = self.children[1].semantics()
            locclInfo['dimen'] = locclInfo['dimen'] + 1 #increases dimension of array by 1
            locclInfo['arr'] = True #flags as an array
            return locclInfo

    def run(self, rover):
        #if no children, no array
        if len(self.children) == 0:
            return None
        #run children
        else:
            boolObj = self.children[0].run(rover)
            locclObj = self.children[1].run(rover)
            # if locclObj is empty then there is no sub array
            if locclObj == None:
                return [boolObj]
            #returns current index and next index
            else:
                return [boolObj] + locclObj
class LocNode(Node):
    def semantics(self):
        global SCOPE
        id = self.children[0].token.value   #identifier, name of the assigned variable
        SCOPE.checkScopes(id)
        #variable must be in the correct scope otherwise considered undeclared
        if not SCOPE.checkScopes(id):
            raise UndeclaredError(id)
        #handling for arrays
        symbol = SCOPE.getId(id)
        type = self.children[1].semantics()
        typeDimen = symbol[id]['dimen'] - type['dimen']
        #if typeDimen is negative, array has a lower dimension
        if typeDimen < 0:
            raise IncorrectTypeError('valid subscript','invalid subscript')
        #if typeDimen is positive, flag array true
        if typeDimen > 0: 
            arr = True
        else:
            arr = False

        return {'ttype': symbol[id]['ttype'],
                'arr': arr,
                'dimen': typeDimen,
                'val': None}

    def run(self, rover):
        global SCOPE
        id = self.children[0].token.value   #gets identifier
        obj = SCOPE.getId(id)
        arr = self.children[1].run(rover)   #checks to see if array
        #not an array
        if arr == None:
            return {'id': id,
                    'val': obj[id]['val'],
                    'ttype': obj[id]['ttype'],
                    'arr': []}

        else:
            return {'id': id,
                    'val': obj[id]['val'],
                    'ttype': obj[id]['ttype'],
                    'arr': arr}

class StmtNode(Node):
    def semantics(self):
        if isinstance(self.children[0], LocNode):
            symbol = self.children[0].semantics()
            type = self.children[2].semantics()
            #mismatched types || array -> value cannot be assigned
            if (not
            (
                symbol['ttype'] == type['ttype'] or (symbol['ttype'] == 'double' and type['ttype'] == 'int')
            )
            or symbol['arr']
            ):
                raise IncorrectTypeError(symbol['ttype'],type['ttype'])
        #evaluate semantics of block
        elif isinstance(self.children[0], BlockNode):
            self.children[0].semantics()
        #evaluate semantics of rover function
        elif self.children[0].token.value == Vocab.ROVER:
            self.children[1].semantics()
        #evaluate semantics of control structures
        #condition of control structure must be type bool
        elif self.children[0].token.value == Vocab.IF or self.children[0].token.value == Vocab.WHILE:
            condition = self.children[1].semantics()

            if condition['ttype'] != 'bool':
                raise IncorrectTypeError('bool',condition['ttype'])
            
            self.children[2].semantics()
            if len(self.children) > 3:
                self.children[4].semantics()

    def run(self, rover):
        global SCOPE
        if isinstance(self.children[0], LocNode):
            id = self.children[0].run(rover)
            val = self.children[2].run(rover)

            SCOPE.assign(id, val)
        #executes block of code
        elif isinstance(self.children[0], BlockNode):
            self.children[0].run(rover)
        #runs command in rover
        elif self.children[0].token.ttype == Vocab.ROVER:
            self.children[1].run(rover)
        #executes if statement if condition is true
        #logical equivalence
        elif self.children[0].token.ttype == Vocab.IF:

            boolObj = self.children[1].run(rover)
            if boolObj:
                self.children[2].run(rover)
            elif len(self.children) > 3 and not boolObj:
                self.children[4].run(rover)
        #loops if condition is true
        #logical equivalence
        elif self.children[0].token.ttype == Vocab.WHILE:
            while True:
                if not (self.children[1].run(rover)):
                    break
                self.children[2].run(rover)

class StmtsNode(Node):
    def semantics(self):
        #allows for multiple statements, evaluate if remaining nodes exist
        if len(self.children) > 0:
            stmtInfo = self.children[0].semantics()
            stmtsInfo = self.children[1].semantics()

    def run(self, rover):
        if len(self.children) > 0:
            stmtObj = self.children[0].run(rover)
            stmtsObj = self.children[1].run(rover)

class TypeclNode(Node):
    def semantics(self):
        #no children
        if len(self.children) == 0:
            return {'ttype': None,
                    'arr': False,
                    'dimen': 0,
                    'val': None}
        #evaluating array
        else:
            type = self.children[1].semantics() #gets info on arrays larger than dimension 1
            type['dimen'] = type['dimen'] + 1 #increases dimension on each iteration
            type['arr'] = True  #flags as array
            return type

    def run(self, rover):
        #empty
        if len(self.children) == 0:
            return None
        
        else:
            length = int(self.children[0].token.value)  #holds length of array
            subarr = self.children[1].run(rover)
            newArr = []
            #fills newArr with each subarray
            for i in range(0, length):
                newArr.append(subarr)

            return newArr

class TypeNode(Node):
    def semantics(self):
        typeclnfo = self.children[1].semantics()
        typeclnfo['ttype'] = self.children[0].token.value   #determines if array
        #returns type of variable
        return typeclnfo

    def run(self, rover):
        #run children
        ttype = self.children[0].token.value
        arr = self.children[1].run(rover)
        #no array
        if arr == None:
            return {'ttype': ttype, 'val': arr}

class DeclNode(Node):
    def semantics(self):
        global SCOPE
        #type and name of declared variable
        type = self.children[0].semantics()
        id = self.children[1].token.value
        SCOPE.top()[id] = type

    def run(self, rover):
        #get info on the variable
        global SCOPE
        typeObj = self.children[0].run(rover)
        id = self.children[1].token.value

        SCOPE.top()[id] = typeObj

class DeclsNode(Node):
    def semantics(self):
        #allows for multiple declarations
        if len(self.children) > 0:
            self.children[0].semantics()
            self.children[1].semantics()

    def run(self, rover):
        if len(self.children) > 0:
            self.children[0].run(rover)
            self.children[1].run(rover)

class BlockNode(Node):
    def semantics(self):
        #when a new block is found, push new scope to stack
        global SCOPE
        SCOPE.push({})

        self.children[0].semantics()
        self.children[1].semantics()
        #pop scope from stack at end of block
        SCOPE.pop()

    def run(self, rover):
        global SCOPE
        SCOPE.push({})

        self.children[0].run(rover)
        self.children[1].run(rover)

        SCOPE.pop()