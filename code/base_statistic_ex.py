import os
import subprocess

def check_suffix(filepath):
    suffix = [".h", ".i", ".c", ".cc", "cpp"] # .i used by tensorflow for helper macros and typemaps
    for s in suffix:
        if filepath.endswith(s):
            return 1
    return 0

def get_file_loc(filepath):
    cmd = "cloc " + filepath
    cmd_result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    cloc_info = cmd_result.stdout.readlines()
    text = bytes.decode(cloc_info[-2]).split(" ")[-1].strip()
    return int(text) if text != "" else 0

class Project:
    def __init__(self, paths):
        self.statistic = {}
        self.loc = 0
        for path in paths:
            self.search_file(path)

    def search_file(self, path):
        for i in os.listdir(path):
            child = path + "/" + i
            if os.path.isfile(child):
                if check_suffix(child):
                    print(child)
                    self.loc += get_file_loc(child)
                    self.get_statistic(child)
            if os.path.isdir(child):
                self.search_file(child)
        
    def get_statistic(self, filename):
        cmd = "./token_processor/build/token-processor " + filename
        cmd_result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        for l in cmd_result.stdout.readlines():
            line = bytes.decode(l)[:-1]
            if line.startswith("Py") or line.startswith("PY"):
                if line in self.statistic:
                    self.statistic[line] += 1
                else:
                    self.statistic[line] = 1

if __name__=="__main__":
    tensorflow_path = [
        "../corpus/tensorflow/tensorflow/tensorflow/python",
        "../corpus/tensorflow/tensorflow/tensorflow/lite/python"
    ]

    pytorch_path = [
        "../corpus/pytorch/pytorch/caffe2/python",
        "../corpus/pytorch/pytorch/torch/csrc"
    ]

    projs = {"tensorflow": tensorflow_path, "pytorch": pytorch_path}
    for (name, path) in projs.items():
        print("===== {} =====".format(name))
        proj = Project(path)
        print("interface loc : {}".format(proj.loc))
        apis = proj.statistic
        apis_sorted = sorted(apis.items(), key = lambda d : d[1], reverse = True)
        path_prefix = "../data/"
        suffix = ".capi.dat"
        with open(path_prefix + name + suffix, 'w') as f:
            for (k, v) in apis_sorted:
                f.write("{}:{}".format(k, v) + '\n')
