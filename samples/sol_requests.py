import requests
import sys
from subprocess import Popen, PIPE, STDOUT

# Note: The first part requires the 'requests' library.
# Install it if you haven't: pip install requests

## 1. Direct GET Request using 'requests'

print("--- Part 1: Direct GET Request (using 'requests') ---")
url = "https://www.google.com"

try:
    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Successfully made direct GET request.")
        # print(f"Content (first 150 chars): {response.text[:150]}")
    else:
        print(f"Request failed with status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Direct request failed: {e}")

print("-" * 50)

## 2. GET Request via 'subprocess.Popen'

print("--- Part 2: GET Request via 'subprocess.Popen' ---")

# This is the Python code we want the subprocess to run.
# We use 'urllib.request' because it's built-in and avoids
# dependency issues in the separate subprocess.
python_code_to_run = """
import urllib.request
import sys

try:
    # Open the URL and get the response
    with urllib.request.urlopen('https://www.google.com') as response:
        # Print the status code from within the subprocess
        print(f'Subprocess Status: {response.status}')
        print('Subprocess successfully made request.')
except Exception as e:
    # Print any errors from within the subprocess
    print(f'Subprocess failed: {e}', file=sys.stderr)
"""

# 'sys.executable' is the path to the current Python interpreter
# '-c' tells the interpreter to run the following string as code
command = [sys.executable, "-c", python_code_to_run]

try:
    # Start the subprocess
    # stdout=PIPE: Captures the standard output
    # stderr=STDOUT: Redirects standard error to standard output
    # text=True: Decodes stdout/stderr as text (using default encoding)
    process = Popen(command, stdout=PIPE, stderr=STDOUT, text=True)

    # Wait for the process to finish and get all its output
    stdout_output, _ = process.communicate()

    print("Output from subprocess:")
    print(stdout_output.strip())

    # Check the return code of the subprocess itself
    if process.returncode == 0:
        print("Subprocess executed successfully.")
    else:
        print(f"Subprocess finished with error code: {process.returncode}")

except Exception as e:
    print(f"Failed to start or run Popen process: {e}")
