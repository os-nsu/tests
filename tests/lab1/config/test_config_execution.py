# tests/lab1/config/test_config_execution.py

import os
import re
import pytest
from steps.build_steps import make, make_clean
from steps.execution_steps import check_test_result
from steps.utils import run_command

@pytest.mark.dependency(depends=["tests/lab1/config/test_config_build.py::test_config_symbols"],
 						scope="session")
@pytest.mark.lab1
def test_config_create_table(proxy_dir, lab_number, set_cwd_to_test_file_dir):

    target = "test_config_create_config_table"
    make_clean()
    make(make_args=[target],
         extra_env={"PROXY_DIR": proxy_dir, "LAB_NUMBER": str(lab_number)},
         check=True)

    bin_path = os.path.join("bin", target)
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    test_result = run_command(args=[bin_path], check=False)
    check_test_result(test_result=test_result, target=target)

@pytest.mark.dependency(depends=["tests/lab1/config/test_config_build.py::test_config_symbols"],
 						scope="session")
@pytest.mark.lab1
def test_config_destroy_table(proxy_dir, lab_number, set_cwd_to_test_file_dir):

    target = "test_config_destroy_config_table"
    make_clean()
    make(make_args=[target],
         extra_env={"PROXY_DIR": proxy_dir, "LAB_NUMBER": str(lab_number)},
         check=True)

    bin_path = os.path.join("bin", target)
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    test_result = run_command(args=[bin_path], check=False)
    check_test_result(test_result=test_result, target=target)