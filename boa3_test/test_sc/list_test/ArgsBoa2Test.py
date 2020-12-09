from typing import Any, List

from boa3.builtin import public


@public
def main(operation: str, items: List[Any]) -> int:
    j = 10

    if operation == 'dostuff':
        j = 3
        if len(items) == 2:
            bytes1 = items[0]
            bytes2 = items[1]

            len1 = len(bytes1)
            len2 = len(bytes2)
            total = bytes1 + bytes2

            j = len1 + len2

            """
            if total == 137707327489:
                log('awesome!')
            else:
                log('bad')
            """
        else:
            j = 23

    elif operation == 'dont':
        j = 4

    return j
