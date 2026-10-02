class ConverterError(ValueError):
    pass

class CalculatorError(ValueError):
    pass


class UnknownUnitError(ConverterError):
    def __init__(self, unit:str):
        super().__init__(f"Unknown unit or invalid character: {unit}")


class NegativeValueError(ConverterError):
    def __init__(self):
        super().__init__("Negative distance/mass")


class DifferentTypesError(ConverterError):
    def __init__(self, from_unit:str, to_unit:str):
        super().__init__(f"Different types of units '{from_unit}' and '{to_unit}'")


class BelowAbsoluteZeroError(ConverterError):
    def __init__(self):
        super().__init__("Temperature is too low")


class EmptyExpressionError(CalculatorError):
    def __init__(self):
        super().__init__("Expression is empty")


class RepeatingElementsError(CalculatorError):
    def __init__(self):
        super().__init__("Repeating elements (operators or numbers)")


class OperatorAtTheEndError(CalculatorError):
    def __init__(self):
        super().__init__("Operator can't be at the end")


class UnknownCharError(CalculatorError):
    def __init__(self, char: str):
        super().__init__(f"Unknown symbol in expression '{char}'")


class NotEnoughBracketsError(CalculatorError):
    def __init__(self):
        super().__init__("There aren't enough brackets")


class EmptyBracketsError(CalculatorError):
    def __init__(self):
        super().__init__("Empty brackets")
