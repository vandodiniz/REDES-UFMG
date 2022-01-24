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

#REQUISITA UM JOGO ESPECIFICO
def Analisa_Jogo(type):
     #ENVIO
    entrada = json.dumps({"type": "getcannons", "auth": SAG}).encode('utf-8')
    client.sendto(entrada, ADDR) 

    #RESPOSTA
    saida = client.recv(bufferSize, 0)
    resposta = json.loads(saida.decode('utf-8'))
    print(resposta)
    if type == 'auth':
        SAGS.append = (resposta['auth'])
    elif type == 'cannons':
        CANNONS.append = (resposta['cannons'])

# REQUISITA OS 100 MELHORES JOGOS DE UM TIPO
def Analisa_Conjunto(type): 

    #ENVIO
    if type == 'sunk':
        entrada = json.dumps({ "ranking": "sunk", "start": 1, "end": 100}).encode('utf-8')
    elif type == 'escaped':
        entrada = json.dumps({ "ranking": "escaped", "start": 1, "end": 100}).encode('utf-8')

    client.sendto(entrada, ADDR) 

    #RESPOSTA
   
    saida = client.recv(bufferSize, 0)
    resposta = json.loads(saida.decode('utf-8'))
    print(resposta)
    game_ids = (resposta['game_ids'])
    return game_ids

# ANALISE 1 
def myFunc(e):
        return e['OCORRENCIAS']

def Immortals(game_ids):
    sags_ordenados = []
    sags_usados = []
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
    return sags_ordenados

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

SAGS = []
CANNONS = []

if COMANDO == 1:
    game_ids = Analisa_Conjunto('sunk')
    for id in game_ids:
        Analisa_Jogo('sunk')
    sags_ordenados = Immortals()

if COMANDO == 2:
    game_ids = Analisa_Conjunto('escaped')
    for id in game_ids:
        Analisa_Jogo('escaped')
    #sags_ordenados = Immortals()






    
        