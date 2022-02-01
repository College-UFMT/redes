import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client_sock.settimeout(10)
    msg = input("Uma mensagem: ")
    client_sock.sendto(msg.encode(), ('127.0.0.1', 5050))
    msg, endereco = client_sock.recvfrom(2048)
    print("Mensagem recebida: ",msg.decode())
except:
    print("Tempo esgotado.")