# Expressions
# Data structure forming a tree
from abc import ABC, abstractmethod

'''
Expressions are the first syntax tree nodes we see
The main Expr class defines the visitor interface used to dispatch against
 the specific expression types, and contains the other expression subclasses as nested classes.
'''
class Expr(ABC):
    def accept(self, visitor):
        method_name = 'visit' + self.__class__.__name__ + 'Expr'
        visit_method = getattr(visitor, method_name, None)
        if visit_method:
            return visit_method(self)
        else:
            raise NotImplementedError(f"No visit method found for {self.__class__.__name__}")

    # Assign Expressions
    # Takes token name and expression value
    class Assign():
        def __init__(self, name, value):
            self.name = name
            self.value = value

        def accept(self, visitor):
            return visitor.visitAssignExpr(self)

    # Binary expression
    # The infix arithmetic (+, -, *, /) and logic operators (==, !=, <, <=, >, >=)
    # Expression, operator, expression
    class Binary():
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right

        def accept(self, visitor):
            return visitor.visitBinaryExpr(self)

        def __str__(self):
            return f"({self.operator.lexeme} {self.left} {self.right})"

    # Call expression
    # primary ( "(" arguments? ")" )*
    # Expression callee, Token paren, List<Expr> arguments
    class Call():
        def __init__(self, callee, paren, arguments):
            self.callee = callee
            self.paren = paren
            self.arguments = arguments

        def accept(self, visitor):
            return visitor.visitCallExpr(self)

    # Get expression
    # Property access, or “get” expressions
    # Expression object, token name
    class Get():
        def __init__(self, object, name):
            self.object = object
            self.name = name

        def accept(self, visitor):
            return visitor.visitGetExpr(self)

    # Grouping expression
    # Using parentheses to group expressions
    # "(" expression ")"
    class Grouping():
        def __init__(self, expression):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visitGroupingExpr(self)

        def __str__(self):
            return str(self.expression)


    # Numbers, strings, Booleans, and nil
    # NUMBER | STRING | "true" | "false" | "nil"
    # Object value
    class Literal():
        def __init__(self, value):
            self.value = value

        def accept(self, visitor):
            return visitor.visitLiteralExpr(self)

        def __str__(self):
            return str(self.value)

    # Logical expression
    # Expression left, operator, expression right, (AND, OR)
    class Logical():
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right

        def accept(self, visitor):
            return visitor.visitLogicalExpr(self)

        def __str__(self):
            return f"({self.left} {self.operator.lexeme} {self.right})"

    # Set expression - Property assignment
    # Expr object, Token name, Expr value
    # Left side of an assignment
    class Set():
        def __init__(self, object, name, value):
            self.object = object
            self.name = name
            self.value = value

        def accept(self, visitor):
            return visitor.visitSetExpr(self)

    # Super expression
    # Token keyword, Token method
    # Used for a method call - super access followed by a function call
    class Super():
        def __init__(self, keyword, method):
            self.keyword = keyword
            self.method = method

        def accept(self, visitor):
            return visitor.visitSuperExpr(self)

    # This expression
    # Evaluates to the instance that the method was called on
    class This():
        def __init__(self, keyword):
            self.keyword = keyword

        def accept(self, visitor):
            return visitor.visitThisExpr(self)

    # Unary expression
    # A prefix ! to perform a logical not, and - to negate a number
    # ( "-" | "!" ) expression
    # Token operator, Expr right
    class Unary():
        def __init__(self, operator, right):
            self.operator = operator
            self.right = right

        def accept(self, visitor):
            return visitor.visitUnaryExpr(self)

        def __str__(self):
            return f"({self.operator.lexeme} {self.right})"

    # Variable expression
    # E.g. 'var 1 = 3';
    class Variable():
        def __init__(self, name):
            self.name = name

        def accept(self, visitor):
            return visitor.visitVariableExpr(self)

        # Return as string when printing
        def __str__(self):
            return str(self.name)
