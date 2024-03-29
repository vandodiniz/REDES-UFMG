import socket
import json
import sys

#REQUISITA UM JOGO ESPECIFICO
def Analisa_Jogo(type, id):
    #ENVIO
    entrada = f"GET /api/game/{id} HTTP/1.1\r\nHost: {IP}\r\n\r\n".encode('utf-8')
    client.send(entrada)  

    #RESPOSTA
    while True:
        buf = client.recv(4096)
        if not buf:
            break
        saida = buf
    resposta = saida.decode('utf-8')
    
    #TRATANDO A REPOSTA CASO NECESSARIO
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
        SUNK.append(resposta['game_stats']['score']['sunk_ships'])
    elif type == 'escaped':
        CANNONS.append(resposta['game_stats']['cannons'])
        ESCAPED.append(resposta['game_stats']['score']['escaped_ships'])

# REQUISITA OS 100 MELHORES JOGOS DE UM TIPO
def Analisa_Conjunto(type): 

    #ENVIO
    if type == 'sunk':
        entrada = f"GET /api/rank/sunk?start=1&end=100 HTTP/1.1\r\nHost: {url}\r\n\r\n".encode('utf-8')
    elif type == 'escaped':
        entrada = f"GET /api/rank/escaped?start=1&end=100 HTTP/1.1\r\nHost: {url}\r\n\r\n".encode('utf-8')

    client.send(entrada) 

    #RESPOSTA:
    while True:
        buf = client.recv(4096)
        if not buf:
            break
        saida = buf
    resposta = saida.decode('utf-8')
    
    #TRATANDO A REPOSTA CASO NECESSARIO:
    cont = 0
    for letra in resposta:
        if letra == '{':
            resposta = resposta[cont:]
            break
        else:
            cont+=1

    resposta = json.loads(resposta)

    #SALVANDO AS INFORMAÇÕES UTEIS:
    game_ids = (resposta['game_ids'])
    return game_ids


def ordena(e):
        return e['OCORRENCIAS']

def ordena2(e):
        return e['MEDIA']
    
# ANALISE 1
def Immortals():
    sags_ordenados = []
    sags_usados = []
    
    # calculando quantas ocorrencias cada SAG teve
    for auth in SAGS:
        if auth not in sags_usados:
            aux = {}
            aux['SAG'] = auth
            aux['OCORRENCIAS'] = SAGS.count(auth)
            sags_ordenados.append(aux)
            sags_usados.append(auth)

    sags_ordenados.sort(key=ordena, reverse=True)
    
    # lista auxiliar para calcular a media
    for c in range(0,100):
        STATS.append({"SAG": SAGS[c], "SUNK": SUNK[c]})

    # adicionando a media de cada SAG
    for elemento in sags_ordenados:
        soma = 0
        for c in STATS:
            if elemento['SAG'] == c['SAG']:
                soma += c['SUNK']
        media = soma/elemento['OCORRENCIAS']
        elemento['MEDIA'] = media

    return sags_ordenados

# ANALISE 2
def Top_Meta():
    #transformando as disposições de canhoes em números:
    metas = []
    for cannons in CANNONS:
        c1 = c2 = c3 = c4 = c5 = 0
        for coordenada in cannons:
            if coordenada[1] == 0:
                c1 += 1
            elif coordenada[1] == 1:
                c2 += 1
            elif coordenada[1] == 2:
                c3 += 1
            elif coordenada[1] == 3:
                c4 += 1
            elif coordenada[1] == 4:
                c5 += 1

        carreiras = [c1,c2,c3,c4,c5]
        meta = []
        for c in range (0,8):
            numero = carreiras.count(c+1)
            meta.append(numero)
        meta = [str(int) for int in meta]
        meta = ''.join(meta)
        metas.append(meta)

    #contando a ocorrencia de cada meta:
    metas_ordenados = []
    metas_usados = []
    
    for meta in metas:
        if meta not in metas_usados:
            aux = {}
            aux['META'] = meta
            aux['OCORRENCIAS'] = metas.count(meta)
            metas_ordenados.append(aux)
            metas_usados.append(meta)
    
    # lista auxiliar para calcular a media
    for c in range(0,100):
        STATS.append({"META": metas[c], "ESCAPED": ESCAPED[c]})

    # adicionando a media de cada meta
    for elemento in metas_ordenados:
        soma = 0
        for c in STATS:
            if elemento['META'] == c['META']:
                soma += c['ESCAPED']
        media = soma/elemento['OCORRENCIAS']
        elemento['MEDIA'] = media

    metas_ordenados.sort(key=ordena2)

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
SUNK = []
ESCAPED = []
STATS = []

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
        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client.connect((IP, PORT))
        Analisa_Jogo('sunk', id)
        
    sags_ordenados = Immortals()
    for ranking in sags_ordenados:
        print(f'{ranking["SAG"]}, {ranking["OCORRENCIAS"]},  {ranking["MEDIA"]}  \n')
    

elif COMANDO == 2:
    game_ids = Analisa_Conjunto('escaped')
    for id in game_ids:
        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client.connect((IP, PORT))
        Analisa_Jogo('escaped', id)

    metas_ordenados = Top_Meta()
    for ranking in metas_ordenados:
        print(f'{ranking["META"]}, {ranking["MEDIA"]}  \n')

client.close()
