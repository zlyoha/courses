# Программа клиента для отправки приветствия серверу и получения ответа
# Согласно PEP8 "import *" рекомендуют не использовать, а указывать явно, доводить до такого вида или не паранойить?
import argparse
import json
import time
from socket import socket, AF_INET, SOCK_STREAM

import logs.client_log_config

logger = logs.client_log_config.config_logger()

# message_text = 'Привет, сервер!'
data = {
    "action": "presence",
    "time": time.time(),
    "type": "status",
    "user": {
        "status": "online"
    }
}


def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('address', nargs='?', default='localhost', help='server address')
    parser.add_argument('port', nargs='?', default=7777, help='server port')
    params = parser.parse_args()
    # print(params)
    return params


# msg = { "msg": 'Привет, сервер, как дела?'}
def send_to_server(data_to_send):
    params = get_params()
    # print(params.address, params.port)
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((params.address, params.port))  # Соединиться с сервером
        except ConnectionRefusedError:
            logger.warning('cannot connect to: %s:%s check your server process', params.address, params.port)
            exit(1)
        client_socket.send(json.dumps(data_to_send).encode('utf-8'))
        server_response = client_socket.recv(1000000)
        server_response_decoded = json.loads(server_response.decode('utf-8'))
        # print('Сообщение от сервера: ', server_response_decoded, ', длиной ', len(data), ' байт')
        logger.info('Сообщение от сервера: %s, длиной %d байт', server_response_decoded, len(data))
    return server_response_decoded


if __name__ == '__main__':
    send_to_server(data)
