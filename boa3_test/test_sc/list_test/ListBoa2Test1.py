from boa3.builtin import public


@public
def main() -> bool:
    m = [2, 4, 1, 5 + 12]

    m[2] = 7 + 10

    m2 = [9, 10, 11, 12]

    m2[0] = 4

    q = m[1]

    return m2[0] == q
