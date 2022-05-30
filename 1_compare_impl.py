# Python dictionary

def norm(char):
    """Codes a character into ASCII and normalizes to 1-26"""
    return ord(char)-ord('a')+1

def rk_hash_function(t, k, p, q):
    """Calculates the hash value for the first window using the Rabin-Karp method"""
    
    hash_val = 0
    i = k-1
    
    for char in t:
        char_val = norm(char) # normalize the coding of the letter
        hash_val += char_val * p**i # multiplie by base p^i
        i -= 1 # decrease the power by 1
        
    return hash_val % q

def rk_rolling_hash(string, prev_hash_val, prev_window, next_window_idx, k, p, q):
    """Returns next hash value and next window given the previous of those using Rabin-Karp method"""
    
    next_hash_val = prev_hash_val - norm(prev_window[0])*p**(k-1) # remove the hash value of first char 
    next_hash_val *= p # shift the window to the right by 1 unit
    next_window = string[next_window_idx:next_window_idx+k] # slice out the new window
    next_hash_val += norm(next_window[-1]) # add the hash value of the last char
    next_hash_val = next_hash_val % q
    
    return next_hash_val, next_window

def dict_insert(x, k, p, q):
    """
    Hashes all length-k substrings of x into a Python dict using rolling hashing.
    
    Input:
        - x: strings
        - k: int, length of substring
        - p: the base to multiply with in the Rabin-Karp method
        - q: the module value, a prime
        
    Output:
        - the hash table used to store x with: 
            (key, value) = (hash value, (substring, starting index)) - nested tuple
    
    """
    
    hash_table = {} # initialize empty dictionary
    
    window = x[:k] # slice out a copy of the first window
    hash_val = rk_hash_function(window, k, p, q) # compute hash value of first window
    hash_table[hash_val] = (window, 0) # update dictionary with key as hash_val and value as (substring, starting index)
    
    for i in range(1, len(x)-k+1): # len(x)-k is the number of windows left
        
        # perform rolling hashing
        next_hash_val, next_window = rk_rolling_hash(x, hash_val, window, i, k, p, q)
        hash_val, window = next_hash_val, next_window # update variable for iteration

        # update history
        if hash_val not in hash_table:
            hash_table[hash_val] = (window, i)
        elif isinstance(hash_table[hash_val], list):
            hash_table[hash_val].append((window, i))
        else:
            hash_table[hash_val] = [hash_table[hash_val], (window, i)]
        
    return hash_table

def dict_search(y, dict_x, k, p, q):
    """
    Computes hash value of y's substring using rolling hashing and uses it to try indexing
    the x's dictionary.
    
    Input:
        - x, y: strings
        - k: int, length of substring
        - p: the base to multiply with in the Rabin-Karp method
        - q: the module value, a prime
    Output:
        - A list of tuples (i, j, substring) where x[i:i+k] = y[j:j+k]
        - substring is the pattern common to both x and y
    
    """
    
    window = y[:k] # slice out a copy of the first window
    hash_val = rk_hash_function(window, k, p, q) # compute hash value of first window
    matches = [] # intialize empty list to store matches
    
    # try indexing x's dictionary with y's hash value using rolling hashing
    if hash_val not in dict_x:
        pass

    elif isinstance(dict_x[hash_val], list):
        for duplicate in dict_x[hash_val]:
            matches.append((duplicate[1], 0, window))

    else:
        matches.append((dict_x[hash_val][1], 0, window))
    
    for j in range(1, len(y)-k+1):
                          
        # perform rolling hashing
        next_hash_val, next_window = rk_rolling_hash(y, hash_val, window, j, k, p, q)
        hash_val, window = next_hash_val, next_window # update variables for iteration
            
        # try indexing x's dictionary with y's hash value using rolling hashing
        if hash_val not in dict_x:
            pass
        
        elif isinstance(dict_x[hash_val], list):
            for duplicate in dict_x[hash_val]:
                matches.append((duplicate[1], j, window))
                
        else:
            matches.append((dict_x[hash_val][1], j, window))
    
    return matches
        
        
def dict_main(x, y, k, p, q):
    """Orchestrates dict_hash() and dict_lookup() functions"""
    
    dict_x = dict_insert(x, k, p, q) # store x's substring in a dictionary
    matches = dict_search(y, dict_x, k, p, q) # return all matches between x and y
    
    return matches
  

  

import time

lengths = [i for i in range(100, 2001, 50)]

avg_python = []
avg_ht1 = []
avg_ht2 = []

for length in lengths:
    
    python = []
    ht1 = []
    ht2 = []
    
    for j in range(50):
    
        x = get_random_string(length)
        y = get_random_string(length)
        k = 10
        size = get_table_size(x, 1.7)

        start = time.time()
        _ = dict_main(x, y, k, 26, size)
        end = time.time()
        python.append(end-start)

        start = time.time()
        ht_one = MyHashTable(size)
        _ = ht_one.insert(x, k, "double")
        _ = ht_one.search(y, k, "double")
        end = time.time()
        ht1.append(end-start)

#         start = time.time()
#         print(f"{length}, {j} time starts")
#         ht_two = MyHashTable2(size, "djb2")
#         print("\ttable initialized")
#         _ = ht_two.insert(x, k, "double")
#         print("\ttable inserted")
#         _ = ht_two.search(y, k, "double")
#         print("\ttable searched")
#         end = time.time()
#         print(f"{length}, {j} time ends")
#         ht2.append(end-start)
        
    avg_python.append(sum(python)/30)
    avg_ht1.append(sum(ht1)/30)
#     avg_ht2.append(sum(ht2)/30)

plt.plot(lengths, avg_python, color="green", label="python")
plt.plot(lengths, avg_ht1, color="blue", label="MyHashTable")
# plt.plot(lengths, avg_ht2, color="red", label="MyHashTable2")
plt.title("time spent on string-matching")
plt.xlabel("input length")
plt.ylabel("time")
plt.legend()
plt.show()
