from boa3.builtin import public


@public
def Main() -> int:
    x = '1234'
    y = x
    x = 1234
    return x
