from typing import Dict, List, Optional, Tuple

from boa3.constants import ROLE_MANAGEMENT
from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetRoleManagementScriptHashMethod(IBuiltinMethod):
    def __init__(self):
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_role-management'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer

        value = ROLE_MANAGEMENT
        return [
            (Opcode.PUSHDATA1, Integer(len(value)).to_byte_array() + value)
        ]


class RoleManagementProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'RoleManagement'
        getter = GetRoleManagementScriptHashMethod()
        super().__init__(identifier, getter)


RoleManagement = RoleManagementProperty()
