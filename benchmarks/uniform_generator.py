import random
class UniformGenerator:
    def __init__(self, n, seed=1729):
        self.seed = seed
        self.n = n
        random.seed(self.seed)
        
    def generate(self, n_requests):
        return [random.randint(1, self.n) for _ in range(n_requests)]
        
        