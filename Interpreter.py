from TokenType import TokenType
from Expr import Expr
from Stmt import Stmt

class Interpreter():
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            print(f"\033[91mErrror: {error}\033[0m")

    # Evaluate expressions, select evaluation method based on expression type
    def evaluate(self, expr):
        if isinstance(expr, Expr.Binary):
            return self.visitBinaryExpr(expr)
        elif isinstance(expr, Expr.Grouping):
            return self.evaluate(expr.expression)
        elif isinstance(expr, Expr.Literal):
            return expr.value
        elif isinstance(expr, Expr.Unary):
            return self.visitUnaryExpr(expr)

    def execute(self, stmt):
        stmt.accept(self)

    def visitExpressionStmt(self, stmt):
        return_binary = self.evaluate(stmt.expression)
        print(f"Expression statement: {self.stringify(return_binary)}")
        return return_binary

    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(f"Print statement: {self.stringify(value)}")
        return None

    # Evaluate binary expressions
    def visitBinaryExpr(self, expr):
        # Left and right binary expression
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.GREATER:
            return left > right
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            return left >= right
        elif expr.operator.type == TokenType.LESS:
            return left < right
        elif expr.operator.type == TokenType.LESS_EQUAL:
            return left <= right
        elif expr.operator.type == TokenType.MINUS:
            return left - right
        elif expr.operator.type == TokenType.PLUS:
            return left + right
        elif expr.operator.type == TokenType.SLASH:
            return left / right
        elif expr.operator.type == TokenType.STAR:
            return left * right
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return left != right
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return left == right
        elif expr.operator.type == TokenType.CARET:  # Handle the CARET "^" operator
            return left ** right
        else:
            # Unexpected operator found
            print(f"Unexpected operator {expr}")
            return

    # Evaluate unary expression
    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            return -right

    # Truthiness and falsiness
    # Something other than true or false in a logic operation like !
    # False and nil are falsey, and everything else is truthy
    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    # This takes in a syntax tree for an expression and evaluates it.
    # If that succeeds, evaluate() returns an object for the result value.
    # interpret() converts that to a string and shows it to the user
    def stringify(self, value):
        if value is None:
            return "nil"
        return str(value)
