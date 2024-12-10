# steps/proxy_steps.py

import os
import subprocess
import time
import pytest

from steps.build_steps import simple_clean, make

def run_proxy(project_dir, proxy_bin_name, args=[], timeout=None, env=None, wait_until_end=True):
	"""
	Runs the proxy with specified arguments.

	If wait is True, waits for the process to complete and returns the CompletedProcess object.
	If wait is False, starts the process and returns the Popen object.
	"""
	try:
		if wait_until_end:
			result = subprocess.run([proxy_bin_name] + args, cwd=project_dir, check=False, capture_output=True, text=True, timeout=timeout, env=env)
			return result
		else:
			proc = subprocess.Popen([proxy_bin_name] + args, cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
			return proc
	except subprocess.TimeoutExpired:
		pytest.fail(f"Proxy not finished in {timeout} seconds.")
	except Exception as e:
		pytest.fail(f"Can't start proxy with args {args}, {e}")

def send_signal(proc, sig):
	"""Sends the specified signal to the process."""
	if proc.poll() is None:
		proc.send_signal(sig)
	else:
		pytest.fail("Cannot send signal; process is not running or already finished.")
