def bellman_ford(cost, capacity, flow, s):
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
    n = len(capacity)
    flow = [[0]*n for _ in range(n)]
    total_cost = 0
    while required_flow > 0:
        dist, parent = bellman_ford(cost, capacity, flow, s)
        if parent[t] == -1:
            break
        path_flow = required_flow
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v] - flow[u][v])
            v = u
        required_flow -= path_flow
        total_cost += path_flow * dist[t]
        v = t
        while v != s:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
    return total_cost