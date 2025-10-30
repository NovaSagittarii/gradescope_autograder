"""
For writing to results.json

Based on Gradescope documentation
https://gradescope-autograders.readthedocs.io/en/latest/specs/#output-format
"""

import json
from types import TracebackType
from enum import Enum
from typing import Literal, Optional

RESULTS_PATH = "/autograder/results/results.json"


class FormatType(Enum):
    """
    You can add rich formatting to your autograder output to further customize
    your autograder experience for students.
    """

    TEXT = "text"
    """
    (default for test output and names) This will do the basic text formatting
    which was previously done on all test names and outputs. No HTML, Markdown,
    or ANSI will be rendered.
    """
    HTML = "html"
    """
    This will render HTML in your output. Note that we sanitize the output so
    you may not be able to use all HTML elements. Additionally, not all tags
    will be styled out of the box.
    """
    SIMPLE = "simple_format"
    """
    (default for top-level output) This is very similar to the `"html"` format
    option but will also convert `\n` into `<br />` and `\n\n+` into a page break.
    """
    MARKDOWN = "md"
    """
    This will render some basic Markdown in your output.
    """
    ANSI = "ansi"
    """
    This will render ANSI colors similar to how the stdout renders them.
    """


class VisibilityType(Enum):
    """
    You can hide some or all test cases based on your desired conditions.
    Visibility can be controlled by setting the "visibility" field at the top
    level for an assignment, or for an individual test.

    Note: Instructors will always see all tests, so for now you'll have to
    create a student account to test visibility settings.

    If an assignment level visibility setting is set, a test can override
    this setting with its own visibility setting. For example, you may set
    `"visibility":"after_due_date"` at the top level so that all tests are
    hidden until after the submission deadline. Then, you can set an individual
    test to have `"visibility":"visible"` if it should always be shown.
    For example, this can be useful for pre-submission checks such as a test
    that checks whether the student's code compiled successfully or not.
    Another possibility is having a subset of tests always visible to guide
    students through the homework, while keeping the set of tests that they
    will be graded on hidden until after the assignment is due.

    If test cases are hidden, students will not be able to see their total score.
    """

    HIDDEN = "hidden"
    """
    Test case will never be shown to students.
    """
    AFTER_DUE_DATE = "after_due_date"
    """
    Test case will be shown after the assignment's due date has passed.
    If late submission is allowed, then test will be shown only after the late due date.
    """
    AFTER_PUBLISHED = "after_published"
    """
    Test case will be shown only when the assignment is explicitly published
    from the "Review Grades" page.
    """
    VISIBLE = "visible"
    """
    (default) Test case will always be shown.
    """


class open_json:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data: dict = {}

    def __enter__(self) -> dict:
        try:
            with open(RESULTS_PATH, "r") as file:
                self.data = json.load(file)
        except (OSError, json.JSONDecodeError):
            pass
        assert isinstance(self.data, dict)
        return self.data

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type and exc_val:
            raise exc_val
        with open(self.filepath, "w") as file:
            json.dump(self.data, file, indent=4)


def append_test(
    name: str,
    status: Literal["passed"] | Literal["failed"],
    score: Optional[float] = None,
    max_score: Optional[float] = None,
    name_format: FormatType = FormatType.TEXT,
    number: Optional[str] = None,
    output: str = "",
    output_format: FormatType = FormatType.TEXT,
    tags: Optional[list[str]] = None,
    visibility: VisibilityType = VisibilityType.VISIBLE,
    extra_data: Optional[dict] = None,
) -> None:
    with open_json(RESULTS_PATH) as results:
        if "tests" not in results:
            results["tests"] = []

        obj = {
            "score": score,
            "max_score": max_score,
            "status": status,
            "name": name,
            "name_format": name_format.value,
            "number": number,
            "output": output,
            "output_format": output_format.value,
            "tags": tags,
            "visibility": visibility.value,
            "extra_data": extra_data,
        }
        results["tests"].append({k: v for k, v in obj.items() if v is not None})


def finalize(
    leaderboard: Optional[list[dict]] = None,
    visibility: VisibilityType = VisibilityType.VISIBLE,
    execution_time: Optional[float] = None,
) -> None:
    with open_json(RESULTS_PATH) as results:
        assert results["tests"]
        total_score = sum(x.get("score", 0) for x in results["tests"])
        obj = {
            "leaderboard": leaderboard,
            "visibility": visibility.value,
            "execution_time": execution_time,
            "score": total_score,
        }
        for k, v in obj.items():
            if v:
                results[k] = v
