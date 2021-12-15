import socket
import struct
import json

def entrada():
    while True:
        entrada = input('Digite sua entrada: ')
        dados = entrada.split(' ')
        try:
            s = dados[0]
            p = int(dados[1])
            n = '2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224'
            break
        except:
            print('Entrada inválida! Tente no seguinte formato: "SERVER PORTA SAG"')
            
    while s != VALID_SERVER:
        entrada = input('Server inválidado! Digite novamente: ')
        dados = entrada.split(' ')
        s = dados[0]
        p = int(dados[1])
        n = '2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224'
        
    while p not in VALID_PORTS:
        entrada = input('Porta inválidada! Digite novamente: ')
        dados = entrada.split(' ')
        s = dados[0]
        p = int(dados[1])
        n = '2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224'

    info =[s,p,n]
    return info

def authreq(sag):
    #ENVIO
    entrada = json.dumps({"type": "authreq", "auth": sag}).encode('utf-8')
    client.sendto(entrada, RIVER[c])
        
    #RESPOSTA
    try:
        saida = client.recv(bufferSize, 0)
        resposta = json.loads(saida.decode('utf-8'))
        print(resposta)
        return 0
    except:
        print('Erro de transmissão')
        return 1

def quit(sag):
    #ENVIO
    entrada = json.dumps({"type": "authreq", "auth": sag}).encode('utf-8')
    client.sendto(entrada, RIVER[0])
    print('Jogo finalizado com sucesso!')

#DEFININDO AS ESPECIFICAÇÕES DO SERVIDOR E PEGANDO AS INFORMAÇÕES DO TECLADO
bufferSize = 4096
RIVER = [0,0,0,0]
VALID_PORTS = [52221,52222,52223,52224]
VALID_SERVER = 'bd20212.dcc023.2advanced.dev'

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for c in range(0,4):
    dados = entrada()
    SERVER = dados[0]
    PORT = int(dados[1])
    SAG = dados[2]
    
    if PORT == VALID_PORTS[0]:
        RIVER[c]=(SERVER, PORT)
    elif PORT == VALID_PORTS[1]:
        RIVER[c]=(SERVER, PORT)
    elif PORT == VALID_PORTS[2]:
        RIVER[c]=(SERVER, PORT)
    elif PORT == VALID_PORTS[3]:
        RIVER[c]=(SERVER, PORT)

    try:
        client.connect(RIVER[c])   
        client.settimeout(3)
    except:
        print('Erro ao conectar com o servidor! Finalizando o programa')
        print(RIVER[c])
        client.close()
        exit()

    auth = authreq(SAG)
    while auth == 1:
        auth = authreq(SAG)

quit(SAG)

client.close()

#bd20212.dcc023.2advanced.dev 52221 2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224