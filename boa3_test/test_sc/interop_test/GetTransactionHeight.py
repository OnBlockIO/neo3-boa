from boa3.builtin import public
from boa3.builtin.interop.blockchain import get_transaction_height


@public
def main(hash: bytes) -> int:
    return get_transaction_height(hash)
