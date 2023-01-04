import unittest
from quote import Quote

class TestQuote(unittest.TestCase):
    def test_calculate_cost(self):
        quote = Quote("John Smith", "Basic", "California", True, True)
        cost = quote.calculate_cost()
        self.assertAlmostEqual(cost, 40.80, places=2)

        quote = Quote("Jane Doe", "Premium", "California", True, True)
        cost = quote.calculate_cost()
        self.assertAlmostEqual(cost, 61.20, places=2)

        quote = Quote("Bob Johnson", "Premium", "New York", True, False)
        cost = quote.calculate_cost()
        self.assertAlmostEqual(cost, 60.00, places=2)

        quote = Quote("Alice Johnson", "Basic", "Texas", False, True)
        cost = quote.calculate_cost()
        self.assertAlmostEqual(cost, 30.00, places=2)

if __name__ == '__main__':
    unittest.main()
