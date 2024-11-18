# tests/lab1/test_execution.py

import subprocess
import pytest
import time
import signal

from steps.build_steps import (
    make_with_env
)

from steps.proxy_steps import (
	build_and_start_proxy,
	run_proxy_with_args,
	send_signal
)

def test_run_without_arguments(project_dir, proxy_bin_name, proxy_timeout):
	"""Tests that the proxy starts successfully without arguments and can be terminated cleanly."""
	proc = build_and_start_proxy(project_dir=project_dir, proxy_bin_name=proxy_bin_name, proxy_timeout=proxy_timeout)
	time.sleep(proxy_timeout)
	try:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=proxy_timeout)
		expected_returncode = -signal.SIGINT
		assert proc.returncode == expected_returncode, f"Proxy exited with code {proc.returncode} after SIGINT, expected {expected_returncode}."
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail("Proxy did not terminate within the timeout period after SIGINT.")

def test_run_with_help_argument(project_dir, proxy_bin_name, proxy_timeout):
	"""Tests running the proxy successfully with '--help' argument."""
	try:
		result = run_proxy_with_args(project_dir=project_dir, proxy_bin_name=proxy_bin_name, args=['--help'], timeout=proxy_timeout)
		expected_returncode = 0
		assert result.returncode == expected_returncode, f"Proxy with '--help' argument finish with code {result.returncode}, exptected {expected_returncode} ."
		assert  result.stdout != "", "Expected usage information in output."
	except subprocess.CalledProcessError as e:
		pytest.fail(f"Proxy with '--help' argument finish with error: {e.stderr}")
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy with '--help' argument not finish in {proxy_timeout} seconds")

def test_run_with_invalid_arguments(project_dir, proxy_bin_name, proxy_timeout):
	"""Tests running the proxy with invalid arguments."""
	try:
		result = run_proxy_with_args(project_dir, proxy_bin_name, ['--invalid_arg'], timeout=proxy_timeout)
		assert result.returncode != 0, "Proxy should exit with non-zero code when given invalid arguments."
		assert "Invalid argument" in result.stderr or "unknown option" in result.stderr, "Expected error message for invalid argument."
	except subprocess.CalledProcessError as e:
		pytest.fail(f"Proxy finish with error: {e.stderr}")
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy ith invalid argument not finished in {proxy_timeout} seconds.")
