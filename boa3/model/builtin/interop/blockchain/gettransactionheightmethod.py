from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class GetTransactionHeightMethod(InteropMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'get_transaction_height'
        syscall = 'System.Blockchain.GetTransactionHeight'
        args: Dict[str, Variable] = {'hash': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=Type.int)
