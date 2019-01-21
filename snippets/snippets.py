# В Python 3 все строки - строки юникода
s = 'Python'

# Отдельный тип - строка байтов
bs = b'Python'

# Отдельный тип - bytearray - изменяемая строка байтов
ba = bytearray(bs)

# Преобразования между строками
s2 = bs.decode('cp1251')  # из байт-строки в юникод-строку
bs2 = s.encode('koi8-r')  # из юникод-строки в строку байтов
ba2 = bytearray(s, 'utf-8')  # из юникод-строки в массив байтов

# TCP-server
# Программа сервера для получения приветствия от клиента и отправки ответа
from socket import *

s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
s.bind(('', 8007))  # Присваивает порт 8888
s.listen(5)  # Переходит в режим ожидания запросов;
# Одновременно обслуживает не более
# 5 запросов.
while True:
    client, addr = s.accept()
    data = client.recv(1000000)
    print('Сообщение: ', data.decode('utf-8'), ', было отправлено клиентом: ', addr)
    msg = 'Привет, клиент'
    client.send(msg.encode('utf-8'))
    client.close()
# UDP-server
s = socket(AF_INET, SOCK_DGRAM)  # Определяем UDP-протокол
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Несколько приложений может слушать сокет
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # Определяем широковещательные пакеты
s.bind(('', 8888))
while True:
    msg = s.recv(128)
    print(msg)

# TCP-client
s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
s.connect(('localhost', 8007))  # Соединиться с сервером
msg = 'Привет, сервер'
s.send(msg.encode('utf-8'))
data = s.recv(1000000)
print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')
s.close()

# or TCP-client
with socket(AF_INET, SOCK_STREAM) as s:
    s.connect(('localhost', 8007))  # Соединиться с сервером
    msg = 'Привет, сервер, как дела?'
    s.send(msg.encode('utf-8'))
    data = s.recv(1000000)
    print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')

# UDP-client
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
while True:
    s.sendto('Запрос на соединение!', ('', 8888))

# декораторы
"""
@property
@classmethod
@staticmethod
@wraps
@functools.lru_cache(maxsize=128, typed=False) сохраняет указанное количество результатов вызовов декорируемой функции (мемоизация);
@functools.singledispatch позволяет реализовать функционал одиночной диспетчеризации (single dispatch) — когда работа функции зависит от типа единственного аргумента, можно зарегистрировать несколько коротких функций, каждая из которых обрабатывает свой тип аргумента, а не создавать большое ветвление if..elif..else;
@contextlib.contextmanager формирует менеджер контекста из декорируемой функции;
@abc.abstractmethod служит для указания абстрактного метода (рассмотрим на занятии по ООП);
@atexit.register(func, *args, **kargs) регистрирует функцию, которая должна быть вызвана при завершении приложения;
@login_required в библиотеке Django (модуль django.contrib.auth.decorators) позволяет указать, какие представления (view) должны быть доступны только авторизованным пользователям;
@app.route(“/”) в библиотеке Flask регистрирует функцию представления для обработки указанного url;
декораторы библиотеке PyTest: @pytest.fixture, @pytest.yield_fixture, @pytest.mark.paramertize.

"""


def wrap(func):
    def call(*args, **kwargs):
        return func(*args, **kwargs)

    call.__doc__ = func.__doc__
    call.__name__ = func.__name__
    return call


from functools import wraps


def wrap(func):
    @wraps(func)
    def call(*args, **kwargs):
        return func(*args, **kwargs)

    return call


from functools import wraps
import time


# ---- Декоратор с параметрами, реализованный через класс ----

class Sleep():
    ''' Фабрика декораторов-замедлителей
    '''

    def __init__(self, timeout):
        self.timeout = timeout

    def __call__(self, func):
        ''' Декоратор-замедлитель
        '''

        @wraps(func)
        def decorated(*args, **kwargs):
            ''' Декорированная функция
            '''
            time.sleep(self.timeout)
            res = func(*args, **kwargs)
            print('Function {} was sleeping in class'.format(func.__name__))
            return res

        return decorated

        # Применение декоратора, основанного на классе,


@Sleep(3)  # заключается в создании объекта данного класса
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


print(' -- Использован декоратор, реализованный через класс --')
print('!!! Обратите внимание на то, сколько раз будет вызван декоратор (рекурсия) !!!')
print(factorial(5))

"""
"""
fmt = logging.Formatter(fmt='%(asctime)s %(message)s')
fh = logging.FileHandler(
    filename='logs/calls.log'
)
fh.setFormatter(fmt)
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
calls = logging.getLogger('calls')
calls.addHandler(sh)
calls.addHandler(fh)

# -------- Эхо-сервер, обрабатывающий "одновременно" несколько клиентов -------
#              Обработка клиентов осуществляется функцией select

import select
from socket import socket, AF_INET, SOCK_STREAM


def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)

    return responses


def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """

    for sock in w_clients:
        if sock in requests:
            try:
                # Подготовить и отправить ответ сервера
                resp = requests[sock].encode('utf-8')
                # Эхо-ответ сделаем чуть непохожим на оригинал
                sock.send(resp.upper())
            except:  # Сокет недоступен, клиент отключился
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)


def mainloop():
    """ Основной цикл обработки запросов клиентов
    """
    address = ('', 10000)
    clients = []

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)  # Таймаут для операций с сокетом
    while True:
        try:
            conn, addr = s.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 10
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                write_responses(requests, w, clients)  # Выполним отправку ответов клиентам


print('Эхо-сервер запущен!')
mainloop()

from subprocess import Popen

p_list = []  # Список клиентских процессов

while True:
    user = input("Запустить 10 клиентов (s) / Закрыть клиентов (x) / Выйти (q) ")

    if user == 'q':
        break
    elif user == 's':
        for _ in range(10):
            # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
            # чтобы каждый процесс запускался в отдельном окне консоли
            p_list.append(Popen('python time_client_random.py', shell=True))

        print(' Запущено 10 клиентов')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()

from socket import *

s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
s.connect(('localhost', 8888))  # Соединиться с сервером

while True:  # Постоянный опрос сервера
    tm = s.recv(1024)
    print("Текущее время: %s" % tm.decode('utf-8'))

s.close()
