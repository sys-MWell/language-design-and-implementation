# Interpreter.py
from TokenType import TokenType
from Expr import Expr
from Stmt import Stmt
from Environment import Environment


class Interpreter():
    environment = Environment(enclosing=None)
    # Interpret expressions - Begin with execute function
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            print(f"\033[91mErrror: {error}\033[0m")

    # Evaluate expressions, select evaluation method based on expression type
    def evaluate(self, expr):
        # Evaluate Binary Expression
        if isinstance(expr, Expr.Binary):
            return self.visitBinaryExpr(expr)
        # Evaluate Grouping - Using parentheses to group expressions - "(" expression ")"
        elif isinstance(expr, Expr.Grouping):
            return self.evaluate(expr.expression)
        # Evaluate Literal Expression - Numbers, strings, Booleans, and nil
        elif isinstance(expr, Expr.Literal):
            return self.visitLiteralExpr(expr)
        # Evaluate Unary Expression - ( "-" | "!" ) expression
        elif isinstance(expr, Expr.Unary):
            return self.visitUnaryExpr(expr)
        # Evaluate Logical Expression - ('AND', 'OR')
        elif isinstance(expr, Expr.Logical):
            return self.visitLogicalExpr(expr)
        # Evaluate Variable Expression
        elif isinstance(expr, Expr.Variable):
            return self.visitVariableExpr(expr)
        # Evaluate Assignment Expression
        elif isinstance(expr, Expr.Assign):
            return self.visitAssignExpr(expr)

    # Execute - Accept Expressions
    def execute(self, stmt):
        return stmt.accept(self)

    # To execute a block
    # Method executes a list of statements in the context of a given environment
    # Field represents the current environment - the environment that corresponds to the innermost scope
    # containing the code to be executed.
    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    # Execute  - Block statements
    def visitBlockStmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None

    # Load expressions - Call evaluate function - Evaluates expression type
    # Return object type
    def visitExpressionStmt(self, stmt):
        return_statement = self.evaluate(stmt.expression)
        print(f"{self.stringify(return_statement)}")
        return return_statement

    '''Syntax tree nodes'''

    # Print statement’s visit method - Print outcome
    # Convert value to a string using the stringify() function
    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(f"{self.stringify(value)}")
        return None

    # Syntax tree - Declaration statements
    # If variable has initialiser, evaluate it, if not other choice
    def visitVarStmt(self, stmt):
        value = None
        if stmt.initialiser:
            value = self.evaluate(stmt.initialiser)

        self.environment.define(stmt.name.lexeme, value)
        return None

    # Syntax tree - Evaluates the right-hand side to get the value, then stores it in the named variable
    # Assignment variable expression
    # StarlingScript can handle variable names longer than two characters
    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        name = expr.name.name
        self.environment.assign(name, value)
        return value

    # Evaluate binary expressions
    # Evaluates left and right variable e.g. 10 > 5
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

    # Convert the literal tree node into a runtime value using Expr.Value
    def visitLiteralExpr(self, expr):
        return expr.value

    # Load logical expressions - 'OR', '|', 'AND', '&'
    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)

        # If operator is 'or' or '|' pipe (same thing) types
        if expr.operator.type == TokenType.OR or expr.operator.type == TokenType.PIPE:
            # Check if value to the left is true or false
            if self.is_truthy(left):
                return left
        # Else so 'and' or '&' (AMPERSAND) types
        else:
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)

    # Evaluate unary expression - ( "-" | "!" ) expression
    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            return -right

    # Evaluate a variable expression
    # Forwards to Environment - make sure the variable is defined
    def visitVariableExpr(self, expr):
        return self.environment.get(expr.name)

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
