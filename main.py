from utils import read_capacity_matrix, read_capacity_cost_matrices, print_matrix, save_trace
from ford_fulkerson import ford_fulkerson
from push_relabel import push_relabel
from min_cost_flow import min_cost_max_flow

def main():
    print("Bienvenue dans le solveur de problème de flot.")
    file = input("Entrez le nom du fichier problème (ex: p1.txt): ")
    problem_type = input("Type (max/cout): ")

    trace_output = ""

    if problem_type == "max":
        n, cap = read_capacity_matrix(f"problems/{file}")
        trace_output += f"Capacités:\n" + "\n".join(" ".join(map(str, row)) for row in cap) + "\n"
        algo = input("Algorithme (ff/pr): ")
        if algo == "ff":
            result = ford_fulkerson(cap, 0, n - 1)
            trace_file = f"trace-{file.replace('.txt','')}-FF.txt"
        else:
            result = push_relabel(cap, 0, n - 1)
            trace_file = f"trace-{file.replace('.txt','')}-PR.txt"
        trace_output += f"Flot maximal = {result}\n"
    else:
        n, cap, cost = read_capacity_cost_matrices(f"problems/{file}")
        trace_output += "Capacités:\n" + "\n".join(" ".join(map(str, row)) for row in cap) + "\n"
        trace_output += "Coûts:\n" + "\n".join(" ".join(map(str, row)) for row in cost) + "\n"
        maxf = ford_fulkerson(cap, 0, n - 1)
        result = min_cost_max_flow(cap, cost, 0, n - 1, maxf // 2)
        trace_output += f"Flot à coût minimal (valeur de flot = {maxf//2}) = {result}\n"
        trace_file = f"trace-{file.replace('.txt','')}-MIN.txt"

    save_trace(trace_file, trace_output)
    print(trace_output)
if __name__ == "__main__":
    main()