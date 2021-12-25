import socket
import json
import traceback
VALIDADOR = '2019057195:12142021:713956ac462e3cc9736660c44697d3b6d91ffbe60ee2911114890582c2435f72+2019056890:12142021:d4ae8849f0d2f8ccf163b12a3fcf45908b61c8f2239f3806fe6292f3428a37ce+3933183216bb827a7cdca38687047dd1a191952b1afb1a01bcfd92ade29ae224'
def entrada():
    while True:
        entrada = input('Digite sua entrada: ')
        dados = entrada.split(' ')
        try:
            s = dados[0]
            p = int(dados[1])
            n = VALIDADOR
            break
        except:
            print('Entrada inválida! Tente no seguinte formato: "SERVER PORTA SAG"')

    while s != VALID_SERVER:
        entrada = input('Server inválidado! Digite novamente: ')
        dados = entrada.split(' ')
        s = dados[0]
        p = int(dados[1])
        n = VALIDADOR
        
    while p not in VALID_PORTS:
        entrada = input('Porta inválidada! Digite novamente: ')
        dados = entrada.split(' ')
        s = dados[0]
        p = int(dados[1])
        n = VALIDADOR

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
        ESTADO.append(resposta['type'])
        if 'gameover' in ESTADO:
                quit()
        return 0
    except:
        print("ERRO NA AUTENTICACAO")
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
        ESTADO.append(resposta['type'])
    except:
        getcannons()

def getturn(turn, rio, adress):
    #ENVIO
    entrada = json.dumps({"type": "getturn", "auth": SAG, "turn": turn}).encode('utf-8')
    rio.sendto(entrada, adress)

def state(rio, boat, lista_resposta):
        try:
            alcance = 8
            if(turno == 272):
                alcance = 1
            for t in range(0,alcance):
                saida = rio.recv(bufferSize, 0)
                resposta = json.loads(saida.decode('utf-8'))
                if(turno != 272):
                    tam = len(resposta['ships'])
                    for c in range(0,tam):
                        ponte = resposta['bridge']
                        boat[ponte-1].append(resposta['ships'][c])
                        ALL_BOATS.append(resposta['ships'][c])
                    ESTADO.append(resposta['type'])
                else:
                    print('TERMINOOOOOOOOOOOOOOOOOOOOOOU')
                
                if(turno == 272):
                    for II in range(0,8):
                        lista_resposta[II] = resposta
                else:
                    lista_resposta[t] = resposta
            return 0
        except:
            #traceback.print_exc()
            print('erro de transmissão no state')
            return 1

def shot(rio, adress, cannon, id):
    entrada = json.dumps({"type": "shot", "auth": SAG, "cannon": cannon, "id": id}).encode('utf-8')
    rio.sendto(entrada, adress)

    #RESPOSTA
    try:
        saida = rio.recv(bufferSize, 0)
        resposta = json.loads(saida.decode('utf-8'))
        print(resposta)
        #ESTADO.append(resposta['type'])
    except:
        #print('Erro de transmissão')
        shot(rio, adress, cannon, id)

def quit():
    #ENVIO
    entrada = json.dumps({"type": "quit", "auth": SAG}).encode('utf-8')                          
    rio1.sendto(entrada, RIVER[0])
    
    rio1.close()
    rio2.close()
    rio3.close()
    rio4.close()
    print('Jogo finalizado com sucesso!')
    exit()

    #bd20212.dcc023.2advanced.dev 52221

def weakest(_listaBarcos):
    betterBoat = _listaBarcos[0]
    for i in _listaBarcos:
        if i['hull'] == 'frigate':
            return i
        elif i['hull'] == 'destroyer':
            betterBoat = i
        elif betterBoat['hull'] != 'destroyer':
            betterBoat = i
    return betterBoat

def refresh(id, lista):
    for c in lista:
        if c['id'] == id:
            barco = c

    barco['hits'] += 1

    if barco['hull'] == 'frigate':
        if barco['hits'] == 1:
            lista.remove(barco)
            ALL_BOATS.remove(barco)

    elif barco['hull'] == 'destroyer':
        if barco['hits'] == 2:
            lista.remove(barco)
            ALL_BOATS.remove(barco)
            

    elif barco['hull'] == 'battleship':
        if barco['hits'] == 3:
            lista.remove(barco)
            ALL_BOATS.remove(barco)

def analisaRio(lista1, lista2):
    vidas1 = vidas2 = 0
    if len(lista1[p-1]) == len(lista2[p-1]) == 0:
        return 0
    else:
        for barco in lista1[p-1]:
            if barco['hull'] == 'frigate':
                vidas1 += 1
            if barco['hull'] == 'destroyer':
                vidas1 += (2 - barco['hits'])
            if barco['hull'] == 'battleship':
                vidas1 += (3 - barco['hits'])
        
        for barco in lista2[p-1]:
            if barco['hull'] == 'frigate':
                vidas2 += 1
            if barco['hull'] == 'destroyer':
                vidas2 += (2 - barco['hits'])
            if barco['hull'] == 'battleship':
                vidas2 += (3 - barco['hits'])
        
        if vidas1 > vidas2:
            return 1
        else:
            return 2


#DEFININDO AS ESPECIFICAÇÕES DO SERVIDOR E PEGANDO AS INFORMAÇÕES DO TECLADO
bufferSize = 4096
RIVER = [0,0,0,0]
VALID_PORTS = [52221,52222,52223,52224]
VALID_SERVER = 'bd20212.dcc023.2advanced.dev'
VALID_CANNONS = []

ESTADO = []
RIOS = [1,2,3,4]
timeout = 0.5

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
        rio1.settimeout(timeout) 
    elif PORT == VALID_PORTS[1]:
        RIVER[1]=(SERVER, PORT)
        rio2.connect(RIVER[1])
        rio2.settimeout(timeout) 
    elif PORT == VALID_PORTS[2]:
        RIVER[2]=(SERVER, PORT)
        rio3.connect(RIVER[2])
        rio3.settimeout(timeout)
    elif PORT == VALID_PORTS[3]:
        RIVER[3]=(SERVER, PORT)
        rio4.connect(RIVER[3])
        rio4.settimeout(timeout)

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
    getcannons()
    turno = 0

    while turno < 273:
        RESPOSTA_RIO1 = ['', '', '', '', '', '', '', '']
        RESPOSTA_RIO2 = ['', '', '', '', '', '', '', '']
        RESPOSTA_RIO3 = ['', '', '', '', '', '', '', '']
        RESPOSTA_RIO4 = ['', '', '', '', '', '', '', '']
        ALL_BOATS = []
        BOATS_1 = [[],[],[],[],[],[],[],[]]
        BOATS_2 = [[],[],[],[],[],[],[],[]]
        BOATS_3 = [[],[],[],[],[],[],[],[]]
        BOATS_4 = [[],[],[],[],[],[],[],[]]
        error = [0,0,0,0]
        print(f'=============== TURNO {turno} ===============')

        getturn(turno, rio1, RIVER[0])
        getturn(turno, rio2, RIVER[1])
        getturn(turno, rio3, RIVER[2])
        getturn(turno, rio4, RIVER[3])
        
        

        error[0] = state(rio1, BOATS_1, RESPOSTA_RIO1)
        
        while error[0] == 1:
            getturn(turno, rio1, RIVER[0])
            error[0] = state(rio1, BOATS_1, RESPOSTA_RIO1)
        

        print('\nRIO 1:')
        for c in RESPOSTA_RIO1:
            print(c)

        error[1] = state(rio2, BOATS_2, RESPOSTA_RIO2)
        while error[1] == 1:
            getturn(turno, rio2, RIVER[1])
            error[1] = state(rio2, BOATS_2, RESPOSTA_RIO2)
        

        print('\nRIO 2:')
        for c in RESPOSTA_RIO2:
            print(c)

        error[2] = state(rio3, BOATS_3, RESPOSTA_RIO3)
        while error[2] == 1:
            getturn(turno, rio3, RIVER[2])
            error[2] = state(rio3, BOATS_3, RESPOSTA_RIO3)
          

        print('\nRIO 3:')
        for c in RESPOSTA_RIO3:
            print(c)

        error[3] = state(rio4, BOATS_4, RESPOSTA_RIO4)
        while  error[3] == 1:
            getturn(turno, rio4, RIVER[3])
            error[3] = state(rio4, BOATS_4, RESPOSTA_RIO4)
        


        print('\nRIO 4:')
        for c in RESPOSTA_RIO4:
            print(c)

        '''print('NAVIOS DISPONIVEIS:', end=' ')
        print(ALL_BOATS)
        print ('rio 1: ', BOATS_1)
        print ('rio 2: ',BOATS_2)
        print ('rio 3: ',BOATS_3)
        print ('rio 4: ',BOATS_4)'''

        try:
            for x in VALID_CANNONS[0]:  
                tiro = True
                p = x[0]
                    
                if x[1] == 0:
                    r = 1
                    if len(BOATS_1[p-1]) > 0:
                        identificador = weakest(BOATS_1[p-1])['id']
                        refresh(identificador, BOATS_1[p-1])
                    else:
                        tiro = False

                if x[1] == 1:

                    escolha = analisaRio(BOATS_1, BOATS_2)

                    if escolha == 1:
                        identificador = weakest(BOATS_1[p-1])['id']
                        refresh(identificador, BOATS_1[p-1])
                    elif escolha == 2:
                        r = 2
                        identificador = weakest(BOATS_2[p-1])['id']
                        refresh(identificador, BOATS_2[p-1])
                    else:
                        tiro = False
                    
                if x[1] == 2:

                    escolha = analisaRio(BOATS_2, BOATS_3)

                    if escolha == 1:
                        identificador = weakest(BOATS_2[p-1])['id']
                        refresh(identificador, BOATS_2[p-1])
                    elif escolha == 2:
                        r = 2
                        identificador = weakest(BOATS_3[p-1])['id']
                        refresh(identificador, BOATS_3[p-1])
                    else:
                        tiro = False
                    
                    
                if x[1] == 3:

                    escolha = analisaRio(BOATS_3, BOATS_4)

                    if escolha == 1:
                        identificador = weakest(BOATS_3[p-1])['id']
                        refresh(identificador, BOATS_3[p-1])
                    elif escolha == 2:
                        r = 2
                        identificador = weakest(BOATS_4[p-1])['id']
                        refresh(identificador, BOATS_4[p-1])
                    else:
                        tiro = False
                    
                    
                if x[1] == 4:
                    r = 4
                    if len(BOATS_4[p-1]) > 0:
                        identificador = weakest(BOATS_4[p-1])['id']
                        refresh(identificador, BOATS_4[p-1])
                    else:
                        tiro = False
                    
                if tiro == True:
                    print('\nRESPOSTA TIRO:')
                    if r == 1:
                        shot(rio1, RIVER[0], x, identificador)
                    if r == 2:
                        shot(rio2, RIVER[1], x, identificador)
                    if r == 3:
                        shot(rio3, RIVER[2], x, identificador)
                    if r == 4:
                        shot(rio4, RIVER[3], x, identificador)
            
        except:
            print('erro ao atirar')
            
        turno += 1
        # input('proximo round')
        if 'gameover' in ESTADO:
            break

else:
    print('FALHA NA AUTENTICAÇÃO')

#print(f'ESTADO {ESTADO}')
print('Gameover!')
quit()
