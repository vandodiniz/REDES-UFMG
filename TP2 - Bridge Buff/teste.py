
CANNONS = [[6,4], [5,4],[5,1],[7,3],[4,2],[5,2],[2,4],[4,0]]
c1 = c2 = c3 = c4 = c5 = 0
for coordenada in CANNONS:
    print(coordenada)
    print(coordenada[1])
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
print(carreiras)
meta = []
for c in range (0,8):
    numero = carreiras.count(c+1)
    meta.append(numero)
meta = [str(int) for int in meta]
meta = ''.join(meta)
print(meta)