from boa3.builtin import public


@public
def main(operation: str, a: int, b: int) -> int:

    if operation == '&':
        return a & b
    elif operation == '|':
        return a | b
    elif operation == '^':
        return a ^ b
    elif operation == '>>':
        return a >> b
    elif operation == '%':
        return a % b
    elif operation == '//':
        return a // b
    elif operation == '~':
        return ~a
