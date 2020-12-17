from boa3.builtin import public
from boa3.builtin.interop.blockchain import get_transaction_from_block, Transaction


@public
def main(block_hash: int, tx_index: int) -> Transaction:
    return get_transaction_from_block(block_hash, tx_index)
