import subprocess
import os

# string -> string list
def exec_command(command):
    # print(command)
    output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, encoding="UTF-8")
    return output.stdout.readlines()

# string -> None 
def check(folder):
    #command = "clang -cc1 -I/Library/Frameworks/Python.framework/Versions/3.7/include/python3.7m -I/Users/hmz/USTC/document/PythonC/empirical/corpus/pillow/Pillow/src/libImaging -I/Users/hmz/USTC/document/PythonC/empirical/corpus/pillow/Pillow/src/Tk -analyze -analyzer-checker=unix.Malloc "
    command = "clang -cc1 -I/Library/Frameworks/Python.framework/Versions/3.7/include/python3.7m -I/Users/hmz/USTC/document/PythonC/empirical/corpus/pillow/Pillow/src/libImaging -I/Users/hmz/USTC/document/PythonC/empirical/corpus/pillow/Pillow/src/Tk -analyze -analyzer-checker=unix.MismatchedDeallocator "

    paths = os.listdir(folder)
    for p in paths:
        abspath = folder + '/' + p
        if p.find('.') == -1:
            check(abspath)
        else:
            if p.endswith('.c'):
                result = exec_command(command + abspath)
                if len(result) == 0:
                    print("{} pass".format(abspath))
                else:
                    for line in result:
                        print(line)

if __name__ == "__main__":
    folder = "/Users/hmz/USTC/document/PythonC/empirical/corpus/pillow/Pillow/src"
    check(folder)
