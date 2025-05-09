#tests/lab1/test_file_structure.py

import os
import pytest
from steps.test_steps import check_directory_exists, check_file_exists

@pytest.mark.globaltest
@pytest.mark.dependency(depends=[
    "tests/test_build.py::test_global_build"],
    scope='session')
@pytest.mark.parametrize("dir_path", [
    "install",
    os.path.join("install", "plugins"),
])
def test_directories_exist(proxy_dir, dir_path):
    full_path = os.path.join(proxy_dir, dir_path)
    if not check_directory_exists(full_path):
        pytest.fail(
            f"Directory '{dir_path}' not found after building the project.\n"
        )

@pytest.mark.globaltest
@pytest.mark.dependency()
def test_global_makefile_exists(proxy_dir):
    global_makefile = os.path.join(proxy_dir, "Makefile")
    if not check_file_exists(global_makefile):
        pytest.fail(
            f"Global Makefile not found in project root ({global_makefile}).\n"
            "Please provide a Makefile at the project's root to build the entire project."
        )