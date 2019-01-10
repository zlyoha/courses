# Программа клиента для отправки приветствия серверу и получения ответа
# Согласно PEP8 "import *" рекомендуют не использовать, а указывать явно, доводить до такого вида или не паранойить?
from socket import socket,AF_INET,SOCK_STREAM

#server_addr =
#port = 
# s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
# s.connect(('localhost', 8007))   # Соединиться с сервером
# msg = 'Привет, сервер, как дела?'
# s.send(msg.encode('utf-8'))
# data = s.recv(1000000)
# print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')
# s.close()


#with socket(AF_INET, SOCK_STREAM) as s:
#     s.connect(('localhost', 8007))  # Соединиться с сервером
#     msg = 'Привет, сервер, как дела?'
#     s.send(msg.encode('utf-8'))
#     data = s.recv(1000000)
#     print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')


def presence():
    pass


#msg = { "msg": 'Привет, сервер, как дела?'}
def send_to_server(msg):
    with socket(AF_INET, SOCK_STREAM) as s:
     s.connect(('localhost', 8007))  # Соединиться с сервером
     s.send(json.dump(msg).encode('utf-8'))
     data = s.recv(1000000)
     print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')


def get_from_server():
    pass


def handle_input():
    pass


# addr
def main(addr, port=7777):
    pass


if __name__ == '__name__':
    main()
