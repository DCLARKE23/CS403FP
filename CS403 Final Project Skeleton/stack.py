
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
            return self.stack[len(self.stack)-1]

    def checkScopes(self, id):
        i = len(self.stack)
        while i > 0:
            if id == self.stack[i]['id']:
                return True
            i -= 1
        return False

    def getId(self, id):
        i = len(self.stack)
        while i > 0:
            if id == self.stack[i]['id']:
                return self.stack[i]
            i -= 1
#-------RAISE ERROR

    def assign(self, obj, val):
        id = obj['id']
        ttype = obj['ttype']
        if ttype == 'int':
            val = int(val)

        if len(obj['arr']) == 0:
            i = len(self.stack)
            while i > 0:
                if id == self.stack[i]['id']:
                    self.stack[i]['val'] = val
                i -= 1
        
        else:
            item = []
            i = len(self.stack)
            while i > 0:
                if id == self.stack[i]['id']:
                    self.stack[i]['val'] = val
                i -= 1
            
            for i in obj['arr'][0:-1]:
                item = item[i]

            item[obj['arr'][-1]] = val