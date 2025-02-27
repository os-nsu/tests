# tests/lab2/logger/test_logger_execution.py

import os
import pytest
import re
from steps.utils import run_command

@pytest.mark.lab2
@pytest.mark.dependency(depends=["tests/lab2/logger/test_logger_build.py::test_logger_build"],
                        scope="session")
def test_logger_rollover_check(current_dir):

    bin_dir = os.path.join(current_dir, "../", "bin")
    binary_path = os.path.join(bin_dir, "test_logger_file_stream_rollover")
    log_path = os.path.join(bin_dir, "rollover_test.log")

    if os.path.exists(log_path):
        os.remove(log_path)

    result = run_command([binary_path], check=True)
    if result.returncode != 0:
        pytest.fail(
            f"Binary {binary_path} crashed or returned error code {result.returncode}.\n"
        )

    if not os.path.exists(log_path):
        pytest.fail(f"{log_path} was not created.")

    with open(log_path, "r") as f:
        content = f.read()

    if "First short line:" in content:
        pytest.fail("Rollover test failed: old line is still present after limit overflow.")

    if "Second line, definitely bigger" not in content:
        pytest.fail("Rollover test failed: the new big line not found in the final log content.")

    print("[test_logger_rollover_check] OK - the log file was truncated, only second line is present.")

    os.remove(log_path)
