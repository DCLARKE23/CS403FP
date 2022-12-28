#added INT, BOOL, CHAR, FLOAT, STRING

"""
Create nodes + parse tree using grammar:

   <program>  ::= <block>
   <block>    ::= { <decls> <stmts> }
   <decls>    ::= e 
                | <decl> <decls>
   <decl>     ::= <type> ID ;
      <type>     ::= BASIC <typecl>
   <typecl>   ::= e 
                | [ NUM ] <typecl>
   <stmts>    ::= e 
                | <stmt> <stmts>
   <stmt>     ::= <loc> = <bool> ;
                | ROVER . ID ( <args> ) ;
                | IF ( <bool> ) <stmt>
                | IF ( <bool> ) <stmt> ELSE <stmt>
                | WHILE ( <bool> ) <stmt>
                | <block>
   <loc>      ::= ID <loccl>
   <loccl>    ::= e 
                | [ <bool> ] <loccl>
   <argscl>   ::= e
                | <loc> <args>
                | <method> ( <args> )
   <bool>     ::= <join> <boolcl>
   <boolcl>   ::= e 
                | || <join> <boolcl>
   <join>     ::= <equality> <joincl>
   <joincl>   ::= e 
                | && <equality> <joincl>
   <equality> ::= <rel> <equalcl>
   <equalcl>  ::= e 
                | == <rel> <equalcl> 
                | != <rel> <equalcl>
   <rel>      ::= <expr> <reltail>
   <reltail>  ::= e 
                | <= <expr>
                | >= <expr>
                | > <expr>
                | < <expr>
                | . ID ( <args> )
   <expr>     ::= <term> <exprcl>
   <exprcl>   ::= e
                | + <term> <exprcl>
                | - <term> <exprcl>
   <term>     ::= <unary> <termcl>
   <termcl>   ::= e
                | * <unary> <termcl>
                | / <unary> <termcl>
   <unary>    ::= ! <unary>
                | - <unary>
                | <factor>
   <factor>   ::= ( <bool> )
                | <loc>
                | NUM
                | REAL
                | TRUE
                | FALSE

"""
#imports
import enum
import sys
import pathlib
from table import table

#import from parser components
from parser_components import (
    FactorNode,
    UnaryNode,
    TermclNode,
    TermNode,
    ExprclNode,
    ExprNode,
    ReltailNode,
    RelNode,
    EqualclNode,
    EqualityNode,
    JoinclNode,
    JoinNode,
    BoolclNode,
    BoolNode,
    LocclNode,
    LocNode,
    StmtNode,
    StmtsNode,
    TypeclNode,
    TypeNode,
    DeclNode,
    DeclsNode,
    BlockNode,
    ProgramNode,
    MinusNode,
    Node,
    NonTerminals,
    NotNode,
    Token,
    Vocab,
)

#variables
CURR_TOKEN = None
FILE_CONTENT = []
TYPES = ["int", "char", "bool", "double"]
currType = None
currSymbol = None
className = None
value = None
length = -1
index = -1

TERMINALS = (
    set(
        [e.value for e in Vocab] + TYPES
    ) - set(
        # Ignore these vocab entries
        ["integer", "float", "basic", "id"]
    )
)

class UnexpectedTokenError(Exception):
    pass

#returns true if the input is a string (starts with " and ends with ")
def is_str(val):
    return val.startswith('"') and val.endswith('"')

#returns false if the input is a string
#returns false if the input is a double
#else returns true
def is_integer(val):
    try:
        if is_str(val):
            return False
        t = int(val)
        if str(t) != val:
            # If we've reached here, then we have a double
            # and the decimals were cut off
            return False
    except Exception:
        return False
    return True

#returns false if the input is a string
#returns flase if the input is an integer
#else returns true
def is_double(val):
    try:
        if is_str(val):
            return False
        t = float(val)
        if str(t) != val:
            return False
        if is_integer(val):
            # A float value would fail
            # the integer check
            return False
    except Exception:
        return False
    return True


def get_token():
    # Check if there's anything left in the file
    if len(FILE_CONTENT) == 0:
        return Token()
    #if there is a vocab entry for current token, return it
    #else return None
    def _get_vocab_entry(curr):
        for entry in Vocab:
            if entry.value == curr:
                return entry
        return None

    # Handle all the standard lexemes, types get a special one
    curr = FILE_CONTENT.pop()
    if curr in TERMINALS:
        if curr in TYPES:
            if curr == Vocab.INT: return Token(curr, Vocab.INT)
            if curr == Vocab.BOOL: return Token(curr, Vocab.BOOL)
            
        return Token(curr, _get_vocab_entry(curr))

    # Handle number literals
    if is_integer(curr):
        return Token(curr, Vocab.NUM)
    if is_double(curr):
        return Token(curr, Vocab.REAL)

    # Everything else is an identifier
    return Token(curr, Vocab.ID)

#determines if the current token is what is supposed to be next in grammar
#return true if current is same as next token in grammar
#else raise exception
def must_be(terminal):
    global CURR_TOKEN
    if Vocab[CURR_TOKEN.ttype.name] != terminal:
        raise UnexpectedTokenError(
            f"Unexpected token found: {CURR_TOKEN.value}, "
            f"expected: {terminal}"
        )
    CURR_TOKEN = get_token()
    return True

#determines if there is a case for the current token
def match_cases(*cases):
    for case in cases:
        if CURR_TOKEN.ttype == case:
            return True
    return False


# <factor>   ::= ( <bool> )
#              | <loc>
#              | NUM
#              | REAL
#              | TRUE
#              | FALSE
def Factor():
    #get current token
    #create new node for Factor
    global CURR_TOKEN
    current = FactorNode(NonTerminals.FACTOR)

    #if token is NUM, REAL, TRUE, or FALSE
    if match_cases(
        Vocab.NUM,
        Vocab.REAL,
        Vocab.TRUE,
        Vocab.FALSE,
    ):
        #add current token to Factor node
        current.add_child(Node(CURR_TOKEN))
        
        #get next token
        CURR_TOKEN = get_token()

    #if token is ID
    elif match_cases(Vocab.ID):
        #call Loc() and add it to Factor node
        current.add_child(Loc())

    else:
        #token is (
        must_be(Vocab.OPEN_PAREN)
        
        #call Bool() and add it to Factor node
        current.add_child(Bool())
        
         #next token is )
        must_be(Vocab.CLOSE_PAREN)

    #return Factor node
    return current


# <unary>    ::= ! <unary>
#              | - <unary>
#              | <factor>
def Unary():
    #get current token
    #create new UnaryNode for Unary
    global CURR_TOKEN
    current = UnaryNode(NonTerminals.UNARY)

    #if token is NOT or MINUS
    if match_cases(
        Vocab.NOT,
        Vocab.MINUS,
    ):
        #if token is NOT
        #create NotNode n
        if match_cases(Vocab.NOT):
            n = NotNode(CURR_TOKEN)

        #else if token is MINUS
        #create MinusNode n
        else:
            n = MinusNode(CURR_TOKEN)

        #add n to Unary node
        current.add_child(n)
        current.operation_node = n

        #get next token
        CURR_TOKEN = get_token()

        #call Unary() and add it to Unary node
        unode = Unary()
        current.add_child(unode)
        current.operand = unode

    #if token is not NOT or MINUS
    else:
        #call Factor and add it to Unary node
        fnode = Factor()
        current.add_child(fnode)
        current.operand = fnode

    #return Unary node
    return current


# <termcl>   ::= e
#              | * <unary> <termcl>
#              | / <unary> <termcl>
def Termcl():
    #get current token
    #create new node for Termcl
    global CURR_TOKEN
    current = TermclNode(NonTerminals.TERMCL)

    #if token is MUL or DIV
    if match_cases(
        Vocab.MUL,
        Vocab.DIV,
    ):
        #add token to Termcl node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #call Unary and Termcl and add each to Termcl node
        current.add_child(Unary())
        current.add_child(Termcl())

    #return Termcl node
    return current


# <term>     ::= <unary> <termcl>
def Term():
    #create new node for term
    current = TermNode(NonTerminals.TERM)

    #call Unary and Termcl and add each to Term node
    current.add_child(Unary())
    current.add_child(Termcl())

    #return term node
    return current


# <exprcl>   ::= e
#              | + <term> <exprcl>
#              | - <term> <exprcl>
def Exprcl():
    #get current token
    #create new node for exprcl
    global CURR_TOKEN
    current = ExprclNode(NonTerminals.EXPRCL)

    #if token is PLUS or MINUS
    if match_cases(
        Vocab.PLUS,
        Vocab.MINUS,
    ):
        #add current token to exprcl node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #call Term and Exprcl and add each to exprcl node
        current.add_child(Term())
        current.add_child(Exprcl())

    #return exprcl node
    return current


# <expr>     ::= <term> <exprcl>
def Expr():
    #create new node for expr
    current = ExprNode(NonTerminals.EXPR)

    #call term and exprcl and add each to expr node
    current.add_child(Term())
    current.add_child(Exprcl())

    #return expr node
    return current


# <reltail>  ::= e 
#              | <= <expr>
#              | >= <expr>
#              | > <expr>
#              | < <expr>
#              | . ID ( <args> )
def Reltail():
    #get current token
    #create new node for Reltail
    global CURR_TOKEN
    current = ReltailNode(NonTerminals.RELTAIL)

    #if token is LTEQ, GTEQ, LT, or GT
    if match_cases(
        Vocab.LTEQ,
        Vocab.GTEQ,
        Vocab.LT,
        Vocab.GT,
    ):
        #add current token to reltail node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #call expr and add to expr
        current.add_child(Expr())

    #if token is DOT
    elif match_cases(Vocab.DOT):
        #add curent token to reltail node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #next tokens must be ID and (
        must_be(Vocab.ID)
        must_be(Vocab.OPEN_PAREN)

        #call args and add to reltail node
        current.add_child(Args())

        #next token must be )
        must_be(Vocab.CLOSE_PAREN)

    #return reltail node
    return current


# <rel>      ::= <expr> <reltail>
def Rel():
    #create new node for rel
    current = RelNode(NonTerminals.REL)

    #call expr and reltail and add each to rel node
    current.add_child(Expr())
    current.add_child(Reltail())

    #return rel node
    return current


# <equalcl>  ::= e 
#              | == <rel> <equalcl> 
#              | != <rel> <equalcl>
def Equalcl():
    #get current token
    #create new node for equalcl
    global CURR_TOKEN
    current = EqualclNode(NonTerminals.EQUALCL)

    #if token is EQ or NEQ
    if match_cases(
        Vocab.EQ,
        Vocab.NEQ,
    ):
        #add current token to equalcl node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #call rel and equalcl and add each to equalcl node
        current.add_child(Rel())
        current.add_child(Equalcl())

    #return equalcl node
    return current


# <equality> ::= <rel> <equalcl>
def Equality():
    #create new node for equality
    current = EqualityNode(NonTerminals.EQUALITY)

    #call rel and equalcl and add each to equality node
    current.add_child(Rel())
    current.add_child(Equalcl())

    #return equality node
    return current


# <joincl>   ::= e 
#              | && <equality> <joincl>
def Joincl():
    #get current token
    #create new node for joincl
    global CURR_TOKEN
    current = JoinclNode(NonTerminals.JOINCL)

    #if token is AND
    if match_cases(Vocab.AND):
        #add next token to joincl node
        current.add_child(Node(CURR_TOKEN))
        
        #get next token
        CURR_TOKEN = get_token()

        #call equality and joincl and add each to joincl node
        current.add_child(Equality())
        current.add_child(Joincl())

    #return joincl node
    return current


# <join>     ::= <equality> <joincl>
def Join():
    #create new node for join
    current = JoinNode(NonTerminals.JOIN)

    #call equality and joincl and add each to join node
    current.add_child(Equality())
    current.add_child(Joincl())

    #return join node
    return current


# <boolcl>   ::= e 
#              | || <join> <boolcl>
def Boolcl():
    #get current token
    #create new node for boolcl
    global CURR_TOKEN
    current = BoolclNode(NonTerminals.BOOLCL)

    #if token if OR
    if match_cases(Vocab.OR):
        #add next token to boolcl node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #call join and boolcl and add each to boolcl node
        current.add_child(Join())
        current.add_child(Boolcl())

    #return boolcl node
    return current


# <bool>     ::= <join> <boolcl>
def Bool():
    #create new node for bool
    current = BoolNode(NonTerminals.BOOL)

    #call join and boolcl and add each to bool node
    current.add_child(Join())
    current.add_child(Boolcl())

    #return bool node
    return current


# <args>     ::= e
#              | <loc> <args>
#              | <method> ( <args> )
def Args():
    #get current token
    #create new node for args
    global CURR_TOKEN
    current = Node(NonTerminals.ARGS)

    #if token is )
    if match_cases(Vocab.CLOSE_PAREN):
        pass

    #if token if ID
    elif match_cases(Vocab.ID):
        #if next token is (
        if match_cases(Vocab.OPEN_PAREN):
            #add next token to args node
            current.add_child(Node(CURR_TOKEN))

            #get next token
            CURR_TOKEN = get_token()

            #call args and add to args node
            current.add_child(Args())

            #next token must be )
            must_be(Vocab.CLOSE_PAREN)

        else:
            #call loc and add to args node
            current.add_child(Loc())

    else:
        #add next token to args node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #call args and add to args node
        current.add_child(Args())

    #return args node
    return current


# <loccl>    ::= e 
#              | [ <bool> ] <loccl>
def Loccl():
    #get current token
    #create new node for loccl
    global CURR_TOKEN
    current = LocclNode(NonTerminals.LOCCL)

    #if token is [
    if match_cases(Vocab.OPEN_SQPAR):
        #get next token
        CURR_TOKEN = get_token()

        #call bool and add to loccl node
        current.add_child(Bool())

        #next token must be ]
        must_be(Vocab.CLOSE_SQPAR)

        #call loccl and add to loccl node
        current.add_child(Loccl())

    #return loccl node
    return current


# <loc>      ::= ID <loccl>
def Loc():
    #get current token
    #create new node for loc
    global CURR_TOKEN
    current = LocNode(NonTerminals.LOC)

    #add next token to loc node
    current.add_child(Node(CURR_TOKEN))

    #get value of token for symbol
    currSymbol = CURR_TOKEN.value

    #next token must be ID
    must_be(Vocab.ID)

    #call loccl and add to loc node
    current.add_child(Loccl())

    #return loc node
    return current


# #  <stmt>     ::= <loc> = <bool> ;
#                 | <loc> . ID ( <args> ) ;
#                 | ID ( <args> ) ;
#                 | IF ( <bool> ) <stmt>
#                 | IF ( <bool> ) <stmt> ELSE <stmt>
#                 | WHILE ( <bool> ) <stmt>
#                 | <block>
def Stmt():
    #get current token
    #create new node for stmt
    global CURR_TOKEN
    current = StmtNode(NonTerminals.STMT)

    #if token is IF
    if match_cases(Vocab.IF):
        #add token to stmt node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #next token must be (
        must_be(Vocab.OPEN_PAREN)

        #call bool and add to stmt node
        current.add_child(Bool())

        #next token must be )
        must_be(Vocab.CLOSE_PAREN)

        #call stmt and add to stmt
        current.add_child(Stmt())

        #if next token is ELSE
        if match_cases(Vocab.ELSE):
            #add token to stmt node
            current.add_child(Node(CURR_TOKEN))

            #get next token
            CURR_TOKEN = get_token()

            #call stmt and add ot stmt node
            current.add_child(Stmt())

    #if token is WHILE
    elif match_cases(Vocab.WHILE):
        #add token to stmt node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #next token must be (
        must_be(Vocab.OPEN_PAREN)

        #call bool and add to stmt node
        current.add_child(Bool())

        #next token must be )
        must_be(Vocab.CLOSE_PAREN)

        #call stmt and add to stmt node
        current.add_child(Stmt())

    #if token is {
    elif match_cases(Vocab.OPEN_BRACE):
        #call block and add to stmt node
        current.add_child(Block())

   

    #if next token is DOT
    elif match_cases(Vocab.ROVER):
        #add token to stmt node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #next tokens must be ID and (
        must_be(Vocab.DOT)
        must_be(Vocab.ID)
        must_be(Vocab.OPEN_PAREN)

        #call args and add to stmt
        current.add_child(Args())

        #next node must be )
        must_be(Vocab.CLOSE_PAREN)

        #next node must be SEMICOLON
        must_be(Vocab.SEMICOLON)
        
    else:
        #call loc and add to stmt node
        current.add_child(Loc())

        #add token to stmt node
        current.add_child(Node(CURR_TOKEN))

        #if next token is ASSIGN (=)
        if match_cases(Vocab.ASSIGN):

            #add token to stmt node
            current.add_child(Node(CURR_TOKEN))

            #get next token
            CURR_TOKEN = get_token()

            #call bool and add to stmt node
            current.add_child(Bool())
        #next node must be SEMICOLON
        must_be(Vocab.SEMICOLON)
    #return stmt node
    return current


# <stmts>    ::= e 
#              | <stmt> <stmts>
def Stmts():
    #create new node for stmts
    current = StmtsNode(NonTerminals.STMTS)

    #if token is }
    if match_cases(Vocab.CLOSE_BRACE):# More concise to start with Follow(<stmts>)
        pass

    else:
        #call stmt and stmts and add to stmts node
        current.add_child(Stmt())
        current.add_child(Stmts())

    #rturn stmts node
    return current


# <typecl>   ::= e 
#              | [ NUM ] <typecl>
def Typecl():
    #get current token
    #create new node for typecl
    global CURR_TOKEN
    current = TypeclNode(NonTerminals.TYPECL)

    #if token if [
    if match_cases(Vocab.OPEN_SQPAR):
        #get next token
        CURR_TOKEN=get_token()

        #add token to typecl node
        current.add_child(Node(CURR_TOKEN))

        #next tokens must be NUM and ]
        must_be(Vocab.NUM)
        must_be(Vocab.CLOSE_SQPAR)

        #call typecl and add to typecl node
        current.add_child(Typecl())

    #rturn typecl node
    return current


# <type>     ::= BASIC <typecl>
def Type():
    #get current token
    #create new node for type
    global CURR_TOKEN
    current = TypeNode(NonTerminals.TYPE)

    #if token is INT, BOOL, CHAR, STRING, or DOUBLE
    if match_cases(Vocab.BASIC):   
        #add token to type node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #call typecl and add to type node
        current.add_child(Typecl())

    #if token is CLASS
    elif match_cases(Vocab.CLASS):
        #add token to type node
        current.add_child(Node(CURR_TOKEN))

        #get next token
        CURR_TOKEN = get_token()

        #next token must be ID
        must_be(Vocab.ID)

    else:
        #call typecl and add to type node
        current.add_child(Typecl())
    
    #return type node
    return current

# <decl>     ::= <type> ID ;
def Decl():
    #get current node
    #create new node for decl
    global CURR_TOKEN
    current = DeclNode(NonTerminals.DECL)

    #call type and add to decl
    current.add_child(Type())

    #add token to type node
    current.add_child(Node(CURR_TOKEN))

    #next tokens must be ID and SEMICOLON
    must_be(Vocab.ID)
    must_be(Vocab.SEMICOLON)

    #return decl node
    return current


# <decls>    ::= e 
#              | <decl> <decls>
# Note: Follow(<decls>) = First(<stmt>) + Follow(<stmts>)
def Decls():
    #create new node for decls
    current = DeclsNode(NonTerminals.DECLS)

    #if token is IF, WHILE, {, ID, or }
    if match_cases(
        Vocab.IF,
        Vocab.WHILE,
        Vocab.OPEN_BRACE,
        Vocab.ID,
        Vocab.CLOSE_BRACE,
    ):
        pass

    else:
        #call decl and decls and add to decls node
        current.add_child(Decl())
        current.add_child(Decls())

    #return decls node
    return current


# <block>    ::= { <decls> <stmts> }
def Block():
    #create new node for block
    current = BlockNode(NonTerminals.BLOCK)
    
    #next token must be {
    must_be(Vocab.OPEN_BRACE)

    #call delcs and stmts and add to block node
    current.add_child(Decls())
    current.add_child(Stmts())

    #next token must be }
    must_be(Vocab.CLOSE_BRACE)

    #return block node
    return current


# <program>  ::= <block>
def Program():
    #crate new node for program
    current = ProgramNode(NonTerminals.PROGRAM)

    #call block and add to program node
    current.add_child(Block())

    #return program node
    return current


def get_parse_tree(file_content):
    """Returns a parse tree (AST) for the given file content.

    The file content needs to be a string. It will be split, and
    reversed by this method.
    """
    #get file content and current token
    global FILE_CONTENT
    global CURR_TOKEN

    #if file is empty, raise exception
    if not file_content:
        raise Exception("Empty program given! Cannot produce a parse tree.")

    # Split the content, then reverse the list so we
    # can use it like a stack
    FILE_CONTENT = file_content.split()[::-1]
    CURR_TOKEN = get_token()

    return Program()


if __name__=="__main__":
    if len(sys.argv) < 2:
        raise Exception("Missing file path to parse.")
    elif len(sys.argv) > 2:
        raise Exception("Only 1 argument is needed, but more were given.")

    fcontent = None
    filepath = pathlib.Path(sys.argv[1])
    with filepath.open() as f:
        fcontent = f.read()

    program = get_parse_tree(fcontent)
    program.check_semantics()
    program.run()