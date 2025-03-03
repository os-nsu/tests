# tests/lab1/master/test_master_execution.py

import os
import shutil
import pytest
from steps.utils import run_command
from steps.backup_utils import file_backup

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_master_config_symbols",
								 "tests/lab1/master/test_master_build.py::test_master_logger_symbols",
								 "tests/lab1/config/test_config_execution.py::test_config_execution[test_config_create_config_table]",
								 "tests/lab1/config/test_config_execution.py::test_config_execution[test_config_destroy_config_table]",
								 "tests/lab1/logger/test_logger_execution.py::test_logger_execution[test_logger_init_logger]",
								 "tests/lab1/logger/test_logger_execution.py::test_logger_execution[test_logger_fini_logger]",
								 "tests/lab1/logger/test_logger_execution.py::test_logger_execution[test_logger_init_logger_args]",
								 "tests/lab1/plugins/greeting/test_plugin_greeting_execution.py::test_plugin_greeting_execution[test_plugin_greeting]"],
						scope="session")
def test_master_execution(proxy_bin_dir):
	proxy_bin = os.path.join(proxy_bin_dir, "proxy")

	result = run_command([proxy_bin], check=True)
	stdout = result.stdout
	stderr = result.stderr

	if result.returncode != 0:
		pytest.fail(
			f"Master bin returned code {result.returncode}, expected 0.\n"
			f"STDERR:\n{stderr}\n"
			f"STDOUT:\n{stdout}"
		)

	if "greeting initialized" not in stdout:
		pytest.fail("Missing 'greeting initialized' in master stdout (init).")
	if "Hello, world!" not in stdout:
		pytest.fail("Missing 'Hello, world!' in master stdout (executor_start_hook).")
	if "greeting finished" not in stdout:
		pytest.fail("Missing 'greeting finished' in master stdout (fini).")
	if "Failed to initialize the config" in stderr:
		pytest.fail("Config init failed unexpectedly.")
	if "Failed to initialize the logger" in stderr:
		pytest.fail("Logger init failed unexpectedly.")

@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_stubs_logger_build"],
						scope="session")
@pytest.mark.lab1
def test_master_logger_missing_init(proxy_bin_dir, file_backup):
	logger_path = os.path.join(proxy_bin_dir, "liblogger.so")

	file_backup.backup(logger_path)

	current_dir = os.path.dirname(os.path.abspath(__file__))
	dummy_logger_path = os.path.join(current_dir, "..", "bin", "logger_bad_init.so")
	shutil.copy2(dummy_logger_path, logger_path)

	proxy_bin = os.path.join(proxy_bin_dir, "proxy")
	result = run_command([proxy_bin], check=False)
	stderr = result.stderr
	expected_msg = "Failed to initialize the logger"
	assert expected_msg in stderr, f"Expected error message not found."
	assert result.returncode == 1, f"Expected return_code 1, got {result.returncode}"

@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_stubs_logger_build"],
						scope="session")
@pytest.mark.lab1
def test_master_logger_missing_fini(proxy_bin_dir, file_backup):
	logger_path = os.path.join(proxy_bin_dir, "liblogger.so")

	file_backup.backup(logger_path)

	current_dir = os.path.dirname(os.path.abspath(__file__))
	dummy_logger_path = os.path.join(current_dir, "..", "bin", "logger_bad_fini.so")
	shutil.copy2(dummy_logger_path, logger_path)

	proxy_bin = os.path.join(proxy_bin_dir, "proxy")
	result = run_command([proxy_bin], check=False)
	stderr = result.stderr
	expected_msg = "Couldn't shut down logger"
	assert expected_msg in stderr, f"Expected error message not found."
	assert result.returncode == 1, f"Expected return_code 1, got {result.returncode}"

@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_stubs_plugin_build"],
						scope="session")
@pytest.mark.lab1
def test_master_plugin_missing(proxy_bin_dir, file_backup):
	plugin_dir = os.path.join(proxy_bin_dir, "plugins")
	plugin_path = os.path.join(plugin_dir, "greeting.so")

	file_backup.backup(plugin_path)

	proxy_bin = os.path.join(proxy_bin_dir, "proxy")
	result = run_command([proxy_bin], check=True)
	stderr = result.stderr
	expected_msg = "Library couldn't be opened."
	assert expected_msg in stderr, f"Expected error message not found."
	assert result.returncode == 1, f"Expected return_code 1, got {result.returncode}"

@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_stubs_plugin_build"],
						scope="session")
@pytest.mark.lab1
def test_master_plugin_missing_init(proxy_bin_dir, file_backup):
	plugin_dir = os.path.join(proxy_bin_dir, "plugins")
	plugin_path = os.path.join(plugin_dir, "greeting.so")

	file_backup.backup(plugin_path)

	current_dir = os.path.dirname(os.path.abspath(__file__))
	fake_plugin_path = os.path.join(current_dir, "..", "bin", "greeting_bad_init.so")
	shutil.copy2(fake_plugin_path, plugin_path)

	proxy_bin = os.path.join(proxy_bin_dir, "proxy")
	result = run_command([proxy_bin], check=False)
	stderr = result.stderr
	expected_msg = "Library couldn't execute init."
	assert expected_msg in stderr, f"Expected message not found."
	assert result.returncode == 1, f"Expected return_code 1, got {result.returncode}"

@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_stubs_plugin_build"],
						scope="session")
@pytest.mark.lab1
def test_master_plugin_missing_name(proxy_bin_dir, file_backup):
	plugin_dir = os.path.join(proxy_bin_dir, "plugins")
	plugin_path = os.path.join(plugin_dir, "greeting.so")

	file_backup.backup(plugin_path)

	current_dir = os.path.dirname(os.path.abspath(__file__))
	fake_plugin_path = os.path.join(current_dir, "..", "bin", "greeting_bad_name.so")
	shutil.copy2(fake_plugin_path, plugin_path)

	proxy_bin = os.path.join(proxy_bin_dir, "proxy")
	result = run_command([proxy_bin], check=False)
	stderr = result.stderr
	expected_msg = "Library couldn't execute name."
	assert expected_msg in stderr, f"Expected message not found."
	assert result.returncode == 1, f"Expected return_code 1, got {result.returncode}"

@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_stubs_plugin_build"],
						scope="session")
@pytest.mark.lab1
def test_master_plugin_missing_fini(proxy_bin_dir, file_backup):
	plugin_dir = os.path.join(proxy_bin_dir, "plugins")
	plugin_path = os.path.join(plugin_dir, "greeting.so")

	file_backup.backup(plugin_path)

	current_dir = os.path.dirname(os.path.abspath(__file__))
	fake_plugin_path = os.path.join(current_dir, "..", "bin", "greeting_bad_fini.so")
	shutil.copy2(fake_plugin_path, plugin_path)

	proxy_bin = os.path.join(proxy_bin_dir, "proxy")
	result = run_command([proxy_bin], check=False)
	stderr = result.stderr
	expected_msg = "Library couldn't execute fini."
	assert expected_msg in stderr, f"Expected message not found."
	assert result.returncode == 1, f"Expected return_code 1, got {result.returncode}"
