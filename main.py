from complexity_analysis import *
from collections import deque
from utils import *
from ford_fulkerson import ford_fulkerson
from push_relabel import push_relabel
from min_cost_flow import min_cost_max_flow

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
                    result, ff_trace = ford_fulkerson(cap, n, 0, n - 1)
                    trace_output += "\n--- Détail des itérations (Ford-Fulkerson) ---\n"
                    trace_output += ff_trace + "\n"
                    trace_output += f"\nValeur du flot max = {result}\n"
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

                flow_val = int(input("Entrez la valeur du flot à envoyer : "))

                result, trace_min = min_cost_max_flow(cap, cost, 0, n - 1, flow_val)
                trace_output += trace_min
                trace_file = f"F5-trace-{file.replace('.txt', '')}-MIN.txt"

            save_trace(trace_file, trace_output)
            print(trace_output)

if __name__ == "__main__":
    main()