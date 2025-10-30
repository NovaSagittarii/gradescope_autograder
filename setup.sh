#!/usr/bin/env bash
set -euo pipefail

### Installing dependencies ###
apt install -y g++ python3 python3-pip
pip3 install pyseccomp

### Generating answer files (ahead of time for faster grading). ###
mkdir -p /autograder/results
cd /autograder/source/src
python3 compile.py solution
python3 exec.py solution

# clean up side-effect of running compile.py and exec.py
echo > /autograder/results/results.json

# setup permissions for grading
find /usr/bin -type f -exec chmod 750 {} \; > /dev/null 2>&1
find /autograder -type f -exec chmod 750 {} \; > /dev/null 2>&1
chmod 755 $(which python3) /usr/bin/env $(which bash)
adduser student --no-create-home --disabled-password --gecos ""
