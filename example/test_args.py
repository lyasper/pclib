import unittest

import args

class argsTestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_default_args(self):
        def testfun(a =1, b=2, c=3, d=4):
            return (a,b,c,d)
        f = args.default_args(testfun, a=5,b=6,c=7,d=8)
        self.assertEqual('testfun', f.__name__, "fun name doesn't match")
        self.assertEqual(f(), (5,6,7,8), "Default args doesn't work")




if __name__ == '__main__':
    unittest.main()
