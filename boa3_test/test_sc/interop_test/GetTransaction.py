from boa3.builtin import public
from boa3.builtin.interop.blockchain import get_transaction, Transaction


@public
def main(hash: bytes) -> Transaction:
    return get_transaction(hash)
