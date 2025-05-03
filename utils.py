import random
import time
import os

def read_capacity_matrix(file_path):
    with open(file_path, 'r') as f:
        n = int(f.readline())
        capacity = [list(map(int, f.readline().split())) for _ in range(n)]
    return n, capacity

def read_capacity_cost_matrices(file_path):
    with open(file_path, 'r') as f:
        n = int(f.readline())
        capacity = [list(map(int, f.readline().split())) for _ in range(n)]
        cost = [list(map(int, f.readline().split())) for _ in range(n)]
    return n, capacity, cost

def print_matrix(matrix, title="Matrix"):
    print(f"\n{title}:")
    for row in matrix:
        print(" ".join(f"{val:4d}" for val in row))

def print_flow_matrix(flow, capacity):
    print("\nAffichage du flot max :")
    n = len(flow)
    print("   " + " ".join(chr(97+i) for i in range(n)))
    for i in range(n):
        line = chr(97+i) + " "
        for j in range(n):
            if capacity[i][j] > 0:
                line += f"{flow[i][j]}/{capacity[i][j]:2d} ".rjust(6)
            else:
                line += "  0   "
        print(line)

def generate_random_flow_problem(n):
    capacity = [[0] * n for _ in range(n)]
    cost = [[0] * n for _ in range(n)]
    edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    random.shuffle(edges)
    for i, j in edges[:(n * n) // 2]:
        capacity[i][j] = random.randint(1, 100)
        cost[i][j] = random.randint(1, 100)
    return capacity, cost

def write_flow_problem_to_file(filename, capacity, cost=None):
    with open(filename, 'w') as f:
        n = len(capacity)
        f.write(f"{n}\n")
        for row in capacity:
            f.write(" ".join(map(str, row)) + "\n")
        if cost:
            for row in cost:
                f.write(" " .join(map(str, row)) + "\n")

def measure_time(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start

def save_trace(filename, content):
    os.makedirs("traces", exist_ok=True)
    with open(os.path.join("traces", filename), 'w', encoding='utf-8') as f:
        f.write(content)

def detect_problem_type(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    if len(lines) == 1 + 2 * n:
        return "cout"
    elif len(lines) == 1 + n:
        return "max"
    else:
        return "unknown"
    

def format_matrix(matrix):
    """
    Formate une matrice en une chaîne de caractères lisible.
    """
    return "\n".join(" ".join(f"{val:5}" for val in row) for row in matrix)