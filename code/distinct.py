import os

if __name__ == "__main__":
    api = set()

    path_prefix = "../data"
    for d in os.listdir(path_prefix):
        if d.endswith("valid.capi.dat"):
            with open(path_prefix + "/" + d, 'r') as f:
                for line in f.readlines():
                    l = line[:-1]
                    api.add(l)
    
    print(len(api))