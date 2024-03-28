from importmonkey import add_path
add_path("../online")
add_path("../offline")
add_path("../benchmarks")
import uniform_generator as ug
import lru 
import belady

N_tests = 100
N_pages = 6
k = 5
sequence_length = 5000

uniform_gen = ug.UniformGenerator(N_pages, seed=42)
for i in range(N_tests):
    request_sequence = uniform_gen.generate(sequence_length)
    
    lru_cache = lru.LRU(k)
    optimal = belady.Belady(k, request_sequence)
    
    cost_lru = lru_cache.run(request_sequence)
    cost_optimal = optimal.run()
    print(f"i = {i}, ratio = {cost_lru/cost_optimal}")
    