import matplotlib.pyplot as plt
from utils import *
from ford_fulkerson import *
from push_relabel import *
from min_cost_flow import *

def generate_sparse_matrix(n, max_value=100):
    cap = [[0 for _ in range(n)] for _ in range(n)]
    cost = [[0 for _ in range(n)] for _ in range(n)]
    num_edges = int((n * n) / 2)
    edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    selected_edges = random.sample(edges, num_edges)

    for i, j in selected_edges:
        cap[i][j] = random.randint(1, max_value)
        cost[i][j] = random.randint(1, max_value)

    return cap, cost

def benchmark_algorithms():
    sizes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]  # valeurs recommandées
    repetitions = 10

    results = {"ff": {}, "pr": {}, "min": {}}

    for n in sizes:
        ff_times = []
        pr_times = []
        min_times = []

        for _ in range(repetitions):
            cap, cost = generate_sparse_matrix(n)

            _, t_ff = measure_time(ford_fulkerson, cap, 0, n - 1)
            _, t_pr = measure_time(push_relabel, cap, 0, n - 1)
            maxf, _ = ford_fulkerson(cap, 0, n - 1)
            _, t_min = measure_time(min_cost_max_flow, cap, cost, 0, n - 1, maxf // 2)

            ff_times.append(t_ff)
            pr_times.append(t_pr)
            min_times.append(t_min)

        results["ff"][n] = ff_times
        results["pr"][n] = pr_times
        results["min"][n] = min_times

    return results

def plot_all(results):
    for algo in ["ff", "pr", "min"]:
        plt.figure()
        data = [results[algo][n] for n in results[algo]]
        plt.boxplot(data, positions=list(results[algo].keys()))
        plt.title(f"Nuage de points - {algo.upper()}")
        plt.xlabel("Taille du graphe (n)")
        plt.ylabel("Temps (s)")
        plt.grid(True)
        plt.savefig(f"nuage_{algo}.png")
        plt.show()

def plot_upper_bounds(results):
    for algo in ["ff", "pr", "min"]:
        n_values = list(results[algo].keys())
        max_values = [max(results[algo][n]) for n in n_values]
        plt.plot(n_values, max_values, marker='o', label=algo.upper())

    plt.title("Complexité dans le pire des cas")
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps maximal (s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("courbe_pire_cas.png")
    plt.show()