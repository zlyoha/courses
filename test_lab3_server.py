import unittest

import lab3_server


class TestMessengerServer(unittest.TestCase):
    test_msg = {
        "action": "presence",
        "time": 1547247081.056431,
        "type": "status",
        "user": {
            "status": "online"
        }
    }
    test_data = b'{"action": "presence", "time": 1547247081.056431, "type": "status", "user": {"status": "online"}}'
    test_username = ('127.0.0.1', 38202)

    def test_get_params(self):
        self.assertTrue(lab3_server.get_params())

    def test_dict_to_data(self):
        self.assertEqual(lab3_server.dict_to_data(self.test_msg), self.test_data)

    def test_data_to_dict(self):
        self.assertEqual(lab3_server.data_to_dict(self.test_data), self.test_msg)

    def test_prepare_response(self):
        self.assertIsInstance(lab3_server.prepare_response(self.test_username), bytes)


if __name__ == "__main__":
    unittest.main()
