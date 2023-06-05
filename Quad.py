from oracle import cubo
from Stack import Stack

class Quad:
    _instance = None
    __current_quad_index = 0
    __pending_jumps = Stack()
    __start_exp_direction = Stack()

    def __new__(self):
        if not self._instance:
            self._instance = super(Quad, self).__new__(self)
        return self._instance

    def __init__(self):
        self.__quad_list = []

    def get_current_quad_index(self):
        return self.__current_quad_index

    def insert(self, operation, left_op, right_op, result):
        self.__quad_list.append([operation, left_op, right_op, result])
        self.__current_quad_index += 1

    def save_jump(self):
        self.__pending_jumps.push(self.__current_quad_index - 1)

    def get_pending_jump(self):
        return self.__pending_jumps.pop()
    
    def save_start_exp_direction(self):
        self.__start_exp_direction.push(self.__current_quad_index)

    def get_go_to_direction_while_statement(self):
        return self.__start_exp_direction.pop()

    def insert_direction_to_quad(self, direction):
        """Insert address direction for a JUMP to go to

            Vars:
                index: int, index of quad
                direction: direction address to add
        """

        pending_jump_address = self.__pending_jumps.pop()
        self.__quad_list[pending_jump_address][3] = direction

    def get_quad_list(self):
        return self.__quad_list
