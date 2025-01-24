# tests/lab1/test_build.py

import os
import pytest

from steps.build_steps import make
from steps.utils import run_command

@pytest.mark.globaltest
@pytest.mark.dependency(depends=[
    "tests/test_file_structure.py::test_global_makefile_exists"],
    scope='session')
def test_global_build(project_dir):
    clean_result = make(project_dir=project_dir, make_args=["clean"], check=False)
    if clean_result.returncode != 0:
        pytest.fail(
            f"[ERROR] Failed to clean the project.\n"
            f"Return code: {clean_result.returncode}\n"
            f"STDERR:\n{clean_result.stderr}\n"
            "Check your Makefile 'clean' target."
        )
    build_result = make(project_dir=project_dir, make_args=["all"], check=False)
    if build_result.returncode != 0:
        pytest.fail(
            f"[ERROR] Failed to build the project with the global Makefile.\n"
            f"Return code: {build_result.returncode}\n"
            f"STDERR:\n{build_result.stderr}\n"
            "Check your source code or Makefile targets."
        )