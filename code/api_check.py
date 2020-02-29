import argparse

import pycapi_comp

class Project:
    def __init__(self, path):
        self.path = path

    def get_apis(self):
        apis = set()
        with open(self.path, 'r') as f:
            for l in f.readlines():
                api = l.split(":")[0].strip()
                if api.find("__") == -1: # PyInit__modulename is the default PyMODINIT_FUNC
                    apis.add(api)
        return apis

class Macro:
    def __init__(self, path):
        self.path = path
        print("load macros from : {}".format(path))

    def get_macros(self):
        macros = set()
        with open(self.path, 'r') as f:
            for l in f.readlines():
                macros.add(l[:-1])
        return macros

if __name__ == "__main__":
    # arguments setting
    ap = argparse.ArgumentParser()
    ap.add_argument("project_data", help=".dat file path of project to be checked")
    ap.add_argument("python_data", help=".dat file path of generated python/c api")

    args = vars(ap.parse_args())
    proj_path = args["project_data"]
    py_path = args["python_data"]
    macro_path = py_path.replace("capi", "macro")
            
    proj_apis = Project(proj_path).get_apis()
    macros = Macro(macro_path).get_macros()
    py = pycapi_comp.Python(py_path)
    all_apis = set(py.capi.keys())
    full_set = set.union(all_apis, macros)

    if proj_apis.issubset(full_set):
        print("Pass!")
    else:
        diff = proj_apis.difference(full_set)
        for api in diff:
            print(api)
        print("{} API out of {} C-APIs".format(len(diff), py.version))
