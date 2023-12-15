#!/bin/bash

# first install coverage.py:
# https://coverage.readthedocs.io/en/latest/install.html

# earse previous coverage and create a new combine
coverage erase

# run through each test dir and run the test case there
echo -e "[   TESTING MODULE RUN   ]\n\n"
for dir in */*; do
    if [ -d "$dir" ]; then
        bash $dir/test.sh
        coverage combine --append $dir/.coverage
    fi
done
echo -e "\n\n\n[   FINISH TESTING MODULE   ]\n"

# print the coverage report, expect 100% coverage rate
echo "Generate Coverage Report:"
coverage report -m
coverage html