from utils import read_capacity_matrix, read_capacity_cost_matrices, print_matrix
from ford_fulkerson import ford_fulkerson
from push_relabel import push_relabel
from min_cost_flow import min_cost_max_flow

def main():
    print("Bienvenue dans le solveur de problème de flot.")
    file = input("Entrez le nom du fichier problème (ex: p1.txt): ")
    problem_type = input("Type (max/cout): ")

    if problem_type == "max":
        n, cap = read_capacity_matrix(f"problems/{file}")
        print_matrix(cap, "Capacités")
        algo = input("Algorithme (ff/pr): ")
        if algo == "ff":
            result = ford_fulkerson(cap, 0, n - 1)
        else:
            result = push_relabel(cap, 0, n - 1)
        print(f"Flot maximal = {result}")
    else:
        n, cap, cost = read_capacity_cost_matrices(f"problems/{file}")
        print_matrix(cap, "Capacités")
        print_matrix(cost, "Coûts")
        maxf = ford_fulkerson(cap, 0, n - 1)
        result = min_cost_max_flow(cap, cost, 0, n - 1, maxf // 2)
        print(f"Flot à coût minimal (valeur de flot = {maxf//2}) = {result}")

if __name__ == "__main__":
    main()