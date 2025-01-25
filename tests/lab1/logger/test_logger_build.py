# tests/lab1/logger/test_logger_build.py

import os
import pytest
from steps.build_steps import make, simple_clean
from steps.test_steps import check_file_exists
from steps.utils import run_command

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    f"tests/lab1/logger/test_logger_file_structure.py::test_logger_files_exist[{os.path.join("install", "liblogger.so")}]",
                        ], scope='session')
def test_logger_symbols(project_dir):
    """
    Check that the dynamic library liblogger.so contains the function init_logger.
    """
    liblogger = os.path.join(project_dir, "install", "liblogger.so")
    if not os.path.isfile(liblogger):
        pytest.fail(f"liblogger.so not found at {liblogger}")

    res = run_command(["nm", "--defined-only", liblogger], cwd=project_dir, check=True)
    symbols = res.stdout
    if "init_logger" not in symbols:
        pytest.fail(
            "[ERROR] 'init_logger' not found in liblogger.so.\n"
            "Make sure you've implemented it or exported it properly."
        )

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    "tests/lab1/logger/test_logger_build.py::test_logger_symbols",
                        ], scope='session')
def test_logger_build(project_dir, test_dir):
    """
    Test the build process for logger and ensure it generates the required binaries.
    """
    simple_clean(project_dir=test_dir)

    make_result = make(
        project_dir=test_dir,
        make_args=["all"],
        extra_env={"PROXY_DIR": project_dir},
        check=False
    )

    if make_result.returncode != 0:
        pytest.fail(
            "[ERROR] Unable to build 'test_logger'.\n"
            "Please ensure all required libraries (e.g., 'liblogger') are installed and accessible."
        )

    test_bin = os.path.join(test_dir, "test_logger")
    if not check_file_exists(test_bin):
        pytest.fail(
            "[ERROR] 'test_logger' binary not found.\n"
            "Please check that the necessary library (e.g., 'liblogger') is installed and correctly configured."
        )