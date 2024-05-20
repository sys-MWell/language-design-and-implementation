[BUILD.txt](https://github.com/sys-MWell/language-design-and-implementation/files/15379629/BUILD.txt)
[README.txt](https://github.com/sys-MWell/language-design-and-implementation/files/15379628/README.txt)

# StarlingScript - Language Design and Implementation

## Overview

This project involves the design and implementation of a custom programming language called StarlingScript. The language supports arithmetic expressions, Boolean logic, text values, global data, and control flow. The implementation follows the structure outlined in the book "Crafting Interpreters" by Robert Nystrom, with the code converted from Java to Python.

## Features

### Stage 1: Basic Calculator (0 – 20%)
- **Arithmetic Expression Parsing**: Supports parenthesis, unary negation, binary addition, subtraction, multiplication, and division.
- **Example Inputs**:
  - `1 - 2`
  - `2.5 + 2.5 - 1.25`
  - `(10 * 2) / 6`
  - `8.5 / (2 * 9) - -3`

### Stage 2: Boolean Logic (20 - 40%)
- **Boolean Expressions**: Supports binary comparison, equality, and inequality between numbers and Booleans, logical "AND" and "OR" operations, and unary negation of Booleans.
- **Example Inputs**:
  - `true == false`
  - `true != false`
  - `(5 < 10)`
  - `!(5 - 4 > 3 * 2 == !false)`

### Stage 3: Text Values (40 – 50%)
- **Text Value Operations**: Supports binary concatenation of text values and binary equality and inequality between text values.
- **Example Inputs**:
  - `"hello" + " " + "world"`
  - `"foo" + "bar" == "foobar"`
  - `"10 corgis" != "10" + "corgis"`

### Stage 4: Global Data (50 – 60%)
- **Global Variables**: Supports creation, reading, and display of named global variables.
- **Example Inputs**:
  - `quickMaths = 10`
  - `quickMaths = quickMaths + 2`
  - `print quickMaths`
  - `stringCatTest = "10 corgis"`
  - `stringCatTest = stringCatTest + 5 + " more corgis"`
  - `print stringCatTest`

### Stage 5: Control Flow (60 – 80%)
- **Control Flow Constructs**: Supports while loops, if-then statements, nested while loops, and if-then-else statements.
- **Example Inputs**:
  - ```
    is_running = true
    shopping_list = ""

    while (is_running == true) {
        item = input("add an item to the shopping list: ")
        
        if (item == "") {
            is_running = false
        }
        
        shopping_list = shopping_list + ", " + item
    }

    print shopping_list
    ```

### Additional Features (80+)
- **Function-Based Code Reusability (+10%)**
- **Local Variables (+15%)**

## Project Structure

The project directory is structured as follows:<br>
├── Callable.py<br>
├── Environment.py<br>
├── Expr.py<br>
├── Function.py<br>
├── Interpreter.py<br>
├── Parser.py<br>
├── Return.py<br>
├── Scanner.py<br>
├── StarlingScript.py<br>
├── Stmt.py<br>
├── Token.py<br>
├── TokenType.py<br>
├── test_cases1.txt<br>
├── test_cases2.txt<br>
├── test_cases3.txt<br>
├── test_cases4.txt<br>
├── test_cases5.txt<br>

## Installation and Setup

### Prerequisites
- Python 3.6 or higher installed on your system.
- Access to the terminal or command prompt on your system.

### Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/starling-script.git
   cd starling-script
2. **Run the StarlingScript Application:**
   ```bash
   python StarlingScript.py
3. **Select a Test Case:**
   The application will prompt you to select a test case file by typing a number between 1 - 5.
   For example, typing 1 and pressing Enter will run the test_cases1.txt script.
