from boa3.builtin import public


@public
def main(string: str, substring: str, start: int, end: int) -> int:
    return string.count(substring, start, end)
