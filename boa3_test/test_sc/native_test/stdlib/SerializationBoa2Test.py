from typing import Any, cast

from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib
from boa3.builtin.interop.storage import get, put


@public
def main(operation: int) -> Any:

    # create an array
    stuff = ['a', 3, ['j', 3, 5], 'jk', 'lmnopqr']

    # serialize it
    to_save = StdLib.serialize(stuff)
    put('serialized', to_save)

    if operation == 1:
        return to_save

    elif operation == 2:
        to_retrieve = get('serialized')
        return to_retrieve

    elif operation == 3:

        to_retrieve = get('serialized')
        deserialized = StdLib.deserialize(to_retrieve)
        return deserialized

    elif operation == 4:

        to_retrieve = get('serialized')
        deserialized = StdLib.deserialize(to_retrieve)
        return cast(list, deserialized)[2]

    return False