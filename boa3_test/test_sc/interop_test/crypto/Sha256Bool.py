from boa3.builtin import public
from boa3.builtin.interop.crypto import sha256


@public
def Main() -> bytes:
    return sha256(True)