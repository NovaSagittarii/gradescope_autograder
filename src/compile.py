"""
Compiles given folder and outputs a binary in that folder.
"""

import os
import subprocess
import sys
from typing import Optional

import gradescope

if len(sys.argv) < 2:
    print("usage: ", sys.argv[0], "[source folder]")
    sys.exit(1)

SOURCE_PATH = sys.argv[1]

language: Optional[str] = None
files = os.listdir(SOURCE_PATH)
for file in files:
    if file.endswith(".cpp"):
        language = "cpp"
    elif file.endswith(".py"):
        language = "py"

subprocess.run(
    f"du -sb {SOURCE_PATH}/* | cut -f 1 > {SOURCE_PATH}/size.meta", shell=True
)

stderr: Optional[str] = None
match language:
    case "cpp":  # build cpp
        p = subprocess.run(
            f"g++ -std=c++20 -o {SOURCE_PATH}/a.out {SOURCE_PATH}/*.cpp",
            stderr=subprocess.PIPE,
            shell=True,
            check=False,
        )
        stderr = p.stderr.decode()
    case "py":  # build python (make an a.out executable that runs the python)
        with open(f"{SOURCE_PATH}/a.out", "w") as f:
            f.write(f"#!/usr/bin/env bash\npython3 {SOURCE_PATH}/*.py")
        subprocess.run(f"chmod +x {SOURCE_PATH}/a.out", shell=True)
    case None:
        pass

print("[compile.py] LANGUAGE=", language)
if stderr:
    print(stderr)
    gradescope.append_test(f"Compile Error ({language})", "failed", output=stderr)
