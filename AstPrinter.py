

class AstPrinter:
    # Print expression
    def print(self, expr):
        return expr.accept(self)

    # Visit binary expressions
    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    # Visit grouping expressions
    def visit_grouping_expr(self, expr):
        return self.parenthesize("group", expr.expression)

    # Visit literal expressions
    def visit_literal_expr(self, expr):
        # Check if the value is None and return "nil", otherwise return the string representation of the value
        if expr.value is None:
            return "nil"
        return str(expr.value)

    # Visit unary expressions
    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    # Parenthesise expressions
    def parenthesize(self, name, *exprs):
        builder = []

        # Append the opening parenthesis and the name of the expression
        builder.append("(" + name)
        # Iterate over the expressions and append their string representation
        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))
        # Append the closing parenthesis
        builder.append(")")

        # Combine all the elements of the builder list into a single string
        return "".join(builder)
