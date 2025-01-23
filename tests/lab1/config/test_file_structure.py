# tests/lab1/config/test_file_structure.py

import os
import pytest
from steps.test_steps import check_file_exists, check_directory_exists

@pytest.mark.dependency()
@pytest.mark.parametrize("file_path", [
    os.path.join("install", "libconfig.a"),
])
def test_files_exist(project_dir, file_path):
    full_path = os.path.join(project_dir, file_path)
    check_file_exists(full_path)
