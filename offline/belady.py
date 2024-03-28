import offline_api

class Belady(offline_api.OfflineCaching):
    def __init__(self, k, request_sequence):
        super().__init__(k, request_sequence)
        
    def evict_non_optional(self, index):
        requested_page = self.request_sequence[index]
        next_use = {}
        evictable_pages = list(self.cache)
        for page in evictable_pages:
            next_use[page] = len(self.request_sequence)
        for i in range(index + 1, len(self.request_sequence)):
            p = self.request_sequence[i]
            if p in next_use:
                next_use[p] = min(next_use[p], i)
        belady_page = max(self.cache, key=lambda x: next_use[x])
        self.cache.remove(belady_page)
    