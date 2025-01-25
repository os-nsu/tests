# tests/lab1/plugins/test_plugin_greeting_file_structure.py

import os
import pytest
from steps.test_steps import check_file_exists

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/test_build.py::test_global_build"], scope="session")
@pytest.mark.parametrize("file_path", [
    os.path.join("greeting.so"),
])
def test_plugin_greeting_files_exist(project_bin_plugins_dir, file_path):
    """
    Verify that greeting.so exists after the global build.
    """
    full_path = os.path.join(project_bin_plugins_dir, file_path)
    if not check_file_exists(full_path):
        pytest.fail(
            f"[ERROR] Required plugin file '{file_path}' was not found.\n"
            f"Expected path: {full_path}\n"
            f"Please verify that your Makefile places greeting.so into '{project_bin_plugins_dir}'."
        )
