class Stack:
    """
    A class representing a stack data structure.

    Attributes:
        stack (list): A list to store the elements of the stack.

    Methods:
        __init__(): Initializes an empty stack.
        push(item): Adds an item to the top of the stack.
        pop(): Removes and returns the item from the top of the stack.
        top(): Returns the item at the top of the stack without removing it.
        is_empty(): Checks if the stack is empty.

    """

    def __init__(self):
        """
        Initializes an empty stack.

        Args:
            None

        Returns:
            None

        """
        self.stack = []

    def push(self, item):
        """
        Adds an item to the top of the stack.

        Args:
            item: The item to be added to the stack.

        Returns:
            None

        """
        self.stack.append(item)

    def pop(self):
        """
        Removes and returns the item from the top of the stack.

        Raises:
            IndexError: If the stack is empty.

        Returns:
            The item that was removed from the top of the stack.

        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.stack.pop()

    def top(self):
        """
        Returns the item at the top of the stack without removing it.

        Raises:
            IndexError: If the stack is empty.

        Returns:
            The item at the top of the stack.

        """
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.stack[-1]

    def is_empty(self):
        """
        Checks if the stack is empty.

        Args:
            None

        Returns:
            True if the stack is empty, False otherwise.

        """
        return len(self.stack) == 0
