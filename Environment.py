# Environment.py
"""
The bindings that associate variables to values need to be stored somewhere
Parentheses, this data structure has been called an environment.
"""


class Environment:
    def __init__(self, enclosing):
        self.enclosing = enclosing
        #  Using dictionary to store variable bindings
        self.values = {}

    # Once variable exists, need way to look it up
    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}' on line {name.line}")

    # Binds a new name to a value
    # Uses variable name as key, with value to be stored in
    # So if var ten = 10; would be self.values[ten] = 10
    def define(self, name, value):
        self.values[name] = value

    # Assignment is not allowed to create a new variable
    # - runtime error if the key does not already exist in the environment’s variable map
    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
