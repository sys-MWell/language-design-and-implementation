from Callable import Callable
from Environment import Environment
from Return import Return

class Function(Callable):
    def __init__(self, declaration, closure):
        self.closure = closure
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except Return as returnValue:
            return returnValue.value
        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
