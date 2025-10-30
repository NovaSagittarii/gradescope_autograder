"""
Runs after execution, grades the output by comparing it to the
model solution.
"""

import sys

import task_details
import gradescope

if len(sys.argv) < 3:
    print("usage: ", sys.argv[0], "[judge folder] [contestant folder]")
    sys.exit(1)
JANS_PATH = sys.argv[1]
ANS_PATH = sys.argv[2]

tests = task_details.generate_tests()

for id, test in tests.items():
    with open(f"{JANS_PATH}/{id}.out", "r") as file:
        jans = file.read()
    with open(f"{ANS_PATH}/{id}.out", "r") as file:
        ans = file.read()
    with open(f"{ANS_PATH}/{id}.err", "r") as file:
        stderr = file.read()
    with open(f"{ANS_PATH}/{id}.time", "r") as file:
        runtime_ms = int(file.read())

    result = task_details.judge(jans, ans)

    partial_output = f"""{'Accepted' if result.passed else 'Wrong answer'}
Runtime: {runtime_ms} ms"""
    full_output = f"""{partial_output}

# Input
```
{test.data}```

# Output
```
{ans}```

# Answer
```
{jans}```"""

    if not test.hidden:
        gradescope.append_test(
            f"Test {id}",
            status="passed",
            score=result.score,
            max_score=test.max_score,
            output=full_output,
            visibility=gradescope.VisibilityType.VISIBLE,
        )
    else:
        gradescope.append_test(
            f"Test {id}",
            status="passed",
            score=result.score,
            max_score=test.max_score,
            output=partial_output,
            visibility=gradescope.VisibilityType.AFTER_DUE_DATE,
        )
        gradescope.append_test(
            f"Test {id} (debug)",
            status="passed",
            score=0,
            max_score=0,
            output=full_output,
            visibility=gradescope.VisibilityType.HIDDEN,
        )

gradescope.finalize()
