from collections import defaultdict
from cubo_semantico import ella_baila_sola


class SymbolTable:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(SymbolTable, self).__new__(self)
        return self._instance

    def __init__(self):
        self.symbols = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        self.current_context = "global"
        self.__current_temporal = 1

    def get_current_temp(self):
        return self.__current_temporal

    def increase_temp_counter(self):
        self.__current_temporal += 1

    def change_context(self, context):
        self.current_context = context

    def insert(self, insert_type, **kwargs):
        if insert_type == "var":
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context]["vars"][kwargs["id_name"]][
                        key
                    ] = value

        if insert_type == "temp":
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context]["temps"][kwargs["id_name"]][
                        key
                    ] = value

        elif insert_type == "func":
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context][key] = value

    def is_it_already_declared(self, id_name):
        """Check whether the identifier has already been declared

        Vars:
            id_name: str, name of the identifier

        Returns:
            Bool: whether it is already declared or not
        """
        if self.symbols[self.current_context]["vars"][id_name] == {}:
            return False

        return True

    def validate(self, identifier):
        """Validate identifier
        Vars:
            column: either "temp" or "var"

        Return:
            Tuple
                0 - identifier
                1 - primitive var_type
                2 - list of dimensions
        """
        if isinstance(identifier, tuple) and len(identifier) == 3:
            id_name, dim, _ = identifier
            is_valid, var_type = self.__validate("temps", id_name, dim)
            identifier = identifier[0]
            if not is_valid:
                raise ValueError(f"{identifier} is not declared")

            return identifier, var_type, dim

        elif isinstance(identifier, tuple) and len(identifier) == 2:
            id_name, dim = identifier
            is_valid, var_type = self.__validate("vars", id_name, dim)
            identifier = identifier[0]
            if not is_valid:
                raise ValueError(f"{identifier} is not declared")

            return identifier, var_type, dim
        else:
            return identifier, identifier, []

    def __validate(self, type_var, id_name, dim):
        """Check if the id_name is registered with correct dimensionality

        Vars:
            type_var: either "vars" or "temps"
            id_name: name of identifier
            dim: list of identifier dimensions

        Return:
            Tuple
                0 - boolean wether it is a valid identifier
                1 - primitive var type
        """

        if self.symbols[self.current_context][type_var][id_name]:
            if self.__valid_dimensionality(type_var, id_name, dim):
                return (
                    True,
                    self.symbols[self.current_context][type_var][id_name]["var_type"],
                )

        curr_context = self.current_context
        self.change_context("global")
        if self.symbols[self.current_context][type_var][id_name]:
            if self.__valid_dimensionality(type_var, id_name, dim):
                return (
                    True,
                    self.symbols[self.current_context][type_var][id_name]["var_type"],
                )
        self.change_context(curr_context)
        return (False, "")

    def __valid_dimensionality(self, column, id_name, dim):
        """Check whether the access dim is valid. Raise errors in case the dim access
        is wrong or there is an out of bounds access.

        Vars:
            search_id_section: column to search in a table
            id_name: name of variable
            dim: list containing dimensions

        Return:
            bool: only return True if it is a valid dimensionality, otherwise
                    it raises an Error.
        """
        searched_dim = self.symbols[self.current_context][column][id_name]["dimensions"]
        if len(searched_dim) != len(dim):
            raise ValueError(
                f"Wrong dimensionality access in {id_name} at {self.current_context} "
            )

        for i, e in enumerate(searched_dim):
            if dim[i] >= e:
                raise ValueError(f"Out of bounds access on {id_name}")
        return True

    def delete(self, name):
        del self.symbols[name]

    def print_symbols(self):
        for key, val in self.symbols.items():
            print(key)
            for key1, val1 in self.symbols[key].items():
                print(f"\t{key1}")
                print(f"\t\t{val1}")
            print()
