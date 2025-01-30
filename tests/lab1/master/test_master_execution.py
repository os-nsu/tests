# tests/lab1/master/test_master_execution.py

import os
import pytest
from steps.utils import run_command

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_master_config_symbols",
                                 "tests/lab1/master/test_master_build.py::test_master_logger_symbols",
                                 "tests/lab1/config/test_config_execution.py::test_config_execution",
                                 "tests/lab1/logger/test_logger_execution.py::test_logger_execution"],
                        scope="session")
def test_master_execution(project_bin_dir):
    proxy_bin = os.path.join(project_bin_dir, "proxy")

    result = run_command([proxy_bin], check=True)
    stdout = result.stdout
    stderr = result.stderr

    if result.returncode != 0:
        pytest.fail(
            f"[ERROR] Master bin returned code {result.returncode}, expected 0.\n"
            f"STDERR:\n{stderr}\n"
            f"STDOUT:\n{stdout}"
        )

    if "greeting initialized" not in stdout:
        pytest.fail("[ERROR] Missing 'greeting initialized' in master stdout (init).")
    if "Hello, world!" not in stdout:
        pytest.fail("[ERROR] Missing 'Hello, world!' in master stdout (executor_start_hook).")
    if "greeting finished" not in stdout:
        pytest.fail("[ERROR] Missing 'greeting finished' in master stdout (fini).")

    if "Failed to initialize the config" in stderr:
        pytest.fail("[ERROR] Config init failed unexpectedly.")
    if "Failed to initialize the logger" in stderr:
        pytest.fail("[ERROR] Logger init failed unexpectedly.")
