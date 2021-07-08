from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class CountMethod(IBuiltinMethod):

    def __init__(self, sequence_type: Optional[SequenceType] = None, arg_value: Optional[IType] = None):
        from boa3.model.type.type import Type
        identifier = 'count'
        if not isinstance(sequence_type, SequenceType):
            sequence_type = Type.sequence
        if not isinstance(arg_value, IType):
            arg_value = Type.any

        args: Dict[str, Variable] = {
            'self': Variable(sequence_type),
            'value': Variable(arg_value)
        }
        super().__init__(identifier, args, return_type=Type.int)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 2:
            return False
        if not all(isinstance(param, IExpression) for param in params):
            return False

        from boa3.model.type.itype import IType
        sequence_type: IType = params[0].type

        if not isinstance(sequence_type, SequenceType):
            return False
        from boa3.model.type.collection.sequence.mutable.listtype import ListType
        from boa3.model.type.collection.sequence.tupletype import TupleType
        from boa3.model.type.collection.sequence.rangetype import RangeType
        if not (isinstance(sequence_type, ListType) or isinstance(sequence_type, TupleType) or isinstance(sequence_type, RangeType)):
            return False
        return True

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count

        jmp_place_holder = (Opcode.JMP, b'\x01')

        repack_array = [            # recreates an array to not change the original one
            (Opcode.UNPACK, b''),
            (Opcode.PACK, b''),
        ]

        sequence_initialize = [     # initializes variables
            (Opcode.PUSH0, b''),    # count = 0
            (Opcode.OVER, b''),
            (Opcode.SIZE, b''),
            (Opcode.DEC, b''),      # index = len(sequence) - -1
        ]

        sequence_verify_while = [   # verifies if all the elements from the sequence were visited
            (Opcode.DUP, b''),      # would be equivalent to: while (index >= 0)
            (Opcode.SIGN, b''),
            (Opcode.PUSH0, b''),    # if index < 0:
            jmp_place_holder,           # jump to clean the stack
        ]

        sequence_get_element = [    # gets a element from the sequence
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b'')  # element = sequence[index]
        ]

        sequence_equals = [         # verifies if the element and the given value are the same
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.EQUAL, b''),    # if element != value:
            jmp_place_holder            # jump to list_tuple_count_index_dec
        ]

        sequence_count_inc = [      # increment count if element == value
            (Opcode.SWAP, b''),
            (Opcode.INC, b''),      # count++
            (Opcode.SWAP, b''),
        ]

        num_jmp_code = get_bytes_count(sequence_count_inc)
        jmp_to_dec_statement = Opcode.get_jump_and_data(Opcode.JMPIFNOT, num_jmp_code, True)
        sequence_equals[-1] = jmp_to_dec_statement

        list_tuple_count_index_dec = [  # decreases the index
            (Opcode.DEC, b''),          # index--
            # return to the while verification
        ]

        num_jmp_code = -get_bytes_count(list_tuple_count_index_dec + sequence_count_inc + sequence_equals +
                                        sequence_get_element + sequence_verify_while)
        jmp_back_to_while_verify_statement = Opcode.get_jump_and_data(Opcode.JMP, num_jmp_code)
        list_tuple_count_index_dec.append(jmp_back_to_while_verify_statement)

        num_jmp_code = get_bytes_count(sequence_get_element + sequence_equals +
                                       sequence_count_inc + list_tuple_count_index_dec)
        jmp_to_clean_statement = Opcode.get_jump_and_data(Opcode.JMPLT, num_jmp_code, True)
        sequence_verify_while[-1] = jmp_to_clean_statement

        clean_stack = [
            (Opcode.DROP, b''),
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

        return (
            repack_array +
            sequence_initialize +
            sequence_verify_while +
            sequence_get_element +
            sequence_equals +
            sequence_count_inc +
            list_tuple_count_index_dec +
            clean_stack
        )

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, List) or isinstance(value, list):
            if len(value) == 2:
                if type(value[0]) == type(self.args['self'].type) and type(value[1]) == type(self.args['value'].type):
                    return self

                return CountMethod(value[0], value[1])
        return super().build(value)