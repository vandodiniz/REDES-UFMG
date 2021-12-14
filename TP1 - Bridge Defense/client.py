import socket
import struct
import json

def authreq(sag, c):
    #ENVIO
    entrada = json.dumps({"type": "authreq", "auth": sag}).encode('utf-8')
    client.sendto(entrada, RIVER[c])
        
    #RESPOSTA
    saida = client.recv(bufferSize, 0)
    resposta = json.loads(saida.decode('utf-8'))
    print(resposta)

#DEFININDO AS ESPECIFICAÇÕES DO SERVIDOR E PEGANDO AS INFORMAÇÕES DO TECLADO
bufferSize = 4096
for c in range(0,4):
    entrada = input('Digite sua entrada: ')
    dados = entrada.split(' ')
    SERVER = dados[0]
    PORT = int(dados[1])
    SAG = '2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224'
    RIVER = [0,0,0,0]
    if PORT == 52221:
        RIVER[c] = (SERVER, PORT)
    elif PORT == 52222:
        RIVER[c] = (SERVER, PORT)
    elif PORT == 52223:
        RIVER[c] = (SERVER, PORT)
    elif PORT == 52224:
        RIVER[c] = (SERVER, PORT)
    else:
        print('Falha na escolha da porta!')
        exit()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect(RIVER[c])
    authreq(SAG, c)

#bd20212.dcc023.2advanced.dev 52221 2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224