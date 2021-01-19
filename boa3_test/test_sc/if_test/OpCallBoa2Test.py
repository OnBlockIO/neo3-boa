from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.crypto import hash160, sha256


@public
def main(operation: str, a: Any, b: Any) -> Any:

    if operation == 'omin':
        return min(a, b)

    elif operation == 'omax':
        return max(a, b)

    elif operation == 'sha256':
        return sha256(a)

    elif operation == 'hash160':
        return hash160(a)

    return 'unknown'
