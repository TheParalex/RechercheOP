import matplotlib.pyplot as plt

def run_benchmark():
    from utils import generate_random_flow_problem, measure_time
    from ford_fulkerson import ford_fulkerson
    from push_relabel import push_relabel
    from min_cost_flow import min_cost_max_flow

    sizes = [10, 20, 40, 100, 400]
    ff_times, pr_times, min_times = [], [], []
    for n in sizes:
        ff_t, pr_t, min_t = [], [], []
        for _ in range(10):
            cap, cost = generate_random_flow_problem(n)
            _, t1 = measure_time(ford_fulkerson, cap, 0, n - 1)
            _, t2 = measure_time(push_relabel, cap, 0, n - 1)
            max_flow = ford_fulkerson(cap, 0, n - 1)
            _, t3 = measure_time(min_cost_max_flow, cap, cost, 0, n - 1, max_flow // 2)
            ff_t.append(t1)
            pr_t.append(t2)
            min_t.append(t3)
        ff_times.append(ff_t)
        pr_times.append(pr_t)
        min_times.append(min_t)

    plt.boxplot(ff_times, positions=sizes)
    plt.title("Ford-Fulkerson")
    plt.show()

    plt.boxplot(pr_times, positions=sizes)
    plt.title("Pousser-Réétiqueter")
    plt.show()

    plt.boxplot(min_times, positions=sizes)
    plt.title("Flot à coût min")
    plt.show()