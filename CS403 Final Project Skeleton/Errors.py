from stack import stack

class errors(Exception):
    def __init__(self, name, expected, type_):
        self.expected = expected
        self.name = name
        self.type_ = type_
        global SCOPE_STACK
        SCOPE_STACK = stack()

    def TypeMismatch(self,expected,type_):
        return f"[TYPE MISMATCH]: expected '{self.expected}' but got '{self.type_}'"

    def UndeclaredVar(self):
        return f"[UNDECLARED VARIABLE]: variable {self.name} is either not defined or outside of scope."

    def RedefinedVar(self):
        return f"[REDEFINED VARIABLE]: variable {self.name} is already defined."