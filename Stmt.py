# Stmt.py
# Statements
from abc import ABC, abstractmethod

'''
Statements form a second hierarchy of syntax tree nodes independent of expressions
'''

class Stmt(ABC):
    # Represents a block of statements
    # The curly-braced block statement that defines a local scope
    # "{" declaration* "}"
    class Block():
        def __init__(self, statements):
            self.statements = statements

        def accept(self, visitor):
            return visitor.visitBlockStmt(self)

        def __str__(self):
            return f"{str(self.statements)}"

    # Represents a class declaration statement
    # Interpret a class declaration statement
    # Token name, List<Stmt.Function> methods
    # "class" IDENTIFIER "{" function* "}"
    class Class():
        def __init__(self, name, superclass, methods):
            self.name = name
            self.superclass = superclass
            self.methods = methods

        def accept(self, visitor):
            return visitor.visitClassStmt(self)

        def __str__(self):
            return f"{str(self.name)} {str(self.superclass)} {str(self.methods)}"

    # Represents an expression statement
    # Expression ";"
    # Called from Interpreter.Accept - Checks expression
    # If expression accepted, call function visitExpressionStmt within interpreter
    class Expression():
        def __init__(self, expression):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visitExpressionStmt(self)

        def __str__(self):
            return f"{str(self.expression)}"

    # Represents a function declaration statement
    # IDENTIFIER "(" parameters? ")" block
    # Token name, List<Token> params," + " List<Stmt> body",
    class Function():
        def __init__(self, name, params, body):
            self.name = name
            self.params = params
            self.body = body

        def accept(self, visitor):
            return visitor.visitFunctionStmt(self)

        def __str__(self):
            return f"{str(self.name)} {str(self.params)} {str(self.body)}"

    # Represents an if statement
    # if statement conditionally executes statements
    # "if" "(" expression ")" statement ( "else" statement )?
    class If():
        def __init__(self, condition, thenBranch, elseBranch):
            self.condition = condition
            self.thenBranch = thenBranch
            self.elseBranch = elseBranch

        def accept(self, visitor):
            return visitor.visitIfStmt(self)

        def __str__(self):
            return f"{str(self.condition)} {str(self.thenBranch)} {str(self.elseBranch)}"

    # Represents a print statement
    # Print statement evaluates an expression and displays the result to the user
    # "print" expression ";"
    class Print():
        def __init__(self, expression):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visitPrintStmt(self)

        def __str__(self):
            return f"{str(self.expression)}"

    # Represents a return statement
    # Dedicated syntax for emitting a result - return statements
    # "return" expression? ";"
    class Return():
        def __init__(self, keyword, value):
            self.keyword = keyword
            self.value = value

        def accept(self, visitor):
            return visitor.visitReturnStmt(self)

        def __str__(self):
            return f"{str(self.keyword)} {str(self.value)}"

    # Represents a variable declaration statement
    # Variable declarations are statements
    # Token name, Expr initialiser
    # It stores the name token so we know what it’s declaring, along with the initialiser expression
    class Var():
        def __init__(self, name, initialiser):
            self.name = name
            self.initialiser = initialiser

        def accept(self, visitor):
            return visitor.visitVarStmt(self)

        def __str__(self):
            return f"{str(self.name)} {str(self.initialiser)}"

    # Represents a while loop statement
    # "while" "(" expression ")" statement
    # Expr condition, Stmt body
    class While():
        def __init__(self, condition, body):
            self.condition = condition
            self.body = body

        def accept(self, visitor):
            return visitor.visitWhileStmt(self)

        def __str__(self):
            return f"{str(self.condition)} {str(self.body)}"

    @abstractmethod
    def accept(self, visitor):
        pass