#!/bin/bash

python3 pycapi_comp.py ../data/python/Python-3.7.0.capi.dat ../data/python/Python-3.6.0.capi.dat > ../data/python/3.7-3.6-comp.dat
python3 pycapi_comp.py ../data/python/Python-3.6.0.capi.dat ../data/python/Python-3.5.0.capi.dat > ../data/python/3.6-3.5-comp.dat
python3 pycapi_comp.py ../data/python/Python-3.5.0.capi.dat ../data/python/Python-3.4.0.capi.dat > ../data/python/3.5-3.4-comp.dat
python3 pycapi_comp.py ../data/python/Python-3.4.0.capi.dat ../data/python/Python-3.3.0.capi.dat > ../data/python/3.4-3.3-comp.dat
python3 pycapi_comp.py ../data/python/Python-3.3.0.capi.dat ../data/python/Python-3.2.capi.dat > ../data/python/3.3-3.2-comp.dat
python3 pycapi_comp.py ../data/python/Python-3.2.capi.dat ../data/python/Python-2.7.capi.dat > ../data/python/3.2-2.7-comp.dat