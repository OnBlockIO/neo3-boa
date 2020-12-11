from typing import Union
from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160
from boa3.builtin.interop.blockchain.block import Block

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


def get_block(index_or_hash: Union[bytes, int]) -> Block:   # TODO: change bytes to UInt256
    """

    :param index_or_hash: the index or hash that corresponds with a block
    :type index_or_hash: bytes
    :return: a block that corresponds with the given index or hash
    :rtype: Block
    :raise Exception: raised if index_or_hash length is out of the accepted range
    """
    pass
