from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes, NotSupportedOperation, UnresolvedOperation
from boa3.model.type.type import Type
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3_test.tests.boa_test import BoaTest


class TestBytes(BoaTest):

    def test_bytes_literal_value(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = b'\x01\x02\x03'
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytesLiteral.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_bytes_get_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytesGetValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_bytes_get_value_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH1
            + Opcode.NEGATE
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytesGetValueNegativeIndex.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_bytes_set_value(self):
        path = '%s/boa3_test/example/bytes_test/BytesSetValue.py' % self.dirname
        self.assertCompilerLogs(UnresolvedOperation, path)

    def test_bytes_from_byte_array(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = bytearray(b'\x01\x02\x03')
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a
            + Opcode.STLOC1
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytesFromBytearray.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_get_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytearrayGetValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_get_value_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH1
            + Opcode.NEGATE
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytearrayGetValueNegativeIndex.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_set_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0] = 0x01
            + Opcode.PUSH0
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.LDARG0
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytearraySetValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_set_value_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[-1] = 0x01
            + Opcode.PUSH1
            + Opcode.NEGATE
                + Opcode.DUP
                + Opcode.SIGN
                + Opcode.PUSHM1
                + Opcode.JMPNE
                + Integer(5).to_byte_array(min_length=1, signed=True)
                + Opcode.OVER
                + Opcode.SIZE
                + Opcode.ADD
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.LDARG0
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytearraySetValueNegativeIndex.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_literal_value(self):
        path = '%s/boa3_test/example/bytes_test/BytearrayLiteral.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_byte_array_from_literal_bytes(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = bytearray(b'\x01\x02\x03')
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytearrayFromLiteralBytes.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_from_variable_bytes(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = b'\x01\x02\x03'
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = bytearray(a)
            + Opcode.STLOC1
            + Opcode.PUSHNULL
            + Opcode.RET        # return
        )

        path = '%s/boa3_test/example/bytes_test/BytearrayFromVariableBytes.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_string(self):
        path = '%s/boa3_test/example/bytes_test/BytearrayFromString.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)

    def test_byte_array_append(self):
        path = '%s/boa3_test/example/bytes_test/BytearrayAppend.py' % self.dirname
        self.assertCompilerLogs(NotSupportedOperation, path)
