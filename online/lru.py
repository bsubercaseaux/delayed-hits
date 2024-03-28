import online_api

class LRU(online_api.OnlineCaching):
    def __init__(self, k):
        super().__init__(k)
        
    def evict_non_optional(self, requested_page):
        last_use = {}
        evictable_pages = list(self.cache)
        for page in evictable_pages:
            last_use[page] = -1
        for i in range(len(self.previous_requests)):
            last_use[self.previous_requests[i]] = i
        lru_page = min(self.cache, key=lambda x: last_use[x])
        self.cache.remove(lru_page)