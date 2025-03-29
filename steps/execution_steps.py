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


def check_error_output(result, expected_message, expected_returncode=1, target=""):
    if expected_message not in result.stderr:
        context = f" for {target}" if target else ""
        pytest.fail(f"Expected error message{context}:\n'{expected_message}', but got:\n{result.stderr}")
    if result.returncode != expected_returncode:
        pytest.fail(f"Expected return code {expected_returncode}, got {result.returncode}")
