"""
Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
  клиент отправляет запрос серверу;
  сервер отвечает соответствующим кодом результата.

Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.

Функции клиента:
  сформировать presence-сообщение;
  отправить сообщение серверу;
  получить ответ сервера;
  разобрать сообщение сервера;
  параметры командной строки скрипта client.py <addr> [<port>]:

addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777.

Функции сервера:
  принимает сообщение клиента;
  формирует ответ клиенту;
  отправляет ответ клиенту;
  имеет параметры командной строки:

-p <port> — TCP-порт для работы (по умолчанию использует 7777);
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).

“action”: “presence” — присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online;
“action”: “prоbe” — проверка присутствия. Сервисное сообщение от сервера для проверки присутствии клиента online;
“action”: “msg” — простое сообщение пользователю или в чат;
“action”: “quit” — отключение от сервера;
“action”: “authenticate” — авторизация на сервере;
“action”: “join” — присоединиться к чату;
“action”: “leave” — покинуть чат.

"""
import argparse
import json
from socket import *

max_clients = 10


def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=7777, help='port to listen')
    parser.add_argument('-a', '--address', default='0.0.0.0', help='listening address')
    params = parser.parse_args(sys.argv[1:])
    return params


def start_server():
    params = get_params()
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((params.address, params.port))
    server_socket.listen(max_clients)

    while True:
        client, addr = server_socket.accept()
        data = client.recv(1000000)
        print('Сообщение: ', json.loads(data.decode('utf-8')), ', было отправлено клиентом: ', addr)
        response = prepare_response()
        client.send(response.encode('utf-8'))
        client.close()


def get_from_client():
    pass


def prepare_response():
    return 'Привет, клиент'


def send_to_client():
    pass


if __name__ == '__main__':
    print(get_params())
    start_server()
