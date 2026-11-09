import heapq

def dijkstra_interactivo():
    print("=== ALGORITMO DE DIJKSTRA ===")
    grafo = {}
    
    n_nodos = int(input("Ingrese el número de nodos: "))
    for i in range(n_nodos):
        nodo = input(f"Nombre del nodo {i+1}: ").strip()
        grafo[nodo] = {}
        
    n_aristas = int(input("Ingrese el número total de aristas dirigidas: "))
    print("Ingrese las aristas en el formato: [origen] [destino] [peso] (ej: A B 4)")
    for i in range(n_aristas):
        origen, destino, peso = input(f"Arista {i+1}: ").split()
        peso = float(peso)
        grafo[origen][destino] = peso
        
    inicio = input("Ingrese el nodo de inicio: ").strip()
    
    # Ejecución de Dijkstra
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    pq = [(0, inicio)]
    
    while pq:
        dist_actual, nodo_actual = heapq.heappop(pq)
        
        if dist_actual > distancias[nodo_actual]:
            continue
            
        for vecino, peso in grafo.get(nodo_actual, {}).items():
            distancia = dist_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(pq, (distancia, vecino))
                
    print("\n--- Resultados (Dijkstra) ---")
    print(f"Distancias mínimas desde '{inicio}':")
    for nodo, dist in distancias.items():
        print(f"  A '{nodo}': {dist}")

# Ejecutar función
dijkstra_interactivo()