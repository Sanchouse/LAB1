from decimal import Decimal

import toolkit.errors as error


def validation(cnum: int, cop: int, crbr: int, clbr: int) -> None:
    """Check errors"""

    #EMPTY
    if not tokens:
        raise error.EmptyBracketsError()

    #REPEATING
    for i in range(len(tokens)-1):
        if tokens[i][0] == tokens[i+1][0] and tokens[i][0] != "LTBRACKETS" and tokens[i][0] != "RTBRACKETS":
            raise error.RepeatingElementsError()

    #OP AT THE END
    if tokens[-1][0] == "OPERATOR":
        raise error.OperatorAtTheEndError()

    #UNKNOWN CHAR
    for i in range(len(tokens)):
        if tokens[i][0] == "ERROR":
            raise error.UnknownCharError(tokens[i][1])

    #example: "3 + (2"
    if crbr != clbr:
        raise error.NotEnoughBracketsError()

    #Empty brackets
    for i in range(len(tokens)-1):
            if tokens[i][0] == "LTBRACKETS" and tokens[i+1][0] == "RTBRACKETS" :
                raise error.EmptyBracketsError()


def tokenization(expr:str) -> None:
    """Create tokens from expression"""

    numbers, count_numbers, count_operators = "", 0, 0
    count_rtbrackets, count_ltbrackets = 0, 0
    if_double_operator = 0

    for i in range(len(expr)):
        if if_double_operator:
            if_double_operator = 0
            continue

        if expr[i] in ["-", "+", "*", "/", "%"]:
            if numbers:
                tokens.append(("NUMBER", Decimal(numbers).quantize(Decimal('1.00'))))
                numbers, count_numbers = "", count_numbers+1

            if i != len(expr)-1:
                if expr[i]+expr[i+1] == "**" or expr[i]+expr[i+1] == "//":
                    tokens.append(("OPERATOR", expr[i]+expr[i+1]))
                    if_double_operator = 1
                else:
                    if not expr[i+1].isdigit() or expr[i] in ["*", "/", "%"]:
                        tokens.append(("OPERATOR", expr[i]))
                    elif expr[i] == "+" or expr[i] == "-":
                        tokens.append(("OPERATOR", "+"))
                        numbers += expr[i]

                count_operators += 1
            else:
                tokens.append(("OPERATOR", expr[i]))
        elif expr[i].isdigit() or expr[i] == ".":
            numbers += expr[i]

        elif expr[i] == "(":
            if numbers:
                tokens.append(("NUMBER", Decimal(numbers).quantize(Decimal('1.00'))))
                numbers, count_numbers = "", count_numbers+1

            tokens.append(("LTBRACKETS", "("))
            count_ltbrackets += 1

        elif expr[i] == ")":
            if numbers:
                tokens.append(("NUMBER", Decimal(numbers).quantize(Decimal('1.00'))))
                numbers, count_numbers = "", count_numbers+1
            tokens.append(("RTBRACKETS", ")"))
            count_rtbrackets += 1

        elif expr[i] == " ":
            if numbers:
                tokens.append(("NUMBER", Decimal(numbers).quantize(Decimal('1.00'))))
                numbers = ""
                count_numbers += 1
            continue
        else:
            tokens.append(("ERROR", expr[i]))

    if numbers:
        tokens.append(("NUMBER", Decimal(numbers).quantize(Decimal('1.00'))))
        count_numbers += 1
    validation(count_numbers, count_operators, count_ltbrackets, count_rtbrackets)


def parse_primary() -> float:
    """Return digit or answer of an expression in brackets"""
    global pos
    if tokens[pos][0] == "LTBRACKETS":
        pos += 1
        result = parse_plus()
        if tokens[pos][0] == "RTBRACKETS":
            pos += 1
        return result


    if tokens[pos][0] == "NUMBER":
        number = tokens[pos][1]
        pos += 1
        return number


def parse_pow() -> float:
    """Check pow in current position"""
    global pos
    left = parse_primary()
    while True:
        if pos >= len(tokens):
            pos -= 1
        if tokens[pos][1] != "**":
            break
        pos += 1

        right = parse_primary()
        left = left**right

    return left

def parse_percent() -> float:
    """Check percent in current position"""
    global pos
    left = parse_pow()
    while True:
        if tokens[pos][1] != "%":
            break
        pos += 1

        right = parse_pow()
        left = left % right

    return left

def parse_integer_division() -> float:
    """Check integer division in current position"""

    global pos
    left = parse_percent()
    while True:
        if pos >= len(tokens):
            continue
        if tokens[pos][1] != "//":
            break
        pos += 1

        right = parse_percent()
        try:
            left = left // right
        except ZeroDivisionError:
            raise ValueError("division by zero")

    return left

def parse_division() -> float:
    """Check division in current position"""

    global pos
    left = parse_integer_division()
    while True:
        if pos >= len(tokens):
            continue
        if tokens[pos][1] != "/":
            break
        pos += 1

        right = parse_integer_division()
        try:
            left = left / right
        except ZeroDivisionError:
            raise ValueError("division by zero")

    return left

def parse_multiplication() -> float:
    """Check multiplication in current position"""

    global pos
    left = parse_division()
    while True:
        if pos >= len(tokens):
            continue
        if tokens[pos][1] != "*":
            break
        pos += 1

        right = parse_division()
        left = left * right

    return left

def parse_minus() -> float:
    """Check minus in current position"""

    global pos
    left = parse_multiplication()
    while True:
        if pos >= len(tokens):
            continue
        if tokens[pos][1] != "-":
            break
        pos += 1
        right = parse_multiplication()
        if left == None:
            left = -1 * right
        else:
            left = left - right

    return left

def parse_plus() -> float:
    """Check plus in current position"""

    global pos
    left = parse_minus()
    while True:
        if pos >= len(tokens):
            continue
        if tokens[pos][1] != "+":
            break
        pos += 1

        right = parse_minus()
        if left == None:
            left = 1 * right
        else:
            left = left + right

    return left

def get_result() -> float:
    """Return result of an expression"""
    return parse_plus()


def calculate(args:str) -> float:
    """Return result of an expression"""
    global tokens, pos
    tokens = []
    pos = 0

    tokenization(args)
    return float(get_result().quantize(Decimal('1.00')))
