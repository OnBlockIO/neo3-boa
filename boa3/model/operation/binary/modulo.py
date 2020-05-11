from typing import List, Optional

from boa3.model.operation.binary.binaryoperation import BinaryOperation
from boa3.model.operation.operator import Operator
from boa3.model.type.type import IType, Type
from boa3.neo.vm.Opcode import Opcode


class Modulo(BinaryOperation):
    _valid_types: List[IType] = [Type.int]

    def __init__(self, left: IType = Type.int, right: IType = Type.int):
        self.operator: Operator = Operator.Mod
        super().__init__(left, right)

    def validate_type(self, *types: IType) -> bool:
        if len(types) != self._get_number_of_operands:
            return False
        left: IType = types[0]
        right: IType = types[1]

        # TODO: change the logic of the validation when implement other numeric types
        return left == right and left in self._valid_types

    def _get_result(self, left: IType, right: IType) -> IType:
        # TODO: change the logic of the return type when implement other numeric types
        if self.validate_type(left, right):
            return left
        else:
            return Type.none

    @property
    def opcode(self) -> Optional[Opcode]:
        return Opcode.MOD
