import sys

def Jaccard(set_1, set_2):
    j = len(set.intersection(set_1, set_2)) / len(set.union(set_1,set_2))
    return round(j, 3)

if __name__=="__main__":
    proj_1 = sys.argv[1]
    proj_2 = sys.argv[2]
    
    set_1 = set()
    set_2 = set()

    with open(proj_1, 'r') as f:
        for line in f.readlines():
            l = line[:-1]
            name = l.split(":")[0].strip()
            set_1.add(name)

    with open(proj_2, 'r') as f:
        for line in f.readlines():
            l = line[:-1]
            name = l.split(":")[0].strip()
            set_2.add(name)

    j = Jaccard(set_1, set_2)
    print(j)