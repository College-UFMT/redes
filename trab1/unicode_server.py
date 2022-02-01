import re
import socket

# Splits a message and returns its value on request's path
def splitMessage(message):
    message = message.split('=')
    message = message[1]
    return message

# Splits new unicode from its labels and returns them
def splitPostUnicode(msg):
    msg = msg.split('&',1)
    
    unicode = msg[0]
    unicode = unicode.split('=')
    unicode = unicode[1]
    msg[1] = msg[1].split('&')

    return unicode, msg[1]
    
# Flips UnicodeDict (codes become keys)
def flipUnicode(unicodeDict):
    flipped = {}
    for key, code in unicodeDict.items():
        for c in code:
            if c not in flipped:
                flipped[c] = [key]
            else:
                flipped[c].append(key)

    return flipped

# 1 - Searches unicode dictionary by label and returns its values
def searchLabel(path, unicodeDict):
    label = path.split('&')
    label = splitMessage(label[1])
    
    labelList = ''
    for key, code in unicodeDict.items():
        if label == key:
            for c in code:
                labelList += c + '\n'
            break
 
    return labelList

# 2 - Returns the length of unicode dictionary 
def getDictLenght(unicodeDict):
    dictLength = 0
    for key in unicodeDict.keys():
        dictLength += len(unicodeDict[key])

    return str(dictLength)

# 3 - Returns unicodes and their respective labels
def getUnicodeList(unicodeDict):
    
    flippedDict = flipUnicode(unicodeDict)
    unicodeList = ''
    for code, label in flippedDict.items():
        unicodeList += code + '\nRotulo(s):\n'
        for l in label:
            unicodeList += l + '\n'
        unicodeList += '\n'
    
    return unicodeList

# 4 - Adds a new unicode with its respectives labels
def addUnicode(path,unicodeDict):
    unicode, labelItems = splitPostUnicode(path)
    labelList = []

    for l in range (0,len(labelItems)):
        labelList.append(splitMessage(labelItems[l]))

    repeatedLabel = []
    dictLabel = list(unicodeDict.keys())
    
    for l in labelList:
        if (l not in dictLabel):
            unicodeDict[l] = [unicode]
        else:
            if (unicode not in unicodeDict.get(l)):
                unicodeDict[l].append(unicode)
            else:
                repeatedLabel.append(l)

    return labelList, repeatedLabel

# 5 - Removes an unicode from unicodes dictionary
def removeUnicode(path,unicodeDict):
    unicode = splitMessage(path)
    
    remCount = 0 
    for label,code in unicodeDict.items():
        if (unicode in code):
            unicodeDict[label].remove(unicode)
            remCount += 1
    
    return remCount

def makeResponse(request,unicodeDict):
    if (unicodeDict == ''):
        return 'HTTP/1.1 404 Not Found\r\n\r\nLista de caracteres não existe'
    serverResponse = 'HTTP/1.1 '
    
    request = request.split()
    method = request[0]
    path = request[1]

    if (method == 'GET'):
        if (path.find('&') != -1):
            labelList = searchLabel(path, unicodeDict)
            if labelList:
                serverResponse += '200 OK\r\n\r\n' + labelList
            else:
                serverResponse += '404 Not Found\r\n\r\nRótulo não encontrado'
        else:
            opt = path[-1]
            if (opt == '2'):
                serverResponse += '200 OK\r\n\r\n' + getDictLenght(unicodeDict) + ' caracter(es) cadastrado(s)'
            else:
                serverResponse += '200 OK\r\n\r\n' + getUnicodeList(unicodeDict)
    
    elif (method == 'POST'):
        labelList, repeatedLabel = addUnicode(request[3],unicodeDict)
        if (len(labelList) == len(repeatedLabel)):
            serverResponse += '400 Bad Request\r\n\r\nO caracter já existe para os rótulos selecionados'
        else:
            serverResponse += '200 OK\r\n\r\nCaracter cadastrado com sucesso\n(Rótulo(s) repetido(s): ' + str(repeatedLabel) + ')'
    
    else:
        remCount = removeUnicode(path, unicodeDict)
        if remCount == 0:
            serverResponse += '404 Not Found\r\n\r\nUnicode não encontrado'    
        else:
            serverResponse += '200 OK\r\n\r\nCaracter removido com sucesso\n(' + str(remCount) + ' rótulo(s) associado(s) )'

    
    return serverResponse

def main():
    # Unicodes dictionary
    unicodeDict = {
        'nuvem': ['U+2601','U+26C8','U+1F325','U+1F327','U+1F328','U+1F32A'],
        'clima': ['U+1F327','U+2600','U+2601','U+26C7','U+1F305','U+1F321','U+1F325','U+1F32A','U+1F32C'],
        'coracao': ['U+2665','U+2763','U+2766','U+1F0B1','U+1F394','U+1F496'],  
        'telefone': ['U+2121','U+260E','U+2706','U+1F57C','U+1F57D','U+1F57F'],
        'computador': ['U+1F4BB','U+1F5A5','U+1F5A7','U+1F5B3'],
        'seta': ['U+02C2','U+02C3','U+02F0','U+02F1','U+2195']     
    }

    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind(('',8080))
    serverSock.listen()

    print('Servidor associado à porta: ', serverSock.getsockname()[1])
    
    connSock, address = serverSock.accept()
    while(1):
        print('Conectado a ', address)
        
        cli_request = connSock.recv(2048).decode()
        if (cli_request == ''):
            print('Cliente desconectado')
            exit()

        print('Request:\n',cli_request)

        serverResponse = makeResponse(cli_request,unicodeDict)

        connSock.send(serverResponse.encode())

    serverSock.close()

main()