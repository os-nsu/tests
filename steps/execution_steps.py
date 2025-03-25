# steps/execution_steps.py

import re
import pytest

def check_test_result(test_result, target):
    if test_result.returncode != 0:
        failed_tests = []
        for line in test_result.stdout.splitlines():
            match = re.search(r"^[^:]+:\d+:([^:]+):FAIL:", line)
            if match:
                failed_tests.append(match.group(1))

        if failed_tests:
            all_failures = ", ".join(failed_tests)
            pytest.fail(f"Unity tests failed in {target}: {all_failures}")
        else:
            pytest.fail(f"Unity test in {target} failed, but no specific tests could be identified.")
