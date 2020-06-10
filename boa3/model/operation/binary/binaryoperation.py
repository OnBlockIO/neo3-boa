from abc import ABC, abstractmethod
from typing import List

from boa3.model.operation.operation import IOperation
from boa3.model.type.itype import IType


class BinaryOperation(IOperation, ABC):
    """
    An interface used to represent binary operations

    :ivar operator: the operator of the operation. Inherited from :class:`IOperation`
    :ivar left: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar right: the left operand type. Inherited from :class:`BinaryOperation`
    :ivar result: the result type of the operation.  Inherited from :class:`IOperation`
    """
    _valid_types: List[IType] = []

    def __init__(self, left: IType, right: IType = None):
        if right is None:
            right = left

        self.left_type: IType = left
        self.right_type: IType = right
        result = self._get_result(left, right)
        super().__init__(self.operator, result)

    @property
    def number_of_operands(self) -> int:
        return 2

    @abstractmethod
    def _get_result(self, left: IType, right: IType) -> IType:
        """
        Gets the result type of the operation given the operands types.

        :param left: left operand type
        :param right: right operand type
        :return: the result type of the operation. Type.none if the operands are not valid.
        """
        pass

    @classmethod
    def build(cls, *operands: IType):
        if len(operands) == 1:
            return cls._build_with_left_arg(operands[0])
        if len(operands) == 2:
            return cls._build_with_two_args(operands[0], operands[1])

    @classmethod
    def _build_with_left_arg(cls, left: IType):
        """
        Creates a binary operation with the given operands types

        :param left: left operand type
        :return: The built operation if the operands is valid. None otherwise
        :rtype: BinaryOperation or None
        """
        return cls(left)

    @classmethod
    def _build_with_two_args(cls, left: IType, right: IType):
        """
        Creates a binary operation with the given operands types

        :param left: left operand type
        :param right: right operand type
        :return: The built operation if the operands are valid. None otherwise
        :rtype: BinaryOperation or None
        """
        return cls(left, right)
