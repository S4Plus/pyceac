# TODO false negative: use if-else/switch for different exceptions (fallthrough)
# TODO macro

import sys
import subprocess
import linecache

# string -> string list
def exec_command(command):
    output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, encoding="UTF-8")
    return output.stdout.readlines()

# string, int -> string
def next_program_line(filepath, lineno):
    current_line = linecache.getline(filepath, lineno).strip()
    lineno += 1
    if (not current_line.endswith(";")):
        return next_program_line(filepath, lineno)
    next_line = linecache.getline(filepath, lineno).strip()
    if (next_line == "}" or next_line == ""):
        return linecache.getline(filepath, lineno + 1).strip()
    else:
        return next_line

# string -> boolean
def postprocess(line):
    post_process_funcs = [
        "Py_DECREF", 
        "PyBuffer_Release", 
        "_PyBytesWriter_Dealloc", 
        "free", 
    ]

    for f in post_process_funcs:
        if line.startswith(f):
            return True
    return False

# string, string -> None 
def check(keyword, path):
    command = "grep -rn \"" + keyword + "\" " + path
    
    for line in exec_command(command):
        # DO NOT use split(":")
        pos_filepath = line.find(":")
        filepath = line[0:pos_filepath]
        filename = filepath[filepath.find(path + "/") + len(path) + 1:] # can be sub-filepath
        if (not filename.endswith(".c")):
            continue
        pos_lineno = line[pos_filepath + 1:].find(":") + pos_filepath + 1
        lineno_str = line[pos_filepath + 1:pos_lineno]
        lineno = int(lineno_str)

        code_line = line[pos_lineno + 1:]
        if code_line.strip().startswith("return"):
            # raise exception and return simultaneously
            continue

        next = next_program_line(filepath, lineno)
        if (not next.startswith("return")):
            if (next.startswith("goto") or postprocess(next)):
                # TODO
                #   false positive: further check
                #   false negative: other post-process (can be user-defined)
                pass
            else:
                print(line.strip())

if __name__ == "__main__":
    keywords = [
        # exceptions
        "PyErr_SetString", 
        "PyErr_SetObject", 
        "PyErr_Format", 
        "PyErr_FormatV", 
        "PyErr_SetNone", 
        "PyErr_BadArgument", 
        "PyErr_NoMemory", 
        "PyErr_SetFromErrno", 
        "PyErr_SetFromErrnoWithFilenameObject", 
        "PyErr_SetFromErrnoWithFilenameObjects", 
        "PyErr_SetFromErrnoWithFilename", 
        "PyErr_SetFromWindowsErr", 
        "PyErr_SetFromWindowsErrWithFilename", 
        "PyErr_SetExcFromWindowsErrWithFilenameObject", 
        "PyErr_SetExcFromWindowsErrWithFilenameObjects", 
        "PyErr_SetExcFromWindowsErrWithFilename", 
        "PyErr_SetImportError", 
        "PyErr_SyntaxLocationObject", 
        "PyErr_SyntaxLocationEx", 
        "PyErr_SyntaxLocation", 
        "PyErr_BadInternalCall", 
        # warnings
        "PyErr_WarnEx", 
        "PyErr_SetImportErrorSubclass", 
        "PyErr_WarnExplicitObject", 
        "PyErr_WarnExplicit", 
        "PyErr_WarnFormat", 
        "PyErr_ResourceWarning", 
    ]
    for k in keywords:
        check(k, sys.argv[1])
