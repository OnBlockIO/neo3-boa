from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classtype import ClassType
from boa3.model.variable import Variable
from boa3.neo.vm.type.StackItem import StackItemType


class ContractPermissionType(ClassType):
    """
    A class used to represent Neo ContractPermission class
    """

    def __init__(self):
        super().__init__('ContractPermission')
        from boa3.model.type.type import Type

        self._variables: Dict[str, Variable] = {
            'contract': Variable(Type.str),
            'methods': Variable(Type.optional.build(Type.list.build_collection([Type.str])))
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

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.Array

    @classmethod
    def build(cls, value: Any = None) -> ContractPermissionType:
        if value is None or cls._is_type_of(value):
            return _ContractPermission

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractPermissionType)


_ContractPermission = ContractPermissionType()