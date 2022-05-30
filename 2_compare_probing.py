probe_methods = ["linear", "quadratic", "double"]

linear = []
quadratic = []
double = []
lengths = [length for length in range(100, 1001, 50)]

for method in probe_methods:
    for length in lengths:
        
        avg_probe = []
        for i in range(100):
            x = get_random_string(length)
            size = get_table_size(x, 1.6)
            ht = MyHashTable(size)
            x_probes = ht.insert(x, k, method)
            avg_probe.append(sum(x_probes))

        if method == "linear":
            linear.append(sum(avg_probe)/100)
        if method == "quadratic":
            quadratic.append(sum(avg_probe)/100)
        if method == "double":
            double.append(sum(avg_probe)/100)

plt.plot(lengths, linear, label="linear probing")
plt.plot(lengths, quadratic, label="quadratic probing")
plt.plot(lengths, double, label="double hashing")
plt.title("probes when inserting x into hash table at various lengths")
plt.xlabel("length of input string x")
plt.ylabel("average sum of probes")
plt.legend()
plt.show()
