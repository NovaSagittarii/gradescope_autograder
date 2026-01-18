"""
Edit this file to modify how tests are generated and how judge output.
"""

from typing import Final, Optional
TIMELIMIT_SECONDS: Final[float] = 10.0


class TestCase:
    def __init__(self, data: str, max_score: float = 1.0, *, hidden: bool = False, label: Optional[str] = None):
        self.data = data
        self.hidden = hidden
        self.max_score = max_score
        self.label = label


class Result:
    def __init__(self, passed: bool, score: float):
        self.passed = passed
        self.score = score


def generate_tests() -> list[TestCase]:
    """
    This returns multiple TestCase().
    This must be deterministic (use `random.seed(0)` to fix the RNG seed).
    It is run separately twice, once for model solution, once for main solution.
    """
    return [
        TestCase("world\n"),
        TestCase("testing\n", hidden=True, label="Hidden test")
    ]


def judge(jans: str, ans: str) -> Result:
    if jans.strip() == ans.strip():
        return Result(True, 1.0)
    else:
        return Result(False, 0.1)
