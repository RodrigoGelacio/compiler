from collections import defaultdict


class SymbolTable:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(SymbolTable, self).__new__(self)
        return self._instance

    def __init__(self):
        self.symbols = defaultdict(lambda: defaultdict(dict))
        self.current_context = "global"

    def change_context(self, context):
        self.current_context = context

    def insert(self, insert_type, **kwargs):
        if insert_type == "var":
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context][kwargs["id_name"]][key] = value
        elif insert_type == "func":
            self.change_context(kwargs["id_name"])
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context][key] = value
            self.change_context("global")

    def lookup(self, name):
        return self.symbols.get(name)

    def delete(self, name):
        del self.symbols[name]

    def print_symbols(self):
        for key, val in self.symbols.items():
            print(key)
            print(f"\t{val}")
