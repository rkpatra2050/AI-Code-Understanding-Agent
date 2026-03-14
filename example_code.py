# example_code.py
# This is a sample file you can use to test the AI Code Understanding Agent.

class Stack:
    """A simple stack data structure."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Push an item onto the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._items)


def reverse_string(s: str) -> str:
    """Reverse a string using a stack."""
    stack = Stack()
    for char in s:
        stack.push(char)

    result = []
    while not stack.is_empty():
        result.append(stack.pop())

    return "".join(result)


if __name__ == "__main__":
    print(reverse_string("Hello, World!dscds"))
