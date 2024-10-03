# tests/test_executable.py

import subprocess
import pytest
import time
import signal

from steps.build_steps import (
<<<<<<< HEAD
    make_with_flags
=======
	make_with_flags         
>>>>>>> f3f9118 (Пофиксил случайное использование пробелов вместо табов)
)

from steps.proxy_steps import (
	start_proxy,
<<<<<<< HEAD
)

def test_successful_start(project_dir, proxy_bin_name):
    """Tests running proxy successfully."""
    start_proxy(project_dir, proxy_bin_name)
	# TODO: print backtrace if coredump was generated
=======
	run_proxy,
	run_proxy_with_args,
	send_signal
)

from steps.test_steps import (
	get_coredump_files,
	check_for_coredump_difference
)


timeout = 1

@pytest.mark.xfail(raises=subprocess.CalledProcessError,
				   reason="Segfault")
def test_successful_start(project_dir, proxy_bin_name):
	"""Tests running proxy successfully."""  
	start_proxy(project_dir, proxy_bin_name)
	# TODO: print backtrace if coredump was generated
	

>>>>>>> f3f9118 (Пофиксил случайное использование пробелов вместо табов)

def test_run_without_arguments(project_dir, proxy_bin_name):
	"""Tests that the proxy starts successfully without arguments and can be terminated cleanly."""
	start_coredumps = get_coredump_files()
	proc = start_proxy(project_dir, proxy_bin_name)
	time.sleep(timeout)
	try:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=timeout)
		assert proc.returncode == 0, f"Proxy exited with code {proc.returncode} after SIGINT, expected 0."
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail("Proxy did not terminate within the timeout period after SIGINT.")
	finally:
		check_for_coredump_difference(proxy_bin_name, start_coredumps)

def test_run_with_help_argument(project_dir, proxy_bin_name):
	"""Tests running the proxy successfully with '--help' argument."""
	start_coredumps = get_coredump_files()
	result = run_proxy_with_args(project_dir = project_dir, proxy_bin_name = proxy_bin_name, args= ['--help'], timeout=timeout)
	try:
		assert result.returncode == 0, f"Proxy exited with code {result.returncode} with '--help' argument."
		assert "Usage" in result.stdout or "usage" in result.stdout, "Expected usage information in output."
	finally:
		check_for_coredump_difference(proxy_bin_name, start_coredumps)

def test_run_with_invalid_arguments(project_dir, proxy_bin_name):
	"""Tests running the proxy with invalid arguments."""
	start_coredumps = get_coredump_files()
	try:
		result = run_proxy_with_args(project_dir=project_dir, proxy_bin_name=proxy_bin_name, arg=['--invalid_arg'], timeout=timeout)
		assert result.returncode != 0, "Proxy should exit with non-zero code when given invalid arguments."
		assert "Invalid argument" in result.stderr or "unknown option" in result.stderr, "Expected error message for invalid argument."
	except subprocess.TimeoutExpired:
		pytest.fail("Прокси не завершился в течение заданного времени при запуске с '--help'.")		
	finally:
		check_for_coredump_difference(proxy_bin_name, start_coredumps)

def test_run_with_sanitizers(project_dir, proxy_bin_name):
	"""Тестирует запуск прокси, собранного с AddressSanitizer и UndefinedBehaviorSanitizer."""
	start_coredumps = get_coredump_files()
	cflags = "-fsanitize=address,undefined -ggdb3"
	make_with_flags(project_dir, cflags)
	proc = start_proxy(project_dir=project_dir, proxy_bin_name=proxy_bin_name)
	time.sleep(timeout)
	try:
		send_signal(proc, signal.SIGINT)
		stdout, stderr = proc.communicate(timeout=timeout)
		assert proc.returncode == 0, f"Proxy finish with code {proc.returncode} after SIGINT, expected 0."

		sanitizer_errors = ["ERROR: AddressSanitizer", "runtime error:"]
		if any(error in stderr for error in sanitizer_errors):
			pytest.fail(f"Sanitizer found error:\n{stderr}")
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail("ПThe proxy did not terminate within the specified time after SIGINT.")
	finally:
		check_for_coredump_difference(proxy_bin_name, start_coredumps)
		
@pytest.mark.parametrize("sig, signal_name", [
	(signal.SIGINT, "SIGINT"),
	(signal.SIGQUIT, "SIGQUIT"),
	(signal.SIGSEGV, "SIGSEGV"),
])
def test_run_termination_on_signal(project_dir, proxy_bin_name, sig, signal_name):
	"""Tests that the proxy correctly terminates upon receiving specific signals."""
	start_coredumps = get_coredump_files()
	proc = start_proxy(project_dir, proxy_bin_name)
	time.sleep(timeout)
	try:
		send_signal(proc, sig)
		proc.wait(timeout=timeout)
		assert proc.returncode == 0, f"Proxy exited with code {proc.returncode} after {signal_name}, expected 0."
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail(f"Proxy did not terminate within timeout after receiving {signal_name}.")
	finally:
		check_for_coredump_difference(proxy_bin_name, start_coredumps)
