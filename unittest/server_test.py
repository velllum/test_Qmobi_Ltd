import unittest

from parse import Parse

class TestPrser(unittest.TestCase):

    # test_dic = {
    #     "Валюта_запроса": "USD",
    #     "Сумма_запроса": 1.5
    # }

    def setUp(self):
        self.parse = Parse()
        # self.parse.fields = self.test_dic


    def test_type(self):
        self.assertRaises(TypeError, self.parse._get_dict(), )
        self.assertRaises(TypeError, self.parse._get_response(), )








if __name__ == '__main__':
    unittest.main()