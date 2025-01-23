# tests/lab1/config/test_build.py

import os
import pytest
from steps.build_steps import make, simple_clean
from steps.test_steps import check_file_exists
from steps.utils import run_command


@pytest.mark.dependency(depends=[
    f"tests/lab1/config/test_config_file_structure.py::test_config_files_exist[{os.path.join("install", "libconfig.a")}]",
], scope='session')
def test_config_build(project_dir, test_dir):
    simple_clean(project_dir=test_dir)

    make(project_dir=test_dir, make_args=["all"], extra_env={
        "PROXY_DIR": project_dir
    })

    check_file_exists(os.path.join(test_dir, "test_config"))