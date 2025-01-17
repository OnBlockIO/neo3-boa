from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(key: str) -> bytes:
    return StdLib.base58_check_decode(key)
