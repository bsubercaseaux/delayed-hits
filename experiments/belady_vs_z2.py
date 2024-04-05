import matplotlib.pyplot as plt
import numpy as np
from importmonkey import add_path

import time
import scipy.stats

add_path("../online")
add_path("../benchmarks")
add_path("../../K_Server")
import belady
import ibm_generator as ibg
import uniform_generator as ug
import delayed_hits as dh_kserver

ibm_gen = ibg.IBMGenerator()

ibm_request_sequence = ibm_gen.generate()[:100]


def comparison_ibm_data(k):

    bldy = belady.Belady(k, 2, ibm_request_sequence)  # Z=2
    ti = time.perf_counter_ns()
    cost_belady = bldy.run(ibm_request_sequence)
    tf = time.perf_counter_ns()
    print(f"Belady: cost = {cost_belady}, time = {(tf-ti)/1e9} [s]")

    answer = dh_kserver.solveZ2(ibm_request_sequence, k)
    print(answer)


S_RANGE = range(10, 120, 5)
def comparison_ug(k, N_pages):
    uniform_gen = ug.UniformGenerator(N_pages, seed=42)
    DATA = {}
    for S in S_RANGE:
        request_sequence = uniform_gen.generate(S)
        #print(request_sequence)
        bldy = belady.Belady(k, 2, request_sequence)  # Z=2
        ti = time.perf_counter_ns()
        cost_belady = bldy.run(request_sequence)
        tf = time.perf_counter_ns()
        DATA[S] = {'belady': {'cost': cost_belady[0], 'time': (tf-ti)/1e9}}
        print(f"Belady: cost = {cost_belady}")
        kserver_answer = dh_kserver.solveZ2(request_sequence, k)
        DATA[S]['kserver'] = {'cost': kserver_answer['cost'], 'time': kserver_answer['time_net']}
        print("K-Server answer: ", kserver_answer)
    return DATA

    
DATA = comparison_ug(5, 10)
print(DATA)
with open('belady_vs_kserver.dict', 'w') as f:
    f.write(str(DATA))
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,8))
X = list(S_RANGE)
Y_cost_belady = []
Y_cost_kserver = []
Y_time_belady = []
Y_time_kserver = []
for x in X:
    belady_data = DATA[x]['belady']
    Y_cost_belady.append(belady_data['cost'])
    Y_time_belady.append(belady_data['time'])
    kserver_data = DATA[x]['kserver']
    Y_cost_kserver.append(kserver_data['cost'])
    Y_time_kserver.append(kserver_data['time'])

ax1.set(xlabel="Length of request sequence", ylabel="Total penalty")
ax2.set(xlabel="Length of request sequence", ylabel="Time [s]")
ax1.plot(X, Y_cost_belady,"r-", label='Belady')
ax1.plot(X, Y_cost_kserver, "g-", label='K-server')
ax2.plot(X, Y_time_belady, "r-", label='Belady')
ax2.plot(X, Y_time_kserver, "g-", label='K-server')
ax1.legend()
ax2.legend()
plt.show()
# for k in range(20, len(ibm_request_sequence) // 2):
#     print(f"Cache size = {k}")
#     comparison_ibm_data(k)
#     print("---------------------------------\n")
