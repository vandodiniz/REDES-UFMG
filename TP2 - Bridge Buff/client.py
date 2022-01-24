import socket
import json

def entrada():
    while True:
        entrada = input('Digite sua entrada: ')
        dados = entrada.split(' ')
        try:
            server = dados[0]
            port = int(dados[1])
            analyse = int(dados[2])
            break
        except:
            print('Entrada inválida! Tente no seguinte formato: "SERVER PORTA ANÁLISE"')

    info =[server,port,analyse]
    return info

#DEFININDO AS ESPECIFICAÇÕES DO SERVIDOR E PEGANDO AS INFORMAÇÕES DO TECLADO
bufferSize = 4096   
dados = entrada()

SERVER = dados[0]
PORT = int(dados[1])
COMANDO = dados[2]
ADDR = (SERVER, PORT)

#CONECTANDO COM O SERVIDOR
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    client.connect(ADDR)
except:
    print('Erro a conectar com o servidor!')
    quit()

# ANALISA UM ID INDIVIDUAL

SAGS = []
CANNONS = []

def Analisa_Jogo(id, type):
     #ENVIO
    entrada = json.dumps({"type": "getcannons", "auth": SAG}).encode('utf-8')
    client.sendto(entrada, ADDR) 

    #RESPOSTA
   
    saida = client.recv(bufferSize, 0)
    resposta = json.loads(saida.decode('utf-8'))
    print(resposta)
    if type == 'auth':
        SAGS.append = (resposta['auth'])
    if type == 'cannons':
        CANNONS.append = (resposta['cannons'])

# REQUISITA OS 100 MELHORES JOGOS 

def Analisa_Conjunto(): 

    #ENVIO
    entrada = json.dumps({"type": "getcannons", "auth": SAG}).encode('utf-8')
    client.sendto(entrada, ADDR) 

    #RESPOSTA
   
    saida = client.recv(bufferSize, 0)
    resposta = json.loads(saida.decode('utf-8'))
    print(resposta)
    game_ids = (resposta['game_ids'])
    return game_ids


# ANALISE 1 

sags_ordenados = []
sags_usados = []

def myFunc(e):
        return e['OCORRENCIAS']

def Immortals(game_ids):
    for id in game_ids:
        Analisa_Jogo(id)

    for auth in SAGS:
        if auth not in sags_usados:
            aux = {}
            aux['SAG'] = auth
            aux['OCORRENCIAS'] = SAGS.count(auth)
            sags_ordenados.append(aux)
            sags_usados.append(auth)
    
    sags_ordenados.sort(key=myFunc, reverse=True)
    print(sags_ordenados)

# ANALISE 2


    
        