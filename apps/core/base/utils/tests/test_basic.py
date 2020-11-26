from django.test import TestCase
from apps.core.base.utils import basic


class TestBasic(TestCase):

    def test_random_hex_code_length(self):
        # default length of basic.random_hex_code() if no parameter given is 8
        self.assertEqual(len(basic.random_hex_code()), 8)
        # basic.random_hex_code() length will be the value of parameter
        self.assertEqual(len(basic.random_hex_code(20)), 20)
        
    def test_random_hex_code_duplicate_possibility(self):
        # random generated code will not match
        for _ in range(1000):
            self.assertNotEqual(basic.random_hex_code(), basic.random_hex_code())
        
    def test_random_hex_code_datatype(self):
        # random generated code will be string
        self.assertFalse(basic.random_hex_code().isnumeric())
        # random generated code will be alphanumeric
        self.assertTrue(basic.random_hex_code().isalnum())
