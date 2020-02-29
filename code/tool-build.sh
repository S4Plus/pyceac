#!/bin/bash

# Build the function prototype extractor
cd function_prototype
mkdir build
cd build
cmake ..
make
cd ../..

# Build the lexical tool
cd token_processor
mkdir build
cd build
cmake ..
make
cd ../..