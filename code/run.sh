#!/bin/bash

# Build the auxiliary tools based on libclang
./tool-build.sh

# Python/C API evolution with Python versions
python3 pycapi.py
./comp-all.sh

# Base statistics from chosen applications
# Including info of:
#   interface code separation
#   LOC
#   api extraction and counting
#echo "python3 base_statistic.py" > ../data/capi.dat.log
#python3 base_statistic.py >> ../data/capi.dat.log
#echo "python3 base_statistic_ex.py" >> ../data/capi.dat.log
#python3 base_statistic_ex.py >> ../data/capi.dat.log
python3 base_statistic.py
python3 base_statistic_ex.py

# Some advanced statistics based on data before.
#echo "python3 api_statistic.py" > ../data/statistics.log
#python3 api_statistic.py >> ../data/statistics.log
python3 api_statistic.py

# API check -- an example
python3 api_check.py -h
#python3 api_check.py ../data/PyAudio-0.2.11.capi.dat ../data/python/Python-3.7.0.capi.dat