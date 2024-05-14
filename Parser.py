# Parser.py
from TokenType import TokenType
from Token import Token
from Expr import Expr
from typing import List
from Stmt import Stmt
'''
Recursive descent - Top-down parser
Fast, robust, and can support sophisticated error handling.
Each method for parsing a grammar rule produces a syntax tree.
'''

class Parser:

    # Custom exception class for parse errors
    class ParseError(RuntimeError):
        pass

    # Constructor to initialize the parser with a list of tokens
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    # Parse the input expression
    def parse(self):
        # raise Parser.ParseError("Forced error")
        statements = []
        # While not at end of token
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    # Parsing the top-level expression
    def expression(self):
        return self.assignment()

    # Parsing the top-level declaration
    def declaration(self):
        # try:
        if self.match(TokenType.FUN):
            return self.function("function")
        if self.match(TokenType.VAR):
            return self.var_declaration()

        return self.statement()
        # except self.ParseError:
        #     self.synchronise()
        #     return None

    # Parsing logical OR expression: handles 'or' operators
    def logical_or(self):
        expr = self.logical_and()

        while self.match(TokenType.OR, TokenType.PIPE):
            operator = self.previous()
            right = self.logical_and()
            expr = Expr.Logical(expr, operator, right)

        return expr

    # Parsing logical AND expression: handles 'and' operators
    def logical_and(self):
        expr = self.equality()

        while self.match(TokenType.AND, TokenType.AMPERSAND):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)

        return expr

    # Parsing equality expression: handles equality operators like '!=' (not equal) and '==' (equal equal)
    def equality(self):
        expr = self.comparison()  # Check if comparison

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    # Parsing comparison expression: handles comparison operators like '>' (greater) and '>=' (greater equal) and '<'
    # (less) and '<=' (less equal)
    def comparison(self):
        expr = self.term()  # Check if term

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    # Parsing term expression: handles term operators like '-' (minus) and '+' (plus)
    def term(self):
        expr = self.factor()  # Check if factor

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)

        return expr

    # Parsing factor expression: handles factor operators like '/' (division) and '*' (multiplication)
    def factor(self):
        expr = self.power()  # Check if power

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.power()
            expr = Expr.Binary(expr, operator, right)

        return expr

    # Parsing power expression: handles power operator '^' - CARET Symbol
    def power(self):
        expr = self.unary()  # Check if Unary

        # Handle ^ operator (exponentiation)
        while self.match(TokenType.CARET):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    # Parsing unary expressions: handles unary operators like '!' (logical NOT) and '-' (negation)
    def unary(self):
        # Handle '!' operator
        if self.match(TokenType.BANG):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        elif self.match(TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        # Return call expression if no unary operator
        return self.call()

    # Parsing function call expressions - from call to finish_call
    # Arguments grammar rule: expression ( "," expression )* - also handle the zero-argument case
    # Check if token is ). If it is, we don’t try to parse any arguments.
    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                # Reports an error if encounters too many arguments.
                # Reports the error and keeps on going.
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break

        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Expr.Call(callee, paren, arguments)

    # Parsing function call expressions
    def call(self):
        expr = self.primary()  # Check if primary
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break
        # Return primary expression if no function call
        return expr

    # Parse chosen statements, if, print, block or expression
    def statement(self) -> Stmt.Print | Stmt.Expression | Stmt.Block | Stmt.If | Stmt.While:
        if self.match(TokenType.FOR):  # If the current token is a for statement
            return self.for_statement()  # Parse and return a for statement
        if self.match(TokenType.IF):  # If the current token is an if statement
            return self.if_statement()  # Parse and return an if statement
        if self.match(TokenType.PRINT):  # If the current token is a print statement
            return self.print_statement()  # Parse and return a print statement
        if self.match(TokenType.RETURN):  # If the current token is a return statement
            return self.return_statement()  # Parse and return a return statement
        if self.match(TokenType.WHILE):  # If the current token is a while statement
            return self.while_statement()  # Parse and return a while statement
        # Detect the beginning of a block by its leading token—in this case the {. In the statement() method
        # If indenting a block -> E.g. local variable scope
        # Local variables use a parent-pointer tree structure to store variables in a stack of hash tables
        if self.match(TokenType.LEFT_BRACE):
            block_stmt = Stmt.Block(self.block())
            return block_stmt
        return self.expression_statement()  # Otherwise, parse and return an expression statement

    # Parse a for statement
    # Translate (desugar) for loops to the while loops and other statements the interpreter already handles.
    # Therefore, no alterations for while loops were made to the interpreter.
    # Interpreter now supports C-style for loops
    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        # Translate 'for' to 'while' initialiser.
        # Check if token following the ( is a semicolon, if so initializer has been omitted.
        # Otherwise, check for a var keyword see if variable declaration.
        # If neither matched, must be expression.
        # Parse that and wrap it in an expression statement so the initialiser is always of type Stmt.
        if self.match(TokenType.SEMICOLON):
            initialiser = None
        elif self.match(TokenType.VAR):
            initialiser = self.var_declaration()
        else:
            initialiser = self.expression_statement()

        # Look for a semicolon to see if the clause has been omitted. The last clause is the increment.
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        # Terminated by the closing parenthesis. All that remains is the body.
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        # Resulting AST nodes sitting in a handful of local variables. Where translating begins, local variables used
        # to synthesise syntax tree nodes that express the semantics of the for loop.
        body = self.statement()
        # Increment clause
        if increment is not None:
            body = Stmt.Block([
                body,
                Stmt.Expression(increment)])

        # Take the condition and the body and build the loop using a while loop.
        # If the condition is omitted, jam in true to make an infinite loop.
        if condition is None:
            condition = Expr.Literal(True)
        body = Stmt.While(condition, body)

        # Initialiser, it runs once before the entire loop. Then again by replacing the whole statement with a block
        # that runs the initialiser.
        if initialiser is not None:
            body = Stmt.Block([initialiser, body])

        return body

    # Parse an if statement
    # Detects an else clause by looking for the preceding else keyword.
    # If there isn’t one, the elseBranch field in the syntax tree is null.
    # The else is bound to the nearest if that precedes it.
    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        # Parse the then branch and the else branch
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return Stmt.If(condition, then_branch, else_branch)

    # Parse a print statement
    def print_statement(self) -> Stmt.Print:
        value = self.expression()  # Parse the expression to be printed
        # Ensure there's a ';' after the expression
        self.consume(TokenType.SEMICOLON, "Expect ';' after value, invalid expression.")
        print_stmt = Stmt.Print(value)  # Return a Print statement with the parsed expression
        return print_stmt

    # Parse a return statement
    def return_statement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Stmt.Return(keyword, value)

    # Parse an expression statement
    def expression_statement(self) -> Stmt.Expression:
        expr = self.expression()  # Parse the expression
        self.consume(TokenType.SEMICOLON,
                     "Expect ';' after expression.")  # Ensure there's a ';' after the expression
        expr_stmt = Stmt.Expression(expr)  # Return an Expression statement with the parsed expression
        return expr_stmt

    # Parse a function declaration
    def function(self, kind):
        # Consumes the identifier token for the function’s name
        # Will pass in “method” for 'kind' so error messages are specific to the kind of declaration being parsed.
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        # Parse the parameters
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")

                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))

                if not self.match(TokenType.COMMA):
                    break
        # Consume the right parenthesis token
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        # Parse the body and wrap it all up in a function node
        self.consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.block()
        return Stmt.Function(name, parameters, body)

    # Parse a block of statements
    # Creates an empty array and then parse statements and add them to the array until we reach the end of the block,
    # marked by the closing }
    # is_at_end implement, avoid infinite loop, if closing } is missing parser will not get stuck
    def block(self):
        statements = []
        # While not at the end of the block
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        # Consume the right brace token
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    # Check expression - expression assignment
    # Returns an expression type e.g. Expr.Logical
    def assignment(self):
        # Check for logical or and logical and
        expr = self.logical_or()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Expr.Variable):
                name = Expr.Variable(expr.name)
                return Expr.Assign(name, value)

            raise self.error(equals, "Invalid assignment target.")

        return expr

    # Parse variables
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    # Parse while statement
    # Parses similarly to IF statement
    def while_statement(self):
        # Parse the condition, body, and return a While statement
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        return Stmt.While(condition, body)

    # Parsing primary expressions, number, strings, false, true and NIL
    def primary(self):
        # If match FALSE token
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        # If match TRUE token
        if self.match(TokenType.TRUE):
            return Expr.Literal(True)
        # If match NIL token
        if self.match(TokenType.NIL):
            return Expr.Literal(None)
        # If match NUMBER or STRING token - Handle literal numbers
        if self.match(TokenType.NUMBER) or self.match(TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        # If match IDENTIFIER token
        if self.match(TokenType.IDENTIFIER):
            return Expr.Variable(self.previous())
        # If match LEFT_PAREN token
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    # Check if the current token matches any of the provided types
    # If so consumes token, returns true. Otherwise, returns false
    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    # Check if the current token matches a specific type
    # Returns true if the current token is of the given type, does not consume
    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    # Move to the next token and return the current token
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    # Check if we have reached the end of the token list
    # Parser checks if we’ve run out of tokens to parse
    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    # Peek at the current token without advancing
    # Returns the current token we have yet to consume
    def peek(self):
        return self.tokens[self.current]

    # Get the previous token
    # Returns the most recently consumed token
    def previous(self):
        return self.tokens[self.current - 1]

    # Consume the current token if it matches the specified type, otherwise raise an error
    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    # Raise a parse error with a given message
    def error(self, token, message):
        # Any parsing errors
        return self.display_error(token, message)

    def display_error(self, token, message):
        error_message = f"Error at line {token.line}\n"
        if token.type == TokenType.EOF:
            error_message = error_message + f"Error at end of input: {message}"
        elif token.type == TokenType.NUMBER:
            error_message = error_message + f"SyntaxError: invalid syntax {token.lexeme}"
        else:
            error_message = error_message + f"Error at '{token.lexeme}': {message}"
        raise Parser.ParseError(error_message)
