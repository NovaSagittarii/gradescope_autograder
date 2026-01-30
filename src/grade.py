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

with open(f"{ANS_PATH}/size.meta", "r") as file:
    filesize = int(file.read())
    print(f"filesize={filesize}")
with open(f"{ANS_PATH}/lang.meta", "r") as file:
    language = file.read()

passed_all = True
for id, test in enumerate(tests):
    with open(f"{JANS_PATH}/{id}.out", "r") as file:
        jans = file.read()  # judge should not output invalid UTF-8
    with open(f"{ANS_PATH}/{id}.out", "rb") as file:
        ans = file.read().decode(errors="replace")
    with open(f"{ANS_PATH}/{id}.exitcode", "r") as file:
        exitcode = int(file.read())
    with open(f"{ANS_PATH}/{id}.err", "r") as file:
        stderr = file.read()
        stderr = f"\n# Errors\n```\n{stderr}```\n" if stderr else ""
    with open(f"{ANS_PATH}/{id}.time", "r") as file:
        runtime_ms = int(file.read())

    result = task_details.judge(jans, ans)
    if not result.passed:
        passed_all = False

    verdict = "Accepted" if result.passed else "Wrong answer"
    if exitcode:
        verdict = "Runtime error"
    if runtime_ms / 1000 >= task_details.TIMELIMIT_SECONDS:
        verdict = f"Time limit exceeded ({task_details.TIMELIMIT_SECONDS:.1f}s)"
    partial_output = f"""{verdict}
Runtime: {runtime_ms} ms"""
    full_output = f"""{partial_output}

# Input
```
{test.data}```

# Output
```
{ans}```
{stderr}
# Answer
```
{jans}```"""

    test_name = f"Test {id+1}" + (f" ({test.label})" if test.label else "")
    status = "passed" if result.passed else "failed"
    if not test.hidden:
        gradescope.append_test(
            test_name,
            status=status,
            score=result.score,
            max_score=test.max_score,
            output=full_output,
            visibility=gradescope.VisibilityType.VISIBLE,
        )
    else:
        gradescope.append_test(
            test_name,
            status=status,
            score=result.score,
            max_score=test.max_score,
            output=partial_output,
            visibility=gradescope.VisibilityType.AFTER_DUE_DATE,
        )
        gradescope.append_test(
            f"{test_name} [*for TAs]",
            status=status,
            score=0,
            max_score=0,
            output=full_output,
            visibility=gradescope.VisibilityType.HIDDEN,
        )

gradescope.finalize(
    leaderboard=(
        [
            gradescope.LeaderboardStat(
                "Size (bytes)", filesize, gradescope.LeaderboardStat.OrderType.ASCENDING
            ),
            gradescope.LeaderboardStat("Language", language),
        ]
        if passed_all
        else None
    )
)
