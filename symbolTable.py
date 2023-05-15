class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def insert(self, name, value):
        self.symbols[name] = value

    def lookup(self, name):
        return self.symbols.get(name)

    def delete(self, name):
        del self.symbols[name]
