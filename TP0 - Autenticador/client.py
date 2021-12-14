import socket
import struct

#FUNÇÃO PARA VERIFICAR ERRO
def verificaErro(saída):
    if(saída[0]==256):                                                                      #caso o header seja 256, retorna um dos erros a seguir e fecha o programa.
        if saída[1] == 1:
            print('Mensagem de tipo desconhecida enviada ao servidor')
        if saída[1] == 2:
            print('Mensagem de tamanho incompatível enviada ao servidor')
        if saída[1] == 3:
            print('Mensagem com erro em algum parâmetro enviada ao servidor')
        if saída[1] == 4:
            print('Token inválido enviada ao servidor')
        if saída[1] == 5:
            print('Token com caractere não ASCII enviada ao servidor')
        client.close()
        exit()

#DEFININDO AS ESPECIFICAÇÕES DO SERVIDOR E PEGANDO AS INFORMAÇÕES DO TECLADO
bufferSize = 4096                                                                           
entrada = input()
dados = entrada.split(' ')
if len(dados) < 4:
    print('Parâmetros insuficientes!')
    print('EXEMPLO')
    print('auth20212.dcc023.2advanced.dev 51212 vsaa SAA')
    print('auth20212.dcc023.2advanced.dev 51212 vsag SAG')
    exit()
SERVER = dados[0]
PORT = int(dados[1])
COMANDO = dados[2]
ADDR = (SERVER, PORT)

#CONECTANDO COM O SERVIDOR
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect(ADDR)

#REQUISIÇÃO DE AUTENTICADOR INDIVIDUAL[1] E RESPOSTA DE AUTENTICADOR INDIVIDUAL[2] 
def rsaa(mat, id):
    #REQUISIÇÃO DE AUTENTICADOR INDIVIDUAL[1]
    header = 1
    entrada = struct.pack('!HII',header, mat, id)
    client.sendto(entrada , ADDR)

    saida = client.recv(bufferSize,0)
    resposta = struct.unpack('!HII64s', saida)
    verificaErro(resposta)
    print(f'\nresposta do servidor: \n{resposta[1]}:{resposta[2]}:{resposta[3].decode("utf-8")}\n')
    

#VERIFICAÇÃO DE AUTENTICADOR INDIVIDUAL[3] E RESULTADO DO AUTENTICADOR INDIVIDUAL[4]
def vsaa(rsaa):
    #VERIFICAÇÃO DE AUTENTICADOR INDIVIDUAL[3]
    header = 3
    rsaaPartes = rsaa.split(':')
    mat = int(rsaaPartes[0])
    id = int(rsaaPartes[1])
    token = rsaaPartes[2]
    print(token)
    entrada = struct.pack('!HII64s', header, mat, id, token.encode("ascii"))
    client.sendto(entrada , ADDR)

    #RESULTADO DO AUTENTICADOR INDIVIDUAL[4]
    saida = client.recv(bufferSize,0)
    resposta = struct.unpack('!HII64sB', saida)
    verificaErro(resposta)
    print(f'\nresposta do servidor: \n{resposta[4]}\n')
    
#REQUISIÇÃO DE AUTENTICADOR COLETIVO [5] E RESPOSTA DE AUTENTICADOR COLETIVO[6]
def rsag(cont, rsaa1, rsaa2):
    #REQUISIÇÃO DE AUTENTICADOR COLETIVO [5]
    header = 5
    rsaa1Partes = rsaa1.split(':')
    mat1 = int(rsaa1Partes[0])
    id1 = int(rsaa1Partes[1])
    token1 = rsaa1Partes[2]
    rsaa2Partes = rsaa2.split(':')
    mat2 = int(rsaa2Partes[0])
    id2 = int(rsaa2Partes[1])
    token2 = rsaa2Partes[2]
    entrada = struct.pack('!HHII64sII64s',header, cont, mat1, id1, token1.encode("ascii"), mat2, id2, token2.encode("ascii"))
    client.sendto(entrada , ADDR)

    #RESPOSTA DE AUTENTICADOR COLETIVO[6]
    saida = client.recv(bufferSize,0)
    resposta = struct.unpack('!HH72s72s64s', saida)
    verificaErro(resposta)
    print(f'\nresposta do servidor: \n{rsaa1}+{rsaa2}+{resposta[4].decode("utf-8")}\n')

#VERIFICAÇÃO DE AUTENTICADOR COLETIVO[7] E RESULTADO DO AUTENTICADOR COLETIVO[8]
def vsag(rsag):
    #VERIFICAÇÃO DE AUTENTICADOR COLETIVO[7]
    header = 7
    cont = 2
    rsaagPartes = rsag.split('+')
    rsaa1 = rsaagPartes[0]
    rsaa2 = rsaagPartes[1]
    autenticadorColetivo = rsaagPartes[2] 

    rsaa1Partes = rsaa1.split(':')
    mat1 = int(rsaa1Partes[0])
    id1 = int(rsaa1Partes[1])
    token1 = rsaa1Partes[2]
    rsaa2Partes = rsaa2.split(':')
    mat2 = int(rsaa2Partes[0])
    id2 = int(rsaa2Partes[1])
    token2 = rsaa2Partes[2]

    entrada = struct.pack('!HHII64sII64s64s',header, cont, mat1, id1, token1.encode("ascii"), mat2, id2, token2.encode("ascii"), autenticadorColetivo.encode("ascii"))
    client.sendto(entrada , ADDR)

    #RESULTADO DO AUTENTICADOR COLETIVO[8]
    saida = client.recv(bufferSize,0)
    resposta = struct.unpack('!HH72s72s64sB', saida)
    verificaErro(resposta)
    print(f'\nresposta do servidor: \n{resposta[5]}\n')   

if COMANDO == 'rsaa':
    if len(dados) < 5:
        print('Comando RSAA precisa de 5 parâmetros')
        print('Exemplo: auth20212.dcc023.2advanced.dev 51212 rsaa MATRICULA IDENTIFICADOR')
        client.close()
        exit()
    matricula = int(dados[3])
    identificador = int(dados[4])
    rsaa(matricula, identificador)

elif COMANDO == 'vsaa':
    RSAA = dados[3]
    vsaa(RSAA)

elif COMANDO == 'rsag':
    if len(dados) < 6:
        print('Comando RSAG precisa de 6 parâmetros')
        print('Exemplo: auth20212.dcc023.2advanced.dev 51212 rsag CONTADOR SAA1 SAA2')
        client.close()
        exit()
    contador = int(dados[3])
    RSAA1 = dados[4]
    RSAA2 = dados[5]
    rsag(contador, RSAA1, RSAA2)

elif COMANDO == 'vsag':
    RSAG = dados[3]
    vsag(RSAG)

else:
    print('Comando inválido!')
    client.close()
    exit()

client.close()