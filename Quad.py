from cubo_semantico import cubo


class Quad:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(Quad, self).__new__(self)
        return self._instance

    def __init__(self):
        self.__quad_list = []

    def insert(self, operation, left_op, right_op, result):
        # preguntale si baila o no
        self.__quad_list.append((operation, left_op, right_op, result))

    def get_quad_list(self):
        return self.__quad_list
