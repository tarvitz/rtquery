import unittest
from rtquery import _version


class VersionUnitTest(unittest.TestCase):
    def test_version(self):
        self.assertNotEqual(_version.version, '')
