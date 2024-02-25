from TokenType import TokenType
from Token import Token
from Expr import Expr
from typing import List
from Stmt import Stmt

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
        statements = []
        # While not at end of token
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    # Parsing the top-level expression
    def expression(self):
        return self.equality()

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
        if self.match(TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()

    # Parse a single statement
    def statement(self) -> Stmt.Print | Stmt.Expression:
        if self.match(TokenType.PRINT):  # If the current token is a print statement
            return self.print_statement()  # Parse and return a print statement
        return self.expression_statement()  # Otherwise, parse and return an expression statement

    # Parse a print statement
    def print_statement(self) -> Stmt.Print:
        value = self.expression()  # Parse the expression to be printed
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")  # Ensure there's a ';' after the expression
        print_stmt = Stmt.Print(value)  # Return a Print statement with the parsed expression
        return print_stmt

    # Parse an expression statement
    def expression_statement(self) -> Stmt.Expression:
        expr = self.expression()  # Parse the expression
        self.consume(TokenType.SEMICOLON,
                     "Expect ';' after expression.")  # Ensure there's a ';' after the expression
        expr_stmt = Stmt.Expression(expr)  # Return an Expression statement with the parsed expression
        return expr_stmt

    # Parsing primary expressions, number, strings, false, true and NIL
    def primary(self):
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.match(TokenType.NIL):
            return Expr.Literal(None)

        if self.match(TokenType.NUMBER) or self.match(TokenType.STRING):
            return Expr.Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        # Handle literal numbers
        if self.match(TokenType.NUMBER):
            return Expr.Literal(self.previous().literal)

        raise self.error(self.peek(), "Expect expression.")

    # Check if the current token matches any of the provided types
    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    # Check if the current token matches a specific type
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
    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    # Peek at the current token without advancing
    def peek(self):
        return self.tokens[self.current]

    # Get the previous token
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
        if token.type == TokenType.EOF:
            raise self.ParseError(f"Error at end of input: {message}")
        if token.type == TokenType.NUMBER:
            raise self.ParseError(f"SyntaxError: invalid syntax {token.lexeme}")
        else:
            raise self.ParseError(f"Error at '{token.lexeme}': {message}")

    def synchronise(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            next_type = self.peek().type
            if next_type in {TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF,
                             TokenType.WHILE, TokenType.PRINT, TokenType.RETURN}:
                return

            self.advance()
