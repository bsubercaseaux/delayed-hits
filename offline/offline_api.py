class OfflineCaching:
    # k is the cache size
    def __init__(self, k, request_sequence, optional_policy=False):
        self.cache = set()
        self.penalty = 0
        self.k = k
        self.optional_policy = optional_policy
        self.request_sequence = request_sequence

    def evict_optional(self, index):
        # implement the optional eviction policy
        pass
        
    def evict_non_optional(self, index):
        # implement the non-optional eviction policy
        pass
    
    def on_request(self, index):
        page = self.request_sequence[index]
        if page not in self.cache:
            self.penalty += 1
            self.cache.add(page)
            if len(self.cache) > self.k:
                # a page needs to be evicted
                if self.optional_policy:
                    self.evict_optional(index)
                else:
                    self.evict_non_optional(index)
                    
    def run(self, debug=False):
        for i in range(len(self.request_sequence)):
            if debug:
                print(f"i={i}, request for {self.request_sequence[i]}")
            self.on_request(i)
            if debug:
                print(f"i={i}, cache = {self.cache}, penalty = {self.penalty}")
        return self.penalty