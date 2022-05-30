# 3 My hash table WITHOUT rolling hashing

class MyHashTableNode2():
    
    def __init__(self, key, value):
        """Initializes a hash table node, a key-value pair"""
        self.key = key # the substring
        self.value = value # the index it starts in
        
    def __repr__(self):
        """Overrides the default implementation of print"""
        return f"({self.key}, {self.value})"

class MyHashTable2():
    
    def __init__(self, capacity, hash_function):
        """Intializes a hash table with size m"""
        self.m = capacity
        self.hash_table = [None for _ in range(capacity)]
        self.hash_function = hash_function
        
    def __repr__(self):
        """Overrides the default implementation of print"""
        return f"{self.hash_table}"
    
    def norm(self, char):
        """Codes a character into ASCII and normalizes to 1-26"""
        return ord(char)-ord('a')+1    
    
    def hf_rabinkarp(self, key):
        """Converts the first key into an index using the Rabin-Karp hash function"""
        hash_val = 0
        i = len(key)-1 # k = len(k)
        
        for char in key:
            char_val = self.norm(char) # normalize the character
            hash_val += char_val * 26**i # base 26
            i -= 1 
            
        return hash_val % self.m # modulo the table size
    
    def hf_djb2(self, string):  
        """Converts a key into an index using the djb2 hash function"""
        hash_val = 5381
        for x in string:
            hash_val = (( hash_val << 5) + hash_val) + ord(x)
            
        return hash_val & 0xFFFFFFFF % self.m
    
    def hf_sdbm(self, string):
        """Converts a key into an index using the sdbm hash function"""
        hash_val = 0
        for plain_chr in string:
            hash_val = ord(plain_chr) + (hash_val << 6) + (hash_val << 16) - hash_val
            
        return hash_val % self.m
    
    def probing_sequence(self, key, hash_val, i, method):
        """
        Probes empty slot using linear/ quadratic/ double hashing: 
            - prev_value is implicitly computed by hash_function1
            - hash_function2 (below) = hash_function1*31 + ord(key[i % k])
            
        Input:
            - key: str, substring of length k
            - prev_value: int, previous hash value
            - i: int, the i-th probe
            - method: str, "linear", "quadratic", or "double"
            """
        if method == "linear":
            return (hash_val + (i+1)) % self.m
        
        if method == "quadratic":
            return (hash_val + (i+1) + (i+1)**2) % self.m
        
        if method == "double":
            return (hash_val*31 + ord(key[(i+1) % len(key)])) % self.m
    
    def insert(self, x, k, method_probe):
        """
        Inserts x's substring using rolling hashing to compute hash value and 
        probes using double hashing to address collision
        
        Input:
            - x: str
            - k: int, length of substring
            - method_probe: str, method of probing (linear/ quadratic/ double)
        """
        
        probes = []
        
        for i in range(0, len(x)-k+1):
            
            window = x[i:i+k]
            
            if self.hash_function == "rabinkarp":
                hash_val = self.hf_rabinkarp(window)
            if self.hash_function == "djb2":
                hash_val = self.hf_djb2(window)
            if self.hash_function == "sdbm":
                hash_val = self.hf_sdbm(window)
            
            n_probe = 0
            probe_val = hash_val
            
            while n_probe < self.m:
                
                # if indexing with the hash value results None, place the key-value pair at that index
                if self.hash_table[probe_val] is None:
                    self.hash_table[probe_val] = MyHashTableNode(window, (i, hash_val))
                    break
                    
                # else if an key-value pair is already present, probe with double hashing
                else:
                    probe_val = self.probing_sequence(window, hash_val, n_probe, method_probe)
                    n_probe += 1 # increase the number of probe by 1
                    
            probes.append(n_probe)
            
        return probes
        
    def search(self, y, k, method_probe):
        """
        Computes y's substring's hash value with rolling hashing and check match in x's hash table
        
        Input:
            - y: str
            - k: int, length of substring
            - method_probe: str, method of probing (linear/ quadratic/ double)
            
        Output:
            - matches: list, list of tuples (i, j, string)
            - probes: list, list of int (number of probes)
        """
        
        matches = [] # initialize empty list to store matches
        probes = [] # initialize probe list
        
        for j in range(0, len(y)-k+1):
            
            window = y[j:j+k]
            
            if self.hash_function == "rabinkarp":
                hash_val = self.hf_rabinkarp(window)
            if self.hash_function == "djb2":
                hash_val = self.hf_djb2(window)
            if self.hash_function == "sdbm":
                hash_val = self.hf_sdbm(window)

            # if the window's hash value matches with a hash value in the hash table
            if self.hash_table[hash_val] is not None:
                
                n_probe = 0
                probe_val = hash_val
                
                while n_probe < self.m and self.hash_table[probe_val] is not None:
                    
                    string = self.hash_table[probe_val].key
                    
                    # and if both hash value and string matches, a match is found and appended
                    if window == string:
                        
                        i = self.hash_table[probe_val].value[0] # starting index in x
                        matches.append((i, j, string))
                    
                    # probe next value anyways as more than one match for the same window is possible
                    probe_val = self.probing_sequence(window, hash_val, n_probe, method_probe)
                    n_probe += 1
                            
                probes.append(n_probe)
                        
            else:
                probes.append(0) # append 0 probe if no element found
                
        return matches, probes
