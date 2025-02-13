# tests/lab1/config/test_config_build.py

import os
import pytest
from steps.build_steps import make, make_clean
from steps.symbols import check_symbols

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
	f"tests/lab1/config/test_config_file_structure.py::test_config_files_exist[libconfig.a]"],
						scope="session")
def test_config_symbols(proxy_bin_dir):
	"""
	Check that the required symbols exists in libconfig.a and are of the correct type.
	"""
	libconfig_path = os.path.join(proxy_bin_dir, "libconfig.a")

	required_symbols = ["create_config_table" , "destroy_config_table"]
	missing = check_symbols(libconfig_path, required_symbols)

	if missing:
		pytest.fail(f"The following required symbols are missing or incorrect in libconfig.a : {', '.join(missing)}")

@pytest.mark.dependency(depends=[
	f"tests/lab1/config/test_config_build.py::test_config_symbols"],
						scope="session")
@pytest.mark.lab1
def test_config_build(current_dir, proxy_dir):
	build_dir = os.path.join(current_dir, "../")
	make_clean(build_dir=build_dir)
	result = make(build_dir=build_dir, make_args=["config"], extra_env={"PROXY_DIR": proxy_dir}, check=True)
	assert result.returncode == 0