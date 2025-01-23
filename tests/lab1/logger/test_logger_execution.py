# tests/lab1/logger/test_execution.py

import os
import pytest
from steps.utils import run_command


@pytest.mark.dependency(depends=["tests/lab1/logger/test_logger_build.py::test_logger_build"],
						scope="session")
def test_logger_execution(test_dir):

    test_logger_bin = os.path.join(test_dir, "test_logger")

    result = run_command([test_logger_bin], cwd=test_dir, check=True)
    stdout = result.stdout

    assert "[TEST 1] create_logger_table first call: PASS" in stdout, "TEST 1 failed"
