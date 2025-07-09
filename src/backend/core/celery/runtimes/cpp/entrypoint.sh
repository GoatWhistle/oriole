#!/bin/sh
set -e

echo "$1" > solution.cpp
g++ -O2 -std=c++17 solution.cpp -o solution.out
./solution.out
