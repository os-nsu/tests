# tests/lab2/time/test_time_file_structure.py

import os
import pytest
from steps.test_steps import check_file_exists

@pytest.mark.lab2
@pytest.mark.dependency(depends=["tests/test_file_structure.py::test_directories_exist[install]"], scope="session")
@pytest.mark.parametrize("file_path", [
    "libtime_wrapper.so",
    "libtime_syscall.so",
    "libtime_assembler.so",
    "libtime.so"
])
def test_time_files_exists(proxy_bin_dir, file_path):
    full_path = os.path.join(proxy_bin_dir, file_path)
    if not check_file_exists(full_path):
        pytest.fail(
            f"Required file '{file_path}' was not found in the expected location after the global build.\n"
            f"Expected path: {full_path}\n"
            "Please verify that your Makefile correctly places the file into the 'install/' directory or subdirectories.\n"
        )

