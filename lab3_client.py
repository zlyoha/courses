# Программа клиента для отправки приветствия серверу и получения ответа
# Согласно PEP8 "import *" рекомендуют не использовать, а указывать явно, доводить до такого вида или не паранойить?
import argparse
import json
from socket import socket, AF_INET, SOCK_STREAM

message = 'Привет, сервер!'


def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('address', nargs='?', default='localhost', help='server address')
    parser.add_argument('port', nargs='?', default=7777, help='server port')
    params = parser.parse_args()
    print(params)
    return params


def presence():
    pass


# msg = { "msg": 'Привет, сервер, как дела?'}
def send_to_server(msg):
    params = get_params()
    print(params.address, params.port)
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect((params.address, params.port))  # Соединиться с сервером
        client_socket.send(json.dumps(msg).encode('utf-8'))
        data = client_socket.recv(1000000)
        print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')


def get_from_server():
    pass


def handle_input():
    pass


if __name__ == '__main__':
    send_to_server({'action': 'Привет, сервер!'})
