import os
import pytest
from steps.test_steps import check_directory_exists, check_file_exists

@pytest.mark.dependency()
@pytest.mark.parametrize("dir_path", [
    "install",
    os.path.join("install", "plugins"),
])
def test_directories_exist(project_dir, dir_path):
    full_path = os.path.join(project_dir, dir_path)
    check_directory_exists(full_path)

@pytest.mark.dependency()
@pytest.mark.parametrize("file_path", [
    "Makefile"
])
def test_files_exist(project_dir, file_path):
    full_path = os.path.join(project_dir, file_path)
    check_file_exists(full_path)