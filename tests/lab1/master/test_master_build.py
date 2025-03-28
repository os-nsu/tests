# tests/lab1/master/test_master_build.py

import os
import pytest
from steps.build_steps import make, make_clean
from steps.symbols import check_symbols
from steps.utils import run_command

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/master/test_master_file_structure.py::test_master_files_exist[proxy]"],
						scope="session")
def test_master_config_symbols(proxy_bin_dir):
	proxy_bin = os.path.join(proxy_bin_dir, "proxy")
	required_symbols = ["create_config_table", "destroy_config_table"]
	missing = check_symbols(proxy_bin, required_symbols)
	if missing:
		pytest.fail(f"The following required symbols are missing or incorrect in proxy: {', '.join(missing)}")

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/master/test_master_file_structure.py::test_master_files_exist[proxy]"],
						scope="session")
def test_master_logger_symbols(proxy_bin_dir):
	proxy_bin = os.path.join(proxy_bin_dir, "proxy")
	res = run_command(["ldd", proxy_bin], check=True)
	dependencies = res.stdout
	if "liblogger.so" not in dependencies:
		pytest.fail(
			"'liblogger.so' not found in proxy's dynamic dependencies of master.\n"
		)
