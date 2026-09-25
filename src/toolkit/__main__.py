import argparse
import sys

from .calculator import calculate
from .converter import convert

parser = argparse.ArgumentParser(
    prog="python -m toolkit",
    description="Калькулятор и конвертер величин"
)

commands = parser.add_subparsers(
    dest="command",
    required=True
)


# ---------- CALC ----------

calc_parser = commands.add_parser(
    "calc",
    help="Вычислить выражение"
)

calc_parser.add_argument(
    "expression",
    help="Арифметическое выражение"
)


# ---------- CONVERT ----------

convert_parser = commands.add_parser(
    "convert",
    help="Конвертировать величину"
)

convert_parser.add_argument(
    "value",
    type=float,
    help="Значение"
)

convert_parser.add_argument(
    "--from",
    dest="from_unit",
    required=True,
    help="Исходная единица"
)

convert_parser.add_argument(
    "--to",
    dest="to_unit",
    required=True,
    help="Целевая единица"
)


def main():
    try:
        args = parser.parse_args()
        
        if args.command == "calc":
            result = calculate(args.expression)

            sys.stdout.write(str(result) + "\n")

            return 0
        elif args.command == "convert":
            result = convert(args)

            sys.stdout.write(str(result) + "\n")
            
            return 0

    except ValueError as e:
        sys.stderr.write(f"Ошибка: {e}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())


