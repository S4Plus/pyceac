import subprocess
import os, sys

# string -> string list
def exec_command(command):
    # print(command)
    output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, encoding="UTF-8")
    return output.stdout.readlines()

# string -> None 
def check(folder):
    command = "clang -cc1 -I/Users/hmz/Projects/pyceac-dev/code/fake_include/ -I/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/include/python3.7m/ -I/Users/hmz/Projects/pyceac-dev/corpus/pillow/Pillow/src/libImaging -I/Users/hmz/Projects/pyceac-dev/corpus/pillow/Pillow/src/Tk -analyze -analyzer-checker=unix.Malloc "
    # command = "clang -cc1 -I/Users/hmz/Projects/pyceac-dev/code/fake_include/ -I/usr/local/Cellar/python/3.7.7/Frameworks/Python.framework/Versions/3.7/include/python3.7m/ -I/Users/hmz/Projects/pyceac-dev/corpus/pillow/Pillow/src/libImaging -I/Users/hmz/Projects/pyceac-dev/corpus/pillow/Pillow/src/Tk -analyze -analyzer-checker=unix.MismatchedDeallocator "

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
    check(sys.argv[1])
