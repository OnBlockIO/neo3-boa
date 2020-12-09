from typing import Any

from boa3.builtin import public


@public
def main(a: Any, b: Any) -> int:
    if a > b:
        return 3
    else:
        return 2
