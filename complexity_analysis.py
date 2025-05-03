import numpy as np
import random
import matplotlib.pyplot as plt
from utils import measure_time
from ford_fulkerson import ford_fulkerson
from push_relabel import push_relabel
from min_cost_flow import min_cost_max_flow
import time

def generate_sparse_matrix(n, max_value=100):
    cap = {}
    cost = {}
    edges = random.sample([(i, j) for i in range(n) for j in range(n) if i != j], (n * (n - 1)) // 4)

    # Forcer un chemin entre la source (0) et le puits (n-1)
    for i in range(n - 1):
        cap[(i, i + 1)] = random.randint(1, max_value)
        cost[(i, i + 1)] = random.randint(1, max_value)

    for i, j in edges:
        if (i, j) not in cap:
            cap[(i, j)] = random.randint(1, max_value)
            cost[(i, j)] = random.randint(1, max_value)

    # Convertir en matrice dense
    cap_matrix = np.zeros((n, n), dtype=int)
    cost_matrix = np.zeros((n, n), dtype=int)
    for (i, j), value in cap.items():
        cap_matrix[i][j] = value
    for (i, j), value in cost.items():
        cost_matrix[i][j] = value

    return cap_matrix, cost_matrix

def benchmark_algorithms():
    sizes = [10, 20, 50, 100]  # Tailles des graphes à tester
    repetitions = 50  # Nombre de répétitions pour chaque taille
    results = {"ff": {}, "pr": {}, "min": {}}  # Stockage des résultats

    print("=== Début des benchmarks ===")
    for n in sizes:
        results["ff"][n] = []
        results["pr"][n] = []
        results["min"][n] = []

        for _ in range(repetitions):
            # Génération du graphe
            cap, cost = generate_sparse_matrix(n)
            V = len(cap)  # Nombre de sommets
            E = sum(1 for i in range(V) for j in range(V) if cap[i][j] > 0)  # Nombre d'arêtes

            # Calcul du flot maximum (F) avec Ford-Fulkerson
            maxf, _ = ford_fulkerson(np.copy(cap), 0, n - 1)

            # Vérification des valeurs calculées
            if maxf == 0:
                print(f"Attention : Aucun flot possible pour un graphe de taille {n}.")
                continue

            # Fonction pour mesurer le temps d'exécution
            def measure_time(algorithm, *args):
                start = time.perf_counter()
                algorithm(*args)
                return time.perf_counter() - start

            # Mesurer les temps pour chaque algorithme
            t_ff = measure_time(ford_fulkerson, np.copy(cap), 0, n - 1)
            t_pr = measure_time(push_relabel, np.copy(cap), 0, n - 1)
            t_min = measure_time(min_cost_max_flow, np.copy(cap), np.copy(cost), 0, n - 1, maxf // 2)

            # Affichage des valeurs de V, E et F pour chaque itération
            print(f"Graph size: {n}, V: {V}, E: {E}, F: {maxf}")
            print(f"Temps Ford-Fulkerson: {t_ff:.8f}s, Push-Relabel: {t_pr:.8f}s, Min-Cost: {t_min:.8f}s")

            # Stockage des résultats
            results["ff"][n].append(t_ff)
            results["pr"][n].append(t_pr)
            results["min"][n].append(t_min)

    print("=== Fin des benchmarks ===")
    return results

def plot_all(results):
    algo_names = {"ff": "Ford-Fulkerson", "pr": "Push-Relabel", "min": "Min-Cost Max-Flow"}
    colors = {"ff": "skyblue", "pr": "lightgreen", "min": "salmon"}

    for algo in ["ff", "pr", "min"]:
        plt.figure(figsize=(8, 6))
        n_values = sorted(results[algo].keys())
        data = [results[algo][n] for n in n_values]

        plt.boxplot(data, positions=n_values, patch_artist=True,
                    boxprops=dict(facecolor=colors[algo], color='black'),
                    medianprops=dict(color='black'),
                    whiskerprops=dict(color='gray'),
                    capprops=dict(color='gray'))

        plt.title(f"Distribution des temps - {algo_names[algo]}")
        plt.xlabel("Taille du graphe (n)")
        plt.ylabel("Temps d'exécution (secondes)")
        plt.grid(True, linestyle='--', alpha=0.6)

        # Explication en texte pour compréhension
        plt.figtext(0.5, -0.05,
            "Chaque boîte représente la répartition des temps d'exécution pour 50 répétitions.\n"
            "La ligne noire au centre est la médiane. Les moustaches indiquent les valeurs extrêmes sans outliers.",
            ha="center", fontsize=9)

        plt.tight_layout()
        plt.savefig(f"nuage_{algo}.png")
        plt.show()

def plot_upper_bounds(results):
    plt.figure(figsize=(8, 6))
    algo_names = {"ff": "Edmonds-Karp", "pr": "Push-Relabel", "min": "Min-Cost Max-Flow"}
    markers = {"ff": "o", "pr": "s", "min": "^"}

    for algo in ["ff", "pr", "min"]:
        n_values = sorted(results[algo].keys())
        max_values = [max(results[algo][n]) for n in n_values]
        plt.plot(n_values, max_values, marker=markers[algo], label=algo_names[algo])

    plt.title("Temps d'exécution maximal par taille de graphe")
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps maximal (secondes)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("courbe_pire_cas.png")
    plt.show()
