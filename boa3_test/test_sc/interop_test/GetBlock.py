from typing import Union
from boa3.builtin import public
from boa3.builtin.interop.blockchain import get_block
from boa3.builtin.interop.blockchain.block import Block


@public
def main(index_or_hash: Union[bytes, int]) -> Block:
    return get_block(index_or_hash)
