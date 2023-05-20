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

    def valid_temp(self, temp):
        id_name, dim, _ = temp

        if self.symbols[self.current_context]["temps"][id_name]:
            if (
                self.symbols[self.current_context]["temps"][id_name]["dimensions"]
                == dim
            ):
                return (
                    True,
                    self.symbols[self.current_context]["temps"][id_name]["var_type"],
                )
            else:
                raise ValueError(
                    f"trying to access a variable with different dimensions. Var '{id_name}' in {self.current_context}"
                )

        if self.symbols["global"]["temps"][id_name]:
            if self.symbols["global"]["temps"][id_name]["dimensions"] == dim:
                return (True, self.symbols["global"]["temps"][id_name]["var_type"])
            else:
                raise ValueError(
                    f"trying to access a variable with different dimensions. Var '{id_name}' in global"
                )

        return (False, "")

    def valid_var(self, var):
        id_name, dim = var
        if self.symbols[self.current_context]["vars"][id_name]:
            if self.symbols[self.current_context]["vars"][id_name]["dimensions"] == dim:
                return (
                    True,
                    self.symbols[self.current_context]["vars"][id_name]["var_type"],
                )
            else:
                raise ValueError(
                    f"trying to access a variable with different dimensions. Var '{id_name}' in {self.current_context}"
                )

        if self.symbols["global"]["vars"][id_name]:
            if self.symbols["global"]["vars"][id_name]["dimensions"] == dim:
                return (True, self.symbols["global"]["vars"][id_name]["var_type"])
            else:
                raise ValueError(
                    f"trying to access a variable with different dimensions. Var '{id_name}' in global"
                )

        return (False, "")

    def validate(self, op):
        if isinstance(op, tuple):
            if len(op) == 2:
                valid_op_l, validated_op_type = self.valid_var(op)
            elif len(op) == 3:
                valid_op_l, validated_op_type = self.valid_temp(op)

            dim = op[1]
            op = op[0]
            if not valid_op_l:
                raise ValueError(f"{op} is not declared")

            print("LOOOL: ", validated_op_type)
            return op, validated_op_type, dim
        else:
            return op, op, []

    def delete(self, name):
        del self.symbols[name]

    def print_symbols(self):
        for key, val in self.symbols.items():
            print(key)
            for key1, val1 in self.symbols[key].items():
                print(f"\t{key1}")
                print(f"\t\t{val1}")
            print()
