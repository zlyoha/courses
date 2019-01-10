#В Python 3 все строки - строки юникода
s = 'Python'

# Отдельный тип - строка байтов
bs = b'Python'

# Отдельный тип - bytearray - изменяемая строка байтов
ba = bytearray(bs)

#Преобразования между строками
s2 = bs.decode('cp1251')    # из байт-строки в юникод-строку
bs2 = s.encode('koi8-r')    # из юникод-строки в строку байтов
ba2 = bytearray(s, 'utf-8') # из юникод-строки в массив байтов

#TCP-server
# Программа сервера для получения приветствия от клиента и отправки ответа
from socket import *
import time

s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
s.bind(('', 8007))                # Присваивает порт 8888
s.listen(5)                       # Переходит в режим ожидания запросов;
                                  # Одновременно обслуживает не более
                                  # 5 запросов.
while True:
    client, addr = s.accept()
    data = client.recv(1000000)
    print('Сообщение: ', data.decode('utf-8'), ', было отправлено клиентом: ', addr)
    msg = 'Привет, клиент'
    client.send(msg.encode('utf-8'))
    client.close()
#UDP-server
s = socket(AF_INET, SOCK_DGRAM)           # Определяем UDP-протокол
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Несколько приложений может слушать сокет
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) # Определяем широковещательные пакеты
s.bind(('', 8888))
while True:
	msg = s.recv(128)
	print(msg)

#TCP-client
s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
s.connect(('localhost', 8007))   # Соединиться с сервером
msg = 'Привет, сервер'
s.send(msg.encode('utf-8'))
data = s.recv(1000000)
print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')
s.close()

#or TCP-client
with socket(AF_INET, SOCK_STREAM) as s:
    s.connect(('localhost', 8007))  # Соединиться с сервером
    msg = 'Привет, сервер, как дела?'
    s.send(msg.encode('utf-8'))
    data = s.recv(1000000)
    print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')

#UDP-client
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
while True:
	s.sendto('Запрос на соединение!',('',8888))
