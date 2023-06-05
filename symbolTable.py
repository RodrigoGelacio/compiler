from collections import defaultdict
import math


class SymbolTable:
    """
    A class representing a symbol table for storing program symbols and their attributes.

    Attributes:
        _instance: The singleton instance of the SymbolTable class.
        symbols: A nested defaultdict to store the symbols and their attributes.
        current_context: The current context in the symbol table.
        temp_counter: A counter for temporary variables.
        ptr_counter: A counter for pointers.
        __pt_address: The starting address for pointers.
        __constant_address: The starting address for constants.
        __local_address: The starting address for local variables.
        __global_address: The starting address for global variables.

    Methods:
        __new__(): Creates a new instance of the SymbolTable class if it doesn't already exist.
        __init__(): Initializes the symbol table with default values.
        get_return_type_func(func_id): Retrieves the return type of a function from the symbol table.
        get_func_var_dims(func_id, var_id): Retrieves the dimensions of a variable in a function from the symbol table.
        get_func_true_size(func_id): Calculates the true size of a function's variables in the symbol table.
        get_param_v_add(func_id, index): Retrieves the virtual address of a parameter in a function from the symbol table.
        get_globals_true_size(): Calculates the true size of global variables in the symbol table.
                get_global_var_dims(var_id): Retrieves the dimensions of a global variable from the symbol table.
        get_vars(func_id): Retrieves the variables of a function from the symbol table.
        get_temps(func_id): Retrieves the temporary variables of a function from the symbol table.
        get_ptrs(): Retrieves the pointers from the symbol table.
        get_globals(): Retrieves the global variables from the symbol table.
        get_constants(): Retrieves the constants from the symbol table.
        get_func_size(func_id): Retrieves the size of a function from the symbol table.
        get_current_ptr(): Retrieves the current pointer counter from the symbol table.
        get_current_temp(): Retrieves the current temporary variable counter from the symbol table.
        change_context(context): Changes the current context in the symbol table.
        get_ptr_v_add(ptr_id): Retrieves the virtual address of a pointer from the symbol table.
        insert(insert_type, dim=False, **kwargs): Inserts symbols of various types into the symbol table.
        get_func_quad(func_name): Get the initial quad index of a function.
        get_func_var_v_address(func_name): Get the virtual address of a function variable.
        get_dim_var_info(name_id): Get information about a dimensional variable.
        if_var_has_dim_allocate_memory(**kwargs): Allocate memory for a dimensional variable.
        insert_quad_index_where_func_starts(quad_index): Insert the quad index where a function starts.
        reset_local_memory(): Reset the local memory counter (temps and local vars).
        reset_locals(): Reset the local memory counter.
        get_current_context(): Get the current context.
        func_exists(func_name): Check if a function exists in the symbol table.
        validate_args(func_id, args): Validate the arguments of a function call.
        insert_func_size(): Insert the size of the current function into the symbol table.
        insert_global_size(): Insert the size of the global variables into the symbol table.
        is_it_already_declared(id_name): Check if an identifier is already declared.
        is_return_type_ok(exp): Check if the return type of an expression matches the current function's return type.
        validate_return_function(function_name): Validate if a function call returns a value.
        validate(identifier): Validate an identifier and retrieve its information.
        get_constant_type(constant): Get the type of a constant.
        get_ptr_info(ptr_id): Get the type and virtual address of a pointer variable.
        get_virtual_add_const(constant): Get the virtual address of a constant.
        __validate(type_var, id_name): Check if an identifier is registered with the correct dimensionality.
        delete(name): Delete a symbol from the symbol table.
        print_symbols(): Print the contents of the symbol table.



    """

    _instance = None

    def __new__(self):
        """
        Creates a new instance of the SymbolTable class if it doesn't already exist.

        Args:
            None

        Returns:
            The singleton instance of the SymbolTable class.

        """
        if not self._instance:
            self._instance = super(SymbolTable, self).__new__(self)
        return self._instance

    def __init__(self):
        """
        Initializes the symbol table with default values.

        Args:
            None

        Returns:
            None

        """
        self.symbols = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        self.current_context = "global"
        self.temp_counter = 1
        self.ptr_counter = 1
        self.__pt_address = 30000
        self.__constant_address = 20000
        self.__local_address = 10000
        self.__global_address = 0

    def get_return_type_func(self, func_id):
        """
        Retrieves the return type of a function from the symbol table.

        Args:
            func_id: The ID of the function.

        Returns:
            The return type of the function.

        """
        return self.symbols[func_id]["return_type"]

    def get_func_var_dims(self, func_id, var_id):
        """
        Retrieves the dimensions of a variable in a function from the symbol table.

        Args:
            func_id: The ID of the function.
            var_id: The ID of the variable.

        Returns:
            The dimensions of the variable as a dictionary.

        """
        dimensions = self.symbols[func_id]["vars"][var_id].get("dimensions", {})
        return dimensions

    def get_func_true_size(self, func_id):
        """
        Calculates the true size of a function's variables in the symbol table.

        Args:
            func_id: The ID of the function.

        Returns:
            The true size of the function's variables.

        """
        func_vars = self.symbols[func_id]["vars"]
        true_size = self.symbols[func_id]["size"]

        for key in func_vars.keys():
            dimensions = func_vars[key].get("dimensions", {})
            if dimensions:
                cells = math.prod(func_vars[key]["dimensions"])
                true_size += cells - 1

        return true_size

    def get_param_v_add(self, func_id, index):
        """
        Retrieves the virtual address of a parameter in a function from the symbol table.

        Args:
            func_id: The ID of the function.
            index: The index of the parameter.

        Returns:
            The virtual address of the parameter.

        """
        return self.symbols[func_id]["param_v_add"][index]

    def get_globals_true_size(self):
        """
        Calculates the true size of global variables in the symbol table.

        Args:
            None

        Returns:
            The true size of global variables.

        """
        glob_vars = self.symbols["global"]["vars"]
        true_size = self.symbols["global"]["size"]

        for key in glob_vars.keys():
            dimensions = glob_vars[key].get("dimensions", {})
            if dimensions:
                cells = math.prod(glob_vars[key]["dimensions"])
                true_size += cells - 1

        return true_size


    def get_global_var_dims(self, var_id):
        """
        Retrieves the dimensions of a global variable from the symbol table.

        Args:
            var_id: The ID of the variable.

        Returns:
            The dimensions of the variable as a dictionary.

        """
        dimensions = self.symbols["global"]["vars"][var_id].get("dimensions", {})
        return dimensions

    def get_vars(self, func_id):
        """
        Retrieves the variables of a function from the symbol table.

        Args:
            func_id: The ID of the function.

        Returns:
            The variables of the function as a dictionary.

        """
        return self.symbols[func_id]["vars"]

    def get_temps(self, func_id):
        """
        Retrieves the temporary variables of a function from the symbol table.

        Args:
            func_id: The ID of the function.

        Returns:
            The temporary variables of the function as a dictionary.

        """
        return self.symbols[func_id]["temps"]

    def get_ptrs(self):
        """
        Retrieves the pointers from the symbol table.

        Args:
            None

        Returns:
            The pointers as a dictionary.

        """
        return self.symbols["pointers"]

    def get_globals(self):
        """
        Retrieves the global variables from the symbol table.

        Args:
            None

        Returns:
            The global variables as a dictionary.

        """
        return self.symbols["global"]["vars"]

    def get_constants(self):
        """
        Retrieves the constants from the symbol table.

        Args:
            None

        Returns:
            The constants as a dictionary.

        """
        return self.symbols["constants"]

    def get_func_size(self, func_id):
        """
        Retrieves the size of a function from the symbol table.

        Args:
            func_id: The ID of the function.

        Returns:
            The size of the function.

        """
        return self.symbols[func_id]["size"]

    def get_current_ptr(self):
        """
        Retrieves the current pointer counter from the symbol table.

        Args:
            None

        Returns:
            The current pointer counter.

        """
        return self.ptr_counter

    def get_current_temp(self):
        """
        Retrieves the current temporary variable counter from the symbol table.

        Args:
            None

        Returns:
            The current temporary variable counter.

        """
        return self.temp_counter

    def change_context(self, context):
        """
        Changes the current context in the symbol table.

        Args:
            context: The new context.

        Returns:
            None

        """
        self.current_context = context

    def get_ptr_v_add(self, ptr_id):
        """
        Retrieves the virtual address of a pointer from the symbol table.

        Args:
            ptr_id: The ID of the pointer.

        Returns:
            The virtual address of the pointer.

        """
        return self.symbols["pointers"][ptr_id]["v_address"]

    def insert(self, insert_type, dim=False, **kwargs):
        """
        Inserts symbols of various types into the symbol table.

        Args:
            insert_type: The type of symbol to insert.
            dim: A boolean indicating whether the symbol has dimensions (default: False).
            **kwargs: Additional keyword arguments specific to each symbol type.

        Returns:
            None

        Raises:
            Exception: If memory limits are exceeded.

        """

        if insert_type == "var":
            """
            Inserts a variable symbol into the symbol table.

            Args:
                insert_type: "var" indicating variable symbol.
                dim: A boolean indicating whether the variable has dimensions.
                **kwargs: Additional keyword arguments.
                    id_name: The name of the variable.
                    Other keyword arguments represent variable attributes.

            Returns:
                None

            Raises:
                Exception: If memory limits are exceeded.

            """
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context]["vars"][kwargs["id_name"]][key] = value

            if self.current_context == "global":
                if self.__global_address < 10000:
                    self.symbols[self.current_context]["vars"][kwargs["id_name"]]["v_address"] = self.__global_address
                    self.__global_address += 1
                else:
                    raise Exception("Global memory exceeded.")
            else:
                if self.__local_address < 20000:
                    self.symbols[self.current_context]["vars"][kwargs["id_name"]]["v_address"] = self.__local_address
                    self.__local_address += 1
                else:
                    raise Exception("Local Memory exceeded")

            if dim:
                self.if_var_has_dim_allocate_memory(**kwargs)

        if insert_type == "temp":
            """
            Inserts a temporary variable symbol into the symbol table.

            Args:
                insert_type: "temp" indicating temporary variable symbol.
                **kwargs: Additional keyword arguments.
                    id_name: The name of the temporary variable.
                    Other keyword arguments represent temporary variable attributes.

            Returns:
                None

            Raises:
                Exception: If memory limits are exceeded.

            """
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context]["temps"][kwargs["id_name"]][key] = value

            if self.__local_address < 20000:
                self.symbols[self.current_context]["temps"][kwargs["id_name"]]["v_address"] = self.__local_address
                self.__local_address += 1
                self.temp_counter += 1
            else:
                raise Exception("Local Memory exceeded")

        elif insert_type == "params":
            """
            Inserts parameter symbols into the symbol table.

            Args:
                insert_type: "params" indicating parameter symbols.
                **kwargs: Additional keyword arguments representing parameter attributes.

            Returns:
                None

            """

            for key, value in kwargs.items():
                self.symbols[self.current_context][key] = value

        elif insert_type == "params_v_addresses":
            """
            Inserts parameter virtual addresses into the symbol table.

            Args:
                insert_type: "params_v_addresses" indicating parameter virtual addresses.
                **kwargs: Additional keyword arguments.
                    params: List of parameter IDs.

            Returns:
                None

            """
            param_v_add = []
            for p_id in kwargs["params"]:
                param_v_add.append(self.symbols[self.current_context]["vars"][p_id]["v_address"])
            self.symbols[self.current_context]["param_v_add"] = param_v_add

        elif insert_type == "constant":
            """
            Inserts a constant symbol into the symbol table.

            Args:
                insert_type: "constant" indicating constant symbol.
                **kwargs: Additional keyword arguments.
                    id_name: The name of the constant.
                    Other keyword arguments represent constant attributes.

            Returns:
                None

            Raises:
                Exception: If memory limits are exceeded.

            """
            if isinstance(kwargs["id_name"], bool):
                kwargs["id_name"] = str(kwargs["id_name"])

            if not self.symbols["constants"][kwargs["id_name"]]:
                if self.__constant_address < 30000:
                    self.symbols["constants"][kwargs["id_name"]]["v_address"] = self.__constant_address
                    self.__constant_address += 1
                else:
                    raise Exception("Constant memory exceeded")

        elif insert_type == "return":
            """
            Inserts a return variable symbol into the symbol table.

            Args:
                insert_type: "return" indicating return variable symbol.
                **kwargs: Additional keyword arguments.
                    var_type: The type of the return variable.

            Returns:
                None

            Raises:
                Exception: If memory limits are exceeded.

            """
            parche_guadalupano = "_" + self.current_context
            if self.__global_address < 10000:
                self.symbols["global"]["vars"][parche_guadalupano]["var_type"] = kwargs["var_type"]
                self.symbols["global"]["vars"][parche_guadalupano]["v_address"] = self.__global_address
                self.__global_address += 1
            else:
                raise Exception("Global Memory exceeded")

        elif insert_type == "pointer":
            """
            Inserts a pointer symbol into the symbol table.

            Args:
                insert_type: "pointer" indicating pointer symbol.
                **kwargs: Additional keyword arguments.
                    id_name: The name of the pointer.
                    Other keyword arguments represent pointer attributes.

            Returns:
                None

            Raises:
                Exception: If memory limits are exceeded.

            """
            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols["pointers"][kwargs["id_name"]][key] = value

            if self.__pt_address < 39999:
                self.symbols["pointers"][kwargs["id_name"]]["v_address"] = self.__pt_address
                self.__pt_address += 1
                self.ptr_counter += 1
            else:
                raise Exception("Pointer memory exceeded")

        elif insert_type == "func":
            """
            Inserts a function symbol into the symbol table.

            Args:
                insert_type: "func" indicating function symbol.
                **kwargs: Additional keyword arguments.
                    Other keyword arguments represent function attributes.

            Returns:
                None

            """

            for key, value in kwargs.items():
                if key != "id_name":
                    self.symbols[self.current_context][key] = value

    def get_func_quad(self, func_name):
        """
        Get the initial quad index of a function.

        Args:
            func_name: The name of the function.

        Returns:
            int: The initial quad index of the function.

        """

        return self.symbols[func_name]["ini_quad"]

    def get_func_var_v_address(self, func_name):
        """
        Get the virtual address of a function variable.

        Args:
            func_name: The name of the function.

        Returns:
            int: The virtual address of the function variable.

        """

        func_var = "_" + func_name

        return self.symbols["global"]["vars"][func_var]["v_address"]

    def get_dim_var_info(self, name_id):
        """
        Get information about a dimensional variable.

        Args:
            name_id: The ID or name of the variable.

        Returns:
            Tuple: A tuple containing the virtual address, dimensions, and variable type.

        Raises:
            ValueError: If the dimensional variable is not defined.

        """

        if self.symbols[self.current_context]["vars"][name_id]:
            return (
                self.symbols[self.current_context]["vars"][name_id]["v_address"],
                self.symbols[self.current_context]["vars"][name_id]["dimensions"],
                self.symbols[self.current_context]["vars"][name_id]["var_type"],
            )
        else:
            del self.symbols[self.current_context]["vars"][name_id]

        if self.symbols["global"]["vars"][name_id]:
            return (
                self.symbols["global"]["vars"][name_id]["v_address"],
                self.symbols["global"]["vars"][name_id]["dimensions"],
                self.symbols["global"]["vars"][name_id]["var_type"],
            )
        else:
            del self.symbols["global"]["vars"][name_id]

        raise ValueError(f"Dimensional var '{name_id}' is not defined")

    def if_var_has_dim_allocate_memory(self, **kwargs):
        """
        Allocate memory for a dimensional variable.

        Args:
            **kwargs: Additional keyword arguments.
                dimensions: A list of dimensions.

        Returns:
            None

        """

        if len(kwargs["dimensions"]) != 0:
            var_size = 1
            for dim in kwargs["dimensions"]:
                var_size *= dim
            if self.current_context != "global":
                self.__local_address += var_size - 1
            else:
                self.__global_address += var_size - 1

    def insert_quad_index_where_func_starts(self, quad_index):
        """
        Insert the quad index where a function starts.

        Args:
            quad_index: The quad index of the first instruction of the function.

        Returns:
            None

        """

        self.symbols[self.current_context]["ini_quad"] = quad_index

    def reset_local_memory(self):
        """
        Resets the local memory counter (temps and local vars).

        Returns:
            None

        """

        self.reset_locals()
        self.temp_counter = 1

    def reset_locals(self):
        """
        Reset the local memory counter.

        Returns:
            None

        """

        self.__local_address = 10000

    def get_current_context(self):
        """
        Get the current context.

        Returns:
            str: The current context.

        """

        return self.current_context

    def func_exists(self, func_name):
        """
        Check if a function exists in the symbol table.

        Args:
            func_name: The name of the function.

        Returns:
            bool: True if the function exists, False otherwise.

        """

        if self.symbols[func_name]:
            return True
        return False


    def validate_args(self, func_id, args):
        """
        Validate the arguments of a function call.

        Args:
            func_id: The ID of the function.
            args: The arguments passed in the function call.

        Returns:
            Tuple: A tuple containing the argument IDs and their virtual addresses.

        Raises:
            ValueError: If the number of arguments does not match the expected number or if an argument's type does not match the parameter's type.

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
        """
        Insert the size of the current function into the symbol table.

        Returns:
            None

        """

        func_vars = len(self.symbols[self.current_context]["vars"])
        func_temp = len(self.symbols[self.current_context]["temps"])

        self.symbols[self.current_context]["size"] = func_vars + func_temp

    def insert_global_size(self):
        """
        Insert the size of the global variables into the symbol table.

        Returns:
            None

        """

        self.change_context("global")
        self.symbols[self.current_context]["size"] = len(
            self.symbols[self.current_context]["vars"]
        )

    def is_it_already_declared(self, id_name):
        """
        Check if an identifier is already declared.

        Args:
            id_name: The name of the identifier.

        Returns:
            bool: True if the identifier is already declared, False otherwise.

        """

        if self.symbols[self.current_context]["vars"][id_name] == {}:
            return False

        return True

    def is_return_type_ok(self, exp):
        """
        Check if the return type of an expression matches the current function's return type.

        Args:
            exp: The expression to check.

        Returns:
            None

        Raises:
            ValueError: If the return type of the expression does not match the current function's return type.

        """

        _, var_type, _ = self.validate(exp)
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
        """
        Validate if a function call returns a value.

        Args:
            function_name: The name of the function.

        Returns:
            str: The return type of the function.

        Raises:
            ValueError: If the function does not return anything.

        """

        if self.symbols[function_name]["return_type"] == "void":
            return self.symbols[function_name]["return_type"]
        glob_func_name = "_" + function_name
        if self.symbols["global"]["vars"][glob_func_name]:
            ret_type = self.symbols["global"]["vars"][glob_func_name]["var_type"]
            return ret_type
        else:
            raise ValueError(f"Function '{function_name}' does not return anything.")

    def validate(self, identifier):
        """
        Validate an identifier and retrieve its information.

        Args:
            identifier: The identifier to validate.

        Returns:
            Tuple: A tuple containing the identifier, primitive var_type, and virtual address.

        """

        if isinstance(identifier, tuple) and identifier[1] == 0:
            id_name, _ = identifier
            is_valid, var_type, v_address = self.__validate("temps", id_name)
            identifier = identifier[0]
            if not is_valid:
                raise ValueError(f"{identifier} is not declared")

            return identifier, var_type, v_address

        elif isinstance(identifier, tuple) and identifier[1] == '_':
            id_name, _ = identifier
            is_valid, var_type, v_address = self.__validate("vars", id_name)
            identifier = identifier[0]
            if not is_valid:
                raise ValueError(f"{identifier} is not declared")

            return identifier, var_type, v_address

        elif isinstance(identifier, tuple) and identifier[1] == "ptr":
            id_name, _ = identifier
            var_type, v_address = self.get_ptr_info(id_name)
            return id_name, var_type, v_address

        else:
            v_address = self.get_virtual_add_const(identifier)
            var_type = self.get_constant_type(identifier)
            return identifier, var_type, v_address

    def get_constant_type(self, constant):
        """
        Get the type of a constant.

        Args:
            constant: The constant value.

        Returns:
            str: The type of the constant.

        Raises:
            Exception: If the constant's type is unknown.

        """

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
        """
        Get the type and virtual address of a pointer variable.

        Args:
            ptr_id: The ID of the pointer variable.

        Returns:
            Tuple: A tuple containing the variable type and virtual address of the pointer.

        """

        var_type = self.symbols["pointers"][ptr_id]["var_type"]
        v_address = self.symbols["pointers"][ptr_id]["v_address"]

        return var_type, v_address

    def get_virtual_add_const(self, constant):
        """
        Get the virtual address of a constant.

        Args:
            constant: The constant value.

        Returns:
            int: The virtual address of the constant.

        """
        return self.symbols["constants"][constant]["v_address"]

    def __validate(self, type_var, id_name):
        """
        Check if an identifier is registered with the correct dimensionality.

        Args:
            type_var: The type of variable ("vars" or "temps").
            id_name: The name of the identifier.

        Returns:
            Tuple: A tuple containing a boolean indicating whether the identifier is valid, the primitive var type, and the virtual address.

        """

        if self.symbols[self.current_context][type_var][id_name]:
            return (
                True,
                self.symbols[self.current_context][type_var][id_name]["var_type"],
                self.symbols[self.current_context][type_var][id_name]["v_address"],
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
                v_address,
            )
        else:
            del self.symbols[self.current_context][type_var][id_name]
        self.change_context(curr_context)
        return (False, "", 0)

    def delete(self, name):
        """
        Delete a symbol from the symbol table.

        Args:
            name: The name of the symbol to delete.

        Returns:
            None

        """

        del self.symbols[name]

    def print_symbols(self):
        """
        Print the contents of the symbol table.

        Returns:
            None

        """

        for key, val in self.symbols.items():
            print(key)
            for key1, val1 in self.symbols[key].items():
                print(f"\t{key1}")
                print(f"\t\t{val1}")
            print()