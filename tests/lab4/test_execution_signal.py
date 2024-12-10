# tests/lab4/test_execution_signal.py

import subprocess
import pytest
import time
import signal

from steps.proxy_steps import send_signal

@pytest.mark.parametrize("sig, signal_name", [
	(signal.SIGINT, "SIGINT"),
	pytest.param(signal.SIGQUIT, "SIGQUIT", marks=pytest.mark.allow_coredump), # Mark allow coredump because SIGQUIT generated coredump
	pytest.param(signal.SIGSEGV, "SIGSEGV", marks=pytest.mark.allow_coredump), # Mark allow coredump because SIGQUIT generated coredump
])
def test_proxy_termination_on_signal(proxy_fixture, sig, signal_name, log_file_path):
	"""Tests that the proxy correctly terminates upon receiving specific signals."""
	proxy = proxy_fixture
	proc = proxy.build_and_run_proxy(log_file_path, wait_until_end=False)
	time.sleep(proxy.proxy_timeout)
	try:
		send_signal(proc, sig)
		proc.wait(timeout=proxy.proxy_timeout)
		expected_returncode = -sig
		assert proc.returncode == expected_returncode, f"Proxy exited with code {proc.returncode} after {signal_name}, expected {expected_returncode}."
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail(f"Proxy did not terminate within timeout({proxy.proxy_timeout} seconds) after receiving {signal_name}.")
