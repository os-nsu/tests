# tests/lab1/config/test_config_file_structure.py

import os
import pytest
from steps.test_steps import check_file_exists

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/test_build.py::test_global_build"],
						scope="session")
@pytest.mark.parametrize("file_path", [
    "libconfig.a",
    ])
def test_config_files_exist(project_bin_dir, file_path):
    full_path = os.path.join(project_bin_dir, file_path)
    if not check_file_exists(full_path):
        pytest.fail(
            f"[ERROR] Required file '{file_path}' was not found in the expected location after the global build.\n"
            f"Expected path: {full_path}\n"
            "Please verify that your Makefile correctly places the file into the 'install/' directory.\n"
        )
