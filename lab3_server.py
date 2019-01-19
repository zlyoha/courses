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
import time
from socket import *

import logs.server_log_config
from logs.log_decorator import log

logger = logs.server_log_config.config_logger()

chats_users = {"chatname": ["username"]}

# I know problem about wrong time, that only init on start
data = {
    "action": "msg",
    "time": time.time(),
    "chatname": "default",
    "from": "server",
    "message": "Hello"
}


def add_to_chat(chatname, username):
    try:
        if username not in chats_users["chatname"]:
            chats_users["chatname"].append(username)
            logger.info(f'User {username} added to chat {chatname}')
    except KeyError:
        logger.info(f'User {username} created chat {chatname}')
        chats_users["chatname"] = [username]


@log
def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=7777, help='port to listen')
    parser.add_argument('-a', '--address', default='0.0.0.0', help='listening address')
    params = parser.parse_args()
    return params


def server_loop():
    params = get_params()
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((params.address, params.port))
    server_socket.listen(5)
    try:
        while True:
            client, addr = server_socket.accept()
            request = data_to_dict(client.recv(1000000))
            # print('Сообщение: ', request, ', было отправлено клиентом: ', addr)
            logger.info('Сообщение: %s было отправлено клиентом: %s', request, addr)
            response = prepare_response(request)
            client.send(response)
            logger.info("request: %s %s %s", request["action"], request["to"], request["user"]["username"])
            if request["action"] == "chatmsg":
                add_to_chat(request["to"], request["user"]["username"])
            client.close()
    except KeyboardInterrupt:
        logger.warning("Server will be shutdown")


def data_to_dict(encoded_data):
    return json.loads(encoded_data.decode('utf-8'))


@log
def dict_to_data(decoded_data):
    return json.dumps(decoded_data).encode('utf-8')


@log
def prepare_response(user_message):
    data["message"] = f"Hello {user_message['user']['username']}"
    response = dict_to_data(data)
    logger.debug("check type of response: %s", type(response))
    return response


if __name__ == '__main__':
    server_loop()
