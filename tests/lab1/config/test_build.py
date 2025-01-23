# tests/lab1/config/test_build.py

import os
import pytest
from steps.build_steps import make, simple_clean
from steps.test_steps import check_file_exists
from steps.utils import run_command

CURRENT_DIR = os.path.dirname(__file__)

@pytest.mark.dependency(depends=[
    f"tests/lab1/config/test_file_structure.py::test_files_exist[{os.path.join("install", "libconfig.a")}]",
], scope='session')
def test_build_config(project_dir):

    simple_clean(project_dir=CURRENT_DIR)

    make(project_dir=CURRENT_DIR, make_args=["all"], extra_env={
        "PROXY_DIR": project_dir
    })

    check_file_exists(os.path.join(CURRENT_DIR, "test_config"))