from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def serialize_bool() -> bytes:
    return StdLib.serialize(True)