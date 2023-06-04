from symbolTable import SymbolTable
from Quad import Quad
from Stack import Stack
from cubo_semantico import ella_baila_sola
import math

ind_to_varStr = {0: "int", 1: "float", 2: "char", 3: "bool"}

global_base = 0
local_base = 10000
constant_base = 20000
ptr_base = 30000

table = SymbolTable()
quads = Quad()

class LocalMemory:
    def __init__(self, func_id):
        self.__local = []

        size = table.get_func_size(func_id)

        for _ in range(size):
            self.__local.append(None)
        
        loc_vars = table.get_vars(func_id)
        loc_temps = table.get_temps(func_id)

        if len(loc_vars) != 0:
            for key in loc_vars.keys():
                var_type = loc_vars[key]["var_type"]
                if var_type == "int":
                    self.__local[loc_vars[key]["v_address"] - local_base] = 0
                
                elif var_type == "float":
                    self.__local[loc_vars[key]["v_address"] - local_base] = 1.5
                
                elif var_type == "bool":
                    self.__local[loc_vars[key]["v_address"] - local_base] = False

                elif var_type == "char":
                    self.__local[loc_vars[key]["v_address"] - local_base] = "a"

                else:
                    raise Exception(f"What type of variable is this?: '{key}'")
        # print(self.__local)
        # print(loc_temps)
        if len(loc_temps) != 0:
            for key in loc_temps.keys():
                var_type = loc_temps[key]["var_type"]
                if var_type == "int":
                    # print(loc_temps[key]["v_address"])
                    self.__local[loc_temps[key]["v_address"] - local_base] = 0
                
                elif var_type == "float":
                    self.__local[loc_temps[key]["v_address"] - local_base] = 1.5
                
                elif var_type == "bool":
                    self.__local[loc_temps[key]["v_address"] - local_base] = False

                elif var_type == "char":
                    self.__local[loc_temps[key]["v_address"] - local_base] = "a"

                else:
                    raise Exception(f"What type of variable is this?: '{key}'")


    def get_value_with_address(self, address):
        return self.__local[address]
    
    def get_curr_memory(self):
        return self.__local
    
    def print_local_memory(self):
        for i, elem in enumerate(self.__local):
            print(f"{i}: {elem}")

class Memory:
    def __init__(self):
        self.__global = []
        self.__constants = []
        self.__pointers = []
        self.__local = Stack()

    def load_pointers(self):
        ptrs = table.get_ptrs()

        ptrs_size = len(ptrs)

        for _ in range(ptrs_size):
            self.__pointers.append(None)
        
        if ptrs_size != 0:
            for key in ptrs.keys():
                var_type = ptrs[key]["var_type"]
                if var_type == "int":
                    self.__pointers[ptrs[key]["v_address"] - ptr_base] = 0
                
                elif var_type == "float":
                    self.__pointers[ptrs[key]["v_address"] - ptr_base] = 1.5
                
                elif var_type == "bool":
                    self.__pointers[ptrs[key]["v_address"] - ptr_base] = False

                elif var_type == "char":
                    self.__pointers[ptrs[key]["v_address"] - ptr_base] = "a"

                else:
                    raise Exception(f"What type of variable is this?: '{key}'")
    def kill_function(self):
        self.__local.pop()

    def load_global(self):
        global_var = table.get_globals()

        global_size = table.get_globals_true_size()

        for _ in range(global_size):
            self.__global.append(None)

        if global_size != 0:
            for key in global_var.keys():
                var_type = global_var[key]["var_type"]
                if var_type == "int":
                    self.__global[global_var[key]["v_address"] - global_base] = 0
                    dims = table.get_global_var_dims(key)

                    if dims:
                        total_cells = math.prod(dims)
                        for i,_ in enumerate(range(total_cells-1)):
                            self.__global[(i+1) + global_var[key]["v_address"] - global_base] = 0

                elif var_type == "float":
                    self.__global[global_var[key]["v_address"] - global_base] = 1.5
                    dims = table.get_global_var_dims(key)

                    if dims:
                        total_cells = math.prod(dims)
                        for i,_ in enumerate(range(total_cells-1)):
                            self.__global[(i+1) + global_var[key]["v_address"] - global_base] = 1.5
                
                elif var_type == "bool":
                    self.__global[global_var[key]["v_address"] - global_base] = False

                elif var_type == "char":
                    self.__global[global_var[key]["v_address"] - global_base] = "a"

                else:
                    raise Exception(f"What type of variable is this?: '{key}'")

    def load_constants(self):
        constants = table.get_constants()

        const_size = len(constants)

        for i in range(const_size):
            self.__constants.append(None)

        # table.print_symbols()
        for const in constants.keys():
            # print(const)
            # print("Type: ", type(const))
            rel_v_add = constants[const]["v_address"] - constant_base
            if isinstance(const, str) and len(const) > 3:
                if const == "True":
                    const = True
                else:
                    const = False
            self.__constants[rel_v_add] = const
    
    def push_to_stack_segment(self, func_id):
        self.__local.push(LocalMemory(func_id))

    def push_local_memory_to_stack_segment(self, localMemory):
        # print("CHECK HEEERE")
        # localMemory.print_local_memory()
        self.__local.push(localMemory)
        # self.__local.top().print_local_memory()
    
    def get_value(self, v_address):
        if v_address < 10000:
            rel_address = v_address
            return self.__global[rel_address]
        
        if v_address < 20000:
            rel_address = v_address - local_base
            # print("this is at the top")
            # self.__local.pop()
            # lol = self.__local.top()
            # lol.print_local_memory()
            # raise Exception("lloooll")
            return self.__local.top().get_value_with_address(rel_address)
        
        if v_address < 30000:
            rel_address = v_address - constant_base
            return self.__constants[rel_address]
        
        else:
            rel_address = v_address - ptr_base
            return self.get_value(self.__pointers[rel_address])
    
    def assign_value(self, v_address, value):
        if v_address < 10000:
            self.__global[v_address] = value
        
        elif v_address < 20000:
            # print("V_ADDRESS: ", v_address)
            rel_address = v_address - local_base
            # print("REL ADD: ", rel_address)
            self.__local.top().get_curr_memory()[rel_address] = value

        elif v_address < 30000:
            rel_address = v_address - constant_base
            self.__constants[rel_address] = value
        
        else:
            rel_addres = v_address - ptr_base
            self.assign_value(rel_addres, value)

    def print_memory(self):
        
        print("<-------- Global ---------->")
        for i, elem in enumerate(self.__global):
            print(f"{i}: {elem}")

        print("<-------- Constant ---------->")
        for i, elem in enumerate(self.__constants):
            print(f"{i}: {elem}")

        print("<-------- Pointers ---------->")
        for i, elem in enumerate(self.__pointers):
            print(f"{i}: {elem}")

        print("<--------- Local --------->")
        aux_stack = Stack()
        while not self.__local.is_empty():
            curr_mem = self.__local.pop()
            aux_stack.push(curr_mem)
            curr_mem_list = curr_mem.get_curr_memory()

            print("<--- Level ---->")
            for i, elem in enumerate(curr_mem_list):
                print(f"{i}: {elem}")
        
        while not aux_stack.is_empty():
            self.__local.push(aux_stack.pop())


class VirtualMachine:
    def __init__(self):
        self.__instruction_pointer = 0
        self.__migajaStack = Stack()
        self.__quads = quads.get_quad_list()
        self.memory = Memory()
        self.pending_local_memory = 0
        self.debug = 0

    def execute(self):
        self.memory.load_constants()
        self.memory.load_global()
        self.memory.load_pointers()

        # print("EXECUTE")
        # table.print_symbols()
        for i, quad in enumerate(self.__quads):
            print(f"{i}: {quad}")

        last_quad = len(self.__quads)

        while self.__instruction_pointer < last_quad:
            self.execute_quad()
        # self.memory.print_memory()

    def get_var_type(self, value):
        # print("VALUE: ", value)
        if isinstance(value, int):
            return "int"

        if isinstance(value, float):
             return "float"

        if isinstance(value, bool):
            return "bool"

        if isinstance(value, str):
            return "char"
        
    def insert_in_pending_local_memory(self, v_address,value):
        rel_address = v_address - local_base

        self.pending_local_memory.get_curr_memory()[rel_address] = value
        # self.pending_local_memory[rel_address] = value
    
    def execute_quad(self):
        operation, left_op, right_op, result = self.__quads[self.__instruction_pointer]

        if operation == "ERA":
            # self.memory.push_to_stack_segment(result)
            self.pending_local_memory = LocalMemory(result)
            self.__instruction_pointer += 1
            print(f"ERA -> {self.__instruction_pointer}")
            # self.memory.print_memory()
            # self.__instruction_pointer == len(self.__quads)

        elif operation == "ERAMAIN":
            self.memory.push_to_stack_segment(result)
            self.__instruction_pointer += 1
            print(f"ERAMAIN -> {self.__instruction_pointer}")
        
        elif operation == "GOTO":
            self.__instruction_pointer = result
            print(f"GOTO -> {self.__instruction_pointer}")

        elif operation == "PRINT":
            value_to_print = self.memory.get_value(result)
            print("ESTO SE DEBERIA DE PRINTEAR")
            print(value_to_print)
            self.__instruction_pointer += 1

        
        elif operation == "GOTOF":
            control_var = self.memory.get_value(left_op)


            if control_var:
                self.__instruction_pointer += 1
            else:
                self.__instruction_pointer = result

            # if self.debug == 5:
            #     print(f"controlllll? : {control_var}")
            #     print(f"GOTOF -> {self.__instruction_pointer}")
            #     raise Exception("MAYBE?")

        elif operation == "RETURN":
          return_value = self.memory.get_value(result)
        #   if self.debug == 5:
        #         print(f"this is returning? : {return_value}")
        #         print(f"v_add: {left_op}")
        #         table.print_symbols()
        #         raise Exception("MAYBE?")
          self.memory.assign_value(left_op, return_value)

          self.memory.kill_function()
          migaja = self.__migajaStack.pop()
          self.__instruction_pointer = migaja
        #   self.__instruction_pointer += 1

          
          print(f"RETURN -> {self.__instruction_pointer}")

        elif operation == "PARAM":
            left_op_value = self.memory.get_value(left_op)
            param_value = self.memory.get_value(result)

            left_op_type = self.get_var_type(left_op_value)
            param_type = self.get_var_type(param_value)

            if left_op_type != param_type:
                raise Exception(f"Expected a '{param_type}' param, received a '{left_op_type}'")


            self.insert_in_pending_local_memory(result, left_op_value)

            # self.pending_local_memory.print_local_memory()
            self.__instruction_pointer += 1
            print(f"PARAM -> {self.__instruction_pointer}")
            # self.__instruction_pointer = len(self.__quads)
        
        elif operation == "GOSUB":
            # print("BEFORE")
            # self.memory.print_memory()
            self.memory.push_local_memory_to_stack_segment(self.pending_local_memory)
            # print("AFTER")
            # self.memory.print_memory()
            self.__migajaStack.push(self.__instruction_pointer + 1)
            self.__instruction_pointer = result
            print(f"GOSUB -> {self.__instruction_pointer}")

            # self.__instruction_pointer = len(self.__quads)

        elif operation == "ENDPROC":
            # raise Exception("we did it!")
            self.memory.kill_function()
            migaja = self.__migajaStack.pop()
            self.__instruction_pointer = migaja
            print(f"ENDPROC -> {self.__instruction_pointer}")

        elif operation == "ENDPROCMAIN":
            self.memory.kill_function()
            self.__instruction_pointer += 1

        elif operation == "=":
            left_op_value = self.memory.get_value(left_op)
            result_value = self.memory.get_value(result)

            left_op_type = self.get_var_type(left_op_value)
            result_type = self.get_var_type(result_value)

            ind = ella_baila_sola(left_op_type, result_type, operation)

            if ind == -1:
                raise Exception(f"'{left_op_type}' can't be assigned to '{result_type}'")

            return_type = ind_to_varStr[ind]

            if return_type == "int":
                final_result = int(left_op_value)
            
            elif return_type == "float":
                final_result = float(left_op_value)

            else:
                final_result = left_op_value


            self.memory.assign_value(result, final_result)
            self.__instruction_pointer += 1

        elif operation == "*":
            left_op_value = self.memory.get_value(left_op)
            right_op_value = self.memory.get_value(right_op)

            left_var_type = self.get_var_type(left_op_value)
            right_var_type = self.get_var_type(right_op_value)

            ind = ella_baila_sola(left_var_type, right_var_type, operation)

            if ind == -1:
                raise Exception(f"'{left_op_type}' not compatible with '{result_type}' on {operation}")

            return_type = ind_to_varStr[ind]
            
            if return_type == "int":
                final_result = int(left_op_value*right_op_value)

            elif return_type == "float":
                final_result = float(left_op_value*right_op_value)

            self.memory.assign_value(result, final_result)
            self.__instruction_pointer += 1

        elif operation == "/":
            left_op_value = self.memory.get_value(left_op)
            right_op_value = self.memory.get_value(right_op)

            left_var_type = self.get_var_type(left_op_value)
            right_var_type = self.get_var_type(right_op_value)

            ind = ella_baila_sola(left_var_type, right_var_type, operation)

            if ind == -1:
                raise Exception(f"'{left_op_type}' not compatible with '{result_type}' on {operation}")

            return_type = ind_to_varStr[ind]

            if right_op_value == 0:
                raise Exception("Error, division by 0.")
            
            if return_type == "int":
                final_result = int(left_op_value/right_op_value)

            elif return_type == "float":
                final_result = float(left_op_value/right_op_value)

            self.memory.assign_value(result, final_result)
            self.__instruction_pointer += 1

        elif operation == "+":
            left_op_value = self.memory.get_value(left_op)
            right_op_value = self.memory.get_value(right_op)

            left_var_type = self.get_var_type(left_op_value)
            right_var_type = self.get_var_type(right_op_value)

            ind = ella_baila_sola(left_var_type, right_var_type, operation)

            if ind == -1:
                raise Exception(f"'{left_op_type}' not compatible with '{result_type}' on {operation}")

            return_type = ind_to_varStr[ind]
            
            if return_type == "int":
                final_result = int(left_op_value+right_op_value)

            elif return_type == "float":
                final_result = float(left_op_value+right_op_value)

            self.memory.assign_value(result, final_result)
            self.__instruction_pointer += 1

        elif operation == "-":
            left_op_value = self.memory.get_value(left_op)
            right_op_value = self.memory.get_value(right_op)

            left_var_type = self.get_var_type(left_op_value)
            right_var_type = self.get_var_type(right_op_value)

            ind = ella_baila_sola(left_var_type, right_var_type, operation)

            if ind == -1:
                raise Exception(f"'{left_op_type}' not compatible with '{result_type}' on {operation}")

            return_type = ind_to_varStr[ind]
            
            if return_type == "int":
                final_result = int(left_op_value-right_op_value)

            elif return_type == "float":
                final_result = float(left_op_value-right_op_value)

            self.memory.assign_value(result, final_result)

            self.memory.assign_value(result, left_op_value - right_op_value)
            self.__instruction_pointer += 1
        
        elif operation == "==":
            self.debug += 1
            left_op_value = self.memory.get_value(left_op)
            right_op_value = self.memory.get_value(right_op)

            left_var_type = self.get_var_type(left_op_value)
            right_var_type = self.get_var_type(right_op_value)

            ind = ella_baila_sola(left_var_type, right_var_type, operation)

            if ind == -1:
                raise Exception(f"'{left_var_type}' not compatible with '{right_var_type}' on {operation}")

            return_type = ind_to_varStr[ind]
            
            if return_type != "bool":
                raise Exception("Should be boolean")
            # table.print_symbols()
            # self.memory.print_memory()
            # print(f"v_add of left_op: {left_op}")
            # if self.debug == 5:
            #     print(f"comparing: {left_op_value} == {right_op_value}")
            #     print(f"type: {left_var_type} == {right_var_type}")
            #     raise Exception("MAYBE?")
            if left_op_value == right_op_value:
                control = True
            else:
                control = False
            
            # if self.debug == 5:
            #     print(f"control? : {control}")
            #     raise Exception("MAYBE?")

            self.memory.assign_value(result, control)
            self.__instruction_pointer += 1

        elif operation == "<":
            left_op_value = self.memory.get_value(left_op)
            right_op_value = self.memory.get_value(right_op)

            left_var_type = self.get_var_type(left_op_value)
            right_var_type = self.get_var_type(right_op_value)

            ind = ella_baila_sola(left_var_type, right_var_type, operation)

            if ind == -1:
                raise Exception(f"'{left_op_type}' not compatible with '{result_type}' on {operation}")

            return_type = ind_to_varStr[ind]
            
            if return_type != "bool":
                raise Exception("Should be boolean")
            
            if left_op_value < right_op_value:
                control = True
            else:
                control = False

            self.memory.assign_value(result, control)
            self.__instruction_pointer += 1

        elif operation == ">":
            left_op_value = self.memory.get_value(left_op)
            right_op_value = self.memory.get_value(right_op)

            left_var_type = self.get_var_type(left_op_value)
            right_var_type = self.get_var_type(right_op_value)

            ind = ella_baila_sola(left_var_type, right_var_type, operation)

            if ind == -1:
                raise Exception(f"'{left_op_type}' not compatible with '{result_type}' on {operation}")

            return_type = ind_to_varStr[ind]
            
            if return_type != "bool":
                raise Exception("Should be boolean")
            
            if left_op_value > right_op_value:
                control = True
            else:
                control = False

            self.memory.assign_value(result, control)
            self.__instruction_pointer += 1

        elif operation == "<=":
            left_op_value = self.memory.get_value(left_op)
            right_op_value = self.memory.get_value(right_op)

            left_var_type = self.get_var_type(left_op_value)
            right_var_type = self.get_var_type(right_op_value)

            ind = ella_baila_sola(left_var_type, right_var_type, operation)

            if ind == -1:
                raise Exception(f"'{left_op_type}' not compatible with '{result_type}' on {operation}")

            return_type = ind_to_varStr[ind]
            
            if return_type != "bool":
                raise Exception("Should be boolean")
            
            if left_op_value <= right_op_value:
                control = True
            else:
                control = False

            self.memory.assign_value(result, control)
            self.__instruction_pointer += 1

        elif operation == ">=":

            left_op_value = self.memory.get_value(left_op)
            right_op_value = self.memory.get_value(right_op)

            left_var_type = self.get_var_type(left_op_value)
            right_var_type = self.get_var_type(right_op_value)

            ind = ella_baila_sola(left_var_type, right_var_type, operation)

            if ind == -1:
                raise Exception(f"'{left_op_type}' not compatible with '{result_type}' on {operation}")

            return_type = ind_to_varStr[ind]
            
            if return_type != "bool":
                raise Exception("Should be boolean")
            
            if left_op_value >= right_op_value:
                control = True
            else:
                control = False

            self.memory.assign_value(result, control)
            self.__instruction_pointer += 1

        
        


        
        
        



    # def load_global_memory(self):
