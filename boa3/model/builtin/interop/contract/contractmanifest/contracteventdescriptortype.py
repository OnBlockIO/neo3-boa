from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classtype import ClassType
from boa3.model.variable import Variable
from boa3.neo.vm.type.StackItem import StackItemType


class ContractEventDescriptorType(ClassType):
    """
    A class used to represent Neo ContractEventDescriptor class
    """

    def __init__(self):
        super().__init__('ContractEventDescriptor')
        from boa3.model.builtin.interop.contract.contractmanifest.contractparameterdefinitiontype import \
            ContractParameterDefinitionType
        from boa3.model.type.type import Type

        self._variables: Dict[str, Variable] = {
            'name': Variable(Type.str),
            'parameters': Variable(Type.list.build_collection(ContractParameterDefinitionType.build()))
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
        return StackItemType.Struct

    @classmethod
    def build(cls, value: Any = None) -> ContractEventDescriptorType:
        if value is None or cls._is_type_of(value):
            return _ContractEventDescriptor

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ContractEventDescriptorType)


_ContractEventDescriptor = ContractEventDescriptorType()