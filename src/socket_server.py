
import socket 
import sys

#Socket params
HOST = ''
PORT = 19000
MAX_PENDING = 10
SHUT_RDWR = socket.SHUT_RDWR

#Create Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind socket with params info 
try:
    server_socket.bind((HOST, PORT))
except socket.error as message:
    print(f'Error while binding socket: {message}')
    sys.exit(1)

print(f'Socket created and binded to [{HOST}, {PORT}]')

#Enable server to accept connections (max. MAX_PENDING pending clients)
server_socket.listen(MAX_PENDING)

print('Socket is able to accept client connections')
