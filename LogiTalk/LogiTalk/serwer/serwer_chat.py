import json
import time
from datetime import datetime

data_file = open('data.json', 'r')
data_dict = dict(json.load(data_file))

from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('26.123.126.212', 55555))
server_socket.setblocking(False)
server_socket.listen(5)
clients = []

while True:
    time.sleep(0.001)
    try:
        connection, address = server_socket.accept()
        print(f'>>>Підключився клієнт {connection}')

        connection.setblocking(True)
        login = connection.recv(1024).decode()
        print(f'* клієнт логін отримано {login}')

        data_file = open('data.json', 'r')
        data_dict = dict(json.load(data_file))
        data_file.close()
        username = data_dict[login][1]
        connection.send(username.encode())
        print(f'* клієнт username надіслано {username}')

        clients.append([connection, login, username])
        print(f"* Кіента додано: {clients[-1]}")
        connection.setblocking(False)
        for clientt in clients:
            try:
                clientt[0].send(f">>> Підключився({datetime.now().strftime('%H:%M')}): {username} ({login})\n".encode())
                # time.sleep(1)
                # clientt[0].send(f"new_online_{str(clients)}".encode())
                # time.sleep(1)
            except:
                pass

    except : pass

    for client in clients:
        try:
            msg = client[0].recv(1024).decode()
            if msg == '':
                print('exit:', client)
                for clientt in clients:
                    try:
                        clientt[0].send(f">>> вийшов({datetime.now().strftime('%H:%M')}): {client[2]} ({client[1]})\n".encode())
                    except:
                        pass
                clients.remove(client)
            elif msg[0:4] == '/ls(':
                too_user = msg[4:msg.find('): ')]
                msg2 = f'>особисте< від {client[2]} ({client[1]}) тобі: ({datetime.now().strftime('%H:%M')}): {msg[(msg.find('): ')+2)::]}\n'
                for clientt in clients:
                    if clientt[1] == too_user:
                        try:
                            clientt[0].send(msg2.encode())
                            client[0].send(f'>особисте< від тебе до {clientt[2]} ({clientt[1]}) : ({datetime.now().strftime('%H:%M')}): {msg[(msg.find('): ')+2)::]}\n'.encode())
                        except: pass
            else:
                msg2 = f'{client[2]} ({client[1]}) ({datetime.now().strftime('%H:%M')}): {msg}\n'
                print(msg2)
                for clientt in clients:
                    try:
                        clientt[0].send(msg2.encode())
                    except: pass
        except: pass