#!/usr/bin/env bash
set -euo pipefail

# load env vars
source /autograder/source/init_env.sh

### Installing dependencies ###
# apt install -y g++ python3 python3-pip
# ^^^ these are already available in gradescope base image

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

# remove any exec on writable files
# find / -type f -perm -007 -exec chmod o-x {} \; 2>/dev/null

# remove any write perms
find / -type d -perm /002 -exec chmod o-w {} \; 2>/dev/null

# restricted user still needs to execute files to run student code
chmod 755 $(which python3) /usr/bin/env $(which bash)

# disallow student processes from having internet access
# iptables -I OUTPUT 1 -m owner --uid-owner student -j DROP
# iptables -I OUTPUT 1 -m owner --gid-owner student -j DROP
