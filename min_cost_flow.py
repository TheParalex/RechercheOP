from utils import *

def bellman_ford_verbose(cost, capacity, flow, s, node_names=None):
    """
    Bellman-Ford qui retourne uniquement l'affichage de la dernière exécution sous forme de texte.
    """
    n = len(cost)
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[s] = 0

    if node_names is None:
        node_names = ['s'] + [chr(97 + i) for i in range(1, n - 1)] + ['t']

    history = []
    history.append(["Init"] + [format_entry(dist[i], parent[i], node_names) for i in range(n)])

    for k in range(1, n + 1):
        updated = False
        new_dist = dist.copy()
        new_parent = parent.copy()
        for u in range(n):
            for v in range(n):
                if capacity[u][v] - flow[u][v] > 0 and dist[u] + cost[u][v] < new_dist[v]:
                    new_dist[v] = dist[u] + cost[u][v]
                    new_parent[v] = u
                    updated = True
        dist = new_dist
        parent = new_parent
        history.append([str(k)] + [format_entry(dist[i], parent[i], node_names) for i in range(n)])
        if not updated:
            break

    output = "\nTable des plus courts chemins de s vers tous les sommets :\n\n"
    headers = ["Itération"] + node_names
    output += tabulate(history, headers=headers, tablefmt="fancy_grid") + "\n"

    return dist, parent, output

def format_entry(distance, parent_index, node_names):
    if distance == float('inf'):
        return "∞ / -"
    else:
        parent_name = '-' if parent_index == -1 else node_names[parent_index]
        return f"{distance} / {parent_name}"

def min_cost_max_flow(capacity, cost, s, t, required_flow):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    total_cost = 0
    trace_log = ""
    iteration = 1
    node_names = ['s'] + [chr(96 + i) for i in range(1, n - 1)] + ['t']

    # Étape 1 : Initialisation
    residuel_cap = deepcopy(capacity)
    residuel_cout = deepcopy(cost)
    flot_actuel = 0

    while flot_actuel < required_flow:
        # Étape 2 : Calcul des plus courts chemins avec Bellman-Ford
        dist, parent, bellman_table = bellman_ford_verbose(residuel_cout, residuel_cap, flow, s)

        if parent[t] == -1:
            trace_log += "Aucun chemin augmentant trouvé. Arrêt de l'algorithme.\n"
            break

        # Étape 3 : Remonter la chaîne augmentante à partir de la table Bellman-Ford
        chemin = []
        v = t
        while v != s:
            u = parent[v]
            if u == -1:
                raise ValueError("Aucun chemin de s à t n'existe")
            chemin.insert(0, (u, v))
            v = u

        # Étape 4 : Déterminer le flot possible sur cette chaîne
        flot_chaine = min(residuel_cap[u][v] for u, v in chemin)
        if flot_actuel + flot_chaine > required_flow:
            flot_chaine = required_flow - flot_actuel

        # Étape 5 : Mise à jour des graphes résiduels
        for u, v in chemin:
            residuel_cap[u][v] -= flot_chaine
            if residuel_cap[u][v] == 0:
                residuel_cap[u][v] = 0  # Supprimer les capacités nulles

            residuel_cap[v][u] += flot_chaine
            residuel_cout[v][u] = -residuel_cout[u][v]

        # Mise à jour des flux et du coût total
        flot_actuel += flot_chaine
        total_cost += flot_chaine * dist[t]

        # Journalisation des résultats intermédiaires
        trace_log += f"\n--- Itération {iteration} ---\n"
        trace_log += bellman_table

        # Correction ici
        trace_log += f"Chaîne augmentante : {' -> '.join(node_names[u] for u, v in chemin)} -> {node_names[t]}\n"
        trace_log += f"Flot injecté : {flot_chaine} | Flot total : {flot_actuel}\n"
        trace_log += "\nMatrice de capacités résiduelles :\n"
        trace_log += format_matrix(residuel_cap)
        trace_log += "\nMatrice de coûts résiduels :\n"
        trace_log += format_matrix(residuel_cout)

        iteration += 1

    # Étape 6 : Résultats finaux
    if flot_actuel < required_flow:
        trace_log += f"\n⚠️ Flot partiellement réalisé : {required_flow - flot_actuel} unités de flot n'ont pas pu être envoyées.\n"

    trace_log += f"\n✅ Flot maximal atteint\n"

   # Affichage de la matrice finale des flux avec les coûts
    trace_log += "\nMatrice finale des flux (flow / capacity avec cost):\n\n"

    # Préparer les données pour tabulate
    headers = [""] + node_names
    table = []
    for i in range(n):
        row = [node_names[i]]
        for j in range(n):
            if capacity[i][j] > 0:
                flow[i][j] = capacity[i][j] - residuel_cap[i][j]
                row.append(f"{flow[i][j]}/{capacity[i][j]} ({cost[i][j]})")
            else:
                row.append("-")
        table.append(row)

    # Utiliser tabulate pour formater la table
    trace_log += tabulate(table, headers=headers, tablefmt="grid")
    trace_log += "\n"

    return total_cost, trace_log