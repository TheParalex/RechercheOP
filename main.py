from complexity_analysis import *
from collections import deque
from utils import *
from ford_fulkerson import ford_fulkerson
from push_relabel import push_relabel
from min_cost_flow import min_cost_max_flow


def format_matrix(matrix):
    return "\n".join(" ".join(f"{val:2d}" for val in row) for row in matrix)

def format_parent_trace(parent, s, t):
    trace = []
    v = t
    while v != s:
        u = parent[v]
        if u == -1:
            return "Pas de chemin trouvé"
        trace.append(f"Π({chr(97+v)}) = {chr(97+u)}")
        v = u
    return "\n".join(reversed(trace))

def main():
    print("Bienvenue dans le solveur de problème de flot.")

    while True:
        print("\n=== Menu Principal ===")
        print("1 - Résoudre un problème de flot depuis un fichier")
        print("2 - Lancer les benchmarks de performance")
        print("0 - Quitter")
        choix = input("Votre choix : ")

        if choix == "0":
            print("Au revoir !")
            break

        elif choix == "2":
            print("Lancement de l'analyse de complexité...")
            results = benchmark_algorithms()
            plot_all(results)
            plot_upper_bounds(results)
        elif choix == "1":
            file = input("Entrez le nom du fichier problème (ex: p1.txt, ou 'exit' pour quitter) : ")
            if file.lower() == "exit":
                break

            path = f"problems/{file}"
            problem_type = detect_problem_type(path)

            if problem_type == "unknown":
                print(
                    "Format de fichier non reconnu : assurez-vous d'avoir n lignes pour un flot max ou 2n lignes pour un flot à coût min.")
                continue

            print(f"Type détecté automatiquement : {problem_type}")
            trace_output = ""

            if problem_type == "max":
                n, cap = read_capacity_matrix(path)
                trace_output += f"* Affichage de la table des capacités :\n{format_matrix(cap)}\n"
                algo = input("Choisissez l'algorithme (ff = Ford-Fulkerson / pr = Pousser-Réétiqueter) : ")

                if algo == "ff":
                    rGraph = [row[:] for row in cap]
                    parent = [-1] * n
                    max_flow = 0
                    flow = [[0] * n for _ in range(n)]
                    iteration = 1

                    def bfs_with_trace(rGraph, s, t, parent):
                        visited = [False] * n
                        queue = deque([s])
                        visited[s] = True
                        while queue:
                            u = queue.popleft()
                            for v, cap_ in enumerate(rGraph[u]):
                                if not visited[v] and cap_ > 0:
                                    queue.append(v)
                                    visited[v] = True
                                    parent[v] = u
                        return visited[t]

                    while bfs_with_trace(rGraph, 0, n - 1, parent):
                        trace_output += f"\n* Itération {iteration} :\n"
                        trace_output += "Le parcours en largeur :\n" + format_parent_trace(parent, 0, n - 1) + "\n"

                        path_flow = float('inf')
                        v = n - 1
                        while v != 0:
                            u = parent[v]
                            path_flow = min(path_flow, rGraph[u][v])
                            v = u
                        trace_output += f"Détection d’une chaîne améliorante : saut de flot {path_flow}.\n"

                        v = n - 1
                        while v != 0:
                            u = parent[v]
                            rGraph[u][v] -= path_flow
                            rGraph[v][u] += path_flow
                            flow[u][v] += path_flow
                            v = u
                        max_flow += path_flow

                        trace_output += f"\nModifications sur le graphe résiduel :\n{format_matrix(rGraph)}\n"
                        iteration += 1

                    trace_output += "\n* Affichage du flot max :\n"
                    trace_output += "    " + "     ".join(chr(97 + i) for i in range(n)) + "\n"
                    for i in range(n):
                        line = chr(97 + i) + " "
                        for j in range(n):
                            if cap[i][j] > 0:
                                line += f"{flow[i][j]}/{cap[i][j]:2d}".rjust(6)
                            else:
                                line += "  0   "
                        trace_output += line + "\n"
                    trace_output += f"\nValeur du flot max = {max_flow}\n"
                    trace_file = f"F5-trace-{file.replace('.txt', '')}-FF.txt"
                else:
                    result, pr_trace = push_relabel(cap, 0, n - 1)
                    trace_output += "\n--- Détail des itérations (Pousser-Réétiqueter) ---\n"
                    trace_output += pr_trace + "\n"
                    trace_output += f"\nValeur du flot max = {result}\n"
                    trace_file = f"F5-trace-{file.replace('.txt', '')}-PR.txt"

            elif problem_type == "cout":
                n, cap, cost = read_capacity_cost_matrices(path)
                trace_output += f"* Table des capacités :\n{format_matrix(cap)}\n"
                trace_output += f"* Table des coûts :\n{format_matrix(cost)}\n"

                mode = input("Choisir méthode de calcul du flot ? (auto/fixe) : ")
                if mode == "fixe":
                    flow_val = int(input("Entrez la valeur du flot à envoyer : "))
                else:
                    flowval, _ = ford_fulkerson(cap, 0, n - 1)
                    flow_val = flowval // 2  # Divisez flowval par 2 pour obtenir flow_val
                    print(f"Valeur automatique utilisée : {flow_val}")

                result, trace_min = min_cost_max_flow(cap, cost, 0, n - 1, flow_val)
                trace_output += trace_min
                trace_file = f"F5-trace-{file.replace('.txt', '')}-MIN.txt"

            save_trace(trace_file, trace_output)
            print(trace_output)

if __name__ == "__main__":
    main()