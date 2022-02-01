import socket
import os 

endereco = ('', 8080)
servidor_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_sock.bind(endereco)
servidor_sock.listen()

while True:
    conexao_sock, endereco = servidor_sock.accept()
    # conexao_sock.settimout(20)
    print("Conexão com", endereco)
    req = conexao_sock.recv(2048).decode()
    print("Requisicao do cliente:")
    print(req)
    linha1 = req.split("\n")[0]
    print("Linha de requisição:", linha1)
    nome_arq = linha1.split(' ')[1]
    print("Nome do arquivo: ", nome_arq)
    nome_arq = nome_arq.strip('/').strip()
    if nome_arq == '':
        nome_arq = "index.html"
    if os.path.isfile(nome_arq):
        linha_status = "HTTP/1.1 200 OK\r\n\r\n".encode()
        conexao_sock.send(linha_status)
        with open(nome_arq, 'rb') as f:
            chunk = f.read(2048)
            while chunk:
                conexao_sock.send(chunk)
                chunk == f.read(2048)
    else:
        resposta = "HTTP/1.1 404 Not Found\r\n\r\n <h1>Não temos o arquivo solicitado</h1>"
        conexao_sock.send(resposta.encode())
    conexao_sock.close()