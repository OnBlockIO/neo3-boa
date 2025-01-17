from boa3.builtin import public
from boa3.builtin.interop.blockchain import Transaction, get_transaction_from_block
from boa3.builtin.type import UInt256


@public
def main(hash_: UInt256, tx_index: int) -> Transaction:
    return get_transaction_from_block(hash_, tx_index)
