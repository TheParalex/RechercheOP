from utils import *

def push_relabel(capacity, s, t):
    """
    Implémente l'algorithme Push-Relabel pour trouver le flot maximum.
    :param capacity: Matrice des capacités (n x n)
    :param s: Source
    :param t: Puits
    :return: Flot maximum et journal des opérations
    """
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    height = [0] * n
    excess = [0] * n
    active = []  # Liste des sommets actifs
    trace_log = ""

    # Initialisation
    height[s] = n
    for v in range(n):
        if capacity[s][v] > 0:  # Vérifie si une capacité existe entre la source et v
            flow[s][v] = capacity[s][v]
            flow[v][s] = -capacity[s][v]
            excess[v] = capacity[s][v]
            excess[s] -= capacity[s][v]
            if v != s and v != t and excess[v] > 0:
                active.append(v)

    def push(u, v):
        residual = capacity[u][v] - flow[u][v]
        if residual > 0 and height[u] == height[v] + 1:
            delta = min(excess[u], residual)
            flow[u][v] += delta
            flow[v][u] -= delta
            excess[u] -= delta
            excess[v] += delta
            trace_log = f"PUSH: {chr(96+u)}→{chr(96+v)} Δ={delta} | e[{chr(96+u)}]={excess[u]} e[{chr(96+v)}]={excess[v]}\n"
            if v != s and v != t and v not in active:
                active.append(v)
            return trace_log
        return ""

    def relabel(u):
        min_height = float('inf')
        for v in range(n):
            if capacity[u][v] - flow[u][v] > 0:  # Arc résiduel
                min_height = min(min_height, height[v])
        old_height = height[u]
        height[u] = min_height + 1
        return f"RELABEL: {chr(96+u)} h:{old_height}→{height[u]}\n"

    def discharge(u):
        nonlocal trace_log
        while excess[u] > 0:
            pushed = False
            for v in range(n):
                push_log = push(u, v)
                if push_log:
                    trace_log += push_log
                    pushed = True
                    if excess[u] == 0:
                        break
            if not pushed:  # Si aucun push n'est possible, relabel
                trace_log += relabel(u)

    # Traitement des sommets actifs
    while active:
        u = active.pop(0)  # Prendre le premier sommet actif
        trace_log += f"\n→ Traitement de {chr(96+u)} (excess = {excess[u]}, height = {height[u]})\n"
        discharge(u)

    # Calcul du flot maximum
    max_flow = sum(flow[s][v] for v in range(n))
    trace_log += f"\nFlot maximum trouvé = {max_flow}\n"

   # Affichage de la matrice finale des flux avec tabulate
    node_names = ['s'] + [chr(96 + i) for i in range(1, n - 1)] + ['t']

    # Préparer les données pour tabulate
    headers = [""] + node_names
    table = []
    for i in range(n):
        row = [node_names[i]]
        for j in range(n):
            if capacity[i][j] > 0:
                row.append(f"{flow[i][j]}/{capacity[i][j]}")
            else:
                row.append("-")
        table.append(row)

    # Utiliser tabulate pour formater la table
    trace_log += "\nMatrice finale des flux (flow / capacity):\n"
    trace_log += tabulate(table, headers=headers, tablefmt="grid")
    trace_log += "\n"


    return max_flow, trace_log