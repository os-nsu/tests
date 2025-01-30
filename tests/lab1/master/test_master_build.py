# tests/lab1/master/test_master_build.py

import os
import pytest
from steps.utils import run_command

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/master/test_master_file_structure.py::test_master_files_exist[proxy]"],
                        scope="session")
def test_master_config_symbols(project_bin_dir):
    proxy_bin = os.path.join(project_bin_dir, "proxy")
    res = run_command(["nm", "--defined-only", proxy_bin], cwd=project_bin_dir, check=True)
    symbols = res.stdout
    if "create_config_table" not in symbols:
        pytest.fail(
            "[ERROR] 'create_config_table' not found in static dependincies of master."
        )

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/master/test_master_file_structure.py::test_master_files_exist[proxy]"],
                        scope="session")
def test_master_logger_symbols(project_bin_dir):
    proxy_bin = os.path.join(project_bin_dir, "proxy")
    res = run_command(["ldd", proxy_bin], cwd=project_bin_dir, check=True)
    dependencies = res.stdout
    if "liblogger.so" not in dependencies:
        pytest.fail(
            "[ERROR] 'liblogger.so' not found in proxy's dynamic dependencies of master.\n"
        )
