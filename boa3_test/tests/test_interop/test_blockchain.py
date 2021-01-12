import json

from boa3 import constants
from boa3.boa3 import Boa3
from boa3.model.builtin.interop.interop import Interop
from boa3.neo.cryptography import hash160
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBlockchainInterop(BoaTest):

    def test_get_current_height(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.CurrentHeight.getter.interop_method_hash
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/blockchain/CurrentHeight.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_current_height_cant_assign(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01\x01'
            + Opcode.LDARG0
            + Opcode.STLOC0
            + Opcode.LDLOC0
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/interop_test/blockchain/CurrentHeightCantAssign.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_get_contract(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00\x01'
            + Opcode.LDARG0
            + Opcode.PUSH1
            + Opcode.PACK
            + Opcode.PUSHDATA1
            + Integer(len(Interop.GetContract.method_name)).to_byte_array(min_length=1)
            + String(Interop.GetContract.method_name).to_bytes()
            + Opcode.PUSHDATA1
            + Integer(len(constants.MANAGEMENT_SCRIPT)).to_byte_array(min_length=1)
            + constants.MANAGEMENT_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/interop_test/blockchain/GetContract.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'main', bytes(20))
        self.assertIsNone(result)

        call_contract_path = '%s/boa3_test/test_sc/arithmetic_test/Addition.py' % self.dirname
        Boa3.compile_and_save(call_contract_path)

        script, manifest = self.get_output(call_contract_path)
        call_hash = hash160(script)
        call_contract_path = call_contract_path.replace('.py', '.nef')

        engine.add_contract(call_contract_path)
        arg_manifest = json.dumps(manifest, separators=(',', ':'))

        result = self.run_smart_contract(engine, path, 'main', call_hash)
        self.assertEqual(5, len(result))
        self.assertEqual(call_hash, result[2])
        self.assertEqual(script, result[3])
        self.assertEqual(json.loads(arg_manifest), json.loads(result[4]))