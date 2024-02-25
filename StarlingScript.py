import sys
from Scanner import Scanner  # Scanner class
from TokenType import TokenType
from Parser import Parser
from Interpreter import Interpreter

hadError = False  # Track errors

def main():
    # Correct number of arguments provided
    # if len(sys.argv) != 2:
    #     print("Usage: python starling_script.py <test_file>")
    #     sys.exit(64)  # Exit with status code 64 (command line usage error)

    # Get the path to the test file from the command line argument
    test_file = 'test_cases.txt'
    # Run the test file
    run_file(test_file)


def run_file(path):
    # Open the file specified by the path in read mode
    with open(path, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Run the scanner on the current line
            run(line)
            # Check if an error occurred during scanning
            if hadError:
                sys.exit(65)  # Exit with status code 65 (data format error)


def run(source):
    # Create a scanner object with the provided source code
    print(f"source: {source}", end="")
    scanner = Scanner(source)
    # Get the tokens by scanning the source code
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(f"token: {token}")
    # Expression parser
    parser = Parser(tokens)
    statements = parser.parse()
    print(f"expression: {statements[0]}")
    # Stop if there was a syntax error
    if hadError:
        print("Error")
        return
    interpreter = Interpreter()
    interpreter.interpret(statements)
    print()


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
