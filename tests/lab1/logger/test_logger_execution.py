# tests/lab1/logger/test_logger_execution.py

import os
import pytest
from steps.utils import run_command

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/logger/test_logger_build.py::test_logger_build"],
						scope="session")
def test_logger_execution(test_dir):

    test_logger_bin = os.path.join(test_dir, "test_logger")

    result = run_command([test_logger_bin], cwd=test_dir, check=True)
    if result.returncode != 0:
        pytest.fail(
            f"[ERROR] test_logger exited with non-zero code {result.returncode}.\n"
            f"STDERR:\n{result.stderr}\n"
            f"STDOUT:\n{result.stdout}"
        )

    stdout = result.stdout
    if "[TEST 1] init_logger first call: PASS" not in stdout:
        pytest.fail(
            "[ERROR] test_logger did not report PASS for init_logger [TEST 1].\n"
            f"Actual stdout:\n{stdout}"
        )
