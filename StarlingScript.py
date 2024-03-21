import sys
from Scanner import Scanner  # Scanner class
from TokenType import TokenType
from Parser import Parser
from Interpreter import Interpreter
from AstPrinter import AstPrinter

hadError = False  # Track errors


def main():
    while True:  # Wrap the main interaction in a loop
        # Reset the error flag for each iteration
        global hadError
        hadError = False

        # Mapping of option numbers to test files
        test_files = {
            1: 'test_cases1.txt',
            2: 'test_cases2.txt',
            3: 'test_cases3.txt',
            4: 'test_cases4.txt',
            5: 'test_cases5.txt'
        }

        # Prompt the user to select a file
        print("\nSelect an example source file by typing an integer between 1-5 (or type 0 to exit):")
        for option, file_name in test_files.items():
            print(f"Type {option} for '{file_name}'")

        try:
            # Get user's choice and convert to integer
            choice = int(input("Test case: "))
            print()
            if choice == 0:
                break  # Exit the loop (and program) if the user chooses 0
            elif choice in test_files:
                test_file = test_files[choice]
                run_file(test_file)
                if hadError:
                    sys.exit(65)  # You may want to remove this line if you want the program to continue despite errors
            else:
                print("Invalid choice. Please select a number between 1-5.")
        except ValueError:
            # Handle the case where the input is not an integer
            print("Invalid input. Please enter an integer.")


def run_file(path: str):
    with open(path, "r") as f:
        run(f.read())


def run(src: str):
    global hadError
    scanner = Scanner(src)
    tokens = scanner.scan_tokens()
    for token in tokens:
        # Token print and debugging
        # print(f"token: {token}")
        pass

    parser = Parser(tokens)
    try:
        statements = parser.parse()
        for statement in statements:
            # Statement parser print and debugging
            # print(f"parser: {statement}")
            pass
        interpreter = Interpreter()
        interpreter.interpret(statements)
    except Parser.ParseError as e:
        print(f"Caught parse error: {e}", file=sys.stderr)
        hadError = True

if __name__ == "__main__":
    main()  # Execute the main function if this script is executed directly
