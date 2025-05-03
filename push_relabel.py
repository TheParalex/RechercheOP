def push_relabel(capacity, s, t):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    height = [0] * n
    excess = [0] * n
    seen = [0] * n  # Pour optimiser discharge
    trace_log = ""

    height[s] = n
    for v in range(n):
        flow[s][v] = capacity[s][v]
        flow[v][s] = -capacity[s][v]  # Arc inverse dans le graphe résiduel
        excess[v] = capacity[s][v]
        excess[s] -= capacity[s][v]

    def push(u, v):
        send = min(excess[u], capacity[u][v] - flow[u][v])
        if send > 0:
            flow[u][v] += send
            flow[v][u] -= send
            excess[u] -= send
            excess[v] += send
            return f"  PUSH: {chr(97+u)} → {chr(97+v)} | flot = {send}"
        return ""

    def relabel(u):
        min_height = float('inf')
        for v in range(n):
            if capacity[u][v] - flow[u][v] > 0:
                min_height = min(min_height, height[v])
        old_height = height[u]
        height[u] = min_height + 1
        return f"  RELABEL: {chr(97+u)} | hauteur {old_height} → {height[u]}"

    def discharge(u):
        nonlocal trace_log
        trace_log += f"\n→ Traitement de {chr(97+u)} (excess = {excess[u]}, height = {height[u]})\n"
        while excess[u] > 0:
            if seen[u] < n:
                v = seen[u]
                if capacity[u][v] - flow[u][v] > 0 and height[u] == height[v] + 1:
                    result = push(u, v)
                    if result:
                        trace_log += result + "\n"
                seen[u] += 1
            else:
                result = relabel(u)
                trace_log += result + "\n"
                seen[u] = 0

    # Utilise une pile (LIFO) avec stratégie "highest label" implicite
    active = [i for i in range(n) if i != s and i != t and excess[i] > 0]
    while active:
        u = active.pop()
        old_height = height[u]
        discharge(u)
        if height[u] > old_height:
            active.insert(0, u)  # Redonne priorité à ce sommet

    max_flow = sum(flow[u][t] for u in range(n))
    trace_log += f"\nFlot maximum trouvé = {max_flow}\n"
    return max_flow, trace_log
