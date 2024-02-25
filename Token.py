from TokenType import TokenType

class Token:
    # Class for token in the source code
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type  # Token type (e.g., TokenType.IDENTIFIER, TokenType.NUMBER)
        self.lexeme = lexeme  # The actual text of the token
        self.literal = literal  # Literal value of the token (e.g., for numbers, strings)
        self.line = line  # Line number where the token appears in the source code

    def __str__(self):
        # String representation of token object
        return f"{self.type} {self.lexeme} {self.literal}"
