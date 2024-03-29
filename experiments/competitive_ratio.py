import matplotlib.pyplot as plt
from importmonkey import add_path
add_path("../online")
add_path("../offline")
add_path("../benchmarks")
import uniform_generator as ug
import lru 
import fifo
import belady


def uniform_CR_suite(N_tests, N_pages, k, sequence_length):
    uniform_gen = ug.UniformGenerator(N_pages, seed=42)
    DATA = {}
    
    for i in range(N_tests):
        
        DATA[i] = {}
        algos = []
        for Z in [1] + list(range(5, 90, 5)):
            algos.append(lru.LRU(k, Z=Z))
            # algos.append(fifo.FIFO(k, Z=Z))
        request_sequence = uniform_gen.generate(sequence_length)
        # print(f"Request sequence = {request_sequence}")
        # optimal = belady.Belady(k, request_sequence)
        # cost_optimal = optimal.run()
        for algo in algos:
            cost_algo = algo.run(request_sequence)
            print(f"i = {i}, {algo.get_name()} cost = {cost_algo}")
            DATA[i][algo.get_name()] = cost_algo
    
    fig, ax = plt.subplots()
    for algo in algos:
        ax.plot([i for i in range(N_tests)], [DATA[i][algo.get_name()] for i in range(N_tests)], label=algo.get_name())
        ax.set(xlabel="Test number", ylabel="Penalty")
    ax.legend()
    plt.show()

N_tests = 50
N_pages = 10
k = 9
sequence_length = 2000
uniform_CR_suite(N_tests, N_pages, k, sequence_length)