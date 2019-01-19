import argparse
import select
import json
import time
from socket import *

import logs.server_log_config
from logs.log_decorator import log

logger = logs.server_log_config.config_logger()

# I know problem about wrong time, that only init on start
data_to_send = {
    "action": "msg",
    "time": time.time(),
    "chatname": "default",
    "from": "server",
    "message": "Hello"
}

chats_users = {"chatname": ["username"]}


def add_to_chat(chatname, username):
    try:
        if username not in chats_users["chatname"]:
            chats_users["chatname"].append(username)
            logger.info(f'User {username} added to chat {chatname}')
    except KeyError:
        logger.info(f'User {username} created chat {chatname}')
        chats_users["chatname"] = [username]


def data_to_dict(encoded_data):
    return json.loads(encoded_data.decode('utf-8'))


@log
def dict_to_data(decoded_data):
    return json.dumps(decoded_data).encode('utf-8')


@log
def prepare_response(user_message):
    data_to_send["message"] = f"Hello {user_message['user']['username']}"
    response = dict_to_data(data_to_send)
    logger.debug("check type of response: %s", type(response))
    return response


@log
def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=7777, help='port to listen')
    parser.add_argument('-a', '--address', default='0.0.0.0', help='listening address')
    params = parser.parse_args()
    return params


def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    requests = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            # received_data = sock.recv(100000)
            received_dict = data_to_dict(sock.recv(1024))
            requests[sock] = received_dict
            logger.info('Сообщение: %s было отправлено клиентом: %s', received_dict, sock)
            if received_dict["action"] == "chatmsg":
                add_to_chat(received_dict["to"], received_dict["user"]["username"])
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)

    return requests


def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """

    for sock in w_clients:
        if sock in requests:
            try:
                # Подготовить и отправить ответ сервера
                resp = prepare_response(requests[sock])
                # Эхо-ответ сделаем чуть непохожим на оригинал
                sock.send(resp.upper())
            except:  # Сокет недоступен, клиент отключился
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)


def new_listen_socket():
    params = get_params()
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((params.address, params.port))
    server_socket.listen(5)
    server_socket.settimeout(0.2)
    return server_socket


def server_loop():
    clients = []
    sock = new_listen_socket()
    try:
        while True:
            try:
                conn, addr = sock.accept()
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
    except KeyboardInterrupt:
        logger.warning("Server will be shutdown")


if __name__ == '__main__':
    server_loop()
