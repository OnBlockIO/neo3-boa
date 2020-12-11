from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classtype import ClassType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.model.type.collection.sequence.uint160type import UInt160Type


class BlockType(ClassType):
    """
    A class used to represent Neo Block class
    """

    def __init__(self):
        super().__init__('Block')

        from boa3.model.type.type import Type
        self._variables: Dict[str, Variable] = {
            'hash': Variable(Type.bytes),
            'version': Variable(Type.int),
            'prev_hash': Variable(Type.bytes),
            'merkle_root': Variable(Type.bytes),
            'timestamp': Variable(Type.int),
            'index': Variable(Type.int),
            'next_consensus': Variable(UInt160Type.build()),
            'transactions_count': Variable(Type.int)
        }
        self._constructor: Method = None

    @property
    def variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Method:
        # was having a problem with recursive import
        if self._constructor is None:
            self._constructor: Method = BlockMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None):
        if value is None or cls._is_type_of(value):
            return _Block

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, BlockType)


_Block = BlockType()


class BlockMethod(IBuiltinMethod):

    def __init__(self, return_type: BlockType):
        identifier = '-Block__init__'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.PUSH0, b''),
            (Opcode.PUSHDATA1, Integer(20).to_byte_array() + bytes(20)),
            (Opcode.PUSH0, b''),
            (Opcode.PUSH0, b''),
            (Opcode.PUSHDATA1, Integer(0).to_byte_array()),
            (Opcode.PUSHDATA1, Integer(0).to_byte_array()),
            (Opcode.PUSH0, b''),
            (Opcode.PUSHDATA1, Integer(0).to_byte_array()),
            (Opcode.PUSH8, b''),
            (Opcode.PACK, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
