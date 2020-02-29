import subprocess

def check_suffix(filepath):
    # return:
    # 0 for invalid
    # 1 for header
    # 2 for non-header
    header_suffix = [".h", ".i"] # .i used by tensorflow for helper macros and typemaps
    non_header_suffix = [".c", ".cc"]
    for s in header_suffix:
        if filepath.endswith(s):
            return 1
    for s in non_header_suffix:
        if filepath.endswith(s):
            return 2
    return 0

def get_file_loc(filepath):
    cmd = "cloc " + filepath
    cmd_result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    cloc_info = cmd_result.stdout.readlines()
    return bytes.decode(cloc_info[-2]).split(" ")[-1].strip()

class Project:
    def __init__(self, path):
        self.path = path
        self.name = path[path.rfind("/") + 1:]
        print("===== {} =====".format(self.name))
        self.module_file_list = []
        self._have_checked = []
        self.get_module_file("Python.h")
        #self.get_module_file("tensorflow/c/c_api.h")
        self.statistic = {}

    def get_total_loc(self):
        cmd = "cloc " + self.path
        #subprocess.Popen(cmd, shell=True)
        cmd_result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        cloc_info = cmd_result.stdout.readlines()
        return bytes.decode(cloc_info[-2]).split(" ")[-1].strip()

    # A file can be an interface file if
    # 1) it includes "Python.h"
    # or, 2) it includes another interface file.
    def get_module_file(self, keyword):
        print("search using header : {}".format(keyword))
        cmd = "grep -rn \"[#,%]include [<,\\\"]\S*" + keyword.replace(".", "\.") + "\" " + self.path
        cmd_result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        module_files = cmd_result.stdout.readlines()
        for m in module_files:
            f = bytes.decode(m).split(":")[0]
            if f in self._have_checked:
                continue
            v = check_suffix(f)
            if (v):
                self.module_file_list.append(f)
                if (v == 1):
                    # search for case 2), non-header file cannot be included
                    new_kw = f[f.rfind("/") + 1:]
                    #new_kw = f[f.find(self.path) + len(self.path) + 1:]
                    self.get_module_file(new_kw)
            self._have_checked.append(f)

    def get_statistic(self):
        for f in set(self.module_file_list):
            cmd = "./token_processor/build/token-processor " + f
            cmd_result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            for l in cmd_result.stdout.readlines():
                line = bytes.decode(l)[:-1]
                if line.startswith("Py") or line.startswith("PY"):
                    if line in self.statistic:
                        self.statistic[line] += 1
                    else:
                        self.statistic[line] = 1
        return self.statistic

if __name__=="__main__":
    with open("corpus-path.txt", 'r') as f:
        proj_count = 0
        proj_api = [] # a list contains api info of every project (a dict)
        for project_path in f.readlines():
            proj_count += 1
            project_path = project_path[:-1] if project_path.endswith("\n") else project_path
            if project_path.startswith("#"):
                continue
            project = Project(project_path)

            print("total loc : {}".format(project.get_total_loc()))
            interface_loc = 0

            module_file_list = project.module_file_list
            for module_file in set(module_file_list):
                print(module_file)
                interface_loc += int(get_file_loc(module_file))
            
            print("interface loc : {}".format(interface_loc))

            api_count = 0
            statistic = project.get_statistic()
            statistic_sorted = sorted(statistic.items(), key = lambda d : d[1], reverse = True)
            proj_api.append(statistic)
            for (k, v) in statistic_sorted:
                api_count += 1
                #print("{} : {}".format(k, v))
            #print("number of used apis : {}".format(api_count))
            # write to file
            path_prefix = "../data/"
            suffix = ".capi.dat"
            with open(path_prefix + project.name + suffix, 'w') as f:
                for (k, v) in statistic_sorted:
                    f.write("{}:{}".format(k, v) + '\n')
