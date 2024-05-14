# Function.py

from Callable import Callable
from Environment import Environment
from Return import Return

'''
Class that implements Callabale -> Instead of Stmt.Function, we wrap in a new class
Each function gets its own environment where it stores its variables.
Environments created dynamically, so each call its own environment which stores variables. Otherwise, recursion would break.
'''
class Function(Callable):
    def __init__(self, declaration, closure):
        self.closure = closure
        self.declaration = declaration

    # Implement call() of Callable
    def call(self, interpreter, arguments):
        # Environment call and define
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except Return as returnValue:
            return returnValue.value
        return None

    # When binding parameters, we assume parameter and argument lists are the same length,
    # visitCallExpr() checks arity before calling call().
    def arity(self):
        return len(self.declaration.params)

    # Implement toString()
    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
