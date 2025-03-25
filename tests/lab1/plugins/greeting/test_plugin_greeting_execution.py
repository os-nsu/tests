# File: tests/lab1/plugins/greeting/test_plugin_greeting_execution.py

import os
import pytest
from steps.build_steps import make, make_clean
from steps.utils import run_command
from steps.execution_steps import check_test_result

current_file_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"],
						scope="session")
@pytest.mark.lab1
def test_plugin_greeting_dlopen(request, proxy_dir, proxy_bin_plugins_dir):

    target = "test_plugin_greeting_dlopen"

    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], extra_env={"PROXY_DIR": proxy_dir}, check=True)

    bin_path = os.path.join(current_file_dir, "bin", "test_plugin_greeting_dlopen")
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    result = run_command([bin_path], extra_env={"LD_LIBRARY_PATH": proxy_bin_plugins_dir}, check=False)
    check_test_result(result, bin_path)


@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"],
						scope="session")
@pytest.mark.lab1
def test_plugin_greeting_dlsym_init(request, proxy_dir):
    target = "test_plugin_greeting_dlsym_init"
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], extra_env={"PROXY_DIR": proxy_dir}, check=True)

    bin_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    result = run_command([bin_path], check=False)
    check_test_result(result, bin_path)


@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"],
						scope="session")
@pytest.mark.lab1
def test_plugin_greeting_dlsym_name(proxy_dir):
    target = "test_plugin_greeting_dlsym_name"
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], extra_env={"PROXY_DIR": proxy_dir}, check=True)

    bin_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    result = run_command([bin_path], check=False)
    check_test_result(result, bin_path)


@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"],
						scope="session")
@pytest.mark.lab1
def test_plugin_greeting_dlsym_fini(proxy_dir):
    target = "test_plugin_greeting_dlsym_fini"
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], extra_env={"PROXY_DIR": proxy_dir}, check=True)

    bin_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    result = run_command([bin_path], check=False)
    check_test_result(result, bin_path)


@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"],
						scope="session")
@pytest.mark.lab1
def test_plugin_greeting_call_init(proxy_dir):
    target = "test_plugin_greeting_call_init"
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], extra_env={"PROXY_DIR": proxy_dir}, check=True)

    bin_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    result = run_command([bin_path], check=False)
    check_test_result(result, bin_path)


@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"],
						scope="session")
@pytest.mark.lab1
def test_plugin_greeting_call_name(proxy_dir):
    target = "test_plugin_greeting_call_name"
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], extra_env={"PROXY_DIR": proxy_dir}, check=True)

    bin_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    result = run_command([bin_path], check=False)
    check_test_result(result, bin_path)


@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"],
						scope="session")
@pytest.mark.lab1
def test_plugin_greeting_call_fini(proxy_dir):
    target = "test_plugin_greeting_call_fini"
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], extra_env={"PROXY_DIR": proxy_dir}, check=True)

    bin_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    result = run_command([bin_path], check=False)
    check_test_result(result, bin_path)


@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"],
						scope="session")
@pytest.mark.lab1
def test_plugin_greeting_dlclose(proxy_dir):
    target = "test_plugin_greeting_dlclose"
    make_clean(build_dir=current_file_dir)
    make(build_dir=current_file_dir, make_args=[target], extra_env={"PROXY_DIR": proxy_dir}, check=True)

    bin_path = os.path.join(current_file_dir, "bin", target)
    assert os.path.exists(bin_path), f"Binary not found: {bin_path}"

    result = run_command([bin_path], check=False)
    check_test_result(result, bin_path)