# tests/lab1/config/test_config_build.py

import os
import pytest
from steps.build_steps import make, simple_clean
from steps.test_steps import check_file_exists

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    f"tests/lab1/config/test_config_file_structure.py::test_config_files_exist[{os.path.join("install", "libconfig.a")}]"],
                        scope='session')
def test_config_build(project_dir, test_dir):
    simple_clean(project_dir=test_dir)

    make_result = make(
        project_dir=test_dir,
        make_args=["all"],
        extra_env={"PROXY_DIR": project_dir},
        check=False
    )

    if make_result.returncode != 0:
        pytest.fail(
            "[ERROR] Unable to build 'test_config'.\n"
            "Please ensure all required libraries (e.g., 'libconfig') are installed and accessible."
        )

    test_bin = os.path.join(test_dir, "test_config")
    if not check_file_exists(test_bin):
        pytest.fail(
            "[ERROR] 'test_config' binary not found.\n"
            "Please check that the necessary library (e.g., 'libconfig') is installed and correctly configured."
        )