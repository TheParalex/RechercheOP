def push_relabel_with_trace(capacity, s, t):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    height = [0] * n
    excess = [0] * n
    trace_log = ""

    height[s] = n
    for v in range(n):
        flow[s][v] = capacity[s][v]
        flow[v][s] = -flow[s][v]
        excess[v] = capacity[s][v]
        excess[s] -= capacity[s][v]

    def push(u, v):
        send = min(excess[u], capacity[u][v] - flow[u][v])
        flow[u][v] += send
        flow[v][u] -= send
        excess[u] -= send
        excess[v] += send
        return f"  PUSH: {chr(97+u)} → {chr(97+v)} | flot envoyé = {send}"

    def relabel(u):
        min_height = float('inf')
        for v in range(n):
            if capacity[u][v] - flow[u][v] > 0:
                min_height = min(min_height, height[v])
        old_height = height[u]
        height[u] = min_height + 1
        return f"  RELABEL: {chr(97+u)} | hauteur passée de {old_height} à {height[u]}"

    def discharge(u):
        nonlocal trace_log
        trace_log += f"\n→ Traitement du sommet {chr(97+u)} (excess = {excess[u]}, height = {height[u]})\n"
        while excess[u] > 0:
            for v in range(n):
                if capacity[u][v] - flow[u][v] > 0 and height[u] == height[v] + 1:
                    trace_log += push(u, v) + "\n"
                    if excess[u] == 0:
                        break
            else:
                trace_log += relabel(u) + "\n"

    active = [i for i in range(n) if i != s and i != t and excess[i] > 0]
    while active:
        u = active.pop(0)
        old_height = height[u]
        discharge(u)
        if height[u] > old_height:
            active.insert(0, u)

    max_flow = sum(flow[s])
    trace_log += f"\n Flot maximum trouvé = {max_flow}\n"
    return max_flow, trace_log
