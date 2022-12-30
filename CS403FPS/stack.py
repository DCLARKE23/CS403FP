from Errors import UndefinedError
#constructed stack to help keep track of variables
class stack:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        self.stack.pop()

    def top(self):
        if len(self.stack) <= 0:
            raise Exception
        else:
            return self.stack[len(self.stack) - 1]
# functions such that each time a function is exited or scope is changed, variables in that scope are popped
    def checkScopes(self, id):
        i = len(self.stack)-1
        while i >= 0:
            if id in self.stack[i]:
                return True
            i -= 1
        return False

    def getId(self, id):
        i = len(self.stack)-1
        while i >= 0:
            if id in self.stack[i]:
                return self.stack[i]
            i -= 1

        raise UndefinedError(id)


    def assign(self, obj, val):
        id = obj['id']
        ttype = obj['ttype']
        if ttype == 'int':
            val = int(val)

        if len(obj['arr']) == 0:
            i = len(self.stack)-1
            while i >= 0:
                if id in self.stack[i]:
                    self.stack[i][id]['val'] = val
                i -= 1

        else:
            item = []
            i = len(self.stack)-1
            while i >= 0:
                if id in self.stack[i]:
                    self.stack[i][id]['val'] = val
                i -= 1

            for i in obj['arr'][0:-1]:
                item = item[i]

            item[obj['arr'][-1]] = val