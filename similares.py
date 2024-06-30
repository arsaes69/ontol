from fuzzywuzzy import fuzz, process
def elementos_similares(listaA, listaB, umbral=50):
    similares = []
    for itemA in listaA:
        for itemB in listaB:
            similitud = fuzz.ratio(itemA, itemB)
            if similitud >= umbral:
                similares.append((itemA, itemB, similitud))
    
    # Filtrar elementos duplicados en la lista resultante
    elementos_comunes = list(set([elem[0] for elem in similares]))
    
    return elementos_comunes

# Ejemplo de uso
listaA = ["pizza", "tomato sauce", "pepperoni", "restaurant"]
listaB = ["pizza", "tomato", "peperone", "restaurant"]

listaC = elementos_similares(listaA, listaB)
print(listaC)
