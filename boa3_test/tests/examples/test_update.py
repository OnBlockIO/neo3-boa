from boa3.boa3 import Boa3
from boa3.neo import to_script_hash
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException


class TestUpdateTemplate(BoaTest):

    default_folder: str = 'examples'

    OWNER_SCRIPT_HASH = bytes(20)
    OTHER_ACCOUNT_1 = to_script_hash(b'NiNmXL8FjEUEs1nfX9uHFBNaenxDHJtmuB')
    OTHER_ACCOUNT_2 = bytes(range(20))

    def test_old_update_compile(self):
        path_old = self.get_contract_path('update_contract.py')
        Boa3.compile_and_save(path_old)

    def test_new_update_compile(self):
        path_new = self.get_contract_path('examples/auxiliary_contracts', 'update_contract.py')
        Boa3.compile_and_save(path_new)

    def test_old_update_deploy(self):
        path_old = self.get_contract_path('update_contract.py')
        engine = TestEngine()

        # needs the owner signature
        result = self.run_smart_contract(engine, path_old, method='deploy',
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should return false if the signature isn't from the owner
        result = self.run_smart_contract(engine, path_old, 'deploy',
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path_old, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # must always return false after first execution
        result = self.run_smart_contract(engine, path_old, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

    def test_new_update_deploy(self):
        path_new = self.get_contract_path('examples/auxiliary_contracts', 'update_contract.py')
        engine = TestEngine()

        # needs the owner signature
        result = self.run_smart_contract(engine, path_new, method='deploy',
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        # should return false if the signature isn't from the owner
        result = self.run_smart_contract(engine, path_new, 'deploy',
                                         signer_accounts=[self.OTHER_ACCOUNT_1],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path_new, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # must always return false after first execution
        result = self.run_smart_contract(engine, path_new, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(False, result)

    def test_update_storage(self):
        path_old = self.get_contract_path('update_contract.py')
        path_new = self.get_contract_path('examples/auxiliary_contracts', 'update_contract.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path_old, 'get_storage',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH], expected_result_type=bytes)
        self.assertEqual(b'', result)

        expected_result = b'neo_boa'
        result = self.run_smart_contract(engine, path_old, 'put_storage', expected_result,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path_old, 'get_storage',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH], expected_result_type=bytes)
        self.assertEqual(expected_result, result)

        result = self.run_smart_contract(engine, path_new, 'get_storage',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH], expected_result_type=bytes)
        self.assertEqual(b'', result)

        expected_result = b'neo_boa'
        result = self.run_smart_contract(engine, path_new, 'put_storage', expected_result,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path_new, 'get_storage',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH], expected_result_type=bytes)
        self.assertEqual(expected_result, result)

    def test_update_update(self):
        path_old = self.get_contract_path('update_contract.py')
        path_new = self.get_contract_path('examples/auxiliary_contracts', 'update_contract.py')
        engine = TestEngine()

        nef, manifest = self.get_bytes_output(path_new)
        import json
        from boa3.neo.vm.type.String import String
        arg_manifest = String(json.dumps(manifest, separators=(',', ':'))).to_bytes()

        # deploying the contract with outdated standard
        result = self.run_smart_contract(engine, path_old, 'deploy',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # calling onNEP17Payment will result in a exception, because this method is not in the smart contract
        with self.assertRaises(TestExecutionException, msg=self.CALLED_CONTRACT_DOES_NOT_EXIST_MSG):
            self.run_smart_contract(engine, path_old, 'onNEP17Payment',
                                    signer_accounts=[self.OWNER_SCRIPT_HASH])

        # updating the contract with the new standard
        result = self.run_smart_contract(engine, path_old, 'update', nef, arg_manifest,
                                         signer_accounts=[self.OWNER_SCRIPT_HASH],
                                         expected_result_type=bool)
        self.assertEqual(True, result)

        # the contract was updated, but the path still is same
        result = self.run_smart_contract(engine, path_old, 'onNEP17Payment',
                                         signer_accounts=[self.OWNER_SCRIPT_HASH])
        self.assertEqual(True, result)
