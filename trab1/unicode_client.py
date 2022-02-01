# Cliente p
import socket
from urllib import request

def makeRequest(opt):
    request = ''

    if (opt == 1):
        label = input("Digite um rótulo: ")
        request = 'GET /res=' + str(opt) + '&label=' + label + ' HTTP/1.1\r\n\r\n'
    elif (opt == 2 or opt == 3):
        request = 'GET /res=' + str(opt) + ' HTTP/1.1\r\n\r\n' 
    elif (opt == 4):
        unicodeChar = input('Digite um caracter: ')
        request = 'POST / HTTP/1.1\r\n\r\nunicode=' + unicodeChar
        i = 0
        while True:
            i += 1
            label = input('Digite o rótulo['+ str(i) +'] (Deixe em branco para sair):') 
            if label == '':
                break
            else:
                request += '&label' + str(i) + '=' + label
    else:
        unicodeChar = input('Digite o caracter a ser removido: ')
        request = 'DELETE /unicode=' + unicodeChar + ' HTTP/1.1\r\n\r\n'
    
    return request
    
def main():
    HOST = '127.0.0.1'
    PORT = 8080
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST,PORT)

    try:  
        clientSock.connect(dest)
    except:
        print("Conexão recusada")
    else:
        opt = -1
        while (opt!=0):
            print('\n############################')
            print('\nSelecione um recurso:')
            print('1 - Retornas caracteres de determinado rótulo\n2 - Quantidade de caracteres cadastrados\n3 - Listagem de caracteres e seus rótulos\n4 - Cadastrar caracter\n5 - Remover um caracter\n0 - Finalizar programa')
            opt = int(input('Opção: '))
            
            if (opt>0 and opt<6):
                clientRequest = makeRequest(opt)
                
                clientSock.send(clientRequest.encode())

                msg = clientSock.recv(2048)
                print("Mensagem recebida:\n",msg.decode())
    finally:
        clientSock.close()
        print('Programa finalizado')

main()