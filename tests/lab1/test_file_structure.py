# tests/lab1/test_file_structure.py

import os
import pytest
from steps.test_steps import check_file_exists, check_directory_exists

# -------------------------------------
# Test the existence of files
# -------------------------------------

@pytest.mark.dependency()
@pytest.mark.parametrize("file_path", [
    "Makefile",
    os.path.join("src", "backend", "master.c"),
    os.path.join("src", "backend", "static_lib.c"),
    os.path.join("src", "backend", "dynamic_lib.c"),
    os.path.join("contrib", "plugin", "plugin.c"),
])
def test_files_exist(project_dir, file_path):
    """Check that the specified files exist."""
    full_path = os.path.join(project_dir, file_path)
    check_file_exists(full_path)

# -------------------------------------
# Test the existence of directories
# -------------------------------------

@pytest.mark.dependency()
@pytest.mark.parametrize("dir_path", [
    "src",
    os.path.join("src", "backend"),
    "contrib",
    os.path.join("contrib", "plugin"),
    "install"
])
def test_directories_exist(project_dir, dir_path):
    """Check that the specified directories exist."""
    full_path = os.path.join(project_dir, dir_path)
    check_directory_exists(full_path)

