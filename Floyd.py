def floyd_warshall_interactivo():
    INF = float('inf')
    print("=== ALGORITMO DE FLOYD-WARSHALL ===")
    
    n_nodos = int(input("Ingrese el número de nodos: "))
    nodos = [input(f"Nombre del nodo {i+1}: ").strip() for i in range(n_nodos)]
    
    nodo_a_indice = {nodo: i for i, nodo in enumerate(nodos)}
    dist = [[INF] * n_nodos for _ in range(n_nodos)]
    
    for i in range(n_nodos):
        dist[i][i] = 0
        
    n_aristas = int(input("Ingrese el número de aristas: "))
    print("Ingrese las aristas en el formato: [origen] [destino] [peso] (ej: A B 3)")
    for i in range(n_aristas):
        origen, destino, peso = input(f"Arista {i+1}: ").split()
        peso = float(peso)
        if origen in nodo_a_indice and destino in nodo_a_indice:
            dist[nodo_a_indice[origen]][nodo_a_indice[destino]] = peso
            
    # Algoritmo de Floyd-Warshall
    for k in range(n_nodos):
        for i in range(n_nodos):
            for j in range(n_nodos):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    print("\n--- Matriz de distancias mínimas ---")
    print("     " + "   ".join(nodos))
    for i in range(n_nodos):
        fila_str = f"{nodos[i]}: "
        for j in range(n_nodos):
            val = "INF" if dist[i][j] == INF else str(dist[i][j])
            fila_str += f"{val:>5} "
        print(fila_str)

# Ejecutar función
floyd_warshall_interactivo()