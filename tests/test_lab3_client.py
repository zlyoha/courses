import time
import unittest

import lab3_client

"""
import datetime
from collections import namedtuple

import unittest

Salary = namedtuple('Salary', ('surname', 'name', 'worked', 'rate'))

def get_salary(line):
    ''' Вычисление зарплаты работника
    '''
    line = line.split()
    if line:
        data = Salary(*line)
        fio = ' '.join((data.surname, data.name))
        salary = int(data.worked) * int(data.rate)
        res = (fio, salary)
    else:
        res = ()
    return res


class TestSalary(unittest.TestCase):

    def test_get_salary_summ(self):
        self.assertEqual(get_salary('Лютиков   Руслан     60    1000'),
                         ('Лютиков Руслан', 60000))

    def test_get_salary_fio(self):
        self.assertEqual(get_salary('Лютиков   Руслан     60    1000')[0],
                         'Лютиков Руслан')

    def test_get_salary_empty(self):
        self.assertEqual(get_salary(''), ('1', '2'))
"""


class TestMessengerClient(unittest.TestCase):
    time = time.time()
    msg = {
        "action": "presence",
        "time": time,
        "type": "status",
        "user": {
            "status": "online"
        }
    }
    default_server_response = "Hello 127.0.0.1"
    def test_get_params(self):
        self.assertTrue(lab3_client.get_params())

    def test_send_to_server(self):
        self.assertEqual(lab3_client.send_to_server(self.msg)["message"], self.default_server_response)


if __name__ == "__main__":
    unittest.main()
