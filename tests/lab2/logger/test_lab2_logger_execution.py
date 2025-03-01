# tests/lab2/logger/test_logger_execution.py

import os
import pytest
import re
from steps.utils import run_command

# Regular expression to check the log message format:
# Format: "YYYY-MM-DDTHH:MM:SS(timezone) filename line_number [PID] | LEVEL: MESSAGE"
LOG_REGEX = re.compile(
    r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\(.+\) .+ \d+ \[[0-9]+\] \| (DEBUG|INFO|WARNING|ERROR|FATAL): .+$'
)

@pytest.mark.dependency(depends=["tests/lab2/logger/test_logger_build.py::test_logger_symbols",
								 "tests/lab1/logger/test_logger_execution.py::test_logger_execution[test_logger_init_logger]",
								 "tests/lab1/logger/test_logger_execution.py::test_logger_execution[test_logger_fini_logger]",],
						scope="session")
@pytest.mark.lab2
def test_write_log_stdout_execution(current_dir):
    """
    Test that the logger writes messages with all levels to STDOUT.
    The C binary 'test_write_log_stdout' is executed and its stdout is captured.
    Each log message should match the expected format.
    """
    bin_dir = os.path.join(current_dir, "../", "bin")

    binary_path = os.path.join(bin_dir, "test_lab2_logger_write_log_stdout")

    result = run_command([binary_path], check=True)
    stdout_lines = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]

    assert len(stdout_lines) >= 5, "Expected at least 5 log messages on STDOUT"

    for line in stdout_lines:
        assert LOG_REGEX.match(line), f"STDOUT log message does not match format: {line}"

# @pytest.mark.lab2
# @pytest.mark.dependency(depends=["tests/lab2/logger/test_logger_build.py::test_logger_build"],
#                         scope="session")
# def test_logger_rollover_check(current_dir):

#     bin_dir = os.path.join(current_dir, "../", "bin")
#     binary_path = os.path.join(bin_dir, "test_logger_file_stream_rollover")
#     log_path = os.path.join(bin_dir, "rollover_test.log")

#     if os.path.exists(log_path):
#         os.remove(log_path)

#     result = run_command([binary_path], check=True)
#     if result.returncode != 0:
#         pytest.fail(
#             f"Binary {binary_path} crashed or returned error code {result.returncode}.\n"
#         )

#     if not os.path.exists(log_path):
#         pytest.fail(f"{log_path} was not created.")

#     with open(log_path, "r") as f:
#         content = f.read()

#     if "First short line:" in content:
#         pytest.fail("Rollover test failed: old line is still present after limit overflow.")

#     if "Second line, definitely bigger" not in content:
#         pytest.fail("Rollover test failed: the new big line not found in the final log content.")

#     print("[test_logger_rollover_check] OK - the log file was truncated, only second line is present.")

#     os.remove(log_path)