class IncorrectTypeError(Exception):
    def __init__(self, expected, type_):
        self.expected = expected
        self.type_ = type_

    def TMerror(self):
        return f"[TYPE MISMATCH]: expected '{self.expected}' but got '{self.type_}'"

class UndeclaredError(Exception):
    def __init__(self, name):
        self.name = name

    def UVerror(self):
        return f"[UNDECLARED VARIABLE]: variable {self.name} is either not defined or outside of scope."

class UndefinedError(Exception):
    def __init__(self, name):
        self.name = name

    def UDerror(self):
        return f"[UNDEFINED VARIABLE]: variable {self.name} is undefined"

class RedefinedError(Exception):
    def __init__(self, name):
        self.name = name

    def RDerror(self):
        return f"[REDEFINED VARIABLE]: variable {self.name} is already defined."