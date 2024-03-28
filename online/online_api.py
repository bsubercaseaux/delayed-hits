class OnlineCaching:
    # k is the cache size
    def __init__(self, k, optional_policy=False):
        self.cache = set()
        self.k = k
        self.penalty = 0
        self.optional_policy = optional_policy
        self.previous_requests = []

    def evict_optional(self, requested_page):
        # implement the optional eviction policy
        pass
        
    def evict_non_optional(self, requested_page):
        # implement the non-optional eviction policy
        pass
    
    def on_request(self, page):
        self.previous_requests.append(page)
        if page not in self.cache:
            self.penalty += 1
            self.cache.add(page)
            if len(self.cache) > self.k: 
                # a page needs to be evicted
                if self.optional_policy:
                    self.evict_optional(page)
                else:
                    self.evict_non_optional(page)
                    
    def run(self, request_sequence, debug=False):
        for i, page in enumerate(request_sequence):
            if debug:
                print(f"i={i}, request for {request_sequence[i]}")
            self.on_request(page)
            if debug:
                print(f"i={i}, cache = {self.cache}, penalty = {self.penalty}")
        return self.penalty