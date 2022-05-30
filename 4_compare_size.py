import time
import random
import string
import matplotlib.pyplot as plt

def get_table_size(x, constant):
    """Determines the hash table size dynamically based on input string and a constant multiplier"""
    x_length = len(x) # get length of input string x
    table_size = int(x_length * constant) # multiple by some factor between 1-2 and floor it
    prime = get_next_prime(table_size) # get the next prime of this length
    
    return prime

def get_load_factor(x, table_size):
    """Computes the load factor (n elements)/(m slots)"""
    return len(x)/table_size
    
def get_next_prime(n):
    """Gets the next prime with a given integer"""
    notprime = [num for num in range (n+1, n+200)]
    isprime = []
        
    for num in notprime:
        val_is_prime = True

        for x in range(2, num-1):
            if num % x == 0:
                val_is_prime = False
                break
                
        if val_is_prime:
            isprime.append(num)
            break
            
    return min(isprime)

def get_random_string(length):
    """Generates a random string in lowercase of a specified length"""
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(length))
    return result 

# plotting 

load_factors = []
constants = [1 + i/100 for i in range(1, 501)]

for constant in constants:
    random_str = get_random_string(100)
    size = get_table_size(random_str, constant)
    load = get_load_factor(random_str, size)
    load_factors.append(load)
    
plt.plot(constants, load_factors)
plt.title("change in load factor over the constant multiplier")
plt.xlabel("constant multiplier of input size")
plt.ylabel("load factor")
plt.show()
