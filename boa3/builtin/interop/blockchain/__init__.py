from typing import Union

from boa3.builtin.interop.blockchain.transaction import Transaction
from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160

current_height: int = 0


def get_contract(hash: UInt160) -> Contract:
    """
    Gets a contract with a given hash

    :param hash: a smart contract hash
    :type hash: UInt160
    :return: a contract
    :rtype: Contract
    :raise Exception: raised if hash length isn't 20 bytes
    """
    pass


def get_transaction(hash: bytes) -> Transaction:    # TODO: change bytes to Hash256 UInt256
    """
    Gets a transaction with a given hash

    :param hash: a transaction hash with the size of 32 bytes
    :type hash: bytes
    :return: a transaction
    :rtype: Transaction
    """
    pass


def get_transaction_from_block(block_hash_or_index: Union[bytes, int], tx_index: int) -> Transaction:  # TODO: change bytes to Hash256 UInt256
    """
    Gets a transaction from a Block with a given hash and transaction index

    :param block_hash_or_index: the block hash with size of 32 bytes or the block index
    :type block_hash_or_index: bytes or int
    :param tx_index: a transaction index from a block
    :type tx_index: int
    :return: a transaction
    :rtype: Transaction
    """
    pass


def get_transaction_height(hash: bytes) -> int:     # TODO: change bytes to Hash256 UInt256
    """
    Gets the height of a transaction

    :param hash: a transaction hash with the size of 32 bytes
    :type hash: bytes
    :return: the height from a transaction
    :rtype: int
    """
    pass
