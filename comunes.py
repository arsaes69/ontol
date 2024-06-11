def elementos_comunes(listaA, listaB):
    # Convertimos ambas listas a conjuntos para facilitar la comparación
    conjuntoA = set(listaA)
    conjuntoB = set(listaB)
    
    # Usamos la intersección de conjuntos para encontrar elementos comunes
    elementos_comunes = list(conjuntoA & conjuntoB)
    
    return elementos_comunes

# Ejemplo de uso
listaA = ["pizza", "tomato sauce", "pepperoni", "restaurant"]
listaB = ["pizza", "tomato", "peperone", "restaurant"]

listaC = elementos_comunes(listaA, listaB)
print(listaC)
