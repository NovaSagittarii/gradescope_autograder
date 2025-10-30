"""
Edit this file to modify how tests are generated and how judge output.
"""


class TestCase:
    def __init__(self, data: str, max_score: float = 1.0, hidden: bool = False):
        self.data = data
        self.hidden = hidden
        self.max_score = max_score


class Result:
    def __init__(self, passed: bool, score: float):
        self.passed = passed
        self.score = score


def generate_tests() -> dict[str, TestCase]:
    """
    This returns {id: inputString}. This must be deterministic.
    """
    return {"1": TestCase("world\n"), "2": TestCase("testing\n", hidden=True)}


def judge(jans: str, ans: str) -> Result:
    if jans.strip() == ans.strip():
        return Result(True, 1.0)
    else:
        return Result(False, 0.1)
