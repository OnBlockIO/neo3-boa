import json

from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestPolicyInterop(BoaTest):

    default_folder: str = 'test_sc/interop_test/policy'

    def test_get_exec_fee_factor(self):
        path = self.get_contract_path('GetExecFeeFactor.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)