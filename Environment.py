# Environment.py
"""
The bindings that associate variables to values need to be stored somewhere
Parentheses, this data structure has been called an environment.
"""


class Environment:
    def __init__(self, enclosing):
        self.enclosing = enclosing
        self.values = {}

    # Once variable exists, need way to look it up
    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    # Binds a new name to a value
    def define(self, name, value):
        self.values[name] = value

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
