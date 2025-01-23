# tests/lab1/logger/test_file_structure.py

import os
import pytest
from steps.test_steps import check_file_exists

@pytest.mark.dependency()
@pytest.mark.parametrize("file_path", [
    os.path.join("install", "liblogger.so"),
])
def test_logger_files_exist(project_dir, file_path):
    full_path = os.path.join(project_dir, file_path)
    check_file_exists(full_path)
