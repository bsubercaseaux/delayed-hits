import matplotlib.pyplot as plt
import numpy as np
from importmonkey import add_path

import scipy.stats

def mean_confidence_interval(data, confidence=0.99):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    min_val = np.min(a)
    max_val = np.max(a)
    return m, min_val, max_val
    # return m, m-h, m+h

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
        ax.plot(
            [i for i in range(N_tests)],
            [DATA[i][algo.get_name()] for i in range(N_tests)],
            label=algo.get_name(),
        )
    ax.set(xlabel="Test number", ylabel="Penalty")
    ax.legend()
    plt.show()


def K_suite(N_tests, N_pages, k, sequence_length):
    uniform_gen = ug.UniformGenerator(N_pages, seed=42)
    DATA = {}

    Z_MAX = 800
    for i in range(N_tests):

        DATA[i] = {}
        algos = []
        for Z in [1] + list(range(5, Z_MAX, 5)):
            algos.append(lru.LRU(k, Z=Z))
            # algos.append(fifo.FIFO(k, Z=Z))
        request_sequence = uniform_gen.generate(sequence_length)
        # print(f"Request sequence = {request_sequence}")
        # optimal = belady.Belady(k, request_sequence)
        # cost_optimal = optimal.run()
        for algo in algos:
            cost_algo, misses_algo = algo.run(request_sequence)
            print(f"i = {i}, {algo.get_name()} cost = {cost_algo}, misses = {misses_algo}")
            DATA[i][algo.get_name()] = (cost_algo, misses_algo)

    fig, ax = plt.subplots()
    X = []
    Y = []
    Z_vals = [1] + list(range(5, Z_MAX, 5))

    lower = []
    upper = []
    for idx, algo in enumerate(algos):
        Z = Z_vals[idx]
        X.append(Z)
        data_algo = [DATA[i][algo.get_name()] for i in range(N_tests)]
        m, lm, hm = mean_confidence_interval([data[0]/data[1] for data in data_algo])
        Y.append(m)
        lower.append(lm)
        upper.append(hm)
    # for algo in algos:
    #     ax.plot(
    #         [i for i in range(N_tests)],
    #         [DATA[i][algo.get_name()] for i in range(N_tests)],
    #         label=algo.get_name(),
    #     )
    Y = np.array(Y)

    ax.plot(X, Y, 'k-')
    ax.plot(X, X, 'r--')    
    ax.set(xlabel="Z", ylabel="Avg penalty per miss")
    plt.fill_between(X,lower, upper)
    # ax.legend()
    plt.show()


N_tests = 30
N_pages = 100
k = 10
sequence_length = 1600
K_suite(N_tests, N_pages, k, sequence_length)
