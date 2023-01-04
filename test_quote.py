import unittest
import uuid
from quote import Quote


class TestQuote(unittest.TestCase):
    def test_calculate_cost(self):
        quote = Quote("John Smith", "Basic", "CA", True, True)
        cost = quote.calculate_cost()
        self.assertAlmostEqual(cost, 40.80, places=2)

        quote = Quote("Jane Doe", "Premium", "CA", True, True)
        cost = quote.calculate_cost()
        self.assertAlmostEqual(cost, 61.20, places=2)

        quote = Quote("Bob Johnson", "Premium", "NY", True, False)
        cost = quote.calculate_cost()
        self.assertAlmostEqual(cost, 60.00, places=2)

        quote = Quote("Alice Johnson", "Basic", "TX", False, True)
        cost = quote.calculate_cost()
        self.assertAlmostEqual(cost, 30.00, places=2)

    def test_validations(self):
        # Test coverage_type validation
        with self.assertRaises(ValueError):
            Quote("John Smith", "Invalid", "CA", True, True)

        # Test name validation
        with self.assertRaises(ValueError):
            Quote(123, "Basic", "CA", True, True)

        # Test state validation
        with self.assertRaises(ValueError):
            Quote("John Smith", "Basic", "California", True, True)

        # Test has_pet validation
        with self.assertRaises(ValueError):
            Quote("John Smith", "Basic", "CA", "yes", True)

        # Test flood_coverage validation
        with self.assertRaises(ValueError):
            Quote("John Smith", "Basic", "CA", True, "yes")

        # Test uuid generation
        quote = Quote("John Smith", "Basic", "CA", True, True)
        self.assertIsInstance(quote.uuid, uuid.UUID)


if __name__ == '__main__':
    unittest.main()
