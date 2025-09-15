import unittest

# add the parent directory to the system path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.utils.Time import AsTime

class MyTestCase(unittest.TestCase):

    def test_as_time(self):
        t1 = AsTime()
        self.assertIsInstance(t1.time, int)
        self.assertGreater(t1.time, 0)

        t2 = AsTime(specific_time_ms=123456789)
        self.assertEqual(t2.time, 123456789)

    def test_as_time_natural_language(self):

        t1 = AsTime(specific_time_ms=123456789)
        natural = t1.natural_language()
        print("Natural language:", natural)


if __name__ == '__main__':
    unittest.main()
