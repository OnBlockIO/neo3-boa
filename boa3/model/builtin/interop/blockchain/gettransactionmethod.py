from typing import Dict

from boa3.model.builtin.interop.blockchain.transactiontype import TransactionType
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class GetTransactionMethod(InteropMethod):

    def __init__(self, transaction_type: TransactionType):
        from boa3.model.type.type import Type
        identifier = 'get_transaction'
        syscall = 'System.Blockchain.GetTransaction'
        args: Dict[str, Variable] = {'hash': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=transaction_type)
