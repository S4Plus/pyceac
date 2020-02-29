import sys

class Python:
    def __init__(self, path):
        self.path = path
        self.version = path[path.rfind("/") + 1 : -9]
        self.capi = {}
        self.get_capi()

    def get_capi(self):
        with open(self.path, 'r') as f:
            for l in f.readlines():
                api = l[:-1]
                api_name = api.split(",")[1].split("(")[0]
                in_out_args = api.split(",")[0] + "," + api.split("(")[1][:-1]
                self.capi[api_name] = in_out_args

def comp(py1, py2):
    capi_1 = py1.capi
    capi_2 = py2.capi
    version_1 = py1.version
    version_2 = py2.version

    # four cases
    only_1 = [] # apis only in py1
    only_2 = [] # apis only in py2
    diff = []   # both have, but different, each item is saved as a tuple
    same = []   # both have, and the same

    for (name_1, args_1) in capi_1.items():
        api_1 = name_1 + "(" + args_1 + ")"
        if name_1 in capi_2:
            if args_1 == capi_2[name_1]:
                same.append(api_1)
            else:
                diff.append((api_1, name_1 + "(" + capi_2[name_1] + ")"))
            # after for cycle, apis left in capi_2 belong to only_2
            capi_2.pop(name_1)
        else:
            only_1.append(api_1)
    for (name_2, args_2) in capi_2.items():
        api_2 = name_2 + "(" + args_2 + ")"
        only_2.append(api_2)

    print("number of APIs only in {} : {}".format(version_1, len(only_1)))
    print("number of APIs only in {} : {}".format(version_2, len(only_2)))
    print("number of APIs both have, but different : {}".format(len(diff)))
    print("number of APIs both have, and the same : {}".format(len(same)))
    # formatted verbose output
    stream = sys.stdout
    template = "{:^59}  {:^59}"
    headline = template.format(version_1, version_2)
    stream.write(headline + "\n" + 120 * "=" + "\n")
    for api in only_1:
        stream.write(template.format(transform(api), "-") + "\n")
    for api in only_2:
        stream.write(template.format("-", transform(api)) + "\n")
    for (api1, api2) in diff:
        stream.write(template.format(transform(api1), transform(api2)) + "\n")

# pass in api in form of:
#   function_name(return_type, passin_types)
# return api in form of:
#   return_type,function_name(passin_types)
def transform(api):
    api_name = api.split("(")[0]
    in_out_args = api.split("(")[1][:-1]
    in_out_index = in_out_args.find(",")
    out_arg = in_out_args[:in_out_index]
    in_args = in_out_args[in_out_index + 1:]
    return out_arg + "," + api_name + "(" + in_args + ")"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: Paths of two *.capi.dat files should be passed in.")
    else:
        dat_1 = sys.argv[1]
        dat_2 = sys.argv[2]
        python_1 = Python(dat_1)
        python_2 = Python(dat_2)
        comp(python_1, python_2)