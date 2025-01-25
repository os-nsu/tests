# tests/lab1/plugins/greeting/test_plugin_greeting_build.py

import os
import pytest
from steps.build_steps import make, simple_clean
from steps.test_steps import check_file_exists
from steps.utils import run_command

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/plugins/greeting/test_plugin_greeting_file_structure.py::test_plugin_greeting_files_exist[greeting.so]"], scope="session")
def test_plugin_greeting_symbols(project_bin_plugins_dir):
    """
    Verify that the plugin (greeting.so) contains the functions init, fini, and name.
    """
    greeting_plugin = os.path.join(project_bin_plugins_dir, "greeting.so")

    res = run_command(["nm", "--defined-only", greeting_plugin], cwd=project_bin_plugins_dir, check=True)
    symbols = res.stdout

    required_symbols = ["init", "fini", "name"]
    for sym in required_symbols:
        if sym not in symbols:
            pytest.fail(
                f"[ERROR] '{sym}' not found in greeting.so.\n"
                "Check your plugin's exported symbols or function naming."
            )

@pytest.mark.lab1
@pytest.mark.dependency(depends=[
    "tests/lab1/plugins/greeting/test_plugin_greeting_build.py::test_plugin_greeting_symbols"
], scope="session")
def test_plugin_greeting_build(project_dir, test_dir):
    """
    Build the local binary 'test_plugin_greeting' (which uses dlopen)
    to test the functionality of init/fini/name.
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
            f"[ERROR] Failed to build 'test_plugin_greeting' in {test_dir}.\n"
            f"Return code: {make_result.returncode}\n"
            f"STDERR:\n{make_result.stderr}\n"
        )

    test_bin = os.path.join(test_dir, "test_plugin_greeting")
    if not check_file_exists(test_bin):
        pytest.fail(
            "[ERROR] 'test_plugin_greeting' binary not found.\n"
            "Please check that the necessary library (e.g., 'greeting') is installed and correctly configured."
        )