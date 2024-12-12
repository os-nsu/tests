# tests/lab1/test_execution.py

import os
import pytest

# -------------------------------------
# Test outputs from static library
# -------------------------------------

@pytest.mark.dependency(depends=["tests/lab1/test_build.py::test_static_library_compilation"],
						scope="session")
<<<<<<< HEAD
def test_static_library_output(proxy_fixture):
	"""Test proxy outputs for the message from static library."""
	proxy = proxy_fixture
	result = proxy.build_and_run_proxy(wait_until_end=True)
=======
def test_static_library_output(project_dir, master_bin_name, proxy_timeout):
	"""Test proxy outputs for the message from static library."""
	result = build_and_run_proxy(
		project_dir=project_dir,
		proxy_bin_name=master_bin_name,
		proxy_timeout=proxy_timeout,
		wait_until_end=True,
		check=True
	)
>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
	stdout = result.stdout
	expected_output = "Hello from static lib!"
	assert expected_output in stdout, f"Expected output '{expected_output}' not found. Actual output: '{stdout}'."

# -------------------------------------
# Test outputs from dynamic library
# -------------------------------------

@pytest.mark.dependency(depends=["tests/lab1/test_build.py::test_dynamic_library_compilation"],
						scope="session")
<<<<<<< HEAD
def test_dynamic_library_output(proxy_fixture):
	"""Test proxy outputs for the message from dynamic library."""
	proxy = proxy_fixture
	result = proxy.build_and_run_proxy(wait_until_end=True)
	stdout = result.stdout
	expected_output = "Hello from dynamic lib!"
=======
def test_dynamic_library_output(project_dir, master_bin_name, proxy_timeout):
	"""Test proxy outputs for the message from dynamic library."""
	result = build_and_run_proxy(
		project_dir=project_dir,
		proxy_bin_name=master_bin_name,
		proxy_timeout=proxy_timeout,
		wait_until_end=True,
		check=True
	)

	stdout = result.stdout
	expected_output = "Hello from dynamic lib!"

>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
	assert expected_output in stdout, f"Expected output '{expected_output}' not found. Actual output: '{stdout}'."

# -------------------------------------
# Test outputs from the plugin
# -------------------------------------

@pytest.mark.dependency(depends=["tests/lab1/test_build.py::test_plugin_compilation"],
						scope="session")
<<<<<<< HEAD
def test_plugin_output(proxy_fixture):
	"""Test prxy outputs for the messages from plugin."""
	proxy = proxy_fixture
	result = proxy.build_and_run_proxy(wait_until_end=True)
=======
def test_plugin_output(project_dir, master_bin_name, proxy_timeout):
	"""Test prxy outputs for the messages from plugin."""
	result = build_and_run_proxy(
		project_dir=project_dir,
		proxy_bin_name=master_bin_name,
		proxy_timeout=proxy_timeout,
		wait_until_end=True,
		check=True
	)

>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
	stdout = result.stdout
	expected_outputs = [
		"init successfully!",
		"hello from then_start()",
		"hello from then_end()"
	]
<<<<<<< HEAD
=======

>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
	for expected_output in expected_outputs:
		assert expected_output in stdout, f"Expected output '{expected_output}' not found. Actual output: '{stdout}'"

# -------------------------------------
# Test everything together
# -------------------------------------

@pytest.mark.dependency(depends=[
	"test_static_library_output",
	"test_dynamic_library_output",
	"test_plugin_output"])
<<<<<<< HEAD
def test_proxy_outputs(proxy_fixture):
	"""Test that proxy outputs has all expected messages."""
	proxy = proxy_fixture
	result = proxy.build_and_run_proxy(wait_until_end=True)
	stdout = result.stdout

=======
def test_proxy_outputs(project_dir, master_bin_name, proxy_timeout):
	"""Test that proxy outputs has all expected messages."""
	result = build_and_run_proxy(
		project_dir=project_dir,
		proxy_bin_name=master_bin_name,
		proxy_timeout=proxy_timeout,
		wait_until_end=True,
		check=True
	)

	stdout = result.stdout
>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
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
<<<<<<< HEAD
def test_plugin_dlclose(proxy_fixture):
	"""Test that the plugin is correctly closed using dlclose."""
	env = os.environ.copy()
	env['LD_DEBUG'] = 'files'
	proxy = proxy_fixture
	result = proxy.build_and_run_proxy(extra_env=env, wait_until_end=True)
	stdout = result.stdout
	stderr = result.stderr
=======
def test_plugin_dlclose(project_dir, master_bin_name, proxy_timeout):
	"""Test that the plugin is correctly closed using dlclose."""
	env = os.environ.copy()
	env['LD_DEBUG'] = 'files'
	result = build_and_run_proxy(
		project_dir=project_dir,
		proxy_bin_name=master_bin_name,
		proxy_timeout=proxy_timeout,
		env=env,
		wait_until_end=True,
		check=True
  	)

	stdout = result.stdout
	stderr = result.stderr

>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
	assert "fini" in stderr or "fini" in stdout, "The dynamic loader did not output a shutdown message; the plugin might not have been closed properly."

# -------------------------------------
# Test something
# -------------------------------------

@pytest.mark.xfail
def test_run_with_help_argument(proxy_fixture):
	"""Tests running the proxy successfully with '--help' argument."""
<<<<<<< HEAD
	try:
		proxy = proxy_fixture
		result = proxy.build_and_run_proxy(args=['--help'], wait_until_end=True)
		expected_returncode = 0
		assert result.returncode == expected_returncode, f"Proxy with '--help' argument finish with code {result.returncode}, exptected {expected_returncode} ."
		assert  result.stdout != "", "Expected usage information in output."
	except subprocess.CalledProcessError as e:
		pytest.fail(f"Proxy with '--help' argument finish with error: {e.stderr}")
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy with '--help' argument not finish in {proxy.proxy_timeout} seconds")
=======
	result = build_and_run_proxy(
	project_dir=project_dir,
	proxy_bin_name=proxy_bin_name,
 	proxy_timeout=proxy_timeout,
	args=['--help'],
	wait_until_end=True, check=True
	)

	assert  result.stdout != "", "Expected usage information in output."
>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)

@pytest.mark.xfail
def test_run_with_invalid_arguments(proxy_fixture):
	"""Tests running the proxy with invalid arguments."""
<<<<<<< HEAD
	try:
		proxy = proxy_fixture
		result = proxy.build_and_run_proxy(args=['--invalid_arg'], wait_until_end=True)
		assert result.returncode != 0, "Proxy should exit with non-zero code when given invalid arguments."
		assert "Invalid argument" in result.stderr or "unrecognized option" in result.stderr, "Expected error message for invalid argument."
	except subprocess.CalledProcessError as e:
		pytest.fail(f"Proxy finish with error: {e.stderr}")
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy ith invalid argument not finished in {proxy.proxy_timeout} seconds.")
=======
	result = build_and_run_proxy(
		project_dir=project_dir,
		proxy_bin_name=proxy_bin_name,
		proxy_timeout=proxy_timeout,
		args=['--invalid_arg'],
		wait_until_end=True,
		check=True
	)

	assert "Invalid argument" in result.stderr or "unrecognized option" in result.stderr, "Expected error message for invalid argument."
>>>>>>> 984549a (a lot of fixes usage subprocess and check errors)
