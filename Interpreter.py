# Interpreter.py
from TokenType import TokenType
from Expr import Expr
from Stmt import Stmt
from Environment import Environment
from Callable import Callable
from Function import Function
from Return import Return


class Interpreter():
    environment = Environment(enclosing=None)

    # Interpret expressions - Begin with execute function
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            print(f"\033[91mError: {error}\033[0m")

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
        # Evaluate Call Expression
        elif isinstance(expr, Expr.Call):
            return self.visitCallExpr(expr)

    # Execute - Accept Expressions
    def execute(self, stmt):
        return stmt.accept(self)

    ''' \/ Syntax tree nodes \/ '''

    # To execute a block
    # Method executes a list of statements in the context of a given environment
    # Field represents the current environment - the environment that corresponds to the innermost scope
    # containing the code to be executed.
    """
    StarlingScript uses lexical scoping, which means that the scope of a variable is determined by:
    A variable usage refers to the preceding declaration with the same name in the innermost 
    scope that encloses the expression where the variable is used.
    """
    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    # Execute - Block statements
    def visitBlockStmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None

    # Load expressions - Call evaluate function - Evaluates expression type
    # Return object type
    def visitExpressionStmt(self, stmt):
        return_statement = self.evaluate(stmt.expression)
        #print(f"{self.stringify(return_statement)}")
        return return_statement

    # Execute class statements
    # Binds the resulting object to a new variable. A
    # After creating Function, create a new binding in the current environment and store a reference to it there.
    def visitFunctionStmt(self, stmt):
        function = Function(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    # Evaluate function if/else statements
    # Looks for an else before returning, innermost call to a nested series will claim the else clause for itself
    # before returning to the outer if statements.
    def visitIfStmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    # Print statement’s visit method - Print outcome
    # Convert value to a string using the stringify() function
    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(f"{self.stringify(value)}")
        return None

    # Evaluate return statements
    # If we have a return value, we evaluate it, otherwise, we use nil
    def visitReturnStmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        # Assuming 'Return' is a custom exception defined to handle return values in your interpreter
        raise Return(value)

    # Syntax tree - Declaration statements
    # If variable has initialiser, evaluate it, if not other choice
    def visitVarStmt(self, stmt):
        value = None
        if stmt.initialiser:
            value = self.evaluate(stmt.initialiser)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitWhileStmt(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
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
            # If either operand is a string, treat the operation as string concatenation
            if isinstance(left, str) or isinstance(right, str):
                # Convert both operands to strings if at least one is a string
                return str(left) + str(right)
            else:
                # Otherwise, proceed with numerical addition
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

    # Evaluate call expressions
    # Call expressions are used to invoke functions
    # Call expressions are evaluated by first evaluating the callee expression
    def visitCallExpr(self, expr):
        exprCheck = expr.callee.name.lexeme
        if exprCheck == "input":  # Assuming callee is a string with the function name
            # Handle input function
            prompt = ""
            if expr.arguments:
                # Evaluate the first argument to use as the prompt
                prompt = self.evaluate(expr.arguments[0])
            user_input = input(prompt)
            return user_input  # Return the user input to be used in the program
        else:
            callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        # Check if the callee is a callable object
        if not isinstance(callee, Callable):
            raise RuntimeError(f"Can only call functions and classes. Line: {expr.paren.line}")
        if not isinstance(callee, Callable):
            raise TypeError("Callee must be an instance of Callable")

        # Arity - fancy term for the number of arguments a function or operation expects.
        # Check to see if the argument list’s length matches the callable’s arity.
        if len(arguments) != callee.arity():
            raise RuntimeError(f"Expected {callee.arity()} arguments but got {len(arguments)}. Line: {expr.paren.line}")

        return callee.call(self, arguments)

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
