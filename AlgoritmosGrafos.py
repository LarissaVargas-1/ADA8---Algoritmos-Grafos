import math
import heapq
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# -------------------------------------------------------------------
# LÓGICA DE ALGORITMOS SOBRE GRAFOS
# -------------------------------------------------------------------

def dijkstra(num_nodes, graph_dict, start_node):
    """
    graph_dict: {u: [(v, weight), ...]}
    """
    distances = {i: float('inf') for i in range(num_nodes)}
    predecessors = {i: None for i in range(num_nodes)}
    distances[start_node] = 0
    
    pq = [(0, start_node)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if current_dist > distances[u]:
            continue
            
        for v, weight in graph_dict.get(u, []):
            distance = current_dist + weight
            if distance < distances[v]:
                distances[v] = distance
                predecessors[v] = u
                heapq.heappush(pq, (distance, v))
                
    return distances, predecessors

def floyd_warshall(num_nodes, adj_matrix):
    dist = [row[:] for row in adj_matrix]
    next_node = [[j if dist[i][j] != float('inf') and i != j else None 
                 for j in range(num_nodes)] for i in range(num_nodes)]
    
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]
                        
    return dist, next_node

def warshall(num_nodes, adj_matrix):
    reach = [[True if adj_matrix[i][j] != float('inf') and adj_matrix[i][j] != 0 
              else (i == j) for j in range(num_nodes)] for i in range(num_nodes)]
    
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
                
    return reach

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            if self.rank[root_i] == self.rank[root_j]:
                self.rank[root_i] += 1
            return True
        return False

def kruskal(num_nodes, edges):
    """
    edges: list of (u, v, weight)
    """
    sorted_edges = sorted(edges, key=lambda item: item[2])
    dsu = DSU(num_nodes)
    mst = []
    total_cost = 0
    
    for u, v, w in sorted_edges:
        if dsu.union(u, v):
            mst.append((u, v, w))
            total_cost += w
            
    return mst, total_cost


# -------------------------------------------------------------------
# INTERFAZ GRÁFICA (TKINTER)
# -------------------------------------------------------------------

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Suite de Algoritmos de Grafos")
        self.root.geometry("850x650")

        # Frame de Controles
        control_frame = ttk.LabelFrame(root, text="Configuración del Grafo")
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(control_frame, text="Número de Nodos (V):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nodes_entry = ttk.Entry(control_frame, width=8)
        self.nodes_entry.insert(0, "4")
        self.nodes_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(control_frame, text="Nodo Origen (Dijkstra):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.source_entry = ttk.Entry(control_frame, width=8)
        self.source_entry.insert(0, "0")
        self.source_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(control_frame, text="Algoritmo:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.algo_box = ttk.Combobox(control_frame, values=["Dijkstra", "Floyd", "Warshall", "Kruskal"], state="readonly")
        self.algo_box.current(0)
        self.algo_box.grid(row=1, column=1, padx=5, pady=5)

        # Entrada de Aristas
        input_frame = ttk.LabelFrame(root, text="Definición de Aristas (Origen Destino Peso)")
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)

        help_text = "Ingrese una arista por línea en formato: u v peso (Ejemplo: 0 1 4)\nPara Warshall, el peso puede ser 1."
        ttk.Label(input_frame, text=help_text, foreground="gray").pack(anchor="w", padx=5, pady=2)

        self.edges_text = scrolledtext.ScrolledText(input_frame, height=8)
        self.edges_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Cargar ejemplo inicial
        default_edges = "0 1 5\n0 2 3\n1 2 2\n1 3 6\n2 3 7"
        self.edges_text.insert(tk.END, default_edges)

        # Botón Ejecutar
        run_btn = ttk.Button(root, text="Ejecutar Algoritmo", command=self.run_algorithm)
        run_btn.pack(pady=5)

        # Salida de Resultados
        output_frame = ttk.LabelFrame(root, text="Resultados")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_text = scrolledtext.ScrolledText(output_frame, height=10, state="disabled")
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)

    def parse_input(self):
        try:
            num_nodes = int(self.nodes_entry.get())
        except ValueError:
            raise ValueError("El número de nodos debe ser un entero válido.")

        raw_text = self.edges_text.get("1.0", tk.END).strip()
        lines = raw_text.split('\n') if raw_text else []
        
        edges = []
        graph_dict = {i: [] for i in range(num_nodes)}
        adj_matrix = [[float('inf')] * num_nodes for _ in range(num_nodes)]
        for i in range(num_nodes):
            adj_matrix[i][i] = 0

        for line_num, line in enumerate(lines, 1):
            parts = line.strip().split()
            if not parts:
                continue
            if len(parts) != 3:
                raise ValueError(f"Línea {line_num} inválida. Formato requerido: u v peso")
            
            u, v, w = int(parts[0]), int(parts[1]), float(parts[2])
            if not (0 <= u < num_nodes and 0 <= v < num_nodes):
                raise ValueError(f"Línea {line_num}: Nodos fuera de rango (0 a {num_nodes-1}).")
            
            edges.append((u, v, w))
            graph_dict[u].append((v, w))
            adj_matrix[u][v] = w

        return num_nodes, edges, graph_dict, adj_matrix

    def run_algorithm(self):
        try:
            num_nodes, edges, graph_dict, adj_matrix = self.parse_input()
            selected_algo = self.algo_box.get()
            output = []

            if selected_algo == "Dijkstra":
                start_node = int(self.source_entry.get())
                if not (0 <= start_node < num_nodes):
                    raise ValueError("El nodo origen de Dijkstra está fuera de rango.")
                
                dist, pred = dijkstra(num_nodes, graph_dict, start_node)
                output.append(f"--- ALGORITMO DE DIJKSTRA (Origen: {start_node}) ---")
                for node in range(num_nodes):
                    d_str = "inf" if dist[node] == float('inf') else f"{dist[node]:.2f}"
                    output.append(f"Distancia a nodo {node}: {d_str} | Predecesor: {pred[node]}")

            elif selected_algo == "Floyd":
                dist_matrix, _ = floyd_warshall(num_nodes, adj_matrix)
                output.append("--- ALGORITMO DE FLOYD (Matriz de Distancias Mínimas) ---")
                for row in dist_matrix:
                    formatted_row = [f"{val:6.1f}" if val != float('inf') else "   inf" for val in row]
                    output.append(" ".join(formatted_row))

            elif selected_algo == "Warshall":
                reach_matrix = warshall(num_nodes, adj_matrix)
                output.append("--- ALGORITMO DE WARSHALL (Clausura Transitiva / Alcanzabilidad) ---")
                for row in reach_matrix:
                    formatted_row = [f"{1 if val else 0:3d}" for val in row]
                    output.append(" ".join(formatted_row))

            elif selected_algo == "Kruskal":
                # Se asume grafo no dirigido agregando la arista simétrica si no existe
                undirected_edges = []
                seen = set()
                for u, v, w in edges:
                    edge_key = tuple(sorted((u, v))) + (w,)
                    if edge_key not in seen:
                        seen.add(edge_key)
                        undirected_edges.append((u, v, w))

                mst, cost = kruskal(num_nodes, undirected_edges)
                output.append("--- ALGORITMO DE KRUSKAL (Árbol de Cobertura Mínima) ---")
                output.append(f"Costo total del MST: {cost:.2f}")
                output.append("Aristas seleccionadas:")
                for u, v, w in mst:
                    output.append(f"  {u} -- {v} (peso: {w})")

            self.display_result("\n".join(output))

        except Exception as e:
            messagebox.showerror("Error de Entrada / Cálculo", str(e))

    def display_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()