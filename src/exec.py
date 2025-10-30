"""
Executes a binary output from compile.py with the following restrictions:
- on a restricted user (minimal access)
- no internet access

For more details, visit:
https://gradescope-autograders.readthedocs.io/en/latest/best_practices/#security-best-practices
"""

import base64
import math
import pyseccomp as seccomp
import socket
import subprocess
import sys
import time

import task_details

if len(sys.argv) < 2:
    print("usage: ", sys.argv[0], "[source folder]")
    sys.exit(1)

SOURCE_PATH = sys.argv[1]

filter = seccomp.SyscallFilter(seccomp.ALLOW)
for network in [socket.AF_INET, socket.AF_INET6]:
    filter.add_rule(
        seccomp.ERRNO(seccomp.errno.EACCES),
        "socket",
        seccomp.Arg(0, seccomp.EQ, network),
    )
filter.load()

for id, payload in task_details.generate_tests().items():
    assert id != "a", "a.out is reserved for the binary"
    # pass as base64 from stdin to avoid any escaping character issues
    base64payload = base64.b64encode(payload.data.encode()).decode()
    cmd = (
        f"echo {base64payload} | base64 -d | "
        + f"runuser -u student -- {SOURCE_PATH}/a.out "
        + f"1> {SOURCE_PATH}/{id}.out 2> {SOURCE_PATH}/{id}.err"
    )
    start = time.time()
    subprocess.run(cmd, shell=True, check=False, timeout=10)
    runtime_ms = math.ceil((time.time() - start) * 1000)
    subprocess.run(f"echo {runtime_ms} > {SOURCE_PATH}/{id}.time", shell=True)
