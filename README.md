# Gradescope Autograder Example

Ubuntu 22.04 Base

Verdicts

- Partial result
- Wrong answer
- Runtime error
- Compile error
- Time limit exceeded

Features

- Custom judge
- Custom generator
- Multiple language (C++ or Python)
- Network access restriction
- File access restriction

## Configuration

- edit env vars in [](./init_env.sh) if needed
- edit solution in [](./src/solution/)
- edit `generate_tests()` and `judge()` in [](./src/task_details.py)
