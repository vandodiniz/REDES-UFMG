import socket
import json
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

client.connect(('152.67.55.32', 8080))  

#REQUISITA UM JOGO ESPECIFICO
def Analisa_Jogo(type, id):
    #ENVIO
    entrada = f"GET /api/game/{id} HTTP/1.1\r\nHost: '{url}'\r\n\r\n".encode('utf-8')
    client.send(entrada)  

    #RESPOSTA
    saida = client.recv(4096, 0)
    resposta = (saida.decode("utf-8"))
    
    #MANIPULANDO A RESPOSTA
    cont = 0
    for letra in resposta:
        if letra == '{':
            resposta = resposta[cont:]
            break
        else:
            cont+=1
    resposta = json.loads(resposta)
   
    #SALVANDO AS INFORMAÇÕES UTEIS
    if type == 'sunk':
        SAGS.append(resposta['game_stats']['auth'])
    elif type == 'escaped':
        CANNONS.append(resposta['game_stats']['cannons'])
    
# REQUISITA OS 100 MELHORES JOGOS DE UM TIPO
def Analisa_Conjunto(type): 

    #ENVIO
    if type == 'sunk':
        entrada = f"GET /api/rank/sunk?start=1&end=100 HTTP/1.1\r\nHost: '{url}'\r\n\r\n".encode('utf-8')
    elif type == 'escaped':
        entrada = f"GET /api/rank/escaped?start=1&end=100 HTTP/1.1\r\nHost: '{url}'\r\n\r\n".encode('utf-8')

    client.send(entrada) 
    #RESPOSTA
    saida = client.recv(4096, 0)
    resposta = (saida.decode("utf-8"))

    #MANIPULANDO A RESPOSTA
    cont = 0
    for letra in resposta:
        if letra == '{':
            resposta = resposta[cont:]
            break
        else:
            cont+=1
    resposta = json.loads(resposta)

    #SALVANDO AS INFORMAÇÕES UTEIS
    game_ids = (resposta['game_ids'])
    return game_ids


def ordena(e):
        return e['OCORRENCIAS']
    
# ANALISE 1
def Immortals():
    sags_ordenados = []
    sags_usados = []
    
    for auth in SAGS:
        if auth not in sags_usados:
            aux = {}
            aux['SAG'] = auth
            aux['OCORRENCIAS'] = SAGS.count(auth)
            sags_ordenados.append(aux)
            sags_usados.append(auth)
    
    sags_ordenados.sort(key=ordena, reverse=True)
    return sags_ordenados

# ANALISE 2
def Top_Meta():
    #transformando as disposições de canhoes em números:
    metas = []
    for cannons in CANNONS:
        p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = 0
        for coordenada in cannons:
            if coordenada[0] == 1:
                p1 += 1
            elif coordenada[0] == 2:
                p2 += 1
            elif coordenada[0] == 3:
                p3 += 1
            elif coordenada[0] == 4:
                p4 += 1
            elif coordenada[0] == 5:
                p5 += 1
            elif coordenada[0] == 6:
                p6 += 1
            elif coordenada[0] == 7:
                p7 += 1
            elif coordenada[0] == 8:
                p8 += 1
        lista_aux = [p1,p2,p3,p4,p5,p6,p7,p8]
        string_ints = [str(int) for int in lista_aux]
        numero = ''.join(string_ints)
        metas.append(numero)
    
    #contando a ocorrencia de cada numero:
    metas_ordenados = []
    metas_usados = []
    
    for meta in metas:
        if meta not in metas_usados:
            aux = {}
            aux['META'] = meta
            aux['OCORRENCIAS'] = metas.count(meta)
            metas_ordenados.append(aux)
            metas_usados.append(meta)
    
    metas_ordenados.sort(key=ordena, reverse=True)
    return metas_ordenados


#DEFININDO AS ESPECIFICAÇÕES DO SERVIDOR E PEGANDO AS INFORMAÇÕES DO TECLADO
dados = sys.argv
url = dados[1]
aux = url.split(':')
IP = aux[0]
PORT = int(aux[1])
COMANDO = int(dados[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

SAGS = []
CANNONS = []

#CONECTANDO COM O SERVIDOR
try:
    client.connect((IP, PORT))
except:
    print('Erro a conectar com o servidor!')
    quit()

#ANALISES
if COMANDO == 1:
    game_ids = Analisa_Conjunto('sunk')
    for id in game_ids:
        Analisa_Jogo('sunk', id)
    sags_ordenados = Immortals()

    cont = 1
    for ranking in sags_ordenados:
        print(f'{cont}. {ranking}')
        cont+=1
    

elif COMANDO == 2:
    game_ids = Analisa_Conjunto('escaped')
    for id in game_ids:
        Analisa_Jogo('escaped', id)
    metas_ordenados = Top_Meta()

    cont = 1
    for ranking in metas_ordenados:
        print(f'{cont}. {ranking}')
        cont+=1

client.close()
