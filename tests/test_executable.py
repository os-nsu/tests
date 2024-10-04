# tests/test_executable.py

import subprocess
import pytest
import time
import signal

from steps.build_steps import (
    make_with_flags
)

from steps.proxy_steps import (
	start_proxy,
	run_proxy,
	run_proxy_with_args,
	send_signal
)

def test_run_without_arguments(project_dir, proxy_bin_name, timeout):
	"""Tests that the proxy starts successfully without arguments and can be terminated cleanly."""
	proc = start_proxy(project_dir, proxy_bin_name)
	time.sleep(timeout)
	try:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=timeout)
		expected_returncode = -signal.SIGINT
		assert proc.returncode == expected_returncode, f"Proxy exited with code {expected_returncode} after SIGINT, expected 0."
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail("Proxy did not terminate within the timeout period after SIGINT.")

def test_run_with_help_argument(project_dir, proxy_bin_name, timeout):
	"""Tests running the proxy successfully with '--help' argument."""
	try:
		result = run_proxy_with_args(project_dir=project_dir, proxy_bin_name=proxy_bin_name, args=['--help'], timeout=timeout)
		expected_returncode = 0
		assert result.returncode == expected_returncode, f"Proxy with '--help' argument finish with code {result.returncode}, exptected {expected_returncode} ."
		assert  result.stdout != "", "Expected usage information in output."
	except subprocess.CalledProcessError as e:
		pytest.fail(f"Proxy with '--help' argument finish with error: {e.stderr}")
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy with '--help' argument not end in {timeout} seconds")

def test_run_with_invalid_arguments(project_dir, proxy_bin_name, timeout):
	"""Tests running the proxy with invalid arguments."""
	try:
		result = run_proxy_with_args(project_dir, proxy_bin_name, ['--invalid_arg'], timeout=timeout)
		assert result.returncode != 0, "Proxy should exit with non-zero code when given invalid arguments."
		assert "Invalid argument" in result.stderr or "unknown option" in result.stderr, "Expected error message for invalid argument."
	except subprocess.CalledProcessError as e:
		pytest.fail(f"Proxy finish with error: {e.stderr}")
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy not finished in {timeout} seconds in running with invalid argument.")

def test_execution_with_sanitizers(project_dir, proxy_bin_name, timeout):
	"""Tests the launch of a proxy built with AddressSanitizer and UndefinedBehaviorSanitizer."""
	cflags = "-fsanitize=address,undefined -ggdb3"
	make_with_flags(project_dir, cflags)
	proc = start_proxy(project_dir, proxy_bin_name)
	time.sleep(timeout)
	try:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=timeout)
		stdout, stderr = proc.communicate(timeout=timeout)
		expected_returncode = -signal.SIGINT
		assert proc.returncode == expected_returncode, f"Proxy finish with code {proc.returncode} after SIGINT, expected {expected_returncode}."
		assert stderr == ""
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail("The proxy did not terminate within the specified time after SIGINT.")

@pytest.mark.parametrize("sig, signal_name", [
	(signal.SIGINT, "SIGINT"),
	(signal.SIGQUIT, "SIGQUIT"),
	(signal.SIGSEGV, "SIGSEGV"),
])
def test_proxy_termination_on_signal(project_dir, proxy_bin_name, sig, signal_name, timeout):
	"""Tests that the proxy correctly terminates upon receiving specific signals."""
	proc = start_proxy(project_dir, proxy_bin_name)
	time.sleep(timeout)
	try:
		send_signal(proc, sig)
		proc.wait(timeout=timeout)
		expected_returncode = -sig
		assert proc.returncode == expected_returncode, f"Proxy exited with code {proc.returncode} after {signal_name}, expected {expected_returncode}."
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail(f"Proxy did not terminate within timeout after receiving {signal_name}.")

