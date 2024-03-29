# Parse IBM Object Store dataset from http://iotta.snia.org/traces/key-value into request sequence

class IBMGenerator:
    def __init__(self):
        datafile = 'IBMObjectStoreSample'
        requests = []        
        page_id_map = {}
        next_page_num = 0
        
        with open(datafile, 'r') as file:
            # Iterate over each line in the file
            for line in file:
                # Split the line by whitespace
                parts = line.strip().split()
                if len(parts) >= 4:
                    page_id = parts[2]
                    requests.append(page_id)
                    if page_id not in page_id_map:
                        page_id_map[page_id] = next_page_num
                        next_page_num += 1

        self.requests = [page_id_map[page_id] for page_id in requests]
        print("Parsed request sequence of length ", len(self.requests), " with ", len(page_id_map), " unique pages")
    
    def generate(self):
        return self.requests


IBM = IBMGenerator()
print(len(IBM.generate()))
