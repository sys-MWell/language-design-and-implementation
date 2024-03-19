import sys
from Scanner import Scanner  # Scanner class
from TokenType import TokenType
from Parser import Parser
from Interpreter import Interpreter
from AstPrinter import AstPrinter

hadError = False  # Track errors


def main():
    test_file = 'test_cases4.txt'
    run_file(test_file)
    if hadError:
        sys.exit(65)

def run_file(path: str):
    with open(path, "r") as f:
        run(f.read())


def run(src: str):
    global hadError
    scanner = Scanner(src)
    tokens = scanner.scan_tokens()
    for token in tokens:
        #print(f"token: {token}")
        pass

    parser = Parser(tokens)
    try:
        statements = parser.parse()
        for statement in statements:
            #print(f"parser: {statement}")
            pass
        interpreter = Interpreter()
        interpreter.interpret(statements)
    except Parser.ParseError as e:
        print(f"Caught parse error: {e}", file=sys.stderr)
        hadError = True

    if hadError:
        return

# This is just after you try to parse the tokens
if hadError:
    sys.exit(65)  # Exit the program if there was a parse error


def report(line, where, message):
    # Report any errors to console and handle with hadError variable
    sys.stderr.write(f"[line {line}] Error {where}: {message}\n")
    global hadError  # Error variable
    hadError = True  # Error occurred


def error(token, message):
    # Function to report an error based on the given token and message
    if token.type == TokenType.EOF:
        report(token.line, " at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)


def runtime_error(error):
    print(f"{error.message}\n[line {error.token.line}]")


if __name__ == "__main__":
    main()  # Execute the main function if this script is executed directly
    # python StarlingScript.py test_cases.txt
