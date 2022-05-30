# test case 1 - random characters

x, y, k = "aastoiasdffffkfioveeaf", "aastuveoaisdfioweaf", 3
ht = MyHashTable2(40, "rabinkarp")
x_probes = ht.insert(x, k, "linear")
matches, y_probes = ht.search(y, k, "linear")

assert matches == [(0, 0, 'aas'), (1, 1, 'ast'), (7, 10, 'sdf'), (14, 12, 'fio'), (19, 16, 'eaf')]

# test case 2 - same characters

x, y = "eeeeeeeeeeeeeeeeeeeeeeeeeee", "eeeeeeeeeeeeeeeeeeeeee"
k = len(y)
ht = MyHashTable2(25, "djb2")
x_probes = ht.insert(x, k, "quadratic")
matches, y_probes = ht.search(y, k, "quadratic")

assert matches == [(0, 0, 'eeeeeeeeeeeeeeeeeeeeee'), (1, 0, 'eeeeeeeeeeeeeeeeeeeeee'), (2, 0, 'eeeeeeeeeeeeeeeeeeeeee'), (3, 0, 'eeeeeeeeeeeeeeeeeeeeee'), (4, 0, 'eeeeeeeeeeeeeeeeeeeeee'), (5, 0, 'eeeeeeeeeeeeeeeeeeeeee')]

# test case 3 - real plagiarised text

x = "The legal system is made up of civil courts, criminal courts and specialty courts, such as family law courts and bankruptcy courts. Each court has its own jurisdiction, which refers to the cases that the court is allowed to hear. In some instances, a case can only be heard in one type of court. For example, a bankruptcy case must be heard in a bankruptcy court. In other instances, more than one court could potentially have jurisdiction. For example, a federal criminal court and a state criminal court would each have jurisdiction over a crime that is a federal drug offense but that is also a state offense.".replace("!", "").replace("?", "").replace(".", "").replace(",", "").replace(";", "").replace(" ", "").lower()
y = "The legal system is made up of criminal and civil courts and specialty courts like bankruptcy and family law courts. Each court is vested with its own jurisdiction. Jurisdiction refers to the types of cases the court is permitted to rule on. Sometimes, only one type of court can hear a particular case. For instance, bankruptcy cases can be ruled on only in bankruptcy court. In other situations, it is possible for more than one court to have jurisdiction. For instance, both a state and federal criminal court could have authority over a criminal case that is also considered an offense under federal and state drug laws.".replace("!", "").replace("?", "").replace(".", "").replace(",", "").replace(";", "").replace(" ", "").lower()
k = 25
ht = MyHashTable2(len(x)*2, "sdbm")
x_probes = ht.insert(x, k, "double")
matches, y_probes = ht.search(y, k, "double")

assert matches == [(0, 0, 'thelegalsystemismadeupofc'), (42, 39, 'lcourtsandspecialtycourts')]
