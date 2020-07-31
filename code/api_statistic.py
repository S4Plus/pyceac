import os
import sys
import math

import api_check

class Project:
    def __init__(self, path_prefix, filename, full_set):
        self.path = path_prefix + '/' + filename
        self.name = filename.split(".capi.dat")[0]
        print("===== " + self.name + " =====")
        self.full_set = full_set

    def get_data(self):
        api_info = {}
        top = 10 # show top called apis in this project
        self.total = 0
        with open(self.path, 'r') as f:
            for line in f.readlines():
                l = line[:-1]
                if top > 0:
                    print(l)
                    top -= 1
                if top == 0:
                    print("...")
                    top -= 1
                num = int(l.split(":")[1].strip())
                name = l.split(":")[0].strip()
                if name in self.full_set:
                    api_info[name] = num
                    self.total += num
        print("all {} apis uesd for {} times in total\n".format(len(api_info), self.total))
        return api_info

# api_set must be a subset, e.g. intersection
def get_set_info(api_set, proj_api):
    api_set_info = {}
    for api in api_set:
        api_set_info[api] = 0
        for api_info in proj_api:
            api_set_info[api] += api_info[api]
    return api_set_info

def union(proj_api):
    api_sets = []
    for api_info in proj_api:
        api_set = set()
        for api in api_info.keys():
            api_set.add(api)
        api_sets.append(api_set)
    return set.union(*api_sets)

def intersection(proj_api):
    api_sets = []
    for api_info in proj_api:
        api_set = set()
        for api in api_info.keys():
            api_set.add(api)
        api_sets.append(api_set)
    return set.intersection(*api_sets)

class Py:
    def __init__(self, path):
        self.py_path = path
        self.macro_path = path.replace("capi", "macro")

    def get_full_set(self):
        print("load {}".format(self.py_path))
        macros = api_check.Macro(self.macro_path).get_macros()
        py = api_check.pycapi_comp.Python(self.py_path)
        all_apis = set(py.capi.keys())
        full_set = set.union(all_apis, macros)
        return full_set

# Jaccard similarity
def Jaccard(set_1, set_2):
    j = len(set.intersection(set_1, set_2)) / len(set.union(set_1,set_2))
    return round(j, 3)

# Ochiai coefficient
def Ochiai(set_1, set_2):
    k = len(set.intersection(set_1, set_2)) / math.sqrt(len(set_1) * len(set_2))
    return round(k, 3)

if __name__ == "__main__":
    print("remove apis not in all Python versions (probably be user-defined in default format)")
    py_paths = [
        "../data/python/Python-3.7.0.capi.dat",
        "../data/python/Python-3.6.0.capi.dat",
        "../data/python/Python-3.5.0.capi.dat",
        "../data/python/Python-3.4.0.capi.dat",
        "../data/python/Python-3.3.0.capi.dat",
        "../data/python/Python-3.2.capi.dat",
        "../data/python/Python-2.7.capi.dat",
    ]
    FS = set()
    for v in py_paths:
        py = Py(v)
        FS = set.union(FS, py.get_full_set())
    print("All these Python versions defined {} C-APIs functions (including from macros) in total".format(len(FS)))

    proj_api = [] # list contains info dicts of projects' apis
    proj_names = []
    proj_count = 0
    path_prefix = "../data"
    for d in os.listdir(path_prefix):
        if d.endswith(".capi.dat"):
            proj_count += 1
            proj = Project(path_prefix, d, FS)
            apis = proj.get_data()
            with open(path_prefix + "/" + proj.name + ".valid.capi.dat", 'w') as f:
                for (k, v) in apis.items():
                    f.write("{}\n".format(k))
            proj_api.append(apis)
            proj_names.append(proj.name[:15])

    print("===== statistic =====")

    apis_union = union(proj_api)
    print("{} project(s) used {} Python/C APIs".format(proj_count, len(apis_union)))

    apis_intersection = intersection(proj_api)
    print("{} APIs used by all the projects".format(len(apis_intersection)))
    intersection_info = get_set_info(apis_intersection, proj_api)
    intersection_info_sorted = sorted(intersection_info.items(), key = lambda d : d[1], reverse = True)
    for (k, v) in intersection_info_sorted:
        print("{} : {}".format(k, v))

    print("\nJaccard similarity")
    proj_num = len(proj_api)
    # Jaccard array
    # j12,j13,...,j1i
    # j23,...,j2i
    # ...
    # ji-1,i
    #lenJ = proj_num * (proj_names - 1) / 2
    #J = [-1] * lenJ
    J = []
    # dict to set
    proj_sets = []
    top = 300
    for d in proj_api:
        proj_sets.append(set(list(d.keys())[:top]))

    # format output
    stream = sys.stdout
    template = "{:^15} " * (proj_num + 1)
    proj_headnames = [""] + proj_names
    headerline = template.format(*proj_headnames)
    stream.write(headerline + "\n")

    i = 0
    while i < proj_num - 1:
        j = i + 1
        tmp = [proj_names[i]] + [""] * (i + 1)
        while j < proj_num:
            jaccard = Jaccard(proj_sets[i], proj_sets[j])
            J.append(jaccard)
            tmp.append(jaccard)
            j += 1
        i += 1
        stream.write(template.format(*tmp) + "\n")
    stream.write(proj_names[i] + "\n")
