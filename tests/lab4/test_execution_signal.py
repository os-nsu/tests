# tests/lab4/test_execution_signal.py

import subprocess
import pytest
import time
import signal

from steps.proxy_steps import (
	build_and_start_proxy,
	send_signal
)

@pytest.mark.parametrize("sig, signal_name", [
	(signal.SIGINT, "SIGINT"),
	pytest.param(signal.SIGQUIT, "SIGQUIT", marks=pytest.mark.allow_coredump), # Mark allow coredump because SIGQUIT generated coredump
	pytest.param(signal.SIGSEGV, "SIGSEGV", marks=pytest.mark.allow_coredump), # Mark allow coredump because SIGQUIT generated coredump
])
def test_proxy_termination_on_signal(project_dir, proxy_bin_name, sig, signal_name, proxy_timeout, log_file_path):
	"""Tests that the proxy correctly terminates upon receiving specific signals."""
	proc = build_and_start_proxy(project_dir=project_dir, proxy_bin_name=proxy_bin_name, proxy_timeout=proxy_timeout, log_file_path=log_file_path)
	time.sleep(proxy_timeout)
	try:
		send_signal(proc, sig)
		proc.wait(timeout=proxy_timeout)
		expected_returncode = -sig
		assert proc.returncode == expected_returncode, f"Proxy exited with code {proc.returncode} after {signal_name}, expected {expected_returncode}."
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail(f"Proxy did not terminate within timeout({proxy_timeout} seconds) after receiving {signal_name}.")
