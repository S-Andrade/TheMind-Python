import threading
import time
import socket
import sys
import random
import re

def gaze(conn, addr, id):

    print(id)
    print(f'Connected by {addr}')
    with conn:
        while True:
            msg = conn.recv(1024)

            print(msg)

            words = re.findall(r'[A-Z][a-z]*', msg.decode())
            target = words[-1]



def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("0.0.0.0", 50009))
            server_socket.listen()
            print(f'Server listening')
        except Exception as e:
            raise

        for i in range(2):
            conn, addr = server_socket.accept()
            first = conn.recv(1024)
            first = first.decode()
            player_id = ''.join(x for x in first if x.isdigit())
            threading.Thread(target=gaze, args=(conn, addr, player_id, )).start()

    hi = False


main()