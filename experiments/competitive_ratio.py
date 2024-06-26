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
import ibm_generator as ibg
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


def avg_penalty_per_miss_uniform(N_tests, N_pages, k, sequence_length):
    uniform_gen = ug.UniformGenerator(N_pages, seed=42)
    ibm_gen = ibg.IBMGenerator()
    DATA = {}
    IMDB_DATA = {}

    Z_MAX = 800
    Z_RANGE = [1] + list(range(5, Z_MAX, 5))
    for i in range(N_tests):

        DATA[i] = {}
        algos = []
        for Z in Z_RANGE:
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

    lower = []
    upper = []
    for idx, algo in enumerate(algos):
        Z = Z_RANGE[idx]
        X.append(Z)
        data_algo = [DATA[i][algo.get_name()] for i in range(N_tests)]
        m, lm, hm = mean_confidence_interval([data[0]/data[1] for data in data_algo])
        Y.append(m)
        lower.append(lm)
        upper.append(hm)

    ibm_request_sequence = ibm_gen.generate()
    Y_2 = []
    for Z in Z_RANGE:
        alg = lru.LRU(k, Z=Z)
        IMDB_DATA[Z] = alg.run(ibm_request_sequence)
        Y_2.append(IMDB_DATA[Z][0]/IMDB_DATA[Z][1])

    # for algo in algos:
    #     ax.plot(
    #         [i for i in range(N_tests)],
    #         [DATA[i][algo.get_name()] for i in range(N_tests)],
    #         label=algo.get_name(),
    #     )
    Y = np.array(Y)
    Y_2 = np.array(Y_2)

    ax.plot(X, Y, 'k-')
    ax.plot(X, X, 'r--')
    ax.plot(X, Y_2, 'b-')
    ax.set(xlabel="Z", ylabel="Avg penalty per miss")
    plt.fill_between(X,lower, upper)
    # ax.legend()
    plt.show()


N_tests = 30
N_pages = 100
k = 10
sequence_length = 1600
avg_penalty_per_miss_uniform(N_tests, N_pages, k, sequence_length)
