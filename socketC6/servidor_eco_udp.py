import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(('',5050))

print('Servidor associado à porta: ', server_sock.getsockname()[1])

while(1):
    msg, endereco = server_sock.recvfrom(2048)
    print('Mensagem de {}: {}'.format(str(endereco), msg.decode()))
    msg = msg.decode().upper()
    server_sock.sendto(msg.encode(), endereco)
server_sock.close()