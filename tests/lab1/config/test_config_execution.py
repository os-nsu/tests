# tests/lab1/config/test_config_execution.py

import os
import pytest
from steps.utils import run_command

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/config/test_config_build.py::test_config_build"],
						scope="session")
def test_config_execution(test_dir):

    test_config_bin = os.path.join(test_dir, "test_config")

    result = run_command([test_config_bin], cwd=test_dir, check=True)
    if result.returncode != 0:
        pytest.fail(
            f"[ERROR] test_config exited with non-zero code {result.returncode}.\n"
            f"STDERR:\n{result.stderr}\n"
            f"STDOUT:\n{result.stdout}"
        )

    stdout = result.stdout
    if "[TEST 1] create_config_table first call: PASS" not in stdout:
        pytest.fail(
            "[ERROR] test_config did not report PASS for create_config_table [TEST 1].\n"
            f"Actual stdout:\n{stdout}"
        )
