#!/usr/bin/env bash
set -euo pipefail

### Installing dependencies ###
# apt install -y g++ python3 python3-pip
pip3 install pyseccomp

# create the student user early (since exec.py runs using restricted user)
adduser student --no-create-home --disabled-password --gecos ""

### Generating answer files (ahead of time for faster grading). ###
mkdir -p /autograder/results
cd /autograder/source/src
python3 compile.py solution
python3 exec.py solution

# clean up side-effect of running compile.py and exec.py
echo > /autograder/results/results.json

### setup permissions for grading ###
find /autograder /gradescope /usr/bin -type f -exec chmod 750 {} \; > /dev/null 2>&1
# remove any exec in var and lib (stuff in /usr is needed for python to work tho)
find /var /lib -type f -perm /001 -exec chmod o-x {} \; 2>/dev/null
# remove any write perms
find / -type d -perm /002 -exec chmod o-w {} \; 2>/dev/null
chmod 755 $(which python3) /usr/bin/env $(which bash)
