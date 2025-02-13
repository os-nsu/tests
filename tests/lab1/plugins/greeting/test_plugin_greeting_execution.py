# tests/lab1/plugins/greeting/test_plugin_greeting_execution.py

import os
import re
import pytest
from steps.utils import run_command

EXPECTED_BINARIES = [
    "test_plugin_greeting",
]

@pytest.mark.lab1
@pytest.mark.parametrize("binary", EXPECTED_BINARIES)
@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_build.py::test_plugin_greeting_build"],
						scope="session")
def test_plugin_greeting_execution(current_dir, proxy_dir, binary):
    """
    Executes the test_plugin_greeting binary, which performs multiple steps like dlopen,
    dlsym calls, and plugin function invocations (init/fini/name).
    Validates that all steps pass without errors, based on the C test output.
    """

    bin_dir = os.path.join(current_dir, "../", "../", "bin")
    binary_path = os.path.join(bin_dir, binary)

    if not os.path.isfile(binary_path):
        pytest.fail(f"Binary not found: {binary_path}")

    plugin_dir = os.path.join(proxy_dir, "install", "plugins")
    env = os.environ.copy()
    current_ld = env.get("LD_LIBRARY_PATH", "")
    env["LD_LIBRARY_PATH"] = plugin_dir + os.pathsep + current_ld

    result = run_command([binary_path])

    if result.returncode != 0:
        failed_tests = []
        for line in result.stdout.splitlines():
            match = re.search(r"^[^:]+:\d+:([^:]+):FAIL:", line)
            if match:
                failed_tests.append(match.group(1))
        if failed_tests:
            all_failures = ", ".join(failed_tests)
            pytest.fail(
                f"Unity tests failed in {binary_path}: {all_failures}\n"
                f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )
        else:
            pytest.fail(
                f"Unity test in {binary_path} failed, but no specific tests could be identified.\n"
                f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )