from copy import deepcopy
from utils import format_matrix

def bellman_ford(cost, capacity, flow, s):
    """
    Implémente l'algorithme de Bellman-Ford pour trouver le plus court chemin en termes de coût
    dans un graphe pondéré avec des capacités résiduelles.
    """
    n = len(cost)
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[s] = 0

    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if capacity[u][v] - flow[u][v] > 0 and dist[v] > dist[u] + cost[u][v]:
                    dist[v] = dist[u] + cost[u][v]
                    parent[v] = u

    return dist, parent


def run_bellman_ford(cost, capacity, flow, s, t, trace_log, iteration):
    """
    Exécute Bellman-Ford et génère un journal des distances et des parents.
    """
    dist, parent = bellman_ford(cost, capacity, flow, s)

    trace_log += f"\n--- Itération {iteration} ---\n"
    trace_log += "Table µ (Bellman) :\n"
    for i in range(len(cost)):
        d = "∞" if dist[i] == float('inf') else f"{dist[i]:.1f}"
        p = "∅" if parent[i] == -1 else chr(97 + parent[i])
        trace_log += f"  µ({chr(97 + i)}) = {d} | π({chr(97 + i)}) = {p}\n"

    if parent[t] == -1:
        trace_log += "Aucune chaîne améliorante trouvée. Fin de l'algorithme.\n"

    return dist, parent, trace_log

def min_cost_max_flow(capacity, cost, s, t, required_flow):
    """
    Calcule un flot à coût minimal du sommet s au sommet t,
    en essayant d'envoyer exactement required_flow unités de flot.
    """
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    total_cost = 0
    trace_log = ""
    iteration = 1

    # Étape 1 : Initialisation
    residuel_cap = deepcopy(capacity)
    residuel_cout = deepcopy(cost)
    flot_actuel = 0

    while flot_actuel < required_flow:
        # Étape 2 : Calcul des plus courts chemins avec Bellman-Ford
        dist, parent = bellman_ford(residuel_cout, residuel_cap, flow, s)

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
        trace_log += f"Chaîne augmentante : {' -> '.join(chr(97 + u) for u, _ in chemin)} -> {chr(97 + t)}\n"
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
    trace_log += "          " + "  ".join(f"{chr(97 + i):>10}" for i in range(n)) + "\n"
    trace_log += "    " + "-" * (12 * n) + "\n"
    for i in range(n):
        row = []
        for j in range(n):
            if capacity[i][j] > 0:
                row.append(f"{flow[i][j]}/{capacity[i][j]} ({cost[i][j]})")
            else:
                row.append("      -      ")
        trace_log += f"{chr(97 + i):>5} | " + "  ".join(f"{val:>10}" for val in row) + "\n"

    return total_cost, trace_log