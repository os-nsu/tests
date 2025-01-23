# tests/lab1/logger/test_build.py

import os
import pytest
from steps.build_steps import make, simple_clean
from steps.test_steps import check_file_exists
from steps.utils import run_command


@pytest.mark.dependency(depends=[
    f"tests/lab1/logger/test_logger_file_structure.py::test_logger_files_exist[{os.path.join("install", "liblogger.so")}]",
], scope='session')
def test_logger_build(project_dir, test_dir):
    print(f"Test dir: {test_dir}\n")
    simple_clean(project_dir=test_dir)

    make(project_dir=test_dir, make_args=["all"], extra_env={
        "PROXY_DIR": project_dir
    })

    check_file_exists(os.path.join(test_dir, "test_logger"))