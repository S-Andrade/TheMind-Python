import time
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor (mesmo IP e porta usados no C#)
server_address = ('127.0.0.1', 8080)
client_socket.connect(server_address)

message = f'GazeAtTarget,player0'
client_socket.sendall(message.encode('utf-8'))

time.sleep(5)

message = f'GazeAtTarget,player1'
client_socket.sendall(message.encode('utf-8'))

time.sleep(5)

message = f'SetPosture,player1,fear'
client_socket.sendall(message.encode('utf-8'))

time.sleep(0.3)

message = f'GazeAtTarget,Rplayer1'
client_socket.sendall(message.encode('utf-8'))

time.sleep(0.3)

message = f'GazeAtTarget,Lplayer1'
client_socket.sendall(message.encode('utf-8'))

time.sleep(0.3)

message = f'GazeAtTarget,Rplayer1'
client_socket.sendall(message.encode('utf-8'))

time.sleep(0.3)

message = f'GazeAtTarget,Lplayer1'
client_socket.sendall(message.encode('utf-8'))

time.sleep(0.3)

message = f'SetPosture,player1,neutral'
client_socket.sendall(message.encode('utf-8'))

time.sleep(5)

client_socket.close()