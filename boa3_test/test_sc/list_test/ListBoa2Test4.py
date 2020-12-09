from boa3.builtin import public
from boa3.builtin.interop.runtime import notify


@public
def main() -> int:

    m = 3

    j = list(length=m)

    j[0] = 3

    j[1] = 2

    q = j[0]

    notify(q)

    return j