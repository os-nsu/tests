# tests/lab1/master/test_master_execution.py

import os
import shutil
import pytest
from steps.build_steps import make, make_clean
from steps.execution_steps import check_error_output
from steps.message_templates import format_library_exec_error, format_library_open_error
from steps.utils import run_command

@pytest.mark.lab1
@pytest.mark.dependency(depends=["tests/lab1/master/test_master_build.py::test_master_config_symbols",
								 "tests/lab1/master/test_master_build.py::test_master_logger_symbols",
								 "tests/lab1/config/test_config_execution.py::test_config_create_table",
								 "tests/lab1/config/test_config_execution.py::test_config_destroy_table",
								 "tests/lab1/logger/test_logger_execution.py::test_logger_init_logger",
								 "tests/lab1/logger/test_logger_execution.py::test_logger_fini_logger",
								 "tests/lab1/logger/test_logger_execution.py::test_logger_init_logger_args",
								 "tests/lab1/plugins/greeting/test_plugin_greeting_execution.py::test_plugin_greeting_dlopen",
		 						 "tests/lab1/plugins/greeting/test_plugin_greeting_execution.py::test_plugin_greeting_dlsym_init",
		 						 "tests/lab1/plugins/greeting/test_plugin_greeting_execution.py::test_plugin_greeting_dlsym_name",
		 						 "tests/lab1/plugins/greeting/test_plugin_greeting_execution.py::test_plugin_greeting_dlsym_fini",
		 						 "tests/lab1/plugins/greeting/test_plugin_greeting_execution.py::test_plugin_greeting_call_init",
		 						 "tests/lab1/plugins/greeting/test_plugin_greeting_execution.py::test_plugin_greeting_call_name",
		 						 "tests/lab1/plugins/greeting/test_plugin_greeting_execution.py::test_plugin_greeting_call_fini",
		 						 "tests/lab1/plugins/greeting/test_plugin_greeting_execution.py::test_plugin_greeting_dlclose"],
						scope="session")
def test_master_execution(proxy_bin_dir):
	proxy_bin = os.path.join(proxy_bin_dir, "proxy")

	result = run_command([proxy_bin], check=True)
	stdout = result.stdout
	stderr = result.stderr

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

@pytest.mark.dependency(depends=["tests/lab1/master/test_master_execution.py::test_master_execution"],
						scope="session")
@pytest.mark.lab1
def test_master_logger_missing_init(proxy_dir, proxy_bin, proxy_logger_lib, lab_number, file_backup, set_cwd_to_test_file_dir):
	target = "logger_bad_init"
	clean_target = f"clean_{target}"
	make(make_args=[clean_target],
		check=True)
	make(make_args=[target],
		 extra_env={"PROXY_DIR": proxy_dir, "LAB_NUMBER": str(lab_number)},
		 check=True)
	logger_bad_init_so = os.path.join("bin", "logger_bad_init.so")

	file_backup.backup(proxy_logger_lib)
	shutil.copy2(logger_bad_init_so, proxy_logger_lib)

	result = run_command([proxy_bin], check=False)

	expected_message = "Failed to initialize the logger"
	check_error_output(result=result, expected_message=expected_message, expected_returncode=1, target="Logger")

@pytest.mark.dependency(depends=["tests/lab1/master/test_master_execution.py::test_master_execution"],
						scope="session")
@pytest.mark.lab1
def test_master_logger_missing_fini(proxy_dir, proxy_bin, proxy_logger_lib, lab_number, file_backup, set_cwd_to_test_file_dir):
	target = "logger_bad_fini"
	clean_target = f"clean_{target}"
	make(make_args=[clean_target],
		check=True)
	make(make_args=[target],
		 extra_env={"PROXY_DIR": proxy_dir, "LAB_NUMBER": str(lab_number)},
		 check=True)

	logger_bad_fini_so = os.path.join("bin", "logger_bad_fini.so")

	file_backup.backup(proxy_logger_lib)
	shutil.copy2(logger_bad_fini_so, proxy_logger_lib)

	result = run_command([proxy_bin], check=False)

	expected_message = "Couldn't shut down logger"
	check_error_output(result=result, expected_message=expected_message, expected_returncode=1, target="Logger")


@pytest.mark.dependency(depends=["tests/lab1/master/test_master_execution.py::test_master_execution"],
						scope="session")
@pytest.mark.lab1
def test_master_plugin_missing(proxy_bin, proxy_plugins_greeting_bin, file_backup, set_cwd_to_test_file_dir):
	file_backup.backup(proxy_plugins_greeting_bin)

	result = run_command([proxy_bin], check=False)

	expected_message = format_library_open_error(plugin_path=proxy_plugins_greeting_bin, dlopen_error="cannot open shared object file: No such file or directory")
	check_error_output(result=result, expected_message=expected_message, expected_returncode=1)


@pytest.mark.dependency(depends=["tests/lab1/master/test_master_execution.py::test_master_execution"],
						scope="session")
@pytest.mark.lab1
def test_master_plugin_missing_hook(proxy_dir, proxy_bin, proxy_plugins_greeting_bin, file_backup, set_cwd_to_test_file_dir):
	target = "greeting_bad_hook"
	clean_target = f"clean_{target}"
	make(make_args=[clean_target],
		check=True)
	make(make_args=[target],
		 extra_env={"PROXY_DIR": proxy_dir},
		 check=True)

	file_backup.backup(proxy_plugins_greeting_bin)

	greeting_bad_hook_so = os.path.join("bin", "greeting_bad_hook.so")
	shutil.copy2(greeting_bad_hook_so, proxy_plugins_greeting_bin)

	result = run_command([proxy_bin], check=False)

	expected_message = format_library_open_error(plugin_path=proxy_plugins_greeting_bin, dlopen_error="undefined symbol: last_executor_start_hook")
	check_error_output(result=result, expected_message=expected_message, expected_returncode=1, target="Plugin greeting")


@pytest.mark.dependency(depends=["tests/lab1/master/test_master_execution.py::test_master_execution"],
						scope="session")
@pytest.mark.lab1
def test_master_plugin_missing_init(proxy_dir, proxy_bin, proxy_plugins_greeting_bin, file_backup, set_cwd_to_test_file_dir):
	target = "greeting_bad_init"
	clean_target = f"clean_{target}"
	make(make_args=[clean_target],
		check=True)
	make(make_args=[target],
		 extra_env={"PROXY_DIR": proxy_dir},
		 check=True)

	file_backup.backup(proxy_plugins_greeting_bin)

	greeting_bad_init_so = os.path.join("bin", "greeting_bad_init.so")
	shutil.copy2(greeting_bad_init_so, proxy_plugins_greeting_bin)

	result = run_command([proxy_bin], check=False)

	expected_message = format_library_exec_error(function_name="init", plugin_name="greeting", plugin_path=proxy_plugins_greeting_bin, dlsym_error="undefined symbol: init")
	check_error_output(result=result, expected_message=expected_message, expected_returncode=1, target="Plugin greeting")


@pytest.mark.dependency(depends=["tests/lab1/master/test_master_execution.py::test_master_execution"],
						scope="session")
@pytest.mark.lab1
def test_master_plugin_missing_name(proxy_dir, proxy_bin, proxy_plugins_greeting_bin, file_backup, set_cwd_to_test_file_dir):
	target = "greeting_bad_name"
	clean_target = f"clean_{target}"
	make(make_args=[clean_target],
		check=True)
	make(make_args=[target],
		 extra_env={"PROXY_DIR": proxy_dir},
		 check=True)

	file_backup.backup(proxy_plugins_greeting_bin)

	greeting_bad_name_so = os.path.join("bin", "greeting_bad_name.so")
	shutil.copy2(greeting_bad_name_so, proxy_plugins_greeting_bin)

	result = run_command([proxy_bin], check=False)

	expected_message = format_library_exec_error(function_name="name", plugin_name="greeting", plugin_path=proxy_plugins_greeting_bin, dlsym_error="undefined symbol: name")
	check_error_output(result=result, expected_message=expected_message, expected_returncode=1, target="Plugin greeting")


@pytest.mark.dependency(depends=["tests/lab1/master/test_master_execution.py::test_master_execution"],
						scope="session")
@pytest.mark.lab1
def test_master_plugin_missing_fini(proxy_dir, proxy_bin, proxy_plugins_greeting_bin, file_backup, set_cwd_to_test_file_dir):
	target = "greeting_bad_fini"
	clean_target = f"clean_{target}"
	make(make_args=[clean_target],
		check=True)
	make(make_args=[target],
		 extra_env={"PROXY_DIR": proxy_dir},
		 check=True)

	file_backup.backup(proxy_plugins_greeting_bin)

	greeting_bad_fini_so = os.path.join("bin", "greeting_bad_fini.so")
	shutil.copy2(greeting_bad_fini_so, proxy_plugins_greeting_bin)

	result = run_command([proxy_bin], check=False)

	expected_message = format_library_exec_error(function_name="fini", plugin_name="greeting", plugin_path=proxy_plugins_greeting_bin, dlsym_error="undefined symbol: fini")
	check_error_output(result=result, expected_message=expected_message, expected_returncode=1, target="Plugin greeting")
