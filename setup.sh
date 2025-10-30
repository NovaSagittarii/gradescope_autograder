### Installing dependencies ###
apt install -y g++ python3 python3-pip
pip3 install pyseccomp


### Setup permissions
find / -type f -exec chmod 640 {}
adduser student --no-create-home --disabled-password --gecos ""

### Generating answer files (ahead of time for faster grading). ###
cd /autograder/source/src
python3 compile.py solution
python3 exec.py solution

# clean up side-effect of running compile.py and exec.py
echo > /autograder/results/results.json

# delete the solution so you can't just include it during student-compile time
mkdir tmp
cp /autograder/source/src/solution/*.out tmp
rm tmp/a.out
rm -rf /autograder/source/src/solution
mkdir /autograder/source/src/solution
cp tmp/*.out /autograder/source/src/solution
