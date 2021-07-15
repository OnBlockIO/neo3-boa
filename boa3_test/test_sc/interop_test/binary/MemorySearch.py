from typing import Union

from boa3.builtin import public
from boa3.builtin.interop.binary import memory_search


@public
def main(mem: Union[bytes, str], value: Union[bytes, str], start: int, backward: bool) -> int:
    return memory_search(mem, value, start, backward)
