import socket
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

client.connect(('152.67.55.32', 8080))  

#REQUISITA UM JOGO ESPECIFICO
def Analisa_Jogo(type, id):
     #ENVIO
    entrada = f"GET /api/game/{id} HTTP/1.1\r\nHost: 'http://152.67.55.32:8080/swagger'\r\n\r\n".encode('utf-8')
    client.send(entrada)  

    #RESPOSTA

    saida = client.recv(4096, 0)
    respostaa = (saida.decode("utf-8"))
    lista = [] 
    botao = 0
    for letra in respostaa:
        if letra == '{':
            botao = 1
        if botao == 1:
            lista.append(letra)
    resposta = ''.join(lista)
            
    resposta = json.loads(resposta)
    print(resposta)
   
    if type == 'sunk':
        SAGS.append(resposta['game_stats']['auth'])
    elif type == 'escaped':
        CANNONS.append(resposta['cannons'])
    

COMANDO = int(input('Analise; '))
SAGS = []
CANNONS = []

if COMANDO == 1:
    Analisa_Jogo('sunk', 1)
    print(SAGS)

elif COMANDO == 2:
   Analisa_Jogo('escaped',1)
   print(CANNONS)