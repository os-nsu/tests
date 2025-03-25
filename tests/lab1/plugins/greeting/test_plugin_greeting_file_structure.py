# tests/lab1/plugins/test_plugin_greeting_file_structure.py

import os
import pytest
from steps.test_steps import check_file_exists

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/test_file_structure.py::test_directories_exist[install/plugins]"],
						scope="session")
@pytest.mark.parametrize("file_path", [
    os.path.join("greeting.so"),
])
def test_plugin_greeting_files_exist(proxy_bin_plugins_dir, file_path):
    """
    Verify that greeting.so exists after the global build.
    """
    full_path = os.path.join(proxy_bin_plugins_dir, file_path)
    if not check_file_exists(full_path):
        pytest.fail(
            f"Required plugin file '{file_path}' was not found.\n"
            f"Expected path: {full_path}\n"
            f"Please verify that your Makefile correctly places greeting.so into '{proxy_bin_plugins_dir}'."
        )
