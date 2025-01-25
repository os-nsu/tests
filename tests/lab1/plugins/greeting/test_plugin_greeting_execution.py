# tests/lab1/plugins/greeting/test_plugin_greeting_execution.py

import os
import pytest
from steps.utils import run_command

@pytest.mark.lab1
@pytest.mark.dependency(
    depends=["tests/lab1/plugins/greeting/test_plugin_greeting_build.py::test_plugin_greeting_build"],
    scope="session"
)
def test_plugin_greeting_execution(test_dir):
    """
    Executes the test_plugin_greeting binary, which performs multiple steps like dlopen,
    dlsym calls, and plugin function invocations (init/fini/name).
    Validates that all steps pass without errors, based on the updated C test output.
    """

    test_bin = os.path.join(test_dir, "test_plugin_greeting")

    result = run_command([test_bin], cwd=test_dir, check=False)

    if result.returncode != 0:
        pytest.fail(
            f"[ERROR] test_plugin_greeting returned non-zero exit code {result.returncode}.\n"
            f"STDERR:\n{result.stderr}\n"
            f"STDOUT:\n{result.stdout}"
        )

    stdout = result.stdout

    expected_outputs = {
        "[TEST 1] dlopen(greeting.so): PASS": "[ERROR] dlopen failed.",
        "[TEST 2] dlsym(\"init\"): PASS": "[ERROR] dlsym(\"init\") failed.",
        "[TEST 3] dlsym(\"name\"): PASS": "[ERROR] dlsym(\"name\") failed.",
        "[TEST 4] dlsym(\"fini\"): PASS": "[ERROR] dlsym(\"fini\") failed.",
        "[TEST 5] init() returned: PASS": "[ERROR] init() call failed.",
        "[TEST 6] name() returned: PASS (got: greeting)": "[TEST 6] name() returned: FAIL (NULL).",
        "[TEST 7] fini() returned: PASS": "[ERROR] fini() call failed.",
        "[TEST 8] dlclose(handle): PASS": "[ERROR] dlclose(handle) failed.",
    }

    for expected, error_message in expected_outputs.items():
        if expected not in stdout:
            pytest.fail(f"{error_message} Expected: {expected}")
