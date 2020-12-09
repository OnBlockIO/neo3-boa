from typing import Any, List

from boa3.builtin import public


@public
def main(operation: str, args: List[str]) -> Any:
    if operation == 'concat':
        return do_concat(args)
    else:
        return False


def do_concat(args: List[str]):
    if len(args) > 1:
        a = args[0]
        b = args[1]
        output = a + b
        return output
    return False
