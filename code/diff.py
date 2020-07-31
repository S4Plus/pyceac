import sys


def get_api_set(filepath):
    api_set = set()
    with open(filepath, 'r') as f:
        for lines in f.readlines():
            api_set.add(lines.strip())
    return api_set

if __name__ == "__main__":
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    api_set_1 = get_api_set(file1)
    api_set_2 = get_api_set(file2)

    in_2_not_1 = api_set_2.difference(api_set_1)
    print(">>> In {} but not in {}".format(file2, file1))
    print(in_2_not_1)

    in_1_not_2 = api_set_1.difference(api_set_2)
    print(">>> In {} but not in {}".format(file1, file2))
    print(in_1_not_2)
