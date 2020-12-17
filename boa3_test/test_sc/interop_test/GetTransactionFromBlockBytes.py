from boa3.builtin import public
from boa3.builtin.interop.blockchain import get_transaction_from_block, Transaction


@public
def main(block_hash: bytes, tx_index: int) -> Transaction:  # TODO: change bytes to UInt256
    return get_transaction_from_block(block_hash, tx_index)
