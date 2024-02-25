from TokenType import TokenType  # Importing the TokenType class from TokenType module
from Token import Token  # Importing the Token class from Token module

class Scanner:
    class ParseError(RuntimeError):
        pass
    def __init__(self, source):
        self.source = source  # The source code to be scanned
        self.tokens = []  # List to store the scanned tokens
        self.start = 0  # Starting index of the current lexeme
        self.current = 0  # Current index in the source code
        self.line = 1  # Current line number

    # Dictionary mapping keywords to their corresponding token types
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    # Scan the tokens from the source code
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    # Check if the scanner has reached the end of the source code
    def is_at_end(self):
        return self.current >= len(self.source)

    # Scan a single token from the source code
    def scan_token(self):
        # Next character from the source code
        c = self.advance()
        # Check the type of the token based on the current character
        if c == '(':
            # Add a LEFT_PAREN token to the list of tokens
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            # Add a RIGHT_PAREN token to the list of tokens
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            # Add a LEFT_BRACE token to the list of tokens
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            # Add a RIGHT_BRACE token to the list of tokens
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            # Add a COMMA token to the list of tokens
            self.add_token(TokenType.COMMA)
        elif c == '.':
            # Add a DOT token to the list of tokens
            self.add_token(TokenType.DOT)
        elif c == '-':
            # Add a MINUS token to the list of tokens
            self.add_token(TokenType.MINUS)
        elif c == '+':
            # Add a PLUS token to the list of tokens
            self.add_token(TokenType.PLUS)
        elif c == ';':
            # Add a SEMICOLON token to the list of tokens
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            # Add a STAR token to the list of tokens
            self.add_token(TokenType.STAR)
        elif c == '^':
            # Add a CARET token to the list of tokens
            self.add_token(TokenType.CARET)
        elif c == '&':
            # Add a AND token to the list of tokens
            self.add_token(TokenType.AMPERSAND)
        elif c == '|':
            # Add a OR token to the list of tokens
            self.add_token(TokenType.PIPE)
        elif c == '!':
            # Check if the next character is '=', then add a BANG_EQUAL token,
            # otherwise, add a BANG token
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            # Check if the next character is '=', then add an EQUAL_EQUAL token,
            # otherwise, add an EQUAL token
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            # Check if the next character is '=', then add a LESS_EQUAL token,
            # otherwise, add a LESS token
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            # Check if the next character is '=', then add a GREATER_EQUAL token,
            # otherwise, add a GREATER token
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            # Check if the next character is '/', indicating a comment,
            # if so, consume the rest of the line as a comment, otherwise, add a SLASH token
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == '"':
            # Handle string literals
            self.string()
        elif c in [' ', '\r', '\t']:
            # Ignore whitespace characters
            pass
        elif c == '\n':
            # Increment line number for newline characters
            self.line += 1
        elif self.is_digit(c):
            # Handle numeric literals
            self.number()
        elif self.is_alpha(c):
            # Handle identifiers and keywords
            self.identifier()
        else:
            # Unexpected character
            raise self.ParseError(f"Unexpected character at line {self.line} with being {c}")
            return

    # Advance to the next character in the source code
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    # Add a token to the list of tokens
    def add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    # Match the current character with an expected character
    def match(self, expected):
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    # Peek at the next character
    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    # Peek at the character after the next character
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    # Check if a character is an alphabetic character or underscore
    def is_alpha(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    # Check if a character is a digit
    def is_digit(self, c):
        return '0' <= c <= '9'

    # Check if a character is an alphanumeric character
    def is_alpha_numeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    # Handle identifiers and keywords
    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    # Handle numeric literals
    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    # Handle string literals
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            print(f"Unterminated string at line {self.line}")
            return

        self.advance()  # Consume the closing double quote

        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)
