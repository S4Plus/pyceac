import sys
import subprocess
import linecache

targets = [
    "strcpy",
    # "strcat",
    # "memcpy",
    # "fscanf",
    # "malloc",
    # "calloc"
]

py_targets = [
    "PyArg_ParseTuple",
    #"PyArg_ParseTupleAndKeywords",
    "PyArg_Parse"
]

# string -> string list
def exec_command(command):
    output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, encoding="UTF-8")
    return output.stdout.readlines()

# string -> (string, int, string)
def grep_parser(grep_line):
    pos_filename = grep_line.find(":")
    filename = grep_line[0:pos_filename]
    pos_lineno = grep_line[pos_filename + 1:].find(":") + pos_filename + 1
    lineno = int(grep_line[pos_filename + 1:pos_lineno])
    content = grep_line[pos_lineno + 1:-1]
    return (filename, lineno, content)

# string, string -> None 
def check(api, path):
    command = "grep -rn \"" + api + "(\" " + path
    
    for line in exec_command(command):
        #(filename, lineno, content) = grep_parser(line)
        print(line.strip())

# string -> string
def fmt_parser(fmt):
    pos = fmt.find(":")
    if pos == -1:
        return fmt[1:-1]
    else:
        return fmt[1:pos]

# string -> bool
def fmt_checker(fmt):
    rules = ['b', 'B', 'H', 'I', 'K', 'k'] # 8: integer overflow
    #rules = ['i'] # used for int -> Py_ssize_t, 10-2: API evolution
    for ch in fmt:
        if ch in rules:
            return True
    return False

# string, string -> None 
def py_check(api, path):
    command = "grep -rn \"" + api + "(\" " + path # pay attention to "(" here
    
    for line in exec_command(command):
        (filename, lineno, content) = grep_parser(line)
        pos_api = content.find(api)
        fmt = content[pos_api + len(api) + 1 :].split(",")[1].strip()
        if fmt.find(" ") != -1:
            for arg in fmt.split(" "):
                if arg.find("\"") != -1:
                    pfmt = fmt_parser(arg)
                    if fmt_checker(pfmt):
                        print(line.strip())
        else:
            if fmt.find("\"") != -1:
                pfmt = fmt_parser(fmt)
                if fmt_checker(pfmt):
                    print(line.strip())

if __name__ == "__main__":
    # # 4: buffer overflow
    # for api in targets:
    #     #print("===== {} =====".format(api))
    #     check(api, sys.argv[1])

    # # 5: TOCTTOU
    for api in ['stat']:
        check(api, sys.argv[1])

    # 8/10-2: see fmt_checker()
    for api in py_targets:
        #print("===== {} =====".format(api))
        py_check(api, sys.argv[1])
