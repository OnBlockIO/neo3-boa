from typing import Dict

from boa3.model.builtin.interop.blockchain import TransactionType
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class GetTransactionFromBlockMethod(InteropMethod):

    def __init__(self, transaction_type: TransactionType):
        from boa3.model.type.type import Type
        identifier = 'get_transaction_from_block'
        syscall = 'System.Blockchain.GetTransactionFromBlock'
        args: Dict[str, Variable] = {
            'block_hash': Variable(Type.union.build([Type.bytes,
                                                     Type.int
                                                     ])),
            'tx_index': Variable(Type.int)
        }
        super().__init__(identifier, syscall, args, return_type=transaction_type)