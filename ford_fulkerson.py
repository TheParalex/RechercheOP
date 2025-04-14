from collections import deque

def bfs(rGraph, s, t, parent):
    visited = [False] * len(rGraph)
    queue = deque([s])
    visited[s] = True
    while queue:
        u = queue.popleft()
        for v, cap in enumerate(rGraph[u]):
            if not visited[v] and cap > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return visited[t]

def ford_fulkerson(capacity, s, t):
    n = len(capacity)
    rGraph = [row[:] for row in capacity]
    parent = [-1] * n
    max_flow = 0
    while bfs(rGraph, s, t, parent):
        path_flow = float('inf')
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, rGraph[u][v])
            v = parent[v]
        max_flow += path_flow
        v = t
        while v != s:
            u = parent[v]
            rGraph[u][v] -= path_flow
            rGraph[v][u] += path_flow
            v = parent[v]
    return max_flow
