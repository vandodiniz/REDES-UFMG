sags_ordenados = []
sags_usados = []

def myFunc(e):
        return e['OCORRENCIAS']

SAGS = ['A','A','A', 'B','B','C', 'D','D','D','D']

for auth in SAGS:
    if auth not in sags_usados:
        aux = {}
        aux['SAG'] = auth
        aux['OCORRENCIAS'] = SAGS.count(auth)
        sags_ordenados.append(aux)
        sags_usados.append(auth)
    
sags_ordenados.sort(key=myFunc, reverse=True)
print(sags_ordenados)
