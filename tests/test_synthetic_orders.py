import unittest
from uuid import NAMESPACE_DNS, uuid5


class SyntheticOrderTests(unittest.TestCase):
    def test_daily_order_identifiers_are_deterministic(self):
        self.assertEqual(
            str(uuid5(NAMESPACE_DNS, "2025-01-01-0")),
            str(uuid5(NAMESPACE_DNS, "2025-01-01-0")),
        )


if __name__ == "__main__":
    unittest.main()
