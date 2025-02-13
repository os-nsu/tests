# tests/lab1/logger/test_logger_build.py

import os
import pytest
from steps.build_steps import make, make_clean
from steps.symbols import check_symbols

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    f"tests/lab1/logger/test_logger_file_structure.py::test_logger_files_exist[liblogger.so]"],
                        scope='session')
def test_logger_symbols(proxy_bin_dir):
    """
    Check that the required symbols exist in liblogger.so and are of the correct type.
    """
    liblogger_path = os.path.join(proxy_bin_dir, "liblogger.so")

    required_symbols = ["init_logger", "fini_logger"]

    missing = check_symbols(liblogger_path, required_symbols)
    if missing:
        pytest.fail(f"The following required symbols are missing or incorrect in liblogger.so: {', '.join(missing)}")

@pytest.mark.dependency(depends=[
	f"tests/lab1/logger/test_logger_build.py::test_logger_symbols"],
						scope="session")
@pytest.mark.lab1
def test_logger_build(current_dir, proxy_dir):
	build_dir = os.path.join(current_dir, "../")
	make_clean(build_dir=build_dir)
	result = make(build_dir=build_dir, make_args=["logger"], extra_env={"PROXY_DIR": proxy_dir}, check=True)
	assert result.returncode == 0, "Logger tests build failed."