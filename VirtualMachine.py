from symbolTable import SymbolTable
from Quad import Quad
from Stack import Stack
from cubo_semantico import ella_baila_sola

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
        
        if len(loc_temps) != 0:
            for key in loc_temps.keys():
                var_type = loc_temps[key]["var_type"]
                if var_type == "int":
                    self.__local[loc_temps[key]["v_address"] - loc_temps] = 0
                
                elif var_type == "float":
                    self.__local[loc_temps[key]["v_address"] - local_base] = 1.5
                
                elif var_type == "bool":
                    self.__local[loc_temps[key]["v_address"] - local_base] = False

                elif var_type == "char":
                    self.__local[loc_temps[key]["v_address"] - local_base] = "a"

                else:
                    raise Exception(f"What type of variable is this?: '{key}'")



    
    def get_curr_memory(self):
        return self.__local

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

    def load_global(self):
        global_var = table.get_globals()

        global_size = len(global_var)

        for _ in range(global_size):
            self.__global.append(None)

        if global_size != 0:
            for key in global_var.keys():
                var_type = global_var[key]["var_type"]
                if var_type == "int":
                    self.__global[global_var[key]["v_address"] - global_base] = 0
                
                elif var_type == "float":
                    self.__global[global_var[key]["v_address"] - global_base] = 1.5
                
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

        for const in constants.keys():
            rel_v_add = constants[const]["v_address"] - constant_base
            self.__constants[rel_v_add] = const
    
    def push_to_stack_segment(self, func_id):
        self.__local.push(LocalMemory(func_id))
    
    def get_value(self, v_address):
        if v_address < 10000:
            rel_address = v_address
            return self.__global[rel_address]
        
        if v_address < 20000:
            rel_address = v_address - local_base
            return self.__local.top().get_curr_memory()[rel_address]
        
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
        while not self.__local.is_empty():
            curr_mem = self.__local.pop()
            curr_mem_list = curr_mem.get_curr_memory()

            print("<--- Level ---->")
            for i, elem in enumerate(curr_mem_list):
                print(f"{i}: {elem}")



class VirtualMachine:
    def __init__(self):
        self.__instruction_pointer = 0
        self.__quads = quads.get_quad_list()
        self.memory = Memory()

    def execute(self):
        self.memory.load_constants()
        self.memory.load_global()
        self.memory.load_pointers()

        # print("EXECUTE")
        # table.print_symbols()

        last_quad = len(self.__quads)

        while self.__instruction_pointer < last_quad:
            # print("current pointer: ", self.__instruction_pointer)
            self.execute_quad()
        self.memory.print_memory()

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
    
    def execute_quad(self):
        operation, left_op, right_op, result = self.__quads[self.__instruction_pointer]

        if operation == "ERA":
            self.memory.push_to_stack_segment(result)
            self.__instruction_pointer += 1
        
        elif operation == "GOTO":
            self.__instruction_pointer = result

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
            
            if left_op_value == right_op_value:
                control = True
            else:
                control = False

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
