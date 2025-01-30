# tests/lab1/master/test_master_file_structure.py

import os
import pytest
from steps.test_steps import check_file_exists

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/test_build.py::test_global_build"], scope="session")
@pytest.mark.parametrize("file_path", [
    "proxy",
])
def test_master_files_exist(project_bin_dir, file_path):
    full_path = os.path.join(project_bin_dir, file_path)
    if not check_file_exists(full_path):
        pytest.fail(
            f"[ERROR] Required master_bin file '{file_path}' not found.\n"
            f"Expected path: {full_path}\n"
            "Check your global Makefile for errors."
        )
