import unittest

class PyjniusTest(unittest.TestCase):

    def test_pyjnius(self):
        from jnius import autoclass
        autoclass('java.lang.System').out.println('Hello world')

if __name__ == '__main__':
    unittest.main()
