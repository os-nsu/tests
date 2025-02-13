# tests/lab1/test_build.py

import os
import pytest

from steps.build_steps import make, make_clean

@pytest.mark.globaltest
@pytest.mark.dependency(depends=[
    "tests/test_file_structure.py::test_global_makefile_exists"],
    scope='session')
def test_global_build(proxy_dir):
    clean_result = make_clean(build_dir=proxy_dir)
    if clean_result.returncode != 0:
        pytest.fail(
            f"Failed to clean the project.\n"
            f"Return code: {clean_result.returncode}\n"
            f"STDERR:\n{clean_result.stderr}\n"
            "Check your Makefile 'clean' target."
        )
    build_result = make(build_dir=proxy_dir, make_args=["all"], check=False)
    if build_result.returncode != 0:
        pytest.fail(
            f"Failed to build the project with the global Makefile.\n"
            f"Return code: {build_result.returncode}\n"
            f"STDERR:\n{build_result.stderr}\n"
            "Check your source code or Makefile targets."
        )