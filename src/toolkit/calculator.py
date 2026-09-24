from decimal import Decimal

tokens, pos = [], 0

def validation(cnum, cop, crbr, clbr):
    
    #EMPTY
    if not tokens:
        raise ValueError("Expression is empty")

    #REPEATING
    for i in range(len(tokens)):
        if tokens[i][0] == tokens[i][1]:
            raise ValueError("repeating elements")

    #OP AT THE END
    if tokens[-1][0] == "OPERATOR":
        raise ValueError("Operator can't be at the end")

    #Incorrect symbol
    for i in range(len(tokens)):
        if tokens[i][0] == "ERROR":
            raise ValueError("Incorrect symbol in expression")


    #example: "10 10"
    if cnum>1 and cop==0:
        raise ValueError("Expression doesn't have operators") 

    #example: "3 + (2"
    if crbr != clbr:
        raise ValueError("There aren’t enough brackets.")

    #Empty brackets
    for i in range(len(tokens)-1):
            if tokens[i][0] == "LTBRACKETS" and tokens[i+1][0] == "RTBRACKETS" :
                raise ValueError("Empty brackets")

    



def tokenization(expr:str):
    global tokens

    numbers, count_numbers, count_operators = "", 0, 0
    count_rtbrackets, count_ltbrackets = 0, 0
    ifdoubleoperator = 0

    for i in range(len(expr)):
        if ifdoubleoperator:
            ifdoubleoperator = 0
            continue

        if expr[i] in ["-", "+", "*", "/", "%"]:
            if numbers:
                tokens.append(("NUMBER", Decimal(numbers).quantize(Decimal('1.00'))))
                numbers, count_numbers = "", count_numbers+1

            if i != len(expr)-1:
                if expr[i]+expr[i+1] == "**" or expr[i]+expr[i+1] == "//":
                    tokens.append(("OPERATOR", expr[i]+expr[i+1]))
                    ifdoubleoperator = 1
                else:
                    tokens.append(("OPERATOR", expr[i]))

                count_operators += 1

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


def parse_primary():
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
    


def parse_pow():
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

def parse_percent():
    global pos
    left = parse_pow()
    while True:
        if tokens[pos][1] != "%":
            break
        pos += 1

        right = parse_pow()
        left = left % right

    return left

def parse_integer_division():
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

def parse_division():
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

def parse_multiplication():
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

def parse_minus():
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

def parse_plus():
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

def get_result():
    return parse_plus()


def calculate(args:str):
    tokenization(args)
    return get_result().quantize(Decimal('1.00'))