def ordena(e):
        return e['OCORRENCIAS']

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

CANNONS = [[[7, 3], [8, 2], [6, 1], [8, 0], [5, 0], [5, 1], [1, 1], [8, 4]], 
           [[7, 3], [8, 2], [6, 1], [8, 0], [5, 0], [5, 1], [1, 3], [8, 3]], 
           [[7, 3], [8, 3], [6, 1], [3, 1], [8, 0], [6, 0], [5, 0], [4, 3]]]

metas_ordenados = Top_Meta()
print(metas_ordenados)

