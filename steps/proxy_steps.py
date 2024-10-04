#steps/proxy_steps.py

import subprocess
import signal
import pytest

def run_proxy(project_dir, proxy_bin_name):
	proxy = subprocess.run([f"{proxy_bin_name}"], cwd=project_dir, check=True)
	assert proxy.returncode == 0, "Proxy exit code is 0"
	return proxy

def start_proxy(project_dir, proxy_bin_name):
	"""Starts the proxy process and returns the Popen object."""
	proc = subprocess.Popen([proxy_bin_name], cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	return proc

def send_signal(proc, sig):
	"""Sends the specified signal to the process."""
	if proc.poll() is None:
		proc.send_signal(sig)
	else:
		pytest.fail("Cannot send signal; process is not running.")

def run_proxy_with_args(project_dir, proxy_bin_name, args, timeout=None):
	"""Runs the proxy with specified arguments and returns the CompletedProcess object."""
	result = subprocess.run([proxy_bin_name] + args, cwd=project_dir, check=True, capture_output=True, text=True, timeout=timeout)
	return result
