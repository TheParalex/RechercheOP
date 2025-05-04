from collections import deque
from utils import *

def bfs_with_trace(rGraph, s, t, parent):
    n = len(rGraph)
    visited = [False] * n
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v, cap_ in enumerate(rGraph[u]):
            if not visited[v] and cap_ > 0:  # Capacité résiduelle positive
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == t:  # Si on atteint le puits, on arrête la recherche
                    return True
    return False

def ford_fulkerson(capacity, n, s, t):
    rGraph = [row[:] for row in capacity]  # Graphe résiduel
    parent = [-1] * n  # Tableau des parents pour reconstruire le chemin
    max_flow = 0
    flow = [[0] * n for _ in range(n)]  # Matrice des flux
    iteration = 1
    trace_log = ""

    while bfs_with_trace(rGraph, s, t, parent):
        trace_log += f"\n* Itération {iteration} :\n"
        trace_log += "Le parcours en largeur :\n" + format_parent_trace(parent, s, t) + "\n"

        # Trouver le flot admissible sur le chemin augmentant
        path_flow = float('inf') 
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, rGraph[u][v])
            v = u
        trace_log += f"Détection d’une chaîne améliorante : saut de flot {path_flow}.\n"

        # Mettre à jour le graphe résiduel et le flot
        v = t
        while v != s:
            u = parent[v]
            rGraph[u][v] -= path_flow
            rGraph[v][u] += path_flow
            flow[u][v] += path_flow
            v = u
        max_flow += path_flow

        trace_log += f"\nModifications sur le graphe résiduel :\n{format_matrix(rGraph)}\n"
        iteration += 1

    trace_log += "\n* Affichage du flot max :\n"
        # Affichage du flot maximum avec tabulate
    headers = [""] + ['s'] + [chr(96 + i) for i in range(1, n - 1)] + ['t']  # En-têtes des colonnes
    table = []
    for i in range(n):
        # Nom du sommet source
        if i == 0:
            row = ['s']
        elif i == n - 1:
            row = ['t']
        else:
            row = [chr(97 + i - 1)]
        for j in range(n):
            if j == 0:
                to_node = 's'
            elif j == n - 1:
                to_node = 't'
            else:
                to_node = chr(97 + j - 1)
            if capacity[i][j] > 0:
                row.append(f"{flow[i][j]}/{capacity[i][j]}")
            else:
                row.append("-")
        table.append(row)

    # Utiliser tabulate pour formater la table
    trace_log += "\n* Affichage du flot max :\n"
    trace_log += tabulate(table, headers=headers, tablefmt="grid")
    trace_log += f"\n\nValeur du flot max = {max_flow}\n"

    return max_flow, trace_log