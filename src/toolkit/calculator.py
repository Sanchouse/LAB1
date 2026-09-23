def tokenization(expr):
    tokens = []
    state = 'START'
    current_token = ''
    
    for char in expr:
        if state == 'START':
            if char.isdigit():
                state = 'NUMBER'
                current_token = char
            # TODO: обработать пробелы, операторы, числа с точкой
                
        elif state == 'NUMBER':
            if char.isdigit():
                current_token += char
            # TODO: обработать точку, завершение числа и переход обратно в START
        # TODO: другие состояния

    # Завершающая обработка
    if state == 'NUMBER':  # или ваше состояние
        tokens.append(('NUMBER', float(current_token)))
    
    return tokens



def calculate(args:str):
    args = args.split()
    tokens = tokenization(args)