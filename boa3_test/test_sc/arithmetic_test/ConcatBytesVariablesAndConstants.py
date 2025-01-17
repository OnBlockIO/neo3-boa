from boa3.builtin import public
from boa3.builtin.interop.runtime import time


VALUE1 = b'value1'
VALUE2 = b'value2'
VALUE3 = b'value3'


@public
def concat1() -> bytes:
    current_time = time.to_bytes() + b'some_bytes_after'
    return VALUE1 + b'  ' + VALUE2 + b'  ' + VALUE3 + b'  ' + current_time


@public
def concat2() -> bytes:
    current_time = time.to_bytes() + b'some_bytes_after'
    return VALUE1 + VALUE2 + VALUE3 + current_time


@public
def concat3() -> bytes:
    current_time = time.to_bytes() + b'some_bytes_after'
    return VALUE1 + b'__' + VALUE2 + b'__' + VALUE3 + b'__' + current_time
