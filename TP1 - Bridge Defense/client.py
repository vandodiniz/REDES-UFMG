import socket
import struct
#DEFININDO AS ESPECIFICAÇÕES DO SERVIDOR E PEGANDO AS INFORMAÇÕES DO TECLADO
bufferSize = 4096
for c in range(0,4):
    entrada = input('Digite sua entrada: ')
    dados = entrada.split(' ')
    SERVER = dados[0]
    PORT = int(dados[1])
    SAG = '2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224'
    if PORT == 52221:
        RIVER = (SERVER, PORT)
    elif PORT == 52222:
        RIVER = (SERVER, PORT)
    elif PORT == 52223:
        RIVER = (SERVER, PORT)
    elif PORT == 52224:
        RIVER = (SERVER, PORT)
    else:
        print('Falha na escolha da porta!')
        exit()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect(RIVER)

    #2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224