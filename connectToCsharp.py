import socket

# Cria um socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor (mesmo IP e porta usados no C#)
server_address = ('127.0.0.1', 8080)
client_socket.connect(server_address)

try:
    # Envia uma mensagem para o servidor
    message = 'Speak,player2,Boa! Passamos um nivel!'
    client_socket.sendall(message.encode('utf-8'))

    # Recebe a resposta do servidor
    response = client_socket.recv(1024)
    print('Resposta do servidor:', response.decode('utf-8'))

finally:
    # Fecha o socket
    client_socket.close()