import subprocess

class Python:
    def __init__(self, path):
        self.header_path = path + "/Include/Python.h"
        self.version = path[path.rfind("/") + 1:]
        self.capi = set()
        self._capi_name = set()
        self.macro = set()
        self.get_header(self.header_path)

    def _get_macro(self, cmd_output, sys_def):
        for l in cmd_output:
            line = bytes.decode(l[:-1])
            if line.startswith("#define"):
                symbol = line[8:].split(" ")[0]
                definition = line[8:].split(" ")[1]
                pos = symbol.find("(")
                if definition in self.macro or definition in self._capi_name or definition in sys_def:
                    if pos == -1:
                        name = symbol
                        if name.startswith("Py"):
                            self.macro.add(name)

    def get_header(self, header_file):
        cmd = "./function_prototype/build/function-prototype " + header_file + " -Ifake_include"
        cmd_result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        for l in cmd_result.stdout.readlines():
            api = bytes.decode(l[:-1])
            self._add_capi(api)
            self._capi_name.add(api.split(",")[1].split("(")[0])
        
        # handle functions defined in macro
        macro_cmd = "clang " + header_file + " -E -dM -Ifake_include"
        macro_cmd_result = subprocess.Popen(macro_cmd, stdout=subprocess.PIPE, shell=True)
        save_result = macro_cmd_result.stdout.readlines()
        for l in save_result:
            line = bytes.decode(l[:-1])
            if line.startswith("#define"):
                symbol = line[8:].split(" ")[0]
                pos = symbol.find("(")
                if pos != -1: # exclude variables
                    name = symbol[:pos]
                    if name.startswith("Py"):
                        self.macro.add(name)
        sys_def = ["malloc", "realloc", "free", "calloc"]
        # for macro functions defined in the way of:
        # #define PyMem_DEL PyMem_FREE/free
        self._get_macro(save_result, sys_def)
        #define PyMem_DEL PyMem_FREE
        #define PyMem_FREE free
        self._get_macro(save_result, sys_def)

    def _add_capi(self, api):
        function_name = api.split(",")[1].split("(")[0]
        # user-visible symbols, exclude internal use by the Python implementation (_Py)
        if function_name.startswith("Py"):
            self.capi.add(api)

if __name__ == "__main__":
    with open("python-path.txt", 'r') as f:
        print("Getting Python/C APIs from ...")
        for l in f.readlines():
            path = l[:-1] if l.endswith("\n") else l
            python = Python(path)
            print("  {}".format(python.version))

            # write to file
            prefix = "../data/python/"
            suffix = ".capi.dat"
            with open(prefix + python.version + suffix, 'w') as f:
                # sorted by function name
                for api in sorted(list(python.capi), key = lambda a : a.split(",")[1].split("(")[0]):
                    f.write(api + "\n")
            # write macro
            macro_suffix = ".macro.dat"
            with open(prefix + python.version + macro_suffix, 'w') as f:
                for name in sorted(list(python.macro)):
                    f.write(name + "\n")