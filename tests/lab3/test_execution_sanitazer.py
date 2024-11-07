# tests/lab3/test_execution_sanitazer.py

import subprocess
import pytest
import time
import signal

from steps.build_steps import (
    make_with_flags
)

from steps.proxy_steps import (
	start_proxy,
	run_proxy_with_args,
	send_signal
)

def test_execution_with_sanitizers(project_dir, proxy_bin_name, proxy_timeout):
	"""Tests the launch of a proxy built with AddressSanitizer and UndefinedBehaviorSanitizer."""
	cflags = "-fsanitize=address,undefined -ggdb3"
	make_with_flags(project_dir, cflags)
	proc = start_proxy(project_dir, proxy_bin_name)
	time.sleep(proxy_timeout)
	try:
		send_signal(proc, signal.SIGINT)
		proc.wait(timeout=proxy_timeout)
		stdout, stderr = proc.communicate(timeout=proxy_timeout)
		expected_returncode = -signal.SIGINT
		assert proc.returncode == expected_returncode, f"Proxy finish with code {proc.returncode} after SIGINT, expected {expected_returncode}."
		assert stderr == ""
	except subprocess.TimeoutExpired:
		proc.kill()
		pytest.fail("The proxy not terminate within the specified time after SIGINT.")