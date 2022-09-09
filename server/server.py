from multiprocessing.connection import Client
import socket
import os
import sys
from _thread import *
from enum import IntEnum


class Type(IntEnum):
    REGISTER = 0
    GET_USERS = 1
    SUBMIT = 2
    FIGHT = 3


def threaded_client(connection):
    connection.send(str.encode('Welcome to the server\n'))
    while True:
        req_type = Type(connection.recv(sys.getsizeof(int))[0])
        data = connection.recv(2048)
        reply = 'Server says: ' + req_type.name + " with data: " + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 6666
ThreadCount = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection...')
ServerSocket.listen(5)

while True:
    client, address = ServerSocket.accept()
    print('Connected to: '+ address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (client, ))
    ThreadCount += 1
    print('Thread Number: '+ str(ThreadCount))

ServerSocket.close()
