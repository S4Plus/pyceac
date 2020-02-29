# TODO save output in a set to remove duplicated warnings
import subprocess
import linecache

rules = {
    "false":[
        "PyArg_ParseTuple"
    ],
    "NULL":[
        "Py_BuildValue",
        "PyLong_FromLong",
        #"PyBytes_FromStringAndSize",
        #"PyBytes_AsString",
        #"PyFloat_FromDouble",
        #"PyObject_GetAttrString",
        #"PyDict_New",
        #"PyDict_GetItemString",
        #"PyDict_GetItem",
        #"PyList_GetItem",
        #"PyList_GET_ITEM",
        "PyList_New",
        "malloc"
    ],
    "-1":[
        #"PyDict_SetItemString",
        #"PyType_Ready",
        #"PyLong_AsLong",
        #"PyFloat_AsDouble", # -1.0
        #"PyModule_AddIntConstant",
        #"PyObject_SetAttrString",
        "PyDict_SetItem",
        #"PyList_Append",
        #"PyList_Insert",
        "PyList_SetItem",
        "PyList_SET_ITEM",
        "PyTuple_SET_ITEM"
    ]
}

append_rules = {
    "false":[],
    "NULL":[],
    "-1":[]
}

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

# string, int -> string
def next_program_line(filename, lineno):
    current_line = linecache.getline(filename, lineno).strip()
    lineno += 1
    if (not current_line.endswith(";")):
        return next_program_line(filename, lineno)
    next_line = linecache.getline(filename, lineno).strip()
    if (next_line == "}" or next_line == ""):
        return linecache.getline(filename, lineno + 1).strip()
    else:
        return next_line

# string -> string
def assignment_parser(assignment):
    pos_left = assignment.find("=")
    left = assignment[0:pos_left].strip()
    if left.find(" ") != -1: # new declarations, remove type identifers
        variable = left.split(" ")[1]
        if variable.startswith("*"): # pointers
            return variable[1:]
        else:
            return variable
    else:
        return left

# string, string, bool -> None 
def check(api, errval, append):
    path = "/Users/hmz/USTC/document/PythonC/empirical/corpus/pillow/Pillow/src"
    command = "grep -rn \"" + api + "\" " + path
    
    for line in exec_command(command):
        (filename, lineno, content) = grep_parser(line)
        if content.strip().startswith("return"):
            continue
        elif content.strip().startswith("if") or content.strip().startswith("else if"):
            continue
        elif content.strip().startswith("//") or content.strip().startswith("/*"):
            continue
        elif content.strip().startswith("#define"):
            if append == True:
                print(content.strip())
                append_rules[errval].append(content.split(" ")[1])
                continue
            else:
                continue
        else:
            next_content = next_program_line(filename, lineno)
            #print(next_content)
            variable = assignment_parser(content)
            #print(variable)
            if next_content.startswith("if") and next_content.find(variable) != -1:
                continue
            elif next_content.startswith("return") and next_content.find(variable) != -1:
                continue
            else:
                #print(filename)
                #print(lineno)
                #print(content)
                #print(next_content)
                print(line.strip())

if __name__ == "__main__":
    for (errval, apis) in rules.items():
        for api in apis:
            #print("===== " + api + " =====")
            check(api, errval, True)

    #print(append_rules)
    for (errval, apis) in append_rules.items():
        for api in apis:
            #print("===== " + api + " =====")
            check(api, errval, False)
