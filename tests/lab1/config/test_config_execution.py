# tests/lab1/config/test_execution.py

import os
import pytest
from steps.test_steps import check_file_exists
from steps.utils import run_command


@pytest.mark.dependency(depends=["tests/lab1/config/test_config_build.py::test_config_build"],
						scope="session")
def test_config_execution(test_dir):

    test_config_bin = os.path.join(test_dir, "test_config")

    result = run_command([test_config_bin], cwd=test_dir, check=True)
    stdout = result.stdout

    assert "[TEST 1] create_config_table first call: PASS" in stdout, "TEST 1 failed"
