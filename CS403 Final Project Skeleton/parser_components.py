import enum
from stack import stack

SCOPE = stack()


class TypeMismatchError(Exception):
    pass

#added INT, BOOL, CHAR, FLOAT, STRING
class Vocab(enum.Enum):
    EOS = ""
    OPEN_PAREN = "("
    CLOSE_PAREN = ")"
    OPEN_BRACE = "{"
    CLOSE_BRACE = "}"
    OPEN_SQPAR = "["
    CLOSE_SQPAR = "]"
    INT = "int"
    BOOL = "bool"
    CHAR = "char"
    FLOAT = "float"
    DOUBLE = "double"
    STRING = "string"
    CLASS = "class"
    FUNTION = "function"
    METHOD = "method"
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

    def match_types(self, target_types):
        my_types = self.get_types()
        if any(
            ttype in my_types
            for ttype in target_types
            ):
            return True
        return False

    def raise_type_mismatch_error(self, target):
        raise TypeMismatchError(
            f"Expected these types {self.get_types()}, "
            f"but found {target}"
        )

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


class ProgramNode(Node):
    def run(self, scope):
        """
        Note that you can also build the SCOPE while going through
        the scope checking for the declarations.
        """
        global SCOPE
        SCOPE = scope

        result = -9
        for child in self.children:
            result = child.run()
        if result in (0,):
            print(f"Successfully ran the program, exited with: {result}")
        else:
            print(f"Failed to run program, exited with: {result}")


class MinusNode(ProgramNode):
    def get_types(self):
        return ("double", "int",)

    def check_scopes(self):
        global SCOPE
        self.operand.check_scopes()

    def check_types(self):
        global SCOPE
        if not self.match_types(self.operand.get_types()):
            self.raise_type_mismatch_error(self.operand.get_types())

    def run(self):
        """ What does this do?

        In this node, you only have one child. We run, the child then
        multiply it's result by -1. In this case, the child MUST return
        an int or a double (hint for type checking above), then we
        return this result.

        Value storage, and retrieval should be done within the scope, e.g.
        the scope entry for an `int i ; i = 10 ;` should look something
        like this within the scope entry:
            SCOPE = {
                "i": {
                    "name": "i"
                    "value": 10
                }
            }
        """
        return self.operand.run() * -1


class NotNode(ProgramNode):
    pass


class FactorNode(Node):
    def semantics(self):
        if isinstance(self.children[0], BoolNode):
            return self.children[0].check_semantics()

        elif isinstance(self.children[0], LocNode):
            type = self.children[0].check_semantics()
            #add error if factor is array

        elif self.children[0].token.ttype == Vocab.NUM:
            return {'ttype': 'int',
                    'arr': False,
                    'dimen': 0,
                    'val': None}

        elif self.children[0].token.ttype == Vocab.REAL:
            return {'ttype': 'double',
                    'arr': False,
                    'dimen': 0,
                    'val': None}

        elif self.children[0].token.ttype == Vocab.TRUE or self.children.token.ttype == Vocab.FALSE:
            return {'ttype': 'bool',
                    'arr': False,
                    'dimen': 0,
                    'val': None}
#change to stop copying
    def run(self, rover):
        def arrIndex(obj):
            arr = obj['val']
            for i in obj['3dArr'][0:-1]:
                arr = arr[i]
            return arr[obj['3dArr'][-1]]

        if isinstance(self.children[0], BoolNode):
            return self.children[0].run(rover)

        elif isinstance (self.children[0], LocNode):
            info = self.children[0].run(rover)
            if len(info['3dArr']) == 0:
                value = info['val']
            else:
                value = arrIndex(info)
            return value

        elif self.children[0].token.ttype == Vocab.NUM:
            return int(self.children[0].token.value)

        elif self.children[0].token.ttype == Vocab.REAL:
            return float(self.children[0].token.value)

        elif self.children[0].token.ttype == Vocab.TRUE:
            return True

        elif self.children[0].token.ttype == Vocab.FALSE:
            return False


class UnaryNode(Node):
    def check_semantics(self):
        if len(self.children) == 1:
            return self.children[0].check_semantics()

        else:
            info = self.children[1].check_semantics()
            operator = self.children[0].token.value
            type = info['ttype']

            if (operator == '!' and type == 'bool') or (operator == '-' and (type == 'int' or type == 'double')):
                return info
    def run(self, rover):
        if len(self.children) == 1:
            return self.children[0].run(rover)
        else:
            obj = self.children[1].run(rover)
            operator = self.children[0].token.value
            if operator == '!':
                return not obj
            else:
                return - obj

class TermclNode(Node):
    def check_semantics(self):
        if len(self.children) == 0:
            return None
        else:
            unaryInfo = self.children[1].check_semantics()
            termclInfo = self.children[2].check_semantics()

            if termclInfo == None:
                return unaryInfo
            
            unaryType = unaryInfo['ttype']
            termclType = termclInfo['ttype']
#-----------raise error
            
            if unaryType != termclType:
                unaryInfo['ttype'] = 'double'
            return unaryInfo

    def run(self, rover, term):
        if len(self.children) == 0:
            return term

        else:
            operator = self.children[0].token.value
            unaryVal = self.children[1].run(rover)

            if operator == '*':
                unaryVal = term * unaryVal
            else:
                if unaryVal == 0:
                    #raise error
                    print("error")
                unaryVal = term/unaryVal

            termclVal = self.children[2].run(rover, unaryVal)
            return termclVal

class TermNode(Node):
    def check_semantics(self):
        unaryInfo = self.children[1].check_semantics()
        termInfo = self.children[2].check_semantics()

        if termInfo == None:
            return unaryInfo
            
        unaryType = unaryInfo['ttype']
        termType = termInfo['ttype']
#-----------raise error
            
        if unaryType != termType:
            unaryInfo['ttype'] = 'double'
        return unaryInfo

    def run(self, rover):
        unaryObj = self.children[0].run(rover)
        termObj = self.children[0].run(rover, unaryObj)
        return termObj


class ExprclNode(Node):
    def check_semantics(self):
        if len(self.children) == 0:
            return None

        else:
            termInfo = self.children[1].check_semantics()
            exprclInfo = self.children[2].check_semantics()

            if termInfo == None:
                return exprclInfo
            
            termTtype = termInfo['ttype']
            exprclType = exprclInfo['ttype']
#-----------raise error
            
            if termTtype != exprclType:
                termInfo['ttype'] = 'double'
            return termInfo

    def run(self, rover, expr):
        if len(self.children) == 0:
            return expr
        else:
            operator = self.children[0].token.value
            termObj = self.children[1].run(rover)

            if operator == '+':
                termObj = expr + termObj
            else:
                termObj = expr - termObj

            exprclObj = self.children[2].run(rover, termObj)
            return exprclObj

class ExprNode(Node):
    def check_semantics(self):
        termInfo = self.children[1].check_semantics()
        exprInfo = self.children[2].check_semantics()

        if termInfo == None:
            return exprInfo
            
        termType = exprInfo['ttype']
        exprType = termInfo['ttype']
#-----------raise error
            
        if termType != exprType:
            termInfo['ttype'] = 'double'
        return termInfo

    def run(self, rover):
        termObj = self.children[0].run(rover)
        exprObj = self.children[0].run(rover, termObj)
        return exprObj

class ReltailNode(Node):
    def check_semantics(self):
        if len(self.children) == 0:
            return None

        else:
            exprInfo = self.children[1].check_semantics()
            return exprInfo

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
    def check_semantics(self):
        exprInfo = self.children[0].check_semantics()
        reltailInfo = self.children[1].check_semantics()

        if reltailInfo == None:
            return exprInfo

        if exprInfo == 'bool' and reltailInfo == 'bool':
            #raise error
            print("error")
        
        exprInfo['ttype'] = 'bool'
        return exprInfo

    def run(self, rover):
        exprObj = self.children[0].run(rover)
        reltailObj = self.children[1].run(rover, exprObj)
        return reltailObj

class EqualclNode(Node):
    def check_semantics(self):
        if len(self.children) == 0:
            return None

        else:
            relInfo = self.children[1].check_semantics()
            equalclInfo = self.children[2].check_semantics()

#-----------raise errors
            relInfo['ttype'] = 'bool'
            return relInfo

    def run(self, rover, rel):
        if len(self.children) == 0:
            return rel

        else:
            operator = self.children[0].token.value
            relObj = self.children[1].run(rover)

            if operator == '==':
                relObj = rel == relObj
            elif operator == '!=':
                relObj = rel != relObj

            equalclObj = self.children[2].run(rover, relObj)
            return equalclObj


class EqualityNode(Node):
    def check_semantics(self):
        relInfo = self.children[0].check_semantics()
        equalclInfo = self.children[1].check_semantics()

        if equalclInfo == None:
            return relInfo

#-----------raise error

        relInfo['ttype'] = 'bool'
        return relInfo
    
    def run(self, rover):
        relObj = self.children[0].run(rover)
        equalclObj = self.children[1].run(rover, relObj)
        return equalclObj

class JoinclNode(Node):
    def check_semantics(self):
        if len(self.children) == 0:
            return None
        
        else:
            equalityInfo = self.children[1].check_semantics()
            joinclInfo = self.children[2].check_semantics()

            if joinclInfo == None:
                return equalityInfo

#-----------raise error

            return equalityInfo

    def run(self, rover, join):
        if len(self.children) == 0:
            return join
        
        else:
            equalityObj = self.children[1].run(rover)
            equalityObj = join and equalityObj
            joinObj = self.children[2].run(rover, equalityObj)
            return joinObj

class JoinNode(Node):
    def check_semantics(self):
        equalityInfo = self.children[0].check_semantics()
        joinclInfo = self.children[1].check_semantics()
        
        if joinclInfo == None:
            return equalityInfo

#-------raise error

        return joinclInfo

    def run(self, rover):
        equalityObj = self.children[0].run(rover)
        joinclObj = self.children[1].run(rover, equalityObj)
        return joinclObj

class BoolclNode(Node):
    def check_semantics(self):
        if len(self.children) == 0:
            return None

        else:
            joinInfo = self.children[1].check_semantics()
            boolclInfo = self.children[2].check_semantics()

            if boolclInfo == None:
                return joinInfo

#-----------raise error

            return joinInfo

    def run(self, rover, boolcl):
        if len(self.children) == 0:
            return boolcl

        else:
            joinObj = self.children[1].run(rover)
            joinObj = boolcl or joinObj

            boolclObj = self.children[2].run(rover, joinObj)
            return boolclObj

class BoolNode(Node):
    def check_semantics(self):
        joinInfo = self.children[0].check_semantics()
        boolclInfo = self.children[1].check_semantics()

        if boolclInfo == None:
            return joinInfo

#-------raise error

        return boolclInfo

    def run(self, rover):
        joinObj = self.children[0].run(rover)
        boolclObj = self.children[1].run(rover, joinObj)
        return boolclObj

class LocclNode(Node):
    def check_semantics(self):
        if len(self.children) == 0:
            return {'ttype': None,
                    'arr': False,
                    'dimen': 0,
                    'val': None}

        else:
           index = self.children[0].check_semantcis()

#----------raise error

           locclInfo = self.children[1].check_semantics()
           locclInfo['dimen'] = locclInfo['dimen'] + 1
           locclInfo['arr'] = True
           return locclInfo

    def run(self, rover):
        if len(self.children) == 0:
            return None

        else:
            boolObj = self.children[0].run(rover)
            locclObj = self.children[1].run(rover)

            if locclObj == None:
                return [boolObj]
            else:
                return [boolObj] + locclObj

class LocNode(Node):
    def check_semantics(self):
        global SCOPE
        id = self.children[0].token.value

#-------raise

        symbol = SCOPE.getId(id)
        type = self.children[1].check_semantics()
        typeDimen = symbol['dimen'] - type['dimen']

#-------raise error

        if typeDimen > 0: 
            arr = True
        else:
            arr = False

        return {'ttype': symbol['ttype'],
                'arr': arr,
                'dimen': typeDimen,
                'val': None}

    def run(self, rover):
        global SCOPE
        id = self.children[0].token.value
        obj = SCOPE.getId(id)
        arr = self.children[1].run(rover)

        if arr == None:
            return {'id': id,
                    'val': obj['val'],
                    'ttype': obj['ttype'],
                    'arr': []}

        else:
            return {'id': id,
                    'val': obj['val'],
                    'ttype': obj['ttype'],
                    'arr': arr}

class StmtNode(Node):
    def check_semantics(self):
        if isinstance(self.children[0], LocNode):
            symbol = self.children[0].check_semantics()
            type = self.children[1].check_semantics()

#-----------raise error

        elif isinstance(self.children[0], BlockNode):
            self.children[0].check_semantics()

        elif self.children[0].token.value == Vocab.ROVER:
            self.children[1].check_semantics()

        elif self.children[0].token.value == Vocab.IF or self.children[0].token.value == Vocab.WHILE:
            condition = self.children[1].check_semantics()

#-----------raise error
            
            self.children[2].check_semantics()
            if len(self.children) > 3:
                self.children[4].check_semantics()

    def run(self, rover):
        global SCOPE
        if isinstance(self.children[0], LocNode):
            id = self.children[0].run(rover)
            val = self.children[2].run(rover)

            SCOPE.assign(id, val)

        elif isinstance(self.children, BlockNode):
            self.children[0].run(rover)

        elif self.children[0].token.value == Vocab.ROVER:
            self.children[1].run(rover)

        elif self.children[0].token.value == Vocab.IF:
            boolObj = self.children[1].run(rover)
            if boolObj:
                self.children[2].run(rover)
            elif len(self.children) > 3 and not boolObj:
                self.children[4].run(rover)

        elif self.children[0].token.value == Vocab.WHILE:
            while True:
                if not (self.children[1].run(rover)):
                    break
                self.children[2].run(rover)

class StmtsNode(Node):
    def check_semantics(self):
        if len(self.children) > 0:
            stmtInfo = self.children[0].check_semantics()
            stmtsInfo = self.children[1].check_semantics()

    def run(self, rover):
        if len(self.children) > 0:
            stmtObj = self.children[0].run(rover)
            stmtsObj = self.children[1].run(rover)

class TypeclNode(Node):
    def check_semantics(self):
        if len(self.children) == 0:
            return {'ttype': None,
                    'arr': False,
                    'dimen': 0,
                    'val': None}

        else:
            type = self.children[1].check_semantics()
            type['dimen'] = type['dimen'] + 1
            type['arr'] = True
            return type

    def run(self, rover):
        if len(self.children) == 0:
            return None
        
        else:
            len = int(self.children[0].token.value)
            subarr = self.children[1].run(rover)
            newArr = []

            for i in range(0, len):
                newArr.append(subarr)

            return newArr

class TypeNode(Node):
    def check_semantics(self):
        typeclnfo = self.children[1].check_semantics()
        typeclnfo['ttype'] = self.children[0].token.value

        return typeclnfo

    def run(self, rover):
        ttype = self.children[0].token.value
        arr = self.children[1].run(rover)

        if arr == None:
            return {'ttype': ttype, 'val': arr}

class DeclNode(Node):
    def check_semantics(self):
        global SCOPE

        type = self.children[0].check_semantics()
        id = self.children[1].token.value

        SCOPE.top()[id] = type

    def run(self, rover):
        global SCOPE
        typeObj = self.children[0].run(rover)
        id = self.children[1].token.value

        SCOPE.top()[id] = typeObj

class DeclsNode(Node):
    def check_semantics(self):
        if len(self.children) > 0:
            self.children[0].check_semantics()
            self.children[1].check_semantics()

    def run(self, rover):
        if len(self.children) > 0:
            self.children[0].run(rover)
            self.children[1].run(rover)

class BlockNode(Node):
    def check_semantics(self):
        global SCOPE
        SCOPE.push({})

        self.children[0].check_semantics()
        self.children[1].check_semantics()

        SCOPE.pop()

    def run(self, rover):
        global SCOPE
        SCOPE.push({})

        self.children[0].run(rover)
        self.children[1].run(rover)

        SCOPE.pop()

class FeatureNode(Node):
    pass