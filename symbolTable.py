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
        self.temp_counter = 1
        self.__constant_address = 20000
        self.__local_address = 10000
        self.__global_address = 0

    def get_current_temp(self):
        return self.temp_counter

    def increase_temp_counter(self):
        self.temp_counter += 1

    def change_context(self, context):
        print("changing context to: ", context)
        self.current_context = context

    def insert(self, insert_type, dim=False, **kwargs):
        if insert_type == "var":
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context]["vars"][kwargs["id_name"]][
                        key
                    ] = value
            if self.current_context == "global":
                self.symbols[self.current_context]["vars"][kwargs["id_name"]]["v_address"] = self.__global_address
                self.__global_address += 1
            else:
                self.symbols[self.current_context]["vars"][kwargs["id_name"]]["v_address"] = self.__local_address
                self.__local_address += 1
            if dim:
                self.if_var_has_dim_allocate_memory(**kwargs)

        if insert_type == "temp":
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context]["temps"][kwargs["id_name"]][
                        key
                    ] = value
            self.symbols[self.current_context]["temps"][kwargs["id_name"]]["v_address"] = self.__local_address
            self.__local_address += 1
        elif insert_type == "params":
            for key, value in kwargs.items():
                self.symbols[self.current_context][key] = value

        elif insert_type == "constant":
            if not self.symbols["constants"][kwargs["id_name"]]:
                self.symbols["constants"][kwargs["id_name"]]["v_address"] = self.__constant_address
                self.__constant_address += 1

        elif insert_type == "return":
            _, var_type, _,_ = self.validate(kwargs["exp"])

            self.symbols["global"]["vars"][self.current_context]["var_type"] = var_type

        elif insert_type == "func":
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context][key] = value

    def if_var_has_dim_allocate_memory(self, **kwargs):
        if len(kwargs["dimensions"]) != 0:
            var_size = 1
            for dim in kwargs["dimensions"]:
                var_size *= dim
            if self.current_context != "global":
                self.__local_address += var_size - 1
            else:
                self.__global_address += var_size - 1

    def insert_quad_index_where_func_starts(self, quad_index):
        """Insert quad index where function starts

            Vars: int, quad index of the first instruction of the function
        """
        self.symbols[self.current_context]["ini_quad"] = quad_index

    def reset_local_memory(self):
        """ Resets the local memory counter (temps and local vars)
        """
        self.reset_locals()
        self.temp_counter = 1


    def reset_locals(self):
        self.__local_address = 10000

    def get_current_context(self):
        return self.current_context

    def func_exists(self, func_name):
        if self.symbols[func_name]:
            return True
        return False

    def validate_args(self, func_id, args):
        """Check whether the number and type of args are correct.
        It raises an error otherwise

        Vars:
            func_id: function to check parameters
            args: list(str), list of args in function call

        Return:
            List(str): list with all the ids of the args
        """
        params = self.symbols[func_id]["params"]
        num_param = len(params)
        num_args = len(args)

        if num_args < num_param or num_args > num_param:
            raise ValueError(
                f"Function {func_id} expected {num_param} arguments, {num_args} received"
            )

        arg_ids = []
        v_addresses = []
        for i, (arg, param_type) in enumerate(zip(args, params)):
            identifier, arg_type, _, v_address = self.validate(arg)
            
            if isinstance(arg_type, int):
                identifier = arg_type
                arg_type = "int"

            elif isinstance(arg_type, float):
                identifier = arg_type
                arg_type = "float"

            elif isinstance(arg_type, bool):
                identifier = arg_type
                arg_type = "bool"

            elif len(arg_type) < 3:
                identifier = arg_type
                arg_type = "char"

            if arg_type != param_type:
                raise ValueError(
                    f"Expected '{param_type}' in arg {i+1}, received a '{arg_type}' in call to function '{func_id}'"
                )

            arg_ids.append(identifier)
            v_addresses.append(v_address)

        return arg_ids, v_addresses

    def insert_func_size(self):
        func_vars = len(self.symbols[self.current_context]["vars"])
        func_temp = len(self.symbols[self.current_context]["temps"])

        self.symbols[self.current_context]["size"] = func_vars + func_temp

    def insert_global_size(self):
        self.symbols[self.current_context]["size"] = len(
            self.symbols[self.current_context]["vars"]
        )

    def insert_main_size(self):
        main_vars = len(self.symbols[self.current_context]["vars"])
        temp_vars = len(self.symbols[self.current_context]["temps"])

        self.symbols[self.current_context]["size"] = main_vars + temp_vars

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

    def is_return_type_ok(self, exp):
        """Checks whether the returned exp is the same type as the function return"""
        id_name, var_type, dim, _ = self.validate(exp)
        func_return_type = self.symbols[self.current_context]["return_type"]

        if isinstance(var_type, int):
            var_type = "int"

        elif isinstance(var_type, float):
            var_type = "float"

        elif isinstance(var_type, bool):
            var_type = "bool"

        elif len(var_type) < 3:
            var_type = "char"

        if var_type != func_return_type:
            raise ValueError(
                f"Return statement in '{self.current_context}' expected type '{func_return_type}', received '{var_type}' instead"
            )

    def validate_return_function(self, function_name):
        """Validate if the function call in fact returned something

        Vars:
            function_name: function name
        """

        if self.symbols[function_name]["return_type"] == "void":
            return self.symbols[function_name]["return_type"]
        
        if self.symbols["global"]["vars"][function_name]:
            ret_type = self.symbols["global"]["vars"][function_name]["var_type"]
            return ret_type
        else:
            raise ValueError(f"Function '{function_name}' does not returning anything.")

    def validate(self, identifier):
        """Validate identifier
        Vars:
            identifier: tuple(3) or tuple(2), or primitive type

        Return:
            Tuple
                0 - identifier
                1 - primitive var_type
                2 - list of dimensions
        """
        # self.print_symbols()
        # print("this is printing: ", identifier)

        if isinstance(identifier, tuple) and len(identifier) == 2:
            id_name, _ = identifier
            is_valid, var_type, v_address = self.__validate("temps", id_name)
            identifier = identifier[0]
            if not is_valid:
                raise ValueError(f"{identifier} is not declared")

            return identifier, var_type, v_address

        elif isinstance(identifier, tuple) and len(identifier):
            id_name = identifier
            is_valid, var_type, v_address = self.__validate("vars", id_name)
            identifier = identifier[0]
            if not is_valid:
                raise ValueError(f"{identifier} is not declared")

            return identifier, var_type, v_address
        else:
            v_address = self.get_virtual_add_const(identifier)
            return identifier, identifier, v_address
    
    def get_virtual_add_const(self,constant):
        """Search for the virtual address of a constant

            Vars:
                constant: int, str, float

            Return:
                virtual address: int
        """
        return self.symbols["constants"][constant]["v_address"]

    def __validate(self, type_var, id_name):
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
            return (
                True,
                self.symbols[self.current_context][type_var][id_name]["var_type"],
                self.symbols[self.current_context][type_var][id_name]["v_address"]
            )
        else:
            del self.symbols[self.current_context][type_var][id_name]

        curr_context = self.current_context
        self.change_context("global")
        if self.symbols[self.current_context][type_var][id_name]:
            var_type = self.symbols[self.current_context][type_var][id_name]["var_type"]
            v_address = self.symbols[self.current_context][type_var][id_name]["v_address"]
            self.change_context(curr_context)

            return (
                True,
                var_type,
                v_address
            )
        else:
            del self.symbols[self.current_context][type_var][id_name]
        self.change_context(curr_context)
        return (False, "",0)

    def delete(self, name):
        del self.symbols[name]

    def print_symbols(self):
        for key, val in self.symbols.items():
            print(key)
            for key1, val1 in self.symbols[key].items():
                print(f"\t{key1}")
                print(f"\t\t{val1}")
            print()
