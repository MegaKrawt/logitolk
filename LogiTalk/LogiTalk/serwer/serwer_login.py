import json
import time

data_file = open('data.json', 'r')
data_dict = dict(json.load(data_file))

from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('26.123.126.212', 12345))
server_socket.setblocking(False)
server_socket.listen(5)
clients = []

while True:
    time.sleep(0.001)
    try:
        connection, address = server_socket.accept()
        print (f'Підключився клієнт {connection}')
        connection.setblocking(False)
        clients.append(connection)
    except : pass

    for client in clients:
        try:
            msg = client.recv(1024).decode()
            print(msg)
            if msg == '':
                print('exit:', client)
                clients.remove(client)
            msg = msg.split('&#&')


            if msg[0] == 'logintry':
                print(2)
                if msg[1] in data_dict.keys():
                    if data_dict[msg[1]][0] == msg[2]:
                        print('good')
                        client.send('good'.encode())
                    else:
                        client.send('password no'.encode())
                        print('password no')
                else:
                    client.send('login no'.encode())
                    print('login no')


            if msg[0] == 'createtry':
                if msg[1] in data_dict.keys():
                    client.send('login вже зайнятий'.encode())
                else:
                    data_dict[msg[1]] = [msg[2], msg[3]]
                    data_file.close()
                    data_file = open('data.json', 'w')
                    json.dump(data_dict, data_file, ensure_ascii=False, indent=2)
                    data_file.close()
                    data_file = open('data.json', 'r')
                    data_dict = dict(json.load(data_file))
                    print(data_dict)
                    print('good')
                    client.send('good'.encode())

            if msg[0] == 'rename':
                data_dict[msg[1]][1] = msg[2]
                data_file.close()
                data_file = open('data.json', 'w')
                json.dump(data_dict, data_file, ensure_ascii=False, indent=2)
                data_file.close()
                data_file = open('data.json', 'r')
                data_dict = dict(json.load(data_file))
                print(data_dict)
                print('good')
                client.send('good'.encode())





        except: pass
