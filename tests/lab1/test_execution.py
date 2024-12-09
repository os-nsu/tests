# tests/lab1/test_execution.py

import os
import subprocess
import pytest

from steps.proxy_steps import (
	build_and_run_proxy,
)
# -------------------------------------
# Test outputs from static library
# -------------------------------------

@pytest.mark.dependency(depends=["tests/lab1/test_build.py::test_static_library_compilation"],
                        scope="session")
def test_static_library_output(project_dir, master_bin_name, proxy_timeout):
    """Test proxy outputs for the message from static library."""
    result = build_and_run_proxy(
        project_dir=project_dir,
        proxy_bin_name=master_bin_name,
        proxy_timeout=proxy_timeout,
        wait_until_end=True
    )
    stdout = result.stdout
    expected_output = "Hello from static lib!"
    assert expected_output in stdout, f"Expected output '{expected_output}' not found. Actual output: '{stdout}'."

# -------------------------------------
# Test outputs from dynamic library
# -------------------------------------

@pytest.mark.dependency(depends=["tests/lab1/test_build.py::test_dynamic_library_compilation"],
                        scope="session")
def test_dynamic_library_output(project_dir, master_bin_name, proxy_timeout):
    """Test proxy outputs for the message from dynamic library."""
    result = build_and_run_proxy(
        project_dir=project_dir,
        proxy_bin_name=master_bin_name,
        proxy_timeout=proxy_timeout,
        wait_until_end=True
    )
    stdout = result.stdout
    expected_output = "Hello from dynamic lib!"
    assert expected_output in stdout, f"Expected output '{expected_output}' not found. Actual output: '{stdout}'."

# -------------------------------------
# Test outputs from the plugin
# -------------------------------------

@pytest.mark.dependency(depends=["tests/lab1/test_build.py::test_plugin_compilation"],
                        scope="session")
def test_plugin_output(project_dir, master_bin_name, proxy_timeout):
    """Test prxy outputs for the messages from plugin."""
    result = build_and_run_proxy(
        project_dir=project_dir,
        proxy_bin_name=master_bin_name,
        proxy_timeout=proxy_timeout,
        wait_until_end=True
    )
    stdout = result.stdout
    expected_outputs = [
        "init successfully!",
        "hello from then_start()",
        "hello from then_end()"
    ]
    for expected_output in expected_outputs:
        assert expected_output in stdout, f"Expected output '{expected_output}' not found. Actual output: '{stdout}'"

# -------------------------------------
# Test everything together
# -------------------------------------

@pytest.mark.dependency(depends=[
    "test_static_library_output",
    "test_dynamic_library_output",
    "test_plugin_output"])
def test_proxy_outputs(project_dir, master_bin_name, proxy_timeout):
    """Test that proxy outputs has all expected messages."""
    result = build_and_run_proxy(
        project_dir=project_dir,
        proxy_bin_name=master_bin_name,
        proxy_timeout=proxy_timeout,
        wait_until_end=True
    )
    stdout = result.stdout

    expected_outputs = [
        "Hello from static lib!",
        "Hello from dynamic lib!",
        "Use default configuration file",
        "init successfully!",
        "hello from then_start()",
        "hello from then_end()"
    ]

    for expected_output in expected_outputs:
        assert expected_output in stdout, f"Expected output '{expected_output}' not found. Actual output: '{stdout}'"

# -------------------------------------
# Test plugin dlclose
# -------------------------------------

@pytest.mark.dependency(depends=["test_plugin_output"])
def test_plugin_dlclose(project_dir, master_bin_name, proxy_timeout):
    """Test that the plugin is correctly closed using dlclose."""
    env = os.environ.copy()
    env['LD_DEBUG'] = 'files'
    result = build_and_run_proxy(
        project_dir=project_dir,
        proxy_bin_name=master_bin_name,
        proxy_timeout=proxy_timeout,
        env=env,
        wait_until_end=True
    )
    stdout = result.stdout
    stderr = result.stderr
    assert "fini" in stderr or "fini" in stdout, "The dynamic loader did not output a shutdown message; the plugin might not have been closed properly."

# -------------------------------------
# Test something
# -------------------------------------

@pytest.mark.xfail
def test_run_with_help_argument(project_dir, proxy_bin_name, proxy_timeout):
	"""Tests running the proxy successfully with '--help' argument."""
	try:
		result = build_and_run_proxy(project_dir, proxy_bin_name, proxy_timeout=proxy_timeout, args=['--help'], wait_until_end=True)
		expected_returncode = 0
		assert result.returncode == expected_returncode, f"Proxy with '--help' argument finish with code {result.returncode}, exptected {expected_returncode} ."
		assert  result.stdout != "", "Expected usage information in output."
	except subprocess.CalledProcessError as e:
		pytest.fail(f"Proxy with '--help' argument finish with error: {e.stderr}")
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy with '--help' argument not finish in {proxy_timeout} seconds")

@pytest.mark.xfail
def test_run_with_invalid_arguments(project_dir, proxy_bin_name, proxy_timeout):
	"""Tests running the proxy with invalid arguments."""
	try:
		result = build_and_run_proxy(project_dir, proxy_bin_name, proxy_timeout=proxy_timeout, args=['--invalid_arg'], wait_until_end=True)
		assert result.returncode != 0, "Proxy should exit with non-zero code when given invalid arguments."
		assert "Invalid argument" in result.stderr or "unrecognized option" in result.stderr, "Expected error message for invalid argument."
	except subprocess.CalledProcessError as e:
		pytest.fail(f"Proxy finish with error: {e.stderr}")
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy ith invalid argument not finished in {proxy_timeout} seconds.")
