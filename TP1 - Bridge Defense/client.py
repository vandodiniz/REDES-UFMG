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

def authreq(rio, adress):
    #ENVIO
    entrada = json.dumps({"type": "authreq", "auth": SAG}).encode('utf-8')
    rio.sendto(entrada, adress)
        
    #RESPOSTA
    try:
        saida = rio.recv(bufferSize, 0)
        resposta = json.loads(saida.decode('utf-8'))
        print(resposta)
        return 0
    except:
        print('Erro de transmissão')
        return 1

def getcannons():
    #ENVIO
    entrada = json.dumps({"type": "getcannons", "auth": SAG}).encode('utf-8')
    rio1.sendto(entrada, RIVER[0]) 

    #RESPOSTA
    try:
        saida = rio1.recv(bufferSize, 0)
        resposta = json.loads(saida.decode('utf-8'))
        print(resposta)
        VALID_CANNONS.append(resposta['cannons'])
        return 0
    except:
        print('Erro de transmissão')
        return 1

def getturn(turn):
    #ENVIO
    entrada = json.dumps({"type": "getturn", "auth": SAG, "turn": turn}).encode('utf-8')
    rio1.sendto(entrada, RIVER[0])
    rio2.sendto(entrada, RIVER[1])
    rio3.sendto(entrada, RIVER[2])
    rio4.sendto(entrada, RIVER[3])
    
def state(rio):

        try:
            saida = rio.recv(bufferSize, 0)
            resposta = json.loads(saida.decode('utf-8'))
            print(resposta)
        except:
            print('Erro de transmissão')

def shot(rio, adress, cannon, id):
    entrada = json.dumps({"type": "shot", "auth": SAG, "cannon": cannon, "id": id}).encode('utf-8')
    rio.sendto(entrada, adress)

    #RESPOSTA
    try:
        saida = rio.recv(bufferSize, 0)
        resposta = json.loads(saida.decode('utf-8'))
        print(resposta)
        return 0
    except:
        print('Erro de transmissão')
        return 1

            
def quit():
    #ENVIO
    entrada = json.dumps({"type": "quit", "auth": SAG}).encode('utf-8')                          
    rio1.sendto(entrada, RIVER[0])
    rio2.sendto(entrada, RIVER[1])
    rio3.sendto(entrada, RIVER[2])
    rio4.sendto(entrada, RIVER[3])
    print('Jogo finalizado com sucesso!')
    
#DEFININDO AS ESPECIFICAÇÕES DO SERVIDOR E PEGANDO AS INFORMAÇÕES DO TECLADO
bufferSize = 4096
RIVER = [0,0,0,0]
VALID_PORTS = [52221,52222,52223,52224]
VALID_SERVER = 'bd20212.dcc023.2advanced.dev'
VALID_CANNONS = []

rio1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rio2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rio3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rio4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
auth = list()

for c in range(0,4):
    dados = entrada()
    SERVER = dados[0]
    PORT = int(dados[1])
    SAG = dados[2]
    
    if PORT == VALID_PORTS[0]:
        RIVER[0]=(SERVER, PORT)
        rio1.connect(RIVER[0])
        rio1.settimeout(1) 
    elif PORT == VALID_PORTS[1]:
        RIVER[1]=(SERVER, PORT)
        rio2.connect(RIVER[1])
        rio2.settimeout(1) 
    elif PORT == VALID_PORTS[2]:
        RIVER[2]=(SERVER, PORT)
        rio3.connect(RIVER[2])
        rio3.settimeout(1)
    elif PORT == VALID_PORTS[3]:
        RIVER[3]=(SERVER, PORT)
        rio4.connect(RIVER[3])
        rio4.settimeout(1)

auth.append(authreq(rio1, RIVER[0]))
while auth[0] == 1:
    auth[0] = (authreq(rio1, RIVER[0]))

auth.append(authreq(rio2, RIVER[1]))
while auth[1] == 1:
    auth[1] = (authreq(rio2, RIVER[1]))

auth.append(authreq(rio3, RIVER[2]))
while auth[2] == 1:
    auth[2] = (authreq(rio3, RIVER[2]))
    
auth.append(authreq(rio4, RIVER[3]))
while auth[3] == 1:
    auth[3] = (authreq(rio4, RIVER[3]))

if auth == [0,0,0,0]:
    error = getcannons()
    while error == 1:
        error = getcannons()
    print(VALID_CANNONS)
    turno = 0

    while turno<5:
        
        getturn(turno)

        print('\nRIO 1:')
        for c in range(0,8):
            state(rio1)

        print('\nRIO 2:')
        for c in range(0,8):
            state(rio2)

        print('\nRIO 3:')
        for c in range(0,8):
            state(rio3)
       
        print('\nRIO 4:')
        for c in range(0,8):
            state(rio4)

        for x in VALID_CANNONS[0]:
            
            r = int(input(f'Em qual rio voce quer que o canhão {x} dispare? '))
            identificador = int(input(f'Digite o ID do navio  que o canhão {x} disparará: '))

            if r == 1:
                shot(rio1, RIVER[0], x, identificador)
            if r == 2:
                shot(rio2, RIVER[1], x, identificador)
            if r == 3:
                shot(rio3, RIVER[2], x, identificador)
            if r == 4:
                shot(rio4, RIVER[3], x, identificador)
        turno += 1
quit()

rio1.close()
rio2.close()
rio3.close()
rio4.close()

#bd20212.dcc023.2advanced.dev 52221 2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224