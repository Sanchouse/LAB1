def tokenization(expr:str):
    tokens, numbers, count_numbers, count_operators = [], "", 0, 0
    for i in range(len(expr)):
        if expr[i] in ["-", "+", "*", "/", "%"]:
            if numbers:
                tokens.append(("NUMBER", float(numbers)))
                numbers, count_numbers = "", count_numbers+1
            if i != len(expr)-1:
                if expr[i]+expr[i+1] == "**" or expr[i]+expr[i+1] == "//":
                    tokens.append(("OPERATOR", expr[i]+expr[i+1]))
                else:
                    tokens.append(("OPERATOR", expr[i]))
                count_operators += 1
                if tokens[-1][0]=="OPERATOR" and tokens[-2][0]=="OPERATOR":
                    raise ValueError("It can't be two or more operators in expression")
            else:
                raise ValueError("Operator can't be at the end")
        elif expr[i].isdigit() or expr[i] == ".":
            numbers += expr[i]
        elif expr[i] == "(":
            tokens.append(("LTBRACKETS", "("))
        elif expr[i] == ")":
            tokens.append(("RTBRACKETS", ")"))
        elif expr[i] == " ":
            if numbers:
                tokens.append(("NUMBER", float(numbers)))
                numbers = ""
                count_numbers += 1
            continue
        else:
            raise ValueError("Incorrect symbol in expression")
    if numbers:
        tokens.append(("NUMBER", float(numbers)))
        count_numbers += 1
    if count_numbers<1:
        raise ValueError("There aren’t enough numbers.")
    elif count_numbers>1 and count_operators == 0: 
        raise ValueError("Expression doesn't have operators")
    return tokens



def calculate(args:str):
    tokens = tokenization(args)
    return tokens


print(calculate("2 ** 2"))