# tests/lab1/logger/test_logger_execution.py

import os
import re
import pytest
from steps.build_steps import make, make_clean
from steps.execution_steps import check_test_result
from steps.utils import run_command


@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    f"tests/lab1/logger/test_logger_file_structure.py::test_logger_files_exist[liblogger.so]"],
                        scope='session')
def test_logger_init_logger(proxy_dir, lab_number, set_cwd_to_test_file_dir):

    target = "test_logger_init_logger"
    make_clean()
    make(make_args=[target],
         extra_env={"PROXY_DIR": proxy_dir, "LAB_NUMBER": str(lab_number)},
         check=True)

    binary_path = os.path.join("bin", target)
    assert os.path.exists(binary_path), f"Binary not found: {binary_path}"

    test_result = run_command([binary_path], check=False)
    check_test_result(test_result, binary_path)

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    f"tests/lab1/logger/test_logger_file_structure.py::test_logger_files_exist[liblogger.so]"],
                        scope='session')
def test_logger_fini_logger(proxy_dir, lab_number, set_cwd_to_test_file_dir):

    target = "test_logger_fini_logger"
    make_clean()
    make(make_args=[target],
         extra_env={"PROXY_DIR": proxy_dir, "LAB_NUMBER": str(lab_number)},
         check=True)

    binary_path = os.path.join("bin", target)
    assert os.path.exists(binary_path), f"Binary not found: {binary_path}"

    test_result = run_command([binary_path], check=False)
    check_test_result(test_result, binary_path)

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    f"tests/lab1/logger/test_logger_file_structure.py::test_logger_files_exist[liblogger.so]"],
                        scope='session')
def test_logger_init_logger_args(proxy_dir, lab_number, set_cwd_to_test_file_dir):

    target = "test_logger_init_logger_args"
    make_clean()
    make(make_args=[target],
         extra_env={"PROXY_DIR": proxy_dir, "LAB_NUMBER": str(lab_number)},
         check=True)


    binary_path = os.path.join("bin", target)
    assert os.path.exists(binary_path), f"Binary not found: {binary_path}"

    test_result = run_command([binary_path], check=False)
    check_test_result(test_result, binary_path)