from boa3.builtin import public
from boa3.builtin.interop.storage import put, find


@public
def main(query: str):

    put('prefix1euo', 1)
    put('prefix1e', 2)
    put('prefix1__osetuh', 3)

    put('blah', 'Hello Storage Find')

    result_iter = find(query)

    items = []
    keys = []
    count = 0
    while result_iter.next():
        val = result_iter.value
        items.append(val)
        keys.append(result_iter.key)
        if query == 'pre' and count == 1:
            break

        count += 1

    if query == 'pref':
        return keys

    return items
