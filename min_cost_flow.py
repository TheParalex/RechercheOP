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

    while required_flow > 0:
        dist, parent = bellman_ford(cost, capacity, flow, s)

        trace_log += f"\n--- Itération {iteration} ---\n"
        trace_log += "Table µ (Bellman) :\n"
        for i in range(n):
            d = "∞" if dist[i] == float('inf') else f"{dist[i]:.1f}"
            p = "∅" if parent[i] == -1 else chr(97 + parent[i])
            trace_log += f"  µ({chr(97 + i)}) = {d} | π({chr(97 + i)}) = {p}\n"

        if parent[t] == -1:
            trace_log += "Aucune chaîne améliorante trouvée. Fin de l'algorithme.\n"
            break

        # Trouver le flot admissible sur ce chemin
        path_flow = required_flow
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v] - flow[u][v])
            v = u

        trace_log += f" Chaîne améliorante trouvée avec flot = {path_flow}\n"

        # Mettre à jour le flot et le coût
        required_flow -= path_flow
        total_cost += path_flow * dist[t]
        v = t
        while v != s:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u

        # Affichage du graphe résiduel
        trace_log += "\nGraphe résiduel mis à jour :\n"
        for i in range(n):
            row = "  " + " ".join(f"{capacity[i][j] - flow[i][j]:3d}" for j in range(n))
            trace_log += f"{chr(97 + i)} :{row}\n"

        iteration += 1

    if required_flow > 0:
        trace_log += f"\n⚠️ Flot partiellement réalisé : {required_flow} unités de flot n'ont pas pu être envoyées.\n"

    trace_log += f"\n✅ Coût total du flot à coût minimal = {total_cost}\n"
    return total_cost, trace_log