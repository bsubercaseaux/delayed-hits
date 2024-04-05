import online_api

class Belady(online_api.OnlineCaching):
    def __init__(self, k, Z, request_sequence):
        super().__init__(k, Z)
        self.request_sequence = request_sequence
        self.page_occs = {}
        self.process_page_occs()
        
    def process_page_occs(self):
        for i, page in enumerate(self.request_sequence):
            if page not in self.page_occs:
                self.page_occs[page] = []
            self.page_occs[page].append(i)
        for page in range(1, self.k+1):
            if page not in self.page_occs:
                self.page_occs[page] = []
        
    def evict_non_optional(self, requested_page):
        next_use = {}
        evictable_pages = list(self.cache)
        for page in evictable_pages:
            try:
                nuse = first_greater_than(self.page_occs[page], self.tick-1)
            except:
                print("page", page)
                print("page_occs", self.page_occs)
                raise
            next_use[page] = nuse[0] if nuse is not None else float("inf")
        # print("next_use", next_use)
        belady_page = max(self.cache, key=lambda x: next_use[x])
        # print("page to evict", belady_page)
        self.cache.remove(belady_page)
        

def first_greater_than(lst, value):
    # binary search as lst is sorted
    left = 0
    right = len(lst) - 1
    if right == -1:
        return None
    while left < right:
        m = (left + right) // 2
        if lst[m] > value:
            right = m
        else:
            left = m + 1
    if lst[left] > value:
        return left, lst[left]
    else:
        return None
    
ex_list = [2, 4, 7, 9, 13, 21, 27, 29, 35, 42]
assert first_greater_than(ex_list, 0)[1] == 2
assert first_greater_than(ex_list, 2)[1] == 4
assert first_greater_than(ex_list, 3)[1] == 4
assert first_greater_than(ex_list, 25)[1] == 27
assert first_greater_than(ex_list, 40)[1] == 42
assert first_greater_than(ex_list, 42) is None 
assert first_greater_than(ex_list, 45) is None 