import unittest
from example.function import greater_than


class TestGreaterThan(unittest.TestCase):
    
    def setUp(self):
        self.value_a = 15
        self.value_b = 20
    
    def test_not_greater(self):
        """Test de a > b = False """
        self.assertFalse(greater_than(self.value_a, self.value_b))

    def test_greater(self):
        """Test de b > a = True """
        self.assertTrue(greater_than(self.value_b, self.value_a))

if __name__ == '__main__':

    unittest.main()
