# How to reproduce the data

Download corpus following csv files before excuting any script in this folder.

```./run.sh``` shows a whole process of data reproduction, but please read through this document ahead of running it for how to use every script in a separated way.

## Build the auxiliary tools

Clang has to be installed, you can follow the [doc](http://clang.llvm.org/get_started.html). But ```make install``` is needed after ```make```.

```bash
./tool-build.sh
```

Auxiliary tools include:

1. a function prototype extractor
2. a lexical tool

For direct use, you can use ```./function_prototype/build/function-prototype file``` and ```./token_processor/build/token-processor file``` respectively, but we automate this in other scripts.

## Python/C API evolution with Python versions

The path of Python source that you want to extract API from should be given in ```python-path.txt```.

```bash
python3 pycapi.py
```

For comparing between two given release versions (functions defined in macro not included):

```bash
python3 pycapi_comp.py ../data/python/Python-3.7.0.capi.dat ../data/python/Python-3.6.0.capi.dat
```

## Identify interface files, LOC and API extraction

You must install [cloc](https://github.com/AlDanial/cloc).

The path of projects that you want to analyse should be given in ```corpus-path.txt```, and lines start with '#' will be ignored.

```bash
python3 base_statistic.py
```

For some special projects, we do this in an exhaustive way.

```bash
python3 base_statistic_ex.py
```

## API statistic

Using data generated in last step (_base_statistic_), you can do some advanced analysis.

```bash
python3 api_statistic.py
```

## API check

Check whether a project used some Python/C API out of given version of Python, provided by data generated in step before (_pycapi_).

```bash
python3 api_check.py ../data/PyAudio-0.2.11.capi.dat ../data/python/Python-3.7.0.capi.dat
```
