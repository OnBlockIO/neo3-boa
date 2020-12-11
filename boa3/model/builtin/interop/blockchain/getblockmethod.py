from typing import Dict

from boa3.model.builtin.interop.blockchain.blocktype import BlockType
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class GetBlockMethod(InteropMethod):

    def __init__(self, block_type: BlockType):
        identifier = 'get_block'
        syscall = 'System.Blockchain.GetBlock'
        from boa3.model.type.type import Type
        args: Dict[str, Variable] = {'index_or_hash': Variable(Type.union.build([Type.bytes,
                                                                                 Type.int
                                                                                 ]))}
        super().__init__(identifier, syscall, args, return_type=block_type)
