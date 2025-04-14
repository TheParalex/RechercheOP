def push_relabel(capacity, s, t):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    height = [0] * n
    excess = [0] * n
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

    def relabel(u):
        min_height = float('inf')
        for v in range(n):
            if capacity[u][v] - flow[u][v] > 0:
                min_height = min(min_height, height[v])
        height[u] = min_height + 1

    def discharge(u):
        while excess[u] > 0:
            for v in range(n):
                if capacity[u][v] - flow[u][v] > 0 and height[u] == height[v] + 1:
                    push(u, v)
                    if excess[u] == 0:
                        break
            else:
                relabel(u)

    active = [i for i in range(n) if i != s and i != t and excess[i] > 0]
    while active:
        u = active.pop(0)
        old_height = height[u]
        discharge(u)
        if height[u] > old_height:
            active.insert(0, u)
    return sum(flow[s])
