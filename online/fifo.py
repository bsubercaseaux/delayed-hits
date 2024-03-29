import online_api

class FIFO(online_api.OnlineCaching):
    def __init__(self, k, Z=1):
        super().__init__(k, Z)
        self.name = f"FIFO (Z={Z})"
        self.cache = []
        
    def cache_page(self, page):
        self.cache.append(page)
        
    def evict_non_optional(self, requested_page):
        self.cache.pop(0)