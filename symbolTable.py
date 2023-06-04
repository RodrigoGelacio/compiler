from collections import defaultdict
import math


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
        self.ptr_counter = 1
        self.__pt_address = 30000
        self.__constant_address = 20000
        self.__local_address = 10000
        self.__global_address = 0

    def get_return_type_func(self, func_id):
        return self.symbols[func_id]["return_type"]

    def get_func_var_dims(self, func_id, var_id):
        dimensions = self.symbols[func_id]["vars"][var_id].get("dimensions", {})
        return dimensions

    def get_func_true_size(self, func_id):
        func_vars = self.symbols[func_id]["vars"]

        true_size = self.symbols[func_id]["size"]

        for key in func_vars.keys():
            # print("THIS IS THE KEY: ", key)
            dimensions = func_vars[key].get("dimensions", {})
            if dimensions:
                cells = math.prod(func_vars[key]["dimensions"])
                true_size += cells - 1

        return true_size

    def get_param_v_add(self, func_id, index):
        return self.symbols[func_id]["param_v_add"][index]
    
    def get_globals_true_size(self):
        glob_vars = self.symbols["global"]["vars"]

        true_size = self.symbols["global"]["size"]

        for key in glob_vars.keys():
            # print("THIS IS THE KEY: ", key)
            dimensions = glob_vars[key].get("dimensions", {})
            if dimensions:
                cells = math.prod(glob_vars[key]["dimensions"])
                true_size += cells - 1

        return true_size

    def get_global_var_dims(self, var_id):
        dimensions = self.symbols["global"]["vars"][var_id].get("dimensions", {})
        return dimensions

    def get_vars(self, func_id):
        return self.symbols[func_id]["vars"]
    
    def get_temps(self, func_id):
        return self.symbols[func_id]["temps"]

    def get_ptrs(self):
        return self.symbols["pointers"]

    def get_globals(self):
        return self.symbols["global"]["vars"]

    def get_constants(self):
        return self.symbols["constants"]
    
    def get_func_size(self, func_id):
        return self.symbols[func_id]["size"]

    def get_current_ptr(self):
        return self.ptr_counter

    def get_current_temp(self):
        return self.temp_counter

    def change_context(self, context):
        # print("changing context to: ", context)
        self.current_context = context
    
    def get_ptr_v_add(self, ptr_id):
        return self.symbols["pointers"][ptr_id]["v_address"]

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
            self.temp_counter += 1

        elif insert_type == "params":
            for key, value in kwargs.items():
                self.symbols[self.current_context][key] = value

        elif insert_type == "params_v_addresses":
            param_v_add = []
            for p_id in kwargs["params"]:
                param_v_add.append(self.symbols[self.current_context]["vars"][p_id]["v_address"])
            self.symbols[self.current_context]["param_v_add"] = param_v_add


        elif insert_type == "constant":
            # print("THIS IS THE KEY: ", kwargs["id_name"])
            if isinstance(kwargs["id_name"], bool):
                    kwargs["id_name"] = str(kwargs["id_name"])

            if not self.symbols["constants"][kwargs["id_name"]]:
                self.symbols["constants"][kwargs["id_name"]]["v_address"] = self.__constant_address
                self.__constant_address += 1

        elif insert_type == "return":
            parche_guadalupano = "_" + self.current_context
            self.symbols["global"]["vars"][parche_guadalupano]["var_type"] = kwargs["var_type"]
            self.symbols["global"]["vars"][parche_guadalupano]["v_address"] = self.__global_address
            self.__global_address += 1

        elif insert_type == "pointer":
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols["pointers"][kwargs["id_name"]][key] = value
            self.symbols["pointers"][kwargs["id_name"]]["v_address"] = self.__pt_address
            self.__pt_address += 1
            self.ptr_counter += 1

        elif insert_type == "func":
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context][key] = value

    def get_func_quad(self, func_name):
        return self.symbols[func_name]["ini_quad"]
        
    def get_func_var_v_address(self, func_name):
        func_var = "_" + func_name

        return self.symbols["global"]["vars"][func_var]["v_address"]

    def get_dim_var_info(self, name_id):
        """Get the lower and upper boundary of dimensional variable

            Vars:
                name_id: str, name of dim variable

            Return:
                list(int): list of sizes of dimensios
        """
        #check for gloabl context alsoooooo

        
        if self.symbols[self.current_context]["vars"][name_id]:
            return (self.symbols[self.current_context]["vars"][name_id]["v_address"], 
                    self.symbols[self.current_context]["vars"][name_id]["dimensions"], 
                    self.symbols[self.current_context]["vars"][name_id]["var_type"])
        else:
            del self.symbols[self.current_context]["vars"][name_id]
        
        if self.symbols["global"]["vars"][name_id]:
            return (self.symbols["global"]["vars"][name_id]["v_address"], 
                    self.symbols["global"]["vars"][name_id]["dimensions"],
                    self.symbols["global"]["vars"][name_id]["var_type"])
        else:
            del self.symbols["global"]["vars"][name_id]

        raise ValueError(f"Dimensional var '{name_id}' is not defined")


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
            identifier, arg_type, v_address = self.validate(arg)
            
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

        self.change_context("global")
        self.symbols[self.current_context]["size"] = len(
            self.symbols[self.current_context]["vars"]
        )



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
        _, var_type, _= self.validate(exp)
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
        glob_func_name = "_" + function_name
        # print("THIS IS THE QUERY: ", glob_func_name)
        # self.print_symbols()
        if self.symbols["global"]["vars"][glob_func_name]:
            ret_type = self.symbols["global"]["vars"][glob_func_name]["var_type"]
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
                2 - virtual address
        """
        # self.print_symbols()
        # print("this is printing: ", identifier)
        if isinstance(identifier, tuple) and identifier[1] == 0:
            id_name, _ = identifier
            is_valid, var_type, v_address = self.__validate("temps", id_name)
            identifier = identifier[0]
            if not is_valid:
                raise ValueError(f"{identifier} is not declared")

            return identifier, var_type, v_address


        elif isinstance(identifier, tuple) and identifier[1] == '_':
            id_name,_ = identifier
            is_valid, var_type, v_address = self.__validate("vars", id_name)
            identifier = identifier[0]
            if not is_valid:
                raise ValueError(f"{identifier} is not declared")

            return identifier, var_type, v_address
        
        elif isinstance(identifier, tuple) and identifier[1] == "ptr":
            id_name,_ = identifier
            var_type, v_address = self.get_ptr_info(id_name)
            return id_name, var_type, v_address

        else:
            v_address = self.get_virtual_add_const(identifier)
            var_type = self.get_constant_type(identifier)
            return identifier, var_type, v_address
    
    def get_constant_type(self, constant):
        # print("LOOOLAZOO", constant)
        if isinstance(constant, bool):
            return "bool"
        elif isinstance(constant, int):
            return "int"
        elif isinstance(constant, float):
            return "float"
        elif isinstance(constant, str):
            return "char"
        else:
            raise Exception(f"What is this in get_constant_type in symbol table?: {constant} ")
    
    def get_ptr_info(self, ptr_id):
        var_type = self.symbols["pointers"][ptr_id]["var_type"]
        v_address = self.symbols["pointers"][ptr_id]["v_address"]

        return var_type, v_address
    
    def get_virtual_add_const(self,constant):
        """Search for the virtual address of a constant

            Vars:
                constant: int, str, float

            Return:
                virtual address: int
        """
        # print("SEARCHED CONSTANT: ", constant)

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
