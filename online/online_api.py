class OnlineCaching:
    # k is the cache size
    def __init__(self, k, Z=1, optional_policy=False):
        self.cache = set()
        self.k = k
        self.penalty = 0
        self.Z = Z
        self.in_transit = {}
        self.pending_requests = {}
        self.arrival_times = {}
        self.page_by_arrival_time = {}
        self.tick = 0
        self.name = "Abstract Online Caching Algorithm"
        self.optional_policy = optional_policy
        self.previous_requests = []

    def evict_optional(self, requested_page):
        # implement the optional eviction policy
        pass
        
    def get_name(self):
        return self.name
    
    def evict_non_optional(self, requested_page):
        # implement the non-optional eviction policy
        pass
    
    def on_not_present(self, page):
        if page not in self.pending_requests:
            self.pending_requests[page] = []
        self.pending_requests[page].append(self.tick)
        if page not in self.arrival_times:
            self.arrival_times[page] = self.tick + self.Z
            self.page_by_arrival_time[self.tick + self.Z] = page
        
    def cache_page(self, page):
        self.cache.add(page)
    
    def on_request(self, page):
        self.previous_requests.append(page)
        if page not in self.cache:
            self.on_not_present(page)
            
        # from pending to cache
        if self.tick in self.page_by_arrival_time:
            p = self.page_by_arrival_time[self.tick]
            for occ in self.pending_requests[p]:
                self.penalty += self.tick - occ
            self.page_by_arrival_time.pop(self.tick)
            self.arrival_times.pop(p)
            self.pending_requests.pop(p)
            self.cache_page(p)
        
        # eviction
        if len(self.cache) > self.k: 
                # a page needs to be evicted
                if self.optional_policy:
                    self.evict_optional(page)
                else:
                    self.evict_non_optional(page)
                    
    def run(self, request_sequence, debug=False):
        for i, page in enumerate(request_sequence):
            if debug:
                print(f"i={i}, request for {request_sequence[i]}, tick = {self.tick}, arrival_times = {self.arrival_times}, page_by_arrival_time = {self.page_by_arrival_time}")
            self.on_request(page)
            if debug:
                print(f"i={i}, cache = {self.cache}, pending = {self.pending_requests} penalty = {self.penalty}")
            self.tick += 1
        return self.penalty