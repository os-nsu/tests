#tests/lab1/logger/test_logger_execution.py

import os
import re
import pytest
from steps.utils import run_command

EXPECTED_BINARIES = [
    "test_logger_init_logger",
    "test_logger_fini_logger",
    "test_logger_init_logger_args"
]

@pytest.mark.lab1
@pytest.mark.parametrize("binary", EXPECTED_BINARIES)
@pytest.mark.dependency(depends=["tests/lab1/logger/test_logger_build.py::test_logger_build"],
                        scope="session")
def test_logger_execution(current_dir, binary):

    bin_dir = os.path.join(current_dir, "../", "bin")
    binary_path = os.path.join(bin_dir, binary)

    if not os.path.isfile(binary_path):
        pytest.fail(f"Binary not found: {binary_path}")

    result = run_command([binary_path])

    if result.returncode != 0:
        failed_tests = []
        for line in result.stdout.splitlines():
            match = re.search(r"^[^:]+:\d+:([^:]+):FAIL:", line)
            if match:
                failed_tests.append(match.group(1))

        if failed_tests:
            all_failures = ", ".join(failed_tests)
            pytest.fail(f"Unity tests failed in {binary_path}: {all_failures}")
        else:
            pytest.fail(f"Unity test in {binary_path} failed, but no specific tests could be identified.")
