from boa3.builtin import public

@public
def main() -> bytearray:
    m = b'\x01\x02'

    j = getba()

    return m + j


def getba() -> bytearray:
    return b'\xaa\xfe'
