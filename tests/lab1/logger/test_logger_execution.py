# tests/lab1/logger/test_logger_execution.py

import os
import re
import pytest
from steps.build_steps import make, make_clean
from steps.execution_steps import check_test_result
from steps.utils import run_command

current_file_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    f"tests/lab1/logger/test_logger_file_structure.py::test_logger_files_exist[liblogger.so]"],
                        scope='session')
def test_logger_init_logger(request, proxy_dir):

    target = request.function.__name__
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], extra_env={"PROXY_DIR": proxy_dir}, check=True)

    binary_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(binary_path), f"Binary not found: {binary_path}"

    test_result = run_command([binary_path], check=False)
    check_test_result(test_result, binary_path)

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    f"tests/lab1/logger/test_logger_file_structure.py::test_logger_files_exist[liblogger.so]"],
                        scope='session')
def test_logger_fini_logger(request):

    target = request.function.__name__
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], check=True)

    binary_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(binary_path), f"Binary not found: {binary_path}"

    test_result = run_command([binary_path], check=False)
    check_test_result(test_result, binary_path)

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    f"tests/lab1/logger/test_logger_file_structure.py::test_logger_files_exist[liblogger.so]"],
                        scope='session')
def test_logger_init_logger_args(request):

    target = request.function.__name__
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], check=True)

    binary_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(binary_path), f"Binary not found: {binary_path}"

    test_result = run_command([binary_path], check=False)
    check_test_result(test_result, binary_path)